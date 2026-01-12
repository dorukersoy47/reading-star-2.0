from fastapi import APIRouter
from models.generation import InstrumentalPrompt, LyricsPrompt
from models.songs import Instrumental, InstrumentalInformation, LyricSet
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

# get a lyric set from its and its instrumental's ID
@router.get("/{inst_id}/lyrics/{set_id}", response_model=LyricSet)
def getLyricSet(inst_id: str, set_id: str):
    return storage.getLyricSet(inst_id, set_id)


"POST"
# generate and store a new instrumental
@router.post("/", response_model=Instrumental)
def createInstrumental(req: InstrumentalPrompt):
    instrumental = generateMusic(req)
    return storage.storeInstrumental(instrumental)

# generate and store a new lyric set
@router.post("/{inst_id}/lyrics", response_model=LyricSet)
def createLyricSet(inst_id: str, req: LyricsPrompt):
    lyric_set = generateLyrics(req)
    return storage.storeLyricSet(inst_id, lyric_set)