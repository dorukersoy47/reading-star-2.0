import time
import scipy.io.wavfile
import numpy as np
from pathlib import Path
from transformers import pipeline

# Local imports
from ..config import MUSIC_MAX_TOKENS, GENRES, MUSIC_MODEL_PATH
from audio_util import extend_audio

print("Initializing AI Model...")
synthesiser = pipeline("text-to-audio", model=MUSIC_MODEL_PATH)


def generate_music(genre, output_folder: Path = None):
    if genre not in GENRES:
        raise ValueError(f"Genre must be one of: {list(GENRES.keys())}")

    config = GENRES[genre]
    print(f"\nGenerating {genre.replace('_', ' ')}...")
    print(f"Prompt: {config['prompt']}")
    print("Generating base audio... (this will take a few minutes)\n")

    # Generate music
    music = synthesiser(
        config["prompt"],
        forward_params={
            "do_sample": True,
            "max_new_tokens": MUSIC_MAX_TOKENS
        }
    )

    audio_data = music["audio"]
    if len(audio_data.shape) > 1:
        audio_data = audio_data.squeeze()

    audio_data = audio_data.astype(np.float32)

    print("\nExtending audio with crossfaded repetitions...")
    extended_audio = extend_audio(
        audio_data,
        music["sampling_rate"],
        target_duration=config["target_duration"],
        fade_duration=1.5
    )

    # Normalize
    if np.max(np.abs(extended_audio)) > 0:
        extended_audio = np.int16(extended_audio / np.max(np.abs(extended_audio)) * 32767)
    else:
        extended_audio = np.int16(extended_audio)

    # Save file
    filename = f"{genre}_extended_{int(time.time())}.wav"

    if output_folder:
        output_folder.mkdir(parents=True, exist_ok=True)
        file_path = output_folder / filename
    else:
        file_path = Path(filename)

    scipy.io.wavfile.write(
        str(file_path),
        rate=music["sampling_rate"],
        data=extended_audio
    )

    print(f"\n✓ Saved: {file_path}")
    return str(file_path)