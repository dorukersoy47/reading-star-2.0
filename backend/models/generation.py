from pydantic import BaseModel
from typing import List

class InstrumentalPrompt(BaseModel):
    text: str
    speed: str
    length: str

class LyricsPrompt(BaseModel):
    topic: str
    stanza_count: int
    syllable_count: int

class GeneratedInstrumental(BaseModel):
    title: str
    prompt: InstrumentalPrompt
    music: str

class GeneratedLyrics(BaseModel):
    title: str
    prompt: LyricsPrompt
    lyrics: List[List[List[str]]]
