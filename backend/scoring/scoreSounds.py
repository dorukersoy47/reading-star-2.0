import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

# Parameters
SILENCE_THRESHOLD = 0.025
SAMPLE_RATE = 44100
CHUNK_SIZE = 1024  # Size of audio chunks to process


def plot_audio_with_threshold(audio, threshold):
    """Plot the audio waveform with a threshold line."""
    time_axis = np.linspace(0, len(audio) / SAMPLE_RATE, num=len(audio))
    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, audio, alpha=0.7, label="Waveform")
    plt.axhline(y=threshold, color='r', linestyle='--', label="Threshold")
    plt.axhline(y=-threshold, color='r', linestyle='--')
    plt.title("Audio Waveform & Scoring Threshold")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid()
    plt.show()


def scoring_system(duration=5):
    score = 0
    is_sounding = False  # This tracks our "state"

    print(f"Recording for {duration} seconds...")
    audio_data = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()
    audio_data = audio_data.flatten()

    plot_audio_with_threshold(audio_data, SILENCE_THRESHOLD)

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


if __name__ == "__main__":
    scoring_system()