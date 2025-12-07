from transformers import pipeline
import time
import scipy

synthesiser = pipeline("text-to-audio", "facebook/musicgen-small")

music = synthesiser(''''- 120 BPM (fixed)
- 4/4 time signature
- Rhythm: 2-4 stressed syllables per line; Simple, bouncy patterns
- Melody: Within an octave; Major keys; Stepwise motion; Rise then fall pattern; Finish on tonic
- Harmony: Major keys (e.g., C major). Simple I-IV-V progressions
- Available Instruments: Piano, Ukulele, Xylophone, Tambourine, Hand Drum, Triangle
- Structure: Generate a 4-bar loop with simple melodic patterns distributed across all 4 bars'''
                    , forward_params={"do_sample": True})

scipy.io.wavfile.write(f"nursery_rhyme{time.time()}.wav", rate=music["sampling_rate"], data=music["audio"])
