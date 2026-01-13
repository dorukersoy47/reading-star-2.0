from models.generation import LyricsPrompt, GeneratedLyrics
from lyricGen.main import main as lyrics

def generateLyrics(prompt : LyricsPrompt) -> GeneratedLyrics:
    return lyrics(prompt)