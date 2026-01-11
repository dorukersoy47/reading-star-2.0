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
        "max_tokens": 1503  # Maximum for musicgen-small
    },
    "hip_hop": {
        "prompt": """hip hop beat with 808 bass, drum machine, trap hi-hats, minor key,
                     dark atmospheric synth pads, 90 BPM""",
        "max_tokens": 1503
    },
    "rock": {
        "prompt": """energetic rock music with distorted electric guitar, driving drums 
                    with backbeat, bass guitar, power chords, 130 BPM""",
        "max_tokens": 1503
    },
    "jazz": {
        "prompt": """smooth jazz with saxophone, piano, upright bass, brush drums, 
                    swing rhythm, improvisation, walking bass line, 120 BPM""",
        "max_tokens": 1503
    },
    "classical": {
        "prompt": """classical orchestra with strings, woodwinds, brass, elegant melody, 
                    symphonic arrangement, dynamic crescendos, refined and sophisticated""",
        "max_tokens": 1503
    },
    "reggae": {
        "prompt": """reggae with offbeat guitar skank, heavy bass, one drop drum pattern, 
                    relaxed groove, organ stabs, laid-back vibe, 80 BPM""",
        "max_tokens": 1503
    },
    "rnb": {
        "prompt": """R&B with smooth vocals, electric piano, grooving bass, tight drums, 
                    soulful melody, contemporary production, 90 BPM""",
        "max_tokens": 1503
    },
    "punk": {
        "prompt": """punk rock with fast distorted power chords, aggressive drums, 
                    driving bass, raw energy, rebellious attitude, 180 BPM""",
        "max_tokens": 1503
    },
    "metal": {
        "prompt": """heavy metal with distorted guitars, palm-muted riffs, double bass drums, 
                    aggressive power chords, intense energy, 140 BPM""",
        "max_tokens": 1503
    },
    "bollywood": {
        "prompt": """Bollywood music with tabla, sitar, orchestral strings, energetic dhol drums, 
                    melodic indian vocals style, vibrant and colorful, 120 BPM""",
        "max_tokens": 1503
    }
}


def generate_music(genre):
    if genre not in GENRES:
        raise ValueError(f"Genre must be one of: {list(GENRES.keys())}")

    config = GENRES[genre]
    print(f"\nGenerating {genre.replace('_', ' ')}...")
    print(f"Prompt: {config['prompt']}")
    print(f"Using maximum tokens: {config['max_tokens']}")
    print("Generating... (this will take a few minutes)\n")

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

    # Normalize and convert to int16
    if np.max(np.abs(audio_data)) > 0:
        audio_data = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)
    else:
        audio_data = np.int16(audio_data)

    # Save with descriptive filename
    filename = f"{genre}_{int(time.time())}.wav"
    scipy.io.wavfile.write(
        filename,
        rate=music["sampling_rate"],
        data=audio_data
    )

    actual_duration = len(audio_data) / music["sampling_rate"]
    print(f"✓ Saved: {filename}")
    print(f"✓ Duration: {actual_duration:.2f} seconds (~{actual_duration / 60:.1f} minutes)")
    return filename


# Example usage:
if __name__ == "__main__":
    choice = 0
    while choice != "11":
        print("\n" + "=" * 50)
        choice = input("Choose a genre (max length ~30 seconds):\n"
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