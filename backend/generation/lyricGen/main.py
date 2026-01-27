from generation.lyricGen.generator import generate_song, generate_title
from generation.lyricGen.parser import format_song
from generation.lyricGen.normalise import normalise_song
from models.generation import LyricsPrompt, GeneratedLyrics

def main(prompt : LyricsPrompt) -> GeneratedLyrics:
    topic = prompt.topic
    keywords = prompt.keywords.split(",")
    syllable_count = {"short": 6, "medium": 8, "long": 10}[prompt.line_length]
    couplet_count = {"short": 2, "medium": 4, "long": 6}[prompt.song_length]
    complexity = prompt.complexity

    title = generate_title(topic)
    song = generate_song(topic, keywords, syllable_count, couplet_count, complexity)
    # song = format_song(song)
    # song = normalise_song(song, target_syllables=prompt.syllable_count)

    print(title + "\n")
    for couplet in song:
        print(couplet)
    
    return GeneratedLyrics(
        title=title,
        prompt=prompt,
        lyrics=song
    )

if __name__ == "__main__":
    sample_prompt = LyricsPrompt(
        topic="A Journey Through Time",
        keywords="adventure, history",
        line_length="medium",
        song_length="short",
        complexity="simple"
    )
    main(sample_prompt)