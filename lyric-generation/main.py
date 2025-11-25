# ========================
# MAIN ENTRY POINT
# ========================
# Generate a song, count syllables, normalize, and output 3D syllable array

from config import SONG_TOPIC, STANZA_COUNT, LINE_COUNT, SYLLABLE_COUNT
from model import load_model
from generator import generate_song
from parser import format_song, parse_to_lines
from normalize_song import normalize_song


def main() -> list[list[list[str]]]:
    """
    Generate a song, normalize syllables, and return 3D syllable array.
    
    Returns:
        3D array: lines -> words -> syllables
        e.g., [[['The'], ['he', 'roes'], ['fly']], ...]
    """
    
    # Load the model
    print("Loading model...")
    load_model()
    
    # Step 1: Generate the song
    print(f"Generating song about '{SONG_TOPIC}'...")
    raw_song = generate_song()
    
    # Step 2: Parse the song
    print("Parsing song...")
    formatted_song = format_song(raw_song, STANZA_COUNT, LINE_COUNT)
    lines = parse_to_lines(formatted_song)
    
    # Step 3: Normalize the song
    print(f"Normalizing to {SYLLABLE_COUNT} syllables per line...")
    result = normalize_song(lines, SYLLABLE_COUNT)
    
    # Output: Final song
    print("\n" + "=" * 40)
    print("FINAL SONG:")
    print("=" * 40)
    for i, line in enumerate(result['normalized_lines'], 1):
        print(f"{line}")
        # Add blank line between stanzas
        if i % LINE_COUNT == 0 and i < len(result['normalized_lines']):
            print()
    print("=" * 40)
    
    # Output: 3D syllable array
    syllable_array = result['syllable_array']
    print("\n3D SYLLABLE ARRAY:")
    print(syllable_array)
    
    return syllable_array


if __name__ == '__main__':
    result = main()
