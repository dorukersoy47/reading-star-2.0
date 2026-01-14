from models.generation import InstrumentalPrompt, GeneratedInstrumental
from pathlib import Path
from generation.musicgen.generator import generate_music

def generateMusic(prompt : InstrumentalPrompt, path: Path) -> GeneratedInstrumental:
    generate_music(prompt.genre, path)
    return GeneratedInstrumental(
        title=prompt.genre,
        prompt=prompt,
    )