from pydantic import BaseModel
from typing import List

class InstrumentalPrompt(BaseModel):
    text: str
    speed: str
    length: str

class LyricsPrompt(BaseModel):
    text: str
    complexity: str


class GeneratedInstrumental(BaseModel):
    title: str
    prompt: InstrumentalPrompt

class GeneratedLyrics(BaseModel):
    title: str
    prompt: LyricsPrompt
    lyrics: List[List[List[str]]]
