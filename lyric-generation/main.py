from time import sleep

from config import SONG_TOPIC, STANZA_COUNT, LINE_COUNT, SYLLABLE_COUNT
from model import load_model
from generator import generate_song
from parser import format_song, parse_to_lines
from normalize_song import normalize_song

def main() -> list[list[list[str]]]:
    print("Loading model...")
    load_model()
    
    print(f"Generating song about '{SONG_TOPIC}'...")
    raw_song = generate_song()

    sleep(1)

    print("Parsing song...")
    formatted_song = format_song(raw_song, STANZA_COUNT, LINE_COUNT)
    lines = parse_to_lines(formatted_song)

    sleep(1)
    
    print(f"Normalizing to {SYLLABLE_COUNT} syllables per line...")
    syllable_array = normalize_song(lines, SYLLABLE_COUNT)

    sleep(1)
    
    print("\n" + "=" * 40)
    print("FINAL SONG (Syllable Array):")
    print("=" * 40)
    for i, line_syllables in enumerate(syllable_array, 1):
        # Reconstruct line from syllables for display
        line_text = " ".join("".join(word) for word in line_syllables)
        print(f"{line_text}")
        if i % LINE_COUNT == 0 and i < len(syllable_array):
            print()
    print("=" * 40)

    sleep(1)
    
    print("\n3D SYLLABLE ARRAY:")
    print(syllable_array)
    
    return syllable_array


if __name__ == '__main__':
    result = main()
