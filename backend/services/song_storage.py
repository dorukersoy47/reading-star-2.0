from fastapi import HTTPException
from models.songs import Instrumental, LyricSet, InstrumentalInformation, LyricSetInformation
from models.generation import GeneratedInstrumental, GeneratedLyrics
from datetime import datetime
from pathlib import Path
import json
from os import environ

APP_NAME = "ReadingStar"
SONG_DIR = Path(environ['APPDATA']) / APP_NAME

"GET"
# retrieve information of every instrumental and their lyric sets
def getAllInstrumentalsAndSets() -> list[InstrumentalInformation]:
    results = []

    if not SONG_DIR.exists():
        return results

    for inst_dir in SONG_DIR.iterdir():
        inst_id = inst_dir.name
        inst_file = _getInstFile(inst_id)

        if not inst_file.exists():
            continue
        
        instrumental = Instrumental(**json.load(open(inst_file)))

        set_summaries = getLyricSets(inst_id)
        
        results.append(
            InstrumentalInformation(
                id=instrumental.id,
                created_at=instrumental.created_at,
                last_played=instrumental.last_played,
                title=instrumental.title,
                lyricSets=set_summaries
            )
        )
    
    return results

# retrieve information of all lyric sets of an instrumental
def getLyricSets(inst_id: str) -> list[LyricSetInformation]:
    lyrics_dir = _getLyricsDir(inst_id)

    set_summaries = []
    if lyrics_dir.exists():
        for set_file in lyrics_dir.glob("set_*.json"):
            lyric_set = LyricSet(**json.load(open(set_file)))
            set_summaries.append(
                LyricSetInformation(
                    id=lyric_set.id,
                    created_at=lyric_set.created_at,
                    last_played=lyric_set.last_played,
                    title=lyric_set.title
                )
            )
    
    return set_summaries

# retrieve an instrumental from its ID
def getInstrumental(inst_id: str) -> Instrumental:
    inst_file = _getInstFile(inst_id)

    if not inst_file.exists():
        raise HTTPException(status_code=404, detail="instrumental not found")

    with open(inst_file, "r") as f:
        data = json.load(f)

    return Instrumental(**data)

# retrieve a lyric set from its and its instrumental's ID
def getLyricSet(inst_id: str, set_id: str) -> LyricSet:
    lyric_file = _getLyricSetFile(inst_id, set_id)

    if not lyric_file.exists():
        raise HTTPException(status_code=404, detail="lyric set not found")
    
    with open(lyric_file, "r") as f:
        data = json.load(f)
    
    return LyricSet(**data)


"POST" 
# store a new generated instrumental
def storeInstrumental(inst_id: str, data: GeneratedInstrumental, audio_url: str) -> Instrumental:
    new_instrumental = Instrumental(
        id=inst_id,
        created_at=datetime.now(),
        last_played=datetime.now(),
        title=data.title,
        prompt=data.prompt,
        audio_url=audio_url
    )

    inst_dir = getInstDir(inst_id)

    with open(inst_dir / "instrumental.json", "w") as f:
        json.dump(new_instrumental.model_dump(), f, default=str)

    (_getLyricsDir(inst_id)).mkdir()

    return new_instrumental

# store a new generated lyric set within an instrumental
def storeLyricSet(inst_id: str, data: GeneratedLyrics) -> LyricSet:
    set_id = _getNextLyricSetId(inst_id)

    new_lyric_set = LyricSet(
        id=set_id,
        created_at=datetime.now(),
        last_played=datetime.now(),
        title=data.title,
        prompt=data.prompt,
        lyrics=data.lyrics
    )

    lyric_path = _getLyricSetFile(inst_id, set_id)

    with open(lyric_path, "w") as f:
        json.dump(new_lyric_set.model_dump(), f, default=str)
    
    return new_lyric_set


"PUT"
# update an instrumental
def updateInstrumental(instrumental: Instrumental) -> None:
    pass

# update a lyric set within an instrumental
def updateLyricSet(inst_id: str, lyric_set: LyricSet) -> None:
    pass


"DELETE"
# delete an instrumental an all associated files from its ID
def deleteInstrumental(inst_id: str) -> None:
    lyrics_dir = _getLyricsDir(inst_id)
    for set_file in lyrics_dir.glob("set_*.json"):
        set_file.unlink()
    lyrics_dir.rmdir()

    _getInstFile(inst_id).unlink()
    getInstrumentalAudioPath(inst_id).unlink()
    getInstDir(inst_id).rmdir()


# delete a lyric set from its and its instrumental's ID
def deleteLyricSet(inst_id: str, set_id: str) -> None:
    set_file = _getLyricSetFile(inst_id, set_id)
    set_file.unlink()


"HELPERS"
# find the next instrumental id
def _getNextInstId() -> str:
    existing = sorted(SONG_DIR.glob("inst_*"))

    if not existing:
        return "inst_001"
    
    last_int = int(existing[-1].stem.split("_")[1])
    return f"inst_{last_int+1:03d}"

# find the next lyric set id
def _getNextLyricSetId(inst_id: str) -> str:
    lyrics_dir = _getLyricsDir(inst_id)
    existing = sorted(lyrics_dir.glob("set_*.json"))

    if not existing:
        return "set_001"

    last_int = int(existing[-1].stem.split("_")[1])
    return f"set_{last_int+1:03d}"

# create the directory for an instrumental, returning the id
def createInstrumentalDirectory() -> str:
    inst_id = _getNextInstId()
    inst_dir = getInstDir(inst_id)
    inst_dir.mkdir(parents=True)
    return inst_id

# get the directory for an instrumental with its id
def getInstDir(inst_id: str) -> Path:
    return SONG_DIR / inst_id

# get the instrumental file for an instrumental with its id
def _getInstFile(inst_id: str) -> Path:
    return SONG_DIR / inst_id / "instrumental.json"

# get the directory of the lyrics of an instrumental with its id
def _getLyricsDir(inst_id: str) -> Path:
    return SONG_DIR / inst_id / "lyrics"

# get the lyric set of an instrumental with their ids
def _getLyricSetFile(inst_id: str, set_id: str) -> Path:
    return _getLyricsDir(inst_id) / f"{set_id}.json"

# get the audio file for an instrumental with its id
def getInstrumentalAudioPath(inst_id: str) -> Path:
    return getInstDir(inst_id) / "instrumental.wav"