import ollama

# --- Configuration ---
# Set the model name exactly as you pulled it in Ollama
# Recommended micro model: 'granite4:micro-h'
MODEL_NAME = "granite4:micro-h"

# The prompt to ask the model
USER_PROMPT = """Output exactly one JSON object representing a song.

    Schema:
    {
      "tempo": <int>,
      "time_signature": "4/4",
      "length_bars": 4,
      "tracks": [
        {
          "name": <instrument name>,
          "channel": <int>,
          "notes": [ { "bar": <int>, "beat": <float>, "pitch": <int>, "velocity": <int> }, ... ]
        }
      ]
    }

    Allowed Instruments: Glockenspiel, Music Box, Celesta, Marimba, Vibraphone, Drumkit.

    Drumkit Mapping:
    - 2=Triangle, 4=Clave, 6=Shaker, 8=Tambourine, 10=Hand Drum, 12=Snare, 14=Bell.

    Rules:
    1. Create a 4-bar loop.
    2. Track 1: A simple melody using "Music Box" or "Marimba" (Pitches 60-80).
    3. Track 2: A rhythmic beat using "Drumkit" (Pitches 2, 4, or 12).
    4. NO text before or after the JSON.
    5. Ensure the JSON is valid and closed correctly.

    GENERATE THE JSON NOW:
    """

# --- Ollama Chat/Inference ---
try:
    # 1. Initialize the connection (uses default http://localhost:11434)
    client = ollama.Client()

    # 2. Call the chat/completion API
    # Using the 'chat' endpoint is often better for conversational prompts
    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {
                'role': 'user',
                'content': USER_PROMPT,
            },
        ],
    )

    # 3. Extract and print the joke from the response
    joke = response['message']['content']
    print(f"\n--- Joke from {MODEL_NAME} ---")
    print(joke)
    print("---------------------------------")

except Exception as e:
    print(f"\nError connecting to Ollama: {e}")
    print("Please ensure the Ollama server is running and the model is pulled correctly.")