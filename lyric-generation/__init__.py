from config import (
    SONG_TOPIC, STANZA_COUNT, LINE_COUNT, SEQUENCE, SYLLABLE_COUNT
)

from generator import generate_song

from parser import (
    format_song,
    parse_to_lines,
    remove_headings,
    remove_empty_lines,
    remove_numbering,
    crop_to_expected_lines
)

from normalize_song import (
    normalize_song,
    normalize_line,
    FILLER_WORDS
)

__version__ = "1.0.0"
__all__ = [
    # Config
    'SONG_TOPIC', 'STANZA_COUNT', 'LINE_COUNT', 'SEQUENCE', 'SYLLABLE_COUNT',
    # Generator
    'generate_song',
    # Parser
    'format_song', 'parse_to_lines', 'remove_headings', 
    'remove_empty_lines', 'remove_numbering', 'crop_to_expected_lines',
    # Normalize song
    'normalize_song', 'normalize_line', 'FILLER_WORDS',
]
