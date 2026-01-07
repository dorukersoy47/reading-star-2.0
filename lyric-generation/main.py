from time import sleep
import time

from config import SONG_TOPIC, STANZA_COUNT, LINE_COUNT, SYLLABLE_COUNT
from generator import generate_song
from parser import format_song, parse_to_lines
from normalize_song import normalize_song

def main() -> list[list[list[str]]]:
    print(f"Generating song about '{SONG_TOPIC}'...")
    start = time.time()
    raw_song = generate_song()
    end = time.time()
    print(f"Total Time Spent: {end - start}")

    sleep(1)

    print("Parsing song...")
    formatted_song = format_song(raw_song, STANZA_COUNT, LINE_COUNT)
    lines = parse_to_lines(formatted_song)

    sleep(1)
    
    print(f"Normalizing to {SYLLABLE_COUNT} syllables per line...")
    syllable_array = normalize_song(lines, SYLLABLE_COUNT)

    sleep(1)

    print("FINAL SONG:")
    print(formatted_song)

    sleep(1)
    
    print("\nSYLLABLE ARRAY:")
    print(syllable_array)
    
    return syllable_array


if __name__ == '__main__':
    result = main()
