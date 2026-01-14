import random
import pyphen

FILLER_WORDS = ["Oh", "Ah", "Hey", "Yeah", "Ooh", "Hmm", "Whoa", "Yay", "Woo"]

def line_to_syllable_array(line: str) -> list[list[str]]:
    
    def split_word_into_syllables(word: str) -> list[str]:
        _hyphenator = pyphen.Pyphen(lang='en_US')

        clean = ''.join(c for c in word.lower() if c.isalpha())
        
        if not clean:
            return []
        
        hyphenated = _hyphenator.inserted(clean)
        syllables = hyphenated.split('-')
        
        if len(syllables) == 1:
            return [word]
        
        result = []
        pos = 0
        for syl in syllables:
            syl_len = len(syl)
            original_part = word[pos:pos + syl_len]
            result.append(original_part)
            pos += syl_len
        
        return result if result else [word]
    
    words = line.split()
    return [split_word_into_syllables(word) for word in words]


def count_total_syllables(syllable_array: list[list[str]]) -> int:
    return sum(len(word_syllables) for word_syllables in syllable_array)


def add_fillers(syllable_array: list[list[str]], needed: int) -> list[list[str]]:
    fillers = [[random.choice(FILLER_WORDS)] for _ in range(needed)]
    return fillers + syllable_array


def combine_syllables(syllable_array: list[list[str]], excess: int) -> list[list[str]]:
    if excess <= 0:
        return syllable_array
    
    multi_syllable_indices = []
    for i, word_syllables in enumerate(syllable_array):
        if len(word_syllables) >= 2:
            multi_syllable_indices.append((i, len(word_syllables)))
    
    multi_syllable_indices.sort(key=lambda x: x[1])
    
    result = [list(word) for word in syllable_array]  # Deep copy
    reductions_made = 0
    
    for word_idx, _ in multi_syllable_indices:
        if reductions_made >= excess:
            break
        
        word_syllables = result[word_idx]
        
        while len(word_syllables) >= 2 and reductions_made < excess:
            word_syllables[0] = word_syllables[0] + word_syllables[1]
            word_syllables.pop(1)
            reductions_made += 1
        
        result[word_idx] = word_syllables
    
    return result


def normalize_line(line: str, target_syllables: int) -> list[list[str]]:
    syllable_array = line_to_syllable_array(line)
    current_syllables = count_total_syllables(syllable_array)
    
    if current_syllables == target_syllables:
        return syllable_array
    elif current_syllables < target_syllables:
        needed = target_syllables - current_syllables
        return add_fillers(syllable_array, needed)
    else:
        excess = current_syllables - target_syllables
        return combine_syllables(syllable_array, excess)


def normalize_song(lines: list[str], target_syllables: int) -> list[list[list[str]]]:
    return [normalize_line(line, target_syllables) for line in lines]