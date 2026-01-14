import json
import random

# --- Available Instruments ---
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

# --- Music Theory Helpers ---
SCALES = {
    "C_major": [60, 62, 64, 65, 67, 69, 71, 72],  # C D E F G A B C
    "C_minor": [60, 62, 63, 65, 67, 68, 70, 72],  # C D Eb F G Ab Bb C
    "A_minor": [57, 59, 60, 62, 64, 65, 67, 69],  # A B C D E F G A
    "A_minor_pentatonic": [57, 60, 62, 64, 67, 69]  # A C D E G A
}

CHORDS = {
    "C_major": [48, 52, 55],  # C E G
    "F_major": [53, 57, 60],  # F A C
    "G_major": [55, 59, 62],  # G B D
    "C_minor": [48, 51, 55],  # C Eb G
    "Bb_major": [46, 50, 53],  # Bb D F
    "Ab_major": [44, 48, 51],  # Ab C Eb
    "A_minor": [45, 48, 52],  # A C E
    "D_minor": [50, 53, 57],  # D F A
    "E_minor": [52, 55, 59],  # E G B
}

# Drumkit pitch mappings
DRUM_SOUNDS = {
    "triangle": 2,
    "clave": 4,
    "shaker": 6,
    "tambourine": 8,
    "hand_drum": 10,
    "brush_snare": 12,
    "bell": 14
}


# --- Nursery Rhyme Generator ---
def generate_nursery_rhyme():
    """Generate a simple, cheerful nursery rhyme in C major"""
    scale = SCALES["C_major"]
    melody_notes = []

    # Simple melody pattern: rise and fall, finish on tonic
    patterns = [
        [0, 1, 2, 3, 4, 4, 3, 2, 1, 1, 2, 2, 0],  # C D E F G G F E D D E E C
        [0, 0, 2, 2, 4, 4, 2, 0, 0, 2, 2, 4, 0],  # C C E E G G E C C E E G C
    ]

    pattern = random.choice(patterns)
    beat = 1.0
    bar = 1

    for scale_degree in pattern:
        melody_notes.append({
            "bar": bar,
            "beat": beat,
            "pitch": scale[scale_degree],
            "duration": 1.0,
            "velocity": 80
        })
        beat += 1.0
        if beat > 4.0:
            beat = 1.0
            bar += 1

    # Ukulele accompaniment - simple chords
    chord_progression = [
        (1, CHORDS["C_major"]),
        (2, CHORDS["F_major"]),
        (3, CHORDS["G_major"]),
        (4, CHORDS["C_major"])
    ]

    ukulele_notes = []
    for bar, chord in chord_progression:
        for beat in [1.0, 2.0, 3.0, 4.0]:
            ukulele_notes.append({
                "bar": bar,
                "beat": beat,
                "pitch": chord[0],  # Root note
                "duration": 0.5,
                "velocity": 70
            })

    # Glockenspiel - occasional high sparkles
    glockenspiel_notes = []
    for bar in [1, 2, 3, 4]:
        if random.random() > 0.3:  # 70% chance
            glockenspiel_notes.append({
                "bar": bar,
                "beat": random.choice([1.0, 3.0]),
                "pitch": random.choice([72, 76, 79]),  # High C, E, G
                "duration": 0.5,
                "velocity": 65
            })

    # Drumkit - tambourine on every beat, triangle accents
    drum_notes = []
    for bar in range(1, 5):
        for beat in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]:
            drum_notes.append({
                "bar": bar,
                "beat": beat,
                "pitch": DRUM_SOUNDS["tambourine"],
                "duration": 0.25,
                "velocity": 55
            })
        # Triangle on beat 1 and 3
        for beat in [1.0, 3.0]:
            drum_notes.append({
                "bar": bar,
                "beat": beat,
                "pitch": DRUM_SOUNDS["triangle"],
                "duration": 0.25,
                "velocity": 60
            })

    return {
        "tempo": 120,
        "time_signature": "4/4",
        "length_bars": 4,
        "tracks": [
            {
                "name": "toy_piano",
                "channel": AVAILABLE_INSTRUMENTS["toy_piano"],
                "notes": melody_notes
            },
            {
                "name": "ukulele",
                "channel": AVAILABLE_INSTRUMENTS["ukulele"],
                "notes": ukulele_notes
            },
            {
                "name": "glockenspiel",
                "channel": AVAILABLE_INSTRUMENTS["glockenspiel"],
                "notes": glockenspiel_notes
            },
            {
                "name": "drumkit",
                "channel": AVAILABLE_INSTRUMENTS["drumkit"],
                "notes": drum_notes
            }
        ]
    }


# --- Hip-Hop Generator ---
def generate_hiphop():
    """Generate a hip-hop beat in C minor"""
    # Bass pattern - typical hip-hop groove
    bass_pattern = [
        (1, 1.0, 36, 0.5, 100),  # Kick on 1
        (1, 1.5, 36, 0.25, 85),
        (1, 3.0, 36, 0.5, 100),  # Kick on 3
    ]

    bass_notes = []
    for bar in range(1, 5):
        for rel_bar, beat, pitch, duration, velocity in bass_pattern:
            bass_notes.append({
                "bar": bar,
                "beat": beat,
                "pitch": pitch,
                "duration": duration,
                "velocity": velocity
            })

    # Synth chord - minor chord progression
    chord_progression = [
        (1, CHORDS["C_minor"]),
        (2, CHORDS["Bb_major"]),
        (3, CHORDS["Ab_major"]),
        (4, CHORDS["C_minor"])
    ]

    synth_notes = []
    for bar, chord in chord_progression:
        for beat in [1.0, 3.0]:
            synth_notes.append({
                "bar": bar,
                "beat": beat,
                "pitch": chord[1],  # Third of chord
                "duration": 2.0,
                "velocity": 75
            })

    # Drums - classic hip-hop pattern
    drum_notes = []
    for bar in range(1, 5):
        # Hand drum on 1 and 3
        for beat in [1.0, 3.0]:
            drum_notes.append({
                "bar": bar,
                "beat": beat,
                "pitch": DRUM_SOUNDS["hand_drum"],
                "duration": 0.25,
                "velocity": 110
            })
        # Brush snare on 2 and 4
        for beat in [2.0, 4.0]:
            drum_notes.append({
                "bar": bar,
                "beat": beat,
                "pitch": DRUM_SOUNDS["brush_snare"],
                "duration": 0.25,
                "velocity": 115
            })
        # Clave hi-hat pattern
        for beat in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]:
            drum_notes.append({
                "bar": bar,
                "beat": beat,
                "pitch": DRUM_SOUNDS["clave"],
                "duration": 0.125,
                "velocity": 80
            })

    return {
        "tempo": 90,
        "time_signature": "4/4",
        "length_bars": 4,
        "tracks": [
            {
                "name": "synth_chord",
                "channel": AVAILABLE_INSTRUMENTS["synth_chord"],
                "notes": synth_notes
            },
            {
                "name": "bass",
                "channel": AVAILABLE_INSTRUMENTS["bass"],
                "notes": bass_notes
            },
            {
                "name": "drumkit",
                "channel": AVAILABLE_INSTRUMENTS["drumkit"],
                "notes": drum_notes
            }
        ]
    }


# --- Rock Generator ---
def generate_rock():
    """Generate a rock riff in A minor"""
    scale = SCALES["A_minor_pentatonic"]

    # Guitar riff - power chord style
    power_chord_roots = [57, 60, 62, 60, 57, 55, 57]  # A minor pentatonic riff
    brass_notes = []

    beat = 1.0
    bar = 1
    for root in power_chord_roots:
        brass_notes.append({
            "bar": bar,
            "beat": beat,
            "pitch": root,
            "duration": 1.0,
            "velocity": 110
        })
        # Add power chord fifth
        brass_notes.append({
            "bar": bar,
            "beat": beat,
            "pitch": root + 7,  # Fifth interval
            "duration": 1.0,
            "velocity": 105
        })
        beat += 1.0
        if beat > 4.0:
            beat = 1.0
            bar += 1

    # Bass follows guitar
    bass_notes = []
    beat = 1.0
    bar = 1
    for root in power_chord_roots:
        bass_notes.append({
            "bar": bar,
            "beat": beat,
            "pitch": root - 12,  # One octave lower
            "duration": 1.0,
            "velocity": 105
        })
        beat += 1.0
        if beat > 4.0:
            beat = 1.0
            bar += 1

    # Drums - rock backbeat
    drum_notes = []
    for bar in range(1, 9):
        # Brush snare on 2 and 4 (backbeat)
        for beat in [2.0, 4.0]:
            drum_notes.append({
                "bar": bar,
                "beat": beat,
                "pitch": DRUM_SOUNDS["brush_snare"],
                "duration": 0.25,
                "velocity": 120
            })
        # Clave for hi-hat eighth notes
        for beat in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]:
            drum_notes.append({
                "bar": bar,
                "beat": beat,
                "pitch": DRUM_SOUNDS["clave"],
                "duration": 0.125,
                "velocity": 85
            })
        # Hand drum for kicks
        for beat in [1.0, 2.5, 3.0]:
            drum_notes.append({
                "bar": bar,
                "beat": beat,
                "pitch": DRUM_SOUNDS["hand_drum"],
                "duration": 0.25,
                "velocity": 115
            })

    return {
        "tempo": 130,
        "time_signature": "4/4",
        "length_bars": 8,
        "tracks": [
            {
                "name": "brass",
                "channel": AVAILABLE_INSTRUMENTS["brass"],
                "notes": brass_notes
            },
            {
                "name": "bass",
                "channel": AVAILABLE_INSTRUMENTS["bass"],
                "notes": bass_notes
            },
            {
                "name": "drumkit",
                "channel": AVAILABLE_INSTRUMENTS["drumkit"],
                "notes": drum_notes
            }
        ]
    }


# --- Main Generator Function ---
def generate_music(genre):
    """Generate music based on genre"""
    if genre == "nursery":
        return generate_nursery_rhyme()
    elif genre == "hiphop":
        return generate_hiphop()
    elif genre == "rock":
        return generate_rock()
    else:
        raise ValueError(f"Unknown genre: {genre}")


# --- Usage ---
if __name__ == "__main__":
    # Choose genre
    genre = "nursery"  # Change to "nursery", "hiphop", or "rock"

    # print(f"Generating {genre} music...")
    music_data = generate_music(genre)

    # print(f"\n--- GENERATED {genre.upper()} MUSIC JSON ---")
    print(json.dumps(music_data, indent=2))

    # Optional: Save to file
    with open(f"{genre}_music.json", "w") as f:
        json.dump(music_data, f, indent=2)
    # print(f"\nSaved to {genre}_music.json")