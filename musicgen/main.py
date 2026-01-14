from transformers import pipeline
import time
import scipy.io.wavfile
import numpy as np

# Initialize the model
synthesiser = pipeline("text-to-audio", "facebook/musicgen-small")

# Genre configurations currently configured
GENRES = {
    "nursery_rhyme": {
        "prompt": """cheerful children's nursery rhyme, major key, simple melody with piano,
                    and acoustic guitar, playful and bouncy, 120 BPM""",
        "max_tokens": 1503,
        "target_duration": 120  # 2 minutes
    },
    "hip_hop": {
        "prompt": """hip hop beat with 808 bass, drum machine, trap hi-hats, minor key,
                     dark atmospheric synth pads, 90 BPM""",
        "max_tokens": 1503,
        "target_duration": 120
    },
    "rock": {
        "prompt": """energetic rock music with distorted electric guitar, driving drums 
                    with backbeat, bass guitar, power chords, 130 BPM""",
        "max_tokens": 1503,
        "target_duration": 120
    },
    "jazz": {
        "prompt": """smooth jazz with saxophone, piano, upright bass, brush drums, 
                    swing rhythm, improvisation, walking bass line, 120 BPM""",
        "max_tokens": 1503,
        "target_duration": 120
    },
    "classical": {
        "prompt": """classical orchestra with strings, woodwinds, brass, elegant melody, 
                    symphonic arrangement, dynamic crescendos, refined and sophisticated""",
        "max_tokens": 1503,
        "target_duration": 120
    },
    "reggae": {
        "prompt": """reggae with offbeat guitar skank, heavy bass, one drop drum pattern, 
                    relaxed groove, organ stabs, laid-back vibe, 80 BPM""",
        "max_tokens": 1503,
        "target_duration": 120
    },
    "rnb": {
        "prompt": """R&B with smooth vocals, electric piano, grooving bass, tight drums, 
                    soulful melody, contemporary production, 90 BPM""",
        "max_tokens": 1503,
        "target_duration": 120
    },
    "punk": {
        "prompt": """punk rock with fast distorted power chords, aggressive drums, 
                    driving bass, raw energy, rebellious attitude, 180 BPM""",
        "max_tokens": 1503,
        "target_duration": 120
    },
    "metal": {
        "prompt": """heavy metal with distorted guitars, palm-muted riffs, double bass drums, 
                    aggressive power chords, intense energy, 140 BPM""",
        "max_tokens": 1503,
        "target_duration": 120
    },
    "bollywood": {
        "prompt": """Bollywood music with tabla, sitar, orchestral strings, energetic dhol drums, 
                    melodic indian vocals style, vibrant and colorful, 120 BPM""",
        "max_tokens": 1503,
        "target_duration": 120
    }
}


def crossfade_sections(section1, section2, sample_rate, fade_duration=1.5):
    """
    Crossfade between two audio sections

    Args:
        section1: first audio section (numpy array)
        section2: second audio section (numpy array)
        sample_rate: sample rate
        fade_duration: duration of crossfade in seconds

    Returns:
        crossfaded audio
    """
    fade_samples = int(sample_rate * fade_duration)

    # Make sure sections are long enough
    if len(section1) < fade_samples or len(section2) < fade_samples:
        return np.concatenate([section1, section2])

    # Extract overlapping parts
    end_of_section1 = section1[-fade_samples:]
    start_of_section2 = section2[:fade_samples]

    # Create fade curves
    fade_out = np.cos(np.linspace(0, np.pi / 2, fade_samples)) ** 2
    fade_in = np.sin(np.linspace(0, np.pi / 2, fade_samples)) ** 2

    # Blend the overlap
    blended = (end_of_section1 * fade_out) + (start_of_section2 * fade_in)

    # Combine: section1 (without end) + blended + section2 (without start)
    result = np.concatenate([
        section1[:-fade_samples],
        blended,
        section2[fade_samples:]
    ])

    return result


