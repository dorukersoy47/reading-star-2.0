from models.generation import LyricsPrompt, GeneratedLyrics

def generateLyrics(prompt : LyricsPrompt) -> GeneratedLyrics:
    return GeneratedLyrics(
        title="test lyrics",
        prompt=prompt,
        lyrics=[[["la", "la"],["lo"]],[["le"],["le"]]]
    )