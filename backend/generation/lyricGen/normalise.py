import random
from typing import List
import pyphen

FILLER_WORDS = ["Oh", "Ah", "Hey", "Yeah", "Ooh", "Hmm", "Whoa", "Yay", "Woo"]

def split_word(word: str) -> List[str]:
    hyphenator = pyphen.Pyphen(lang='en_GB')

    clean = ''.join(c for c in word.lower() if c.isalpha())

    if not clean:
        return []
    
    hyphenated = hyphenator.inserted(clean)
    syllables = hyphenated.split('-')

    return syllables


def line_to_array(line: str) -> List[List[str]]:
    words = line.split()
    return [split_word(word) for word in words]


def count_syllables(line: List[List[str]]):
    return sum(len(syllable) for syllable in line)


def add_fillers(line: List[List[str]], needed: int) -> List[List[str]]:
    fillers = [[random.choice(FILLER_WORDS)] for _ in range(needed)]
    return fillers + line 


def combine_syllables(line: List[List[str]], excess: int) -> List[List[str]]:
    if excess <= 0:
        return line
    
    result = [list(word) for word in line]
    reductions = 0

    while reductions < excess:
        max_idx = -1
        max_len = 1
        min_idx = 0
        min_len = float('inf')

        for i, word in enumerate(result):
            if len(word) > max_len:
                max_len = len(word)
                max_idx = i
            
            if len(word[0]) < min_len:
                min_len = len(word[0])
                min_idx = i
        
        if max_idx != -1:
            result[max_idx][0] = result[max_idx][0] + result[max_idx][1]
            result[max_idx].pop(1)
            reductions += 1
        else:
            if len(result) < 2:
                break
            
            if min_idx < len(result) - 1:
                result[min_idx] = [result[min_idx][0] + " " + result[min_idx + 1][0]]
                result.pop(min_idx + 1)
            else:
                result[min_idx - 1] = [result[min_idx - 1][0] + " " + result[min_idx][0]]
                result.pop(min_idx)
            
            reductions += 1

    return result


def normalise_line(line: str, target_syllables: int) -> List[List[str]]:
    array = line_to_array(line)
    current = count_syllables(array)
    
    if current == target_syllables:
        return array
    elif current < target_syllables:
        needed = target_syllables - current
        return add_fillers(array, needed)
    else:
        excess = current - target_syllables
        return combine_syllables(array, excess)


def normalise_song(song: list[str], target_syllables: int) -> list[list[list[str]]]:
    return [normalise_line(line, target_syllables) for line in song]