def extend_audio(audio_data, sample_rate, target_duration=120, fade_duration=1.5):
    """
    Extend audio to target duration by repeating middle section with crossfades
    Pattern: [START] [MIDDLE] [BLENDED] [MIDDLE] [BLENDED] ... [END]

    Args:
        audio_data: original audio
        sample_rate: sample rate
        target_duration: target duration in seconds
        fade_duration: crossfade duration in seconds

    Returns:
        extended audio
    """
    original_duration = len(audio_data) / sample_rate
    fade_samples = int(sample_rate * fade_duration)

    # Split into START, MIDDLE, END
    # START: first 20% of audio
    # END: last 20% of audio
    # MIDDLE: the core 60% that we'll repeat
    section_size = len(audio_data) // 5

    start_section = audio_data[:section_size]
    end_section = audio_data[-section_size:]
    middle_section = audio_data[section_size:-section_size]

    print(f"Original audio: {original_duration:.1f}s")
    print(f"START section: {len(start_section) / sample_rate:.1f}s")
    print(f"MIDDLE section: {len(middle_section) / sample_rate:.1f}s")
    print(f"END section: {len(end_section) / sample_rate:.1f}s")

    # Start building the extended audio
    extended = start_section.copy()

    # Calculate how many times we need to repeat MIDDLE
    current_duration = len(extended) / sample_rate
    middle_duration = len(middle_section) / sample_rate

    repetitions = 0
    while current_duration + middle_duration + (len(end_section) / sample_rate) < target_duration:
        print(f"Adding MIDDLE repetition #{repetitions + 1}...")
        extended = crossfade_sections(extended, middle_section, sample_rate, fade_duration)
        current_duration = len(extended) / sample_rate
        repetitions += 1

    # Add the END section
    print("Adding END section...")
    extended = crossfade_sections(extended, end_section, sample_rate, fade_duration)

    final_duration = len(extended) / sample_rate
    print(f"Final duration: {final_duration:.1f}s ({repetitions} middle repetitions)")

    return extended


def generate_music(genre):
    if genre not in GENRES:
        raise ValueError(f"Genre must be one of: {list(GENRES.keys())}")

    config = GENRES[genre]
    print(f"\nGenerating {genre.replace('_', ' ')}...")
    print(f"Prompt: {config['prompt']}")
    print(f"Target duration: {config['target_duration']} seconds (~{config['target_duration'] / 60:.1f} minutes)")
    print("Generating base audio... (this will take a few minutes)\n")

    # Generate music with maximum possible tokens
    music = synthesiser(
        config["prompt"],
        forward_params={
            "do_sample": True,
            "max_new_tokens": config["max_tokens"]
        }
    )

    # Process audio data
    audio_data = music["audio"]
    if len(audio_data.shape) > 1:
        audio_data = audio_data.squeeze()

    # Convert to float for processing
    audio_data = audio_data.astype(np.float32)

    # Extend the audio to target duration
    print("\nExtending audio with crossfaded repetitions...")
    extended_audio = extend_audio(
        audio_data,
        music["sampling_rate"],
        target_duration=config["target_duration"],
        fade_duration=1.5
    )

    # Normalize and convert to int16
    if np.max(np.abs(extended_audio)) > 0:
        extended_audio = np.int16(extended_audio / np.max(np.abs(extended_audio)) * 32767)
    else:
        extended_audio = np.int16(extended_audio)

    # Save with descriptive filename
    filename = f"{genre}_extended_{int(time.time())}.wav"
    scipy.io.wavfile.write(
        filename,
        rate=music["sampling_rate"],
        data=extended_audio
    )

    actual_duration = len(extended_audio) / music["sampling_rate"]
    print(f"\n✓ Saved: {filename}")
    print(f"✓ Final duration: {actual_duration:.1f} seconds (~{actual_duration / 60:.1f} minutes)")
    return filename


# Example usage:
if __name__ == "__main__":
    choice = 0
    while choice != "11":
        print("\n" + "=" * 50)
        choice = input("Choose a genre (~2 minute extended versions):\n"
                       "1. Nursery Rhyme\n"
                       "2. Hip-Hop\n"
                       "3. Rock\n"
                       "4. Jazz\n"
                       "5. Classical\n"
                       "6. Reggae\n"
                       "7. R&B\n"
                       "8. Punk\n"
                       "9. Metal\n"
                       "10. Bollywood\n"
                       "11. Quit\n"
                       "Enter number: ")

        if choice == "1":
            generate_music("nursery_rhyme")
        elif choice == "2":
            generate_music("hip_hop")
        elif choice == "3":
            generate_music("rock")
        elif choice == "4":
            generate_music("jazz")
        elif choice == "5":
            generate_music("classical")
        elif choice == "6":
            generate_music("reggae")
        elif choice == "7":
            generate_music("rnb")
        elif choice == "8":
            generate_music("punk")
        elif choice == "9":
            generate_music("metal")
        elif choice == "10":
            generate_music("bollywood")
        elif choice == "11":
            print("\nGoodbye!")
        else:
            print("Invalid choice. Please try again.")