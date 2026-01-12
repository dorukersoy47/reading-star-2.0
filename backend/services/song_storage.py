from fastapi import HTTPException
from models.songs import Instrumental, LyricSet, InstrumentalInformation, LyricSetInformation
from models.generation import GeneratedInstrumental, GeneratedLyrics
from datetime import datetime
from pathlib import Path
import json

SONG_DIR = Path(__file__).parent.parent.resolve() / "songs"

"GET"
# retrieve information of every instrumental and their lyric sets
def getAllInstrumentalsAndSets() -> list[InstrumentalInformation]:
    results = []

    for inst_dir in SONG_DIR.iterdir():
        inst_file = inst_dir / "instrumental.json"
        lyrics_dir = inst_dir / "lyrics"

        if not inst_file.exists():
            continue
        
        instrumental = Instrumental(**json.load(open(inst_file)))

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

# retrieve an instrumental from its ID
def getInstrumental(instrumental_id: str) -> Instrumental:
    inst_file = SONG_DIR / instrumental_id / "instrumental.json"

    if not inst_file.exists():
        raise HTTPException(status_code=404, detail="instrumental not found")

    with open(inst_file, "r") as f:
        data = json.load(f)

    return Instrumental(**data)

# retrieve a lyric set from its and its instrumental's ID
def getLyricSet(instrumental_id: str, set_id: str) -> LyricSet:
    lyric_file = SONG_DIR / instrumental_id / "lyrics" / f"{set_id}.json"

    if not lyric_file.exists():
        raise HTTPException(status_code=404, detail="lyric set not found")
    
    with open(lyric_file, "r") as f:
        data = json.load(f)
    
    return LyricSet(**data)


"POST" 
# store a new generated instrumental
def storeInstrumental(data: GeneratedInstrumental) -> Instrumental:
    inst_id = _getNextInstrumentalId()

    new_instrumental = Instrumental(
        id=inst_id,
        created_at=datetime.now(),
        last_played=datetime.now(),
        title=data.title,
        prompt=data.prompt,
        music=data.music
    )

    inst_dir = SONG_DIR / inst_id
    inst_dir.mkdir(parents=True)

    with open(inst_dir / "instrumental.json", "w") as f:
        json.dump(new_instrumental.model_dump(), f, default=str)

    (inst_dir / "lyrics").mkdir()

    return new_instrumental

# store a new generated lyric set within an instrumental
def storeLyricSet(instrumental_id: str, data: GeneratedLyrics) -> LyricSet:
    set_id = _getNextLyricSetId(instrumental_id)

    new_lyric_set = LyricSet(
        id=set_id,
        created_at=datetime.now(),
        last_played=datetime.now(),
        title=data.title,
        prompt=data.prompt,
        lyrics=data.lyrics
    )

    lyric_path = SONG_DIR / instrumental_id / "lyrics" / f"{set_id}.json"

    with open(lyric_path, "w") as f:
        json.dump(new_lyric_set.model_dump(), f, default=str)
    
    return new_lyric_set


"PUT"
# update an instrumental
def updateInstrumental(instrumental: Instrumental) -> None:
    pass

# update a lyric set within an instrumental
def updateLyricSet(instrumental_id: str, lyric_set: LyricSet) -> None:
    pass


"DELETE"
# delete an instrumental from its ID
def deleteInstrumental(instrumental_id: str) -> None:
    pass

# delete a lyric set from its and its instrumental's ID
def deleteLyricSet(instrumental_id: str, set_id: str) -> None:
    pass


"HELPERS"
# find the next instrumental id
def _getNextInstrumentalId() -> str:
    existing = sorted(SONG_DIR.glob("inst_*"))

    if not existing:
        return "inst_001"
    
    last_int = int(existing[-1].stem.split("_")[1])
    return f"inst_{last_int+1:03d}"

# find the next lyric set id
def _getNextLyricSetId(instrumental_id: str) -> str:
    lyrics_dir = SONG_DIR / instrumental_id / "lyrics"
    existing = sorted(lyrics_dir.glob("set_*.json"))

    if not existing:
        return "set_001"

    last_int = int(existing[-1].stem.split("_")[1])
    return f"set_{last_int+1:03d}"
