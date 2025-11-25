# ========================
# MAIN ENTRY POINT
# ========================
# Generate a song, count syllables, normalize, and output 2D syllable array

from config import SONG_TOPIC, STANZA_COUNT, LINE_COUNT, SYLLABLE_COUNT
from model import load_model
from generator import generate_song
from parser import format_song, parse_to_lines
from syllable_counter import count_syllables_in_line, get_syllable_breakdown
from normalize_song import normalize_song


def main() -> list[list[str]]:
    """
    Generate a song, normalize syllables, and return 2D syllable array.
    
    Returns:
        2D array where each line is an array of syllable strings
    """
    
    # Load the model
    print("Loading model...")
    load_model()
    
    # Step 1: Generate the song (stanza by stanza)
    print(f"\n🎵 Generating song about: {SONG_TOPIC}")
    print(f"   ({STANZA_COUNT} stanzas, {LINE_COUNT} lines each)")
    print("=" * 60)
    
    raw_song = generate_song()
    
    print(f"\n📝 Generated Song:\n{raw_song}\n")
    print("=" * 60)
    
    # Step 2: Parse the song (remove headings, empty lines, numbering)
    formatted_song = format_song(raw_song, STANZA_COUNT, LINE_COUNT)
    lines = parse_to_lines(formatted_song)
    
    print(f"\n✂️ Parsed Lines ({len(lines)} lines):")
    for i, line in enumerate(lines, 1):
        print(f"   {i}. {line}")
    print("=" * 60)
    
    # Step 3: Count syllables per line (before normalization)
    print(f"\n📊 Syllable Count (target: {SYLLABLE_COUNT}):\n")
    
    for i, line in enumerate(lines, 1):
        syllable_count = count_syllables_in_line(line)
        breakdown = get_syllable_breakdown(line)
        breakdown_str = ", ".join(f"{w}={s}" for w, s in breakdown)
        
        status = "✅" if syllable_count == SYLLABLE_COUNT else "❌"
        diff = syllable_count - SYLLABLE_COUNT
        diff_str = f"({diff:+d})" if diff != 0 else ""
        
        print(f"{status} Line {i}: {syllable_count} syllables {diff_str}")
        print(f"   \"{line}\"")
        print(f"   [{breakdown_str}]\n")
    
    print("=" * 60)
    
    # Step 4: Normalize the song
    print(f"\n🔧 Normalizing song to {SYLLABLE_COUNT} syllables per line...\n")
    
    result = normalize_song(lines, SYLLABLE_COUNT)
    
    # Show normalization details
    for i, detail in enumerate(result['details'], 1):
        action_icon = {
            'none': '✅',
            'added_fillers': '➕',
            'combined_words': '🔗'
        }.get(detail['action'], '?')
        
        print(f"{action_icon} Line {i}: {detail['action']}")
        print(f"   Original ({detail['original_count']}): \"{detail['original']}\"")
        print(f"   Normalized ({detail['final_count']}): \"{detail['normalized']}\"")
        print(f"   Syllables: {detail['syllables']}\n")
    
    print("=" * 60)
    
    # Step 5: Output the final 2D syllable array
    syllable_array = result['syllable_array']
    
    print(f"\n🎼 Final 2D Syllable Array ({len(syllable_array)} lines):\n")
    for i, line_syllables in enumerate(syllable_array, 1):
        print(f"   Line {i}: {line_syllables}")
    
    print("\n" + "=" * 60)
    print("✨ Song generation complete!")
    
    return syllable_array


if __name__ == '__main__':
    result = main()
    print(f"\n📦 Returned syllable_array: {result}")
