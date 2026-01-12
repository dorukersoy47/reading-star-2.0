from fastapi import APIRouter
from models.generation import LyricsPrompt
from models.songs import LyricSet
from services.lyric_generation import generateLyrics
from services.song_storage import storeLyricSet

router = APIRouter()

# POST
@router.post("/{instId}/lyrics", response_model=LyricSet)
def createLyrics(instId : str, req: LyricsPrompt):
    lyricSet = generateLyrics(req)
    return storeLyricSet(instId, lyricSet)