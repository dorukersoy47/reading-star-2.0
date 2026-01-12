from fastapi import APIRouter
from models.generation import InstrumentalPrompt
from models.songs import Instrumental
from services.music_generation import generateMusic
from services.song_storage import storeInstrumental

router = APIRouter()

# POST
@router.post("/", response_model=Instrumental)
def createInstrumental(req: InstrumentalPrompt):
    instrumental = generateMusic(req)
    return storeInstrumental(instrumental)