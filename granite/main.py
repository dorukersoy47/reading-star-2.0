import torch
import json
import os

from transformers import AutoModelForCausalLM, AutoTokenizer

os.environ['USE_TF'] = '0'
os.environ['USE_TORCH'] = '1'

# --- 1. Define Available Instruments ---
AVAILABLE_INSTRUMENTS = {
    "glockenspiel": 0,
    "music_box": 1,
    "celesta": 2,
    "marimba": 3,
    "toy_piano": 4,
    "ocarina": 5,
    "ukulele": 6,
    "harp": 7,
    "synth_chord": 8,
    "pizzicato": 9,
    "bass": 10,
    "brass": 11,
    "vibraphone": 12,
    "drumkit": 13
}

# --- 2. Define Genre Rules ---
HIPHOP_RULES = """
- 90 BPM (fixed)
- 4/4 time signature
- Rhythm: Kick pattern on beats 1 and 3; Snare pattern on beats 2 and 4
- Harmony: Minor keys. Use a simple 2-4 chord loop (e.g., C minor)
- Available Instruments: Synth Chord (channel 8), Bass (channel 10), Drumkit (channel 13)
- Drumkit notes: hand_drum (pitch 10), brush_snare (pitch 12), clave (pitch 4)
- Structure: Generate a 4-bar loop with notes distributed across all 4 bars
"""

NURSERY_RULES = """
- 120 BPM (fixed)
- 4/4 time signature
- Rhythm: 2-4 stressed syllables per line; Simple, bouncy patterns
- Melody: Within an octave; Major keys; Stepwise motion; Rise then fall pattern; Finish on tonic
- Harmony: Major keys (e.g., C major). Simple I-IV-V progressions
- Available Instruments: Toy Piano (channel 4), Ukulele (channel 6), Glockenspiel (channel 0), Drumkit (channel 13)
- Drumkit notes: tambourine (pitch 8), hand_drum (pitch 10), triangle (pitch 2)
- Structure: Generate a 4-bar loop with simple melodic patterns distributed across all 4 bars
"""

ROCK_RULES = """
- 130 BPM (fixed)
- 4/4 time signature
- Rhythm: Strong backbeat on beats 2 and 4; Eighth-note patterns
- Melody: Pentatonic scale; Minor keys preferred
- Harmony: Minor keys. Power chords (root and fifth). Use I-IV-V progressions (e.g., A minor)
- Available Instruments: Brass (channel 11), Bass (channel 10), Drumkit (channel 13)
- Drumkit notes: brush_snare (pitch 12) on beats 2 and 4, clave (pitch 4) for hi-hat pattern
- Structure: Generate an 8-bar loop with notes distributed across all bars
"""

# --- 3. Define JSON Format (Generic Template) ---
JSON_FORMAT = """
{
  "tempo": [BPM as integer],
  "time_signature": "4/4",
  "length_bars": [number of bars],
  "tracks": [
    {
      "name": "[instrument_name]",
      "channel": [channel_number],
      "notes": [
        {"bar": [1-4], "beat": [1.0-4.5], "pitch": [MIDI note], "duration": [float], "velocity": [0-127]}
      ]
    }
  ]
}

IMPORTANT: 
- Create multiple notes across ALL bars (1, 2, 3, 4), not just bar 1
- Vary the beat positions (1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5)
- Each track should have 10-20 notes distributed across the bars
- Drumkit uses specific pitch values for sounds, other instruments use standard MIDI pitches
"""

# --- 4. Load Model ---
model_path = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # or whatever model you're using
device = "cuda" if torch.cuda.is_available() else "cpu"
if torch.backends.mps.is_available(): device = "mps"

print(f"Loading model on device: {device}")

tokenizer = AutoTokenizer.from_pretrained(model_path)

# FIX: Use proper device_map for the micro model
if device == "cuda":
    # Try to load entirely on GPU
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="cuda",  # Force to CUDA instead of "auto"
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True
    )
elif device == "cpu":
    # Load entirely on CPU
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float32  # Use float32 on CPU
    )
    model = model.to(device)
else:  # MPS
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float32
    )
    model = model.to(device)

model.eval()

# --- 5. Select Genre and Construct Prompt ---
genre = "nursery"  # Change to "hiphop", "nursery", or "rock"

if genre == "hiphop":
    rules = HIPHOP_RULES
    length_bars = 4
    tempo = 90
elif genre == "nursery":
    rules = NURSERY_RULES
    length_bars = 4
    tempo = 120
elif genre == "rock":
    rules = ROCK_RULES
    length_bars = 8
    tempo = 130
else:
    raise ValueError(f"Unknown genre: {genre}")

chat = [
    {"role": "system",
     "content": """You are a Music Generation Assistant. Generate complete musical compositions in JSON format.

CRITICAL RULES:
- Drumkit (channel 13): Use specific pitch values: triangle=2, clave=4, shaker=6, tambourine=8, hand_drum=10, brush_snare=12, bell=14
- All other instruments: Use standard MIDI pitch values (middle C = 60)
- Spread notes across ALL bars - do not put everything in bar 1
- Create rhythmic variety with different beat positions (1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5)
- Output ONLY valid JSON, no explanatory text or code blocks"""},
    {"role": "user", "content": f"""
Generate a complete {genre} music composition following these rules:

{rules}

Use this JSON structure:
{JSON_FORMAT}

Create a musically interesting {length_bars}-bar composition with notes spread throughout all bars.
"""},
]

# --- 6. Generate Output ---
input_tokens = tokenizer.apply_chat_template(chat, return_tensors="pt", add_generation_prompt=True).to(device)

with torch.no_grad():
    output = model.generate(
        input_tokens,
        max_new_tokens=500,
        do_sample=True,  # Changed to True
        temperature=0.7,  # Added temperature
        top_p=0.9  # Added top_p for better generation
    )

decoded_output = tokenizer.decode(output[0], skip_special_tokens=False)

# --- 7. Extract and Validate JSON ---
try:
    json_start = decoded_output.find("<|start_of_role|>assistant<|end_of_role|>") + len(
        "<|start_of_role|>assistant<|end_of_role|>")
    json_end = decoded_output.find("<|end_of_text|>", json_start)

    raw_json = decoded_output[json_start:json_end].strip()

    # Clean up common LLM formatting issues
    if raw_json.startswith("```json"):
        raw_json = raw_json[7:]
    if raw_json.startswith("```"):
        raw_json = raw_json[3:]
    if raw_json.endswith("```"):
        raw_json = raw_json[:-3]

    generated_music_data = json.loads(raw_json)

    # --- 8. Post-process to enforce correct values ---
    generated_music_data["tempo"] = tempo
    generated_music_data["length_bars"] = length_bars

    print(f"\n--- SUCCESSFULLY GENERATED {genre.upper()} MUSIC JSON ---")
    print(json.dumps(generated_music_data, indent=2))

except Exception as e:
    print(f"\n--- ERROR PARSING JSON ---")
    print("Raw Model Output:")
    print(decoded_output)
    print(f"\nError: {e}")