from pydantic import BaseModel
from typing import List
from datetime import datetime
from models.generation import InstrumentalPrompt, LyricsPrompt

class LyricSet(BaseModel):
    id: str
    created_at: datetime
    last_played: datetime
    title: str
    prompt: LyricsPrompt
    lyrics: List[List[List[str]]]

class Instrumental(BaseModel):
    id: str
    created_at: datetime
    last_played: datetime
    title: str
    prompt: InstrumentalPrompt
    audio_url: str


class LyricSetInformation(BaseModel):
    id: str
    created_at: datetime
    last_played: datetime
    title: str

class InstrumentalInformation(BaseModel):
    id: str
    created_at: datetime
    last_played: datetime
    title: str
    lyricSets: List[LyricSetInformation]