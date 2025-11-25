# ========================
# CONFIGURATION MODULE
# ========================
# Central configuration for song generation parameters

# Model configuration
MODEL_PATH = "ibm-granite/granite-4.0-micro"

# Song structure constants
STANZA_COUNT = 2
LINE_COUNT = 4
SEQUENCE = "AABB"
SYLLABLE_COUNT = 8

# Song topic
SONG_TOPIC = "video games"

# Generation parameters
MAX_TOKENS_SONG = 400
TEMPERATURE = 0.7
TOP_P = 0.9
