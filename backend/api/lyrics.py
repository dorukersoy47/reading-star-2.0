from fastapi import APIRouter
from models.generation import LyricsPrompt
from models.songs import LyricSet
from services.lyric_generation import generateLyrics
from services.song_storage import storeLyricSet, getLyricSet

router = APIRouter()

# GET
@router.get("/{instId}/lyrics/{setId}", response_model=LyricSet)
def findLyricSet(instId: str, setId: str):
    return getLyricSet(instId, setId)

# POST
@router.post("/{instId}/lyrics", response_model=LyricSet)
def createLyricSet(instId : str, req: LyricsPrompt):
    lyricSet = generateLyrics(req)
    return storeLyricSet(instId, lyricSet)