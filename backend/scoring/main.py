import sounddevice as sd
import numpy as np
import time

# Parameters
SILENCE_THRESHOLD = 0.01  # Threshold for silence (adjust based on mic sensitivity)
SAMPLE_RATE = 44100  # Audio sample rate

def is_silent(audio_chunk):
    """Check if the audio chunk is silent."""
    return np.max(np.abs(audio_chunk)) < SILENCE_THRESHOLD

def scoring_system(bpm=60):
    score = 0
    beat_duration = 60 / bpm
    print("Start making sounds on the beat!")
    while True:
        # Record audio for one beat duration
        audio = sd.rec(int(beat_duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
        sd.wait()
        # Split the audio into two halves to check for silence and sound
        mid_point = len(audio) // 2
        first_half = audio[:mid_point]
        second_half = audio[mid_point:]
        # Check for silence in the first half and sound in the second half
        if is_silent(first_half) and not is_silent(second_half):
            score += 1
            print(f"Point scored! Total score: {score}")
        else:
            print("No point scored. Try again!")
        time.sleep(beat_duration)  # Wait for the next beat

# Run the scoring system
scoring_system()
