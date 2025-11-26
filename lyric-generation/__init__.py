# ========================
# Lyric Generation Package
# ========================
# A modular system for generating children's songs with syllable counting

"""
Lyric Generation Package
========================

Modules:
--------
- config: Central configuration constants
- model: LLM model loading and text generation
- generator: Song generation
- parser: Song text formatting and parsing
- syllable_counter: Syllable counting methods
- normalize_song: Normalize lines to target syllable count

Usage:
------
    python main.py
"""

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

from syllable_counter import (
    count_syllables_in_word,
    count_syllables_in_line,
    count_syllables_per_line,
    get_syllable_breakdown,
    split_word_into_syllables
)

from normalize_song import (
    normalize_song,
    normalize_line,
    add_fillers_to_line,
    combine_words_for_syllables,
    split_line_to_syllables,
    FILLER_WORDS
)

__version__ = "2.0.0"
__all__ = [
    # Config
    'SONG_TOPIC', 'STANZA_COUNT', 'LINE_COUNT', 'SEQUENCE', 'SYLLABLE_COUNT',
    # Generator
    'generate_song',
    # Parser
    'format_song', 'parse_to_lines', 'remove_headings', 
    'remove_empty_lines', 'remove_numbering', 'crop_to_expected_lines',
    # Syllable counter
    'count_syllables_in_word', 'count_syllables_in_line',
    'count_syllables_per_line', 'get_syllable_breakdown',
    # Normalize song
    'normalize_song', 'normalize_line', 'add_fillers_to_line',
    'combine_words_for_syllables', 'split_line_to_syllables', 'FILLER_WORDS',
]
