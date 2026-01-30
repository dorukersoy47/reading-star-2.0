from generation.lyricGen.generator import generate_song, generate_title
from generation.lyricGen.parser import format_song
from generation.lyricGen.normalise import normalise_song
from models.generation import LyricsPrompt, GeneratedLyrics

def main(prompt : LyricsPrompt) -> GeneratedLyrics:
    topic = prompt.topic
    keywords = prompt.keywords.split(",") if prompt.keywords else None
    syllable_count = {"short": 6, "medium": 7, "long": 8}[prompt.line_length]
    couplet_count = {"short": 2, "medium": 4, "long": 6}[prompt.song_length]

    print("Generating title...")
    title = generate_title(topic)
    print("Generating lyrics...")
    song = generate_song(topic, keywords, syllable_count, couplet_count)
    print("Formatting lyrics...")
    song = format_song(song)
    print("Normalising lyrics...")
    song = normalise_song(song, syllable_count)
    print(song)
    
    print("Successfully generated lyrics.")
    
    return GeneratedLyrics(
        title=title,
        prompt=prompt,
        lyrics=song
    )

if __name__ == '__main__':
    p = LyricsPrompt(
        topic="love",
        keywords="heart,forever,dreams",
        line_length="short",
        song_length="short"
    )

    main(p)