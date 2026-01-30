from pydantic import BaseModel
from typing import List, Optional

class InstrumentalPrompt(BaseModel):
    genre: str
    bpm: int
    keywords: str

class LyricsPrompt(BaseModel):
    topic: str
    keywords: Optional[str] # separated by comma
    line_length: str # short (6) | medium (7) | long (8)
    song_length: str # short (2*2) | medium (4*2) | long (6*2)

class GeneratedInstrumental(BaseModel):
    title: str
    prompt: InstrumentalPrompt

class GeneratedLyrics(BaseModel):
    title: str
    prompt: LyricsPrompt
    lyrics: List[List[List[str]]]
