from fastapi import HTTPException
from models.songs import Instrumental, LyricSet
from models.generation import GeneratedInstrumental, GeneratedLyrics
from datetime import datetime
from pathlib import Path
import json

SONG_DIR = Path(__file__).parent.parent.resolve() / "songs"

"GET"
# retrieve an instrumental from its ID
def getInstrumental(instrumentalId : str) -> Instrumental:
    instFile = SONG_DIR / instrumentalId / "instrumental.json"

    if not instFile.exists():
        raise HTTPException(status_code=404, detail="instrumental not found")

    with open(instFile, "r") as f:
        data = json.load(f)

    return Instrumental(**data)

# retrieve a lyric set from its and its instrumental's ID
def getLyricSet(instrumentalId : str, lyricSetId : str) -> LyricSet:
    lyricFile = SONG_DIR / instrumentalId / "lyrics" / f"{lyricSetId}.json"

    if not lyricFile.exists():
        raise HTTPException(status_code=404, detail="lyric set not found")
    
    with open(lyricFile, "r") as f:
        data = json.load(f)
    
    return LyricSet(**data)


"POST" 
# store a new generated instrumental
def storeInstrumental(data : GeneratedInstrumental) -> Instrumental:
    instId = _getNextInstrumentalId()

    newInstrumental = Instrumental(
        id=instId,
        created_at=datetime.now(),
        last_played=datetime.now(),
        title=data.title,
        prompt=data.prompt,
        music=data.music
    )

    instDir = SONG_DIR / instId
    instDir.mkdir(parents=True)

    with open(instDir / "instrumental.json", "w") as f:
        json.dump(newInstrumental.model_dump(), f, default=str)

    (instDir / "lyrics").mkdir()

    return newInstrumental

# store a new generated lyric set within an instrumental
def storeLyricSet(instrumentalId : str, data : GeneratedLyrics) -> LyricSet:
    lyricsId = _getNextLyricSetId(instrumentalId)

    newLyricSet = LyricSet(
        id=lyricsId,
        created_at=datetime.now(),
        last_played=datetime.now(),
        title=data.title,
        prompt=data.prompt,
        lyrics=data.lyrics
    )

    lyricPath = SONG_DIR / instrumentalId / "lyrics" / f"{lyricsId}.json"

    with open(lyricPath, "w") as f:
        json.dump(newLyricSet.model_dump(), f, default=str)
    
    return newLyricSet


"PUT"
# update an instrumental
def updateInstrumental(instrumental : Instrumental) -> None:
    pass

# update a lyric set within an instrumental
def updateLyricSet(instrumentalId : str, lyricSet : LyricSet) -> None:
    pass


"DELETE"
# delete an instrumental from its ID
def deleteInstrumental(instrumentalId : str) -> None:
    pass

# delete a lyric set from its and its instrumental's ID
def deleteLyricSet(instrumentalId : str, lyricSetId : str) -> None:
    pass


"HELPERS"
# find the next instrumental id
def _getNextInstrumentalId() -> str:
    existing = sorted(SONG_DIR.glob("inst_*"))

    if not existing:
        return "inst_001"
    
    lastInt = int(existing[-1].stem.split("_")[1])
    return f"inst_{lastInt+1:03d}"

# find the next lyric set id
def _getNextLyricSetId(instrumentalId : str) -> str:
    lyrics_dir = SONG_DIR / instrumentalId / "lyrics"
    existing = sorted(lyrics_dir.glob("set_*.json"))

    if not existing:
        return "set_001"

    lastInt = int(existing[-1].stem.split("_")[1])
    return f"set_{lastInt+1:03d}"
