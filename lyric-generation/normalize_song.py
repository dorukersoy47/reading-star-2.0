# ========================
# NORMALIZE SONG MODULE
# ========================
# Adjusts lines to match target syllable count and formats output

import random
from syllable_counter import count_syllables_in_line, count_syllables_in_word, split_word_into_syllables

# Filler words (1 syllable each) to add when line is too short
FILLER_WORDS = ["Oh", "Ah", "Hey", "Yeah", "Ooh", "Hmm", "Whoa", "Yay", "Woo"]


def add_fillers_to_line(line: str, current_syllables: int, target_syllables: int) -> str:
    needed = target_syllables - current_syllables
    if needed <= 0:
        return line
    
    # Select fillers randomly
    fillers = [random.choice(FILLER_WORDS) for _ in range(needed)]
    
    # Join fillers and prepend to line
    filler_str = " ".join(fillers)
    return f"{filler_str} {line}"


def combine_words_for_syllables(words: list[str], current_syllables: int, target_syllables: int) -> list[str]:
    """
    Combine adjacent words to reduce syllable count.
    Prioritizes combining the shortest adjacent word pairs first.
    
    Args:
        words: List of words in the line
        current_syllables: Current syllable count
        target_syllables: Target syllable count
        
    Returns:
        List of words with some combined using '~'
    """
    excess = current_syllables - target_syllables
    if excess <= 0 or len(words) < 2:
        return words
    
    # Work with a mutable list
    result = list(words)
    combinations_made = 0
    
    while combinations_made < excess and len(result) >= 2:
        # Find the adjacent pair with the shortest total length
        min_length = float('inf')
        min_index = -1
        
        for i in range(len(result) - 1):
            # Calculate combined length of adjacent pair
            pair_length = len(result[i]) + len(result[i + 1])
            if pair_length < min_length:
                min_length = pair_length
                min_index = i
        
        if min_index == -1:
            break
        
        # Combine the shortest pair
        combined = f"{result[min_index]}~{result[min_index + 1]}"
        result = result[:min_index] + [combined] + result[min_index + 2:]
        combinations_made += 1
    
    return result


def split_line_to_syllables(line: str, target_syllables: int) -> list[list[str]]:
    # Split by spaces to get words/word-groups
    parts = line.split()
    word_syllables = []
    
    for part in parts:
        if "~" in part:
            # Combined words - keep them together as one unit
            # Split each component and flatten, but mark as combined
            combined_parts = part.split("~")
            all_syllables = []
            for subpart in combined_parts:
                syllables = split_word_into_syllables(subpart)
                all_syllables.extend(syllables)
            # Join with ~ to show they're combined (sung as one beat)
            word_syllables.append(["~".join(all_syllables)])
        else:
            # Regular word - split into syllables
            syllables = split_word_into_syllables(part)
            word_syllables.append(syllables)
    
    return word_syllables


def normalize_line(line: str, target_syllables: int) -> dict:
    current_syllables = count_syllables_in_line(line)
    
    if current_syllables == target_syllables:
        # Already correct
        syllable_list = split_line_to_syllables(line, target_syllables)
        return {
            'original': line,
            'normalized': line,
            'syllables': syllable_list,
            'action': 'none',
            'original_count': current_syllables,
            'final_count': target_syllables
        }
    
    elif current_syllables < target_syllables:
        # Too short - add fillers
        normalized = add_fillers_to_line(line, current_syllables, target_syllables)
        syllable_list = split_line_to_syllables(normalized, target_syllables)
        return {
            'original': line,
            'normalized': normalized,
            'syllables': syllable_list,
            'action': 'added_fillers',
            'original_count': current_syllables,
            'final_count': target_syllables
        }
    
    else:
        # Too long - combine words
        words = line.split()
        combined_words = combine_words_for_syllables(words, current_syllables, target_syllables)
        normalized = " ".join(combined_words)
        syllable_list = split_line_to_syllables(normalized, target_syllables)
        return {
            'original': line,
            'normalized': normalized,
            'syllables': syllable_list,
            'action': 'combined_words',
            'original_count': current_syllables,
            'final_count': target_syllables
        }


def normalize_song(lines: list[str], target_syllables: int) -> dict:
    normalized_lines = []
    syllable_array = []
    details = []
    
    for line in lines:
        result = normalize_line(line, target_syllables)
        normalized_lines.append(result['normalized'])
        syllable_array.append(result['syllables'])
        details.append(result)
    
    return {
        'normalized_lines': normalized_lines,
        'syllable_array': syllable_array,
        'details': details
    }
