from models.generation import InstrumentalPrompt, GeneratedInstrumental
from pathlib import Path

def musicGen(genre: str, path: Path): # simulated call to music generation module
    pass

def generateMusic(prompt : InstrumentalPrompt, path: Path) -> GeneratedInstrumental:
    musicGen(prompt.length, ) # CHANGE TO GENRE OR SOMETHING
    return GeneratedInstrumental(
        title="test instrumental",
        prompt=prompt,
    )