import time
import scipy.io.wavfile
import numpy as np
import sys
from pathlib import Path
from transformers import MusicgenForConditionalGeneration, AutoProcessor

# Local imports
from generation.config import MUSIC_MAX_TOKENS, GENRES
from .audio_util import extend_audio
from models.generation import InstrumentalPrompt

# Path to the locally downloaded model
LOCAL_MODEL_PATH = Path(__file__).parent.parent / "ai_models" / "music_model"

processor = AutoProcessor.from_pretrained(LOCAL_MODEL_PATH)
model = MusicgenForConditionalGeneration.from_pretrained(LOCAL_MODEL_PATH)


def generate_music(prompt: InstrumentalPrompt, output_folder: Path = None):
    if prompt.genre not in GENRES:
        raise ValueError(f"Genre must be one of: {list(GENRES.keys())}")

    config = GENRES[prompt.genre]
    bpm = prompt.bpm if prompt.bpm else config["bpm"]
    keywords = f" It should be {prompt.keywords}." if prompt.keywords else ""
    text = f"{config["prompt"]}, {bpm} BPM.{keywords}"
    print(f"\nGenerating {prompt.genre.replace('_', ' ')}...")
    print(f"Prompt: {text}")
    print("Generating base audio... (this will take a few minutes)\n")

    # Prepare inputs using the processor
    inputs = processor(
        text=[text],
        padding=True,
        return_tensors="pt"
    )

    # Generate music using ONNX model
    audio_values = model.generate(
        **inputs,
        do_sample=True,
        max_new_tokens=MUSIC_MAX_TOKENS
    )

    # Extract audio data
    audio_data = audio_values[0, 0].numpy()
    sampling_rate = model.config.audio_encoder.sampling_rate

    print("\nExtending audio with crossfaded repetitions...")
    extended_audio = extend_audio(
        audio_data,
        sampling_rate,
        target_duration=config["target_duration"],
        fade_duration=1.5
    )

    # Normalize
    if np.max(np.abs(extended_audio)) > 0:
        extended_audio = np.int16(extended_audio / np.max(np.abs(extended_audio)) * 32767)
    else:
        extended_audio = np.int16(extended_audio)

    # Save file
    filename = f"instrumental.wav"

    if output_folder:
        output_folder.mkdir(parents=True, exist_ok=True)
        file_path = output_folder / filename
    else:
        file_path = Path(filename)

    scipy.io.wavfile.write(
        str(file_path),
        rate=sampling_rate,
        data=extended_audio
    )

    print(f"\n✓ Saved: {file_path}")
    return str(file_path)