import sounddevice as sd
import numpy as np

# Parameters
SILENCE_THRESHOLD = 0.025
SAMPLE_RATE = 44100
CHUNK_SIZE = 1024  # Size of audio chunks to process

def scoring_system(duration=5):
    score = 0
    is_sounding = False  # This tracks our "state"

    print(f"Recording for {duration} seconds...")
    audio_data = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()
    audio_data = audio_data.flatten()

    for i in range(0, len(audio_data), CHUNK_SIZE):
        chunk = audio_data[i: i + CHUNK_SIZE]
        chunk_amplitude = np.mean(np.abs(chunk))

        if chunk_amplitude >= SILENCE_THRESHOLD:
            # If this is the START of a new sound
            if not is_sounding:
                score += 3
                is_sounding = True  # Lock it so we don't count the next chunk
        else:
            # The sound has dropped below the threshold
            is_sounding = False

    print(f"Final Score (Distinct Bursts): {score}")
    return score