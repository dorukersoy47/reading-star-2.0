from pydantic import BaseModel
from typing import List
from datetime import datetime
from models.generation import InstrumentalPrompt, LyricsPrompt

class Instrumental(BaseModel):
    id: str
    created_at: datetime
    last_played: datetime
    title: str
    prompt: InstrumentalPrompt
    music: str

class LyricSet(BaseModel):
    id: str
    created_at: datetime
    last_played: datetime
    title: str
    prompt: LyricsPrompt
    lyrics: List[List[List[str]]]

# class Track(BaseModel):
#     instrumental: Instrumental
#     lyricSets: List[LyricSet]

# class SongLibrary(BaseModel):
#     tracks: List[Track]