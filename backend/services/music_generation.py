from models.generation import InstrumentalPrompt, GeneratedInstrumental
from pathlib import Path

def musicGen(genre: str, path: Path): # simulated call to music generation module, will store a wav file in path
    print(genre, path)

def generateMusic(prompt : InstrumentalPrompt, path: Path) -> GeneratedInstrumental:
    musicGen(prompt.genre, path)
    return GeneratedInstrumental(
        title="test instrumental",
        prompt=prompt,
    )