import numpy as np


def crossfade_sections(section1, section2, sample_rate, fade_duration=1.5):
    """Crossfade between two audio sections"""
    fade_samples = int(sample_rate * fade_duration)

    if len(section1) < fade_samples or len(section2) < fade_samples:
        return np.concatenate([section1, section2])

    end_of_section1 = section1[-fade_samples:]
    start_of_section2 = section2[:fade_samples]

    fade_out = np.cos(np.linspace(0, np.pi / 2, fade_samples)) ** 2
    fade_in = np.sin(np.linspace(0, np.pi / 2, fade_samples)) ** 2

    blended = (end_of_section1 * fade_out) + (start_of_section2 * fade_in)

    result = np.concatenate([
        section1[:-fade_samples],
        blended,
        section2[fade_samples:]
    ])

    return result


def extend_audio(audio_data, sample_rate, target_duration=120, fade_duration=1.5):
    """Extend audio to target duration by repeating middle section"""
    original_duration = len(audio_data) / sample_rate

    # Split into START, MIDDLE, END
    section_size = len(audio_data) // 5

    start_section = audio_data[:section_size]
    end_section = audio_data[-section_size:]
    middle_section = audio_data[section_size:-section_size]

    print(f"Original audio: {original_duration:.1f}s")

    # Start building extended audio
    extended = start_section.copy()
    current_duration = len(extended) / sample_rate
    middle_duration = len(middle_section) / sample_rate

    repetitions = 0
    while current_duration + middle_duration + (len(end_section) / sample_rate) < target_duration:
        print(f"Adding MIDDLE repetition #{repetitions + 1}...")
        extended = crossfade_sections(extended, middle_section, sample_rate, fade_duration)
        current_duration = len(extended) / sample_rate
        repetitions += 1

    print("Adding END section...")
    extended = crossfade_sections(extended, end_section, sample_rate, fade_duration)

    final_duration = len(extended) / sample_rate
    print(f"Final duration: {final_duration:.1f}s ({repetitions} middle repetitions)")

    return extended