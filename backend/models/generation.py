from pydantic import BaseModel
from typing import List

class InstrumentalPrompt(BaseModel):
    genre: str
    genre: str

class LyricsPrompt(BaseModel):
    topic: str
    stanza_count: int
    syllable_count: int
    topic: str
    stanza_count: int
    syllable_count: int


class GeneratedInstrumental(BaseModel):
    title: str
    prompt: InstrumentalPrompt

class GeneratedLyrics(BaseModel):
    title: str
    prompt: LyricsPrompt
    lyrics: List[List[List[str]]]
