from models.generation import LyricsPrompt, GeneratedLyrics
from generation.lyricGen.main import main as lyrics

def generateLyrics(prompt : LyricsPrompt) -> GeneratedLyrics:
    return lyrics(prompt)