from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from models.generation import InstrumentalPrompt, LyricsPrompt
from models.songs import Instrumental, InstrumentalInformation, LyricSet, LyricSetInformation
from typing import List
from services.music_generation import generateMusic
from services.lyric_generation import generateLyrics
import services.song_storage as storage

router = APIRouter()

"GET"
# get information of every instrumental and their lyric sets
@router.get("/", response_model=list[InstrumentalInformation])
def getAll():
    return storage.getAllInstrumentalsAndSets()

# get an instrumental from its ID
@router.get("/{inst_id}", response_model=Instrumental)
def getInstrumental(inst_id: str):
    return storage.getInstrumental(inst_id)

# get information of an instrumental's lyric sets
@router.get("/{inst_id}/lyrics", response_model=List[LyricSetInformation])
def getLyricSets(inst_id: str):
    return storage.getLyricSets(inst_id)

# get a lyric set from its and its instrumental's ID
@router.get("/{inst_id}/lyrics/{set_id}", response_model=LyricSet)
def getLyricSet(inst_id: str, set_id: str):
    return storage.getLyricSet(inst_id, set_id)

# get an instrumental's audio as a file response from its ID
@router.get("/{inst_id}/audio")
def getInstrumentalAudio(inst_id: str):
    audio_path = storage.getInstrumentalAudioPath(inst_id)

    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="audio not found")
    
    return FileResponse(audio_path, media_type="audio/wav", filename="instrumental.wav")


"POST"
# generate and store a new instrumental
@router.post("/", response_model=Instrumental)
def createInstrumental(req: InstrumentalPrompt):
    inst_id = storage.createInstrumentalDirectory()
    instrumental = generateMusic(req, storage.getInstDir(inst_id))
    return storage.storeInstrumental(inst_id, instrumental, f"/instrumentals/{inst_id}/audio")

# generate and store a new lyric set
@router.post("/{inst_id}/lyrics", response_model=LyricSet)
def createLyricSet(inst_id: str, req: LyricsPrompt):
    lyric_set = generateLyrics(req)
    return storage.storeLyricSet(inst_id, lyric_set)