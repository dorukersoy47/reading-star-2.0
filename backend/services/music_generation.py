from models.generation import InstrumentalPrompt, GeneratedInstrumental
from pathlib import Path
from generation.musicgen.generator import generate_music
from generation.lyricGen.generator import generate_instrumental_title

def generateMusic(prompt : InstrumentalPrompt, path: Path) -> GeneratedInstrumental:
    generate_music(prompt, path)
    title = generate_instrumental_title(prompt.genre, prompt.keywords)
    return GeneratedInstrumental(
        title=title,
        prompt=prompt,
        bpm = prompt.bpm
    )