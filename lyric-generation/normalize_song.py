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
    Reduce syllable count by marking multi-syllable words to be sung as fewer syllables.
    Prioritizes shorter words first (fewer syllables = less distortion when merged).
    
    Words marked with internal '~' indicate syllables should be sung together.
    E.g., "heroes" (2 syl) -> "he~roes" (sung as 1 syl)
    
    Args:
        words: List of words in the line
        current_syllables: Current syllable count
        target_syllables: Target syllable count
        
    Returns:
        List of words, some with '~' marking merged syllables
    """
    from syllable_counter import count_syllables_in_word, split_word_into_syllables
    
    excess = current_syllables - target_syllables
    if excess <= 0:
        return words
    
    # Build list of (index, word, syllable_count) for multi-syllable words
    # Sorted by syllable count (shortest first = priority)
    multi_syllable_words = []
    for i, word in enumerate(words):
        syl_count = count_syllables_in_word(word)
        if syl_count >= 2:
            multi_syllable_words.append((i, word, syl_count))
    
    # Sort by syllable count (prioritize shorter words)
    multi_syllable_words.sort(key=lambda x: x[2])
    
    result = list(words)
    reductions_made = 0
    
    for idx, word, syl_count in multi_syllable_words:
        if reductions_made >= excess:
            break
        
        # Split word into syllables
        syllables = split_word_into_syllables(word)
        
        if len(syllables) < 2:
            continue
        
        # Calculate how many syllables we can merge in this word
        # We can reduce (syl_count - 1) at most (merge all into 1)
        max_reduction = len(syllables) - 1
        needed_reduction = excess - reductions_made
        actual_reduction = min(max_reduction, needed_reduction)
        
        # Merge syllables from the end
        # E.g., ['he', 'ro', 'es'] with reduction=1 -> ['he', 'ro~es']
        # E.g., ['he', 'ro', 'es'] with reduction=2 -> ['he~ro~es']
        merged_count = actual_reduction + 1  # How many syllables to merge into one
        
        if merged_count >= len(syllables):
            # Merge all syllables
            merged_word = "~".join(syllables)
        else:
            # Keep some syllables separate, merge the last ones
            keep_separate = syllables[:-merged_count]
            merge_together = syllables[-merged_count:]
            merged_word = "~".join(keep_separate + ["~".join(merge_together)])
        
        result[idx] = merged_word
        reductions_made += actual_reduction
    
    return result


def split_line_to_syllables(line: str, target_syllables: int) -> list[list[str]]:
    """
    Split a line into a 3D structure: list of words, where each word is a list of syllables.
    
    Words with '~' indicate merged syllables (sung as one beat).
    E.g., "he~roes" -> [['he~roes']] (one syllable unit)
    E.g., "heroes" -> [['he', 'roes']] (two syllables)
    
    Args:
        line: The normalized line (may contain ~ for merged syllables)
        target_syllables: Target number of syllables (for reference)
        
    Returns:
        List of words, where each word is a list of its syllable strings
    """
    # Split by spaces to get words
    parts = line.split()
    word_syllables = []
    
    for part in parts:
        if "~" in part:
            # Word has merged syllables - the merged portion counts as 1 syllable
            # Split by ~ to find merged groups, but keep the ~ notation
            segments = part.split("~")
            
            # For display, we keep the merged syllables joined with ~
            # Each segment that was merged together becomes one "syllable unit"
            # But we need to reconstruct which are merged vs separate
            
            # Simple approach: the whole thing with ~ is one merged unit
            word_syllables.append([part])
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
