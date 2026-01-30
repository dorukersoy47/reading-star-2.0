# Lyric generation
LYRIC_MODEL_PATH = "ibm-granite/granite-3.0-2b-instruct"
LYRIC_MAX_TOKENS = 65
TITLE_MAX_TOKENS = 10
TEMPERATURE = 0.7
TOP_P = 0.9

# Music generation
MUSIC_MODEL_PATH = "facebook/musicgen-small"
MUSIC_MAX_TOKENS = 1503
TARGET_DURATION = 120 # 2 minutes
GENRES = {
    "nursery_rhyme": {
        "prompt": """soothing children's nursery rhyme, major key, simple melody with piano,
                    and acoustic guitar, playful and calming, 120 BPM""",
        "max_tokens": MUSIC_MAX_TOKENS,
        "target_duration": TARGET_DURATION
    },
    "hip_hop": {
        "prompt": """hip hop beat with 808 bass, drum machine, trap hi-hats, minor key,
                     dark atmospheric synth pads, 90 BPM""",
        "max_tokens": MUSIC_MAX_TOKENS,
        "target_duration": TARGET_DURATION
    },
    "rock": {
        "prompt": """energetic rock music with distorted electric guitar, driving drums 
                    with backbeat, bass guitar, power chords, 130 BPM""",
        "max_tokens": MUSIC_MAX_TOKENS,
        "target_duration": TARGET_DURATION
    },
    "jazz": {
        "prompt": """smooth jazz with saxophone, piano, upright bass, brush drums, 
                    swing rhythm, improvisation, walking bass line, 120 BPM""",
        "max_tokens": MUSIC_MAX_TOKENS,
        "target_duration": TARGET_DURATION
    },
    "classical": {
        "prompt": """classical orchestra with strings, woodwinds, brass, elegant melody, 
                    symphonic arrangement, dynamic crescendos, refined and sophisticated""",
        "max_tokens": MUSIC_MAX_TOKENS,
        "target_duration": TARGET_DURATION
    },
    "reggae": {
        "prompt": """reggae with offbeat guitar skank, heavy bass, one drop drum pattern, 
                    relaxed groove, organ stabs, laid-back vibe, 80 BPM""",
        "max_tokens": MUSIC_MAX_TOKENS,
        "target_duration": TARGET_DURATION
    },
    "rnb": {
        "prompt": """R&B with smooth vocals, electric piano, grooving bass, tight drums, 
                    soulful melody, contemporary production, 90 BPM""",
        "max_tokens": MUSIC_MAX_TOKENS,
        "target_duration": TARGET_DURATION
    },
    "punk": {
        "prompt": """punk rock with fast distorted power chords, aggressive drums, 
                    driving bass, raw energy, rebellious attitude, 180 BPM""",
        "max_tokens": MUSIC_MAX_TOKENS,
        "target_duration": TARGET_DURATION
    },
    "metal": {
        "prompt": """heavy metal with distorted guitars, palm-muted riffs, double bass drums, 
                    aggressive power chords, intense energy, 140 BPM""",
        "max_tokens": MUSIC_MAX_TOKENS,
        "target_duration": TARGET_DURATION
    },
    "bollywood": {
        "prompt": """Bollywood music with tabla, sitar, orchestral strings, energetic dhol drums, 
                    melodic indian vocals style, vibrant and colorful, 120 BPM""",
        "max_tokens": MUSIC_MAX_TOKENS,
        "target_duration": TARGET_DURATION
    }
}