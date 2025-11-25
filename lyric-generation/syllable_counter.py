# ========================
# SYLLABLE COUNTING MODULE
# ========================
# Libraries and methods for counting syllables in text

import re
import nltk
from nltk.corpus import cmudict

# Ensure CMUDict is downloaded for syllable counting
try:
    _cmudict = cmudict.dict()
except LookupError:
    nltk.download('cmudict')
    _cmudict = cmudict.dict()


def _count_syllables_fallback(word: str) -> int:
    word = word.lower().strip()
    if not word:
        return 0
    
    vowels = "aeiouy"
    count = 0
    prev_is_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel
    
    # Handle silent 'e' at end
    if word.endswith('e') and count > 1 and not word.endswith(('le', 'ee', 'ie', 'ye')):
        count -= 1
    
    # Handle "-le" endings
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        count += 1
    
    return max(1, count)


def count_syllables_in_word(word: str) -> int:
    clean = ''.join(c for c in word.lower() if c.isalpha())
    
    if not clean:
        return 0
    
    # Try CMUDict first (phoneme-based, most accurate)
    if clean in _cmudict:
        pronunciations = _cmudict[clean]
        return max(len([ph for ph in pron if ph[-1].isdigit()]) for pron in pronunciations)
    
    # Fallback for words not in dictionary
    return _count_syllables_fallback(clean)


def count_syllables_in_line(line: str) -> int:
    words = re.findall(r"[a-zA-Z']+", line)
    return sum(count_syllables_in_word(word) for word in words)


def count_syllables_per_line(lines: list[str]) -> list[int]:
    return [count_syllables_in_line(line) for line in lines]


def get_syllable_breakdown(line: str) -> list[tuple[str, int]]:
    words = re.findall(r"[a-zA-Z']+", line)
    return [(word, count_syllables_in_word(word)) for word in words]
