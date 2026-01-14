from generation.lyricGen.generator import generate_song, generate_title
from generation.lyricGen.parser import format_song, parse_to_lines
from generation.lyricGen.normalise import normalise_song
from models.generation import LyricsPrompt, GeneratedLyrics

def main(prompt : LyricsPrompt) -> GeneratedLyrics:
    title = generate_title(prompt.topic)
    raw_song = generate_song(topic=prompt.topic, stanza_count=prompt.stanza_count, syllable_count=prompt.syllable_count)

    formatted_song = format_song(raw_song, stanza_count=prompt.stanza_count)
    lines = parse_to_lines(formatted_song)

    syllable_array = normalise_song(lines, target_syllables=prompt.syllable_count)
    
    return GeneratedLyrics(
        title=title,
        prompt=prompt,
        lyrics=syllable_array
    )
