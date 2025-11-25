# ========================
# NORMALIZE SONG MODULE
# ========================
# Adjusts lines to match target syllable count and formats output

from syllable_counter import count_syllables_in_line, count_syllables_in_word

# Filler words (1 syllable each) to add when line is too short
FILLER_WORDS = ["Oh", "Ah", "Hey", "Yeah", "Ooh", "Hmm", "Whoa", "Yay", "Woo"]


def add_fillers_to_line(line: str, current_syllables: int, target_syllables: int) -> str:
    """
    Add filler words at the start of a line to reach target syllable count.
    
    Args:
        line: The original line
        current_syllables: Current syllable count
        target_syllables: Target syllable count
        
    Returns:
        Line with filler words prepended
    """
    needed = target_syllables - current_syllables
    if needed <= 0:
        return line
    
    # Select fillers (cycle through the list if needed)
    fillers = []
    for i in range(needed):
        fillers.append(FILLER_WORDS[i % len(FILLER_WORDS)])
    
    # Join fillers and prepend to line
    filler_str = " ".join(fillers)
    return f"{filler_str} {line}"


def combine_words_for_syllables(words: list[str], current_syllables: int, target_syllables: int) -> list[str]:
    """
    Combine adjacent words with '~' to indicate they should be sung as fewer syllables.
    This marks words to be slurred together in singing.
    
    Args:
        words: List of words in the line
        current_syllables: Current syllable count
        target_syllables: Target syllable count
        
    Returns:
        List of words/word-groups with some combined using '~'
    """
    excess = current_syllables - target_syllables
    if excess <= 0:
        return words
    
    result = []
    i = 0
    combinations_made = 0
    
    while i < len(words):
        if combinations_made < excess and i + 1 < len(words):
            # Combine this word with the next one
            # The '~' indicates these words are sung together as one beat
            combined = f"{words[i]}~{words[i+1]}"
            result.append(combined)
            combinations_made += 1
            i += 2  # Skip the next word since we combined it
        else:
            result.append(words[i])
            i += 1
    
    return result


def split_line_to_syllables(line: str, target_syllables: int) -> list[str]:
    """
    Split a line into a list of syllable strings.
    Words that are combined (with ~) count as one syllable unit.
    
    Args:
        line: The normalized line (may contain ~ for combined words)
        target_syllables: Target number of syllables
        
    Returns:
        List of strings, one per syllable beat
    """
    # Split by spaces to get words/word-groups
    parts = line.split()
    syllables = []
    
    for part in parts:
        if "~" in part:
            # Combined words count as one syllable unit
            syllables.append(part)
        else:
            # Split word into its syllables (approximate by distributing)
            word_syllable_count = count_syllables_in_word(part)
            if word_syllable_count == 1:
                syllables.append(part)
            else:
                # For multi-syllable words, we add the word once per syllable
                # with a marker to show which syllable it is
                for s in range(word_syllable_count):
                    if s == 0:
                        syllables.append(part)  # First syllable gets the word
                    else:
                        syllables.append("-")   # Continuation marker
    
    return syllables


def normalize_line(line: str, target_syllables: int) -> dict:
    """
    Normalize a single line to match target syllable count.
    
    Args:
        line: Original line text
        target_syllables: Target syllable count
        
    Returns:
        Dict with 'original', 'normalized', 'syllables' (list), and 'action' taken
    """
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
    """
    Normalize all lines of a song to match target syllable count.
    
    Args:
        lines: List of line strings
        target_syllables: Target syllables per line
        
    Returns:
        Dict with:
        - 'normalized_lines': List of normalized line strings
        - 'syllable_array': 2D array - each line is an array of syllable strings
        - 'details': List of detailed info for each line
    """
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
