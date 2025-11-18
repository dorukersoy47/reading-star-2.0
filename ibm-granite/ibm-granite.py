# Libraries
import ast
import re
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model and tokenizer
model_path = "ibm-granite/granite-4.0-micro"
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

# Constants for song structure
STANZA_COUNT = 2
LINE_COUNT = 4
SEQUENCE = "AABB"
WORD_COUNT = 8


# Methods #

def generate_song(topic: str, stanza_count: int = STANZA_COUNT, line_count: int = LINE_COUNT, sequence: str = SEQUENCE, word_count: int = WORD_COUNT) -> str:
    chat = [
        {
            "role": "system",
            "content": "You are a creative assistant that writes simple, child-friendly song lyrics about reading and stories."
        },
        {
            "role": "user",
            "content": f"Write a song with {stanza_count} stanzas, each {line_count}-line children’s song about {topic}. Make it rhyme in a {sequence} sequence. Make every line have {word_count} words."
        },
    ]

    formatted = tokenizer.apply_chat_template(
        chat, tokenize=False, add_generation_prompt=True
    )
    
    # tokenize the text
    input_tokens = tokenizer(formatted, return_tensors="pt").to(device)

    # generate output tokens
    with torch.no_grad():
        output = model.generate(
            **input_tokens,
            max_new_tokens=100,
        )

    # Only keep the newly generated tokens (not the prompt)
    generated_tokens = output[0][input_tokens["input_ids"].shape[1]:]

    # decode only the generated part
    answer = tokenizer.decode(generated_tokens, skip_special_tokens=True)

    return answer.strip()

def parse_song(song):
    lines = [ln.strip() for ln in str(song).splitlines() if ln.strip()]

    # Remove heading lines such as "(Verse 1)", "Verse 2", "Chorus" etc.
    heading_re = re.compile(r"^\s*(?:\(?\s*(?:verse|chorus|bridge|refrain)\b.*\)?)\s*$", re.I)
    filtered_lines = [ln for ln in lines if not heading_re.match(ln)]

    # Truncate to the expected number of lines (no extra stanza)
    expected = STANZA_COUNT * LINE_COUNT
    if len(filtered_lines) > expected:
        filtered_lines = filtered_lines[:expected]

    parsed_lines = []
    word_re = re.compile(r"\b[\w']+\b")
    for ln in filtered_lines:
        words = word_re.findall(ln)
        parsed_lines.append(words)

    # Group into stanzas: each stanza is LINE_COUNT lines
    stanzas = [parsed_lines[i:i+LINE_COUNT] for i in range(0, len(parsed_lines), LINE_COUNT)]

    # Ensure we return exactly STANZA_COUNT stanzas (truncate or pad with empty lines)
    if len(stanzas) > STANZA_COUNT:
        stanzas = stanzas[:STANZA_COUNT]
    elif len(stanzas) < STANZA_COUNT:
        # pad with empty lines (each line is an empty list)
        for _ in range(STANZA_COUNT - len(stanzas)):
            stanzas.append([[] for _ in range(LINE_COUNT)])

    return stanzas

def check_song(parsed_song, stanza_count=STANZA_COUNT, line_count=LINE_COUNT, word_count=WORD_COUNT):
    # Expect nested structure: list of stanzas -> list of lines -> list of words
    if len(parsed_song) != stanza_count:
        raise ValueError(f"Expected {stanza_count} stanzas, got {len(parsed_song)}")

    for s_idx, stanza in enumerate(parsed_song):
        if len(stanza) != line_count:
            raise ValueError(f"Stanza {s_idx+1} expected to have {line_count} lines, got {len(stanza)}")
        for l_idx, line in enumerate(stanza):
            if len(line) != word_count:
                raise ValueError(f"Stanza {s_idx+1} line {l_idx+1} expected to have {word_count} words, got {len(line)}")
    


def sanitize_parsed_song(parsed_song):
    """Reconstruct a sanitized song text (no headings) from nested parsed_song.

    parsed_song: list of stanzas -> list of lines -> list of words
    returns: string with stanzas separated by a blank line
    """
    stanza_texts = []
    for stanza in parsed_song:
        stanza_lines = [" ".join(words) for words in stanza]
        stanza_texts.append("\n".join(stanza_lines))

    sanitized_text = "\n\n".join(stanza_texts[:STANZA_COUNT])
    return sanitized_text


def run_song_flow(topic: str):
    """Generate a song, parse it into stanzas, validate with check_song,
    and return a result dict containing original song, parsed nested array,
    sanitized text, and check status/message.
    """
    try:
        song = generate_song(topic)
    except Exception as e:
        return {"song": None, "parsed_song": None, "sanitized_text": "", "check_ok": False, "check_error": f"Error generating song: {e}"}

    parsed_song = parse_song(song)

    # Attempt to validate; capture any validation error
    try:
        check_song(parsed_song)
        check_ok = True
        check_error = None
    except Exception as e:
        check_ok = False
        check_error = str(e)

    sanitized_text = sanitize_parsed_song(parsed_song)

    return {"song": song, "parsed_song": parsed_song, "sanitized_text": sanitized_text, "check_ok": check_ok, "check_error": check_error}


if __name__ == '__main__':
    model.to(device)
    model.eval()
    # Keep main minimal: call run_song_flow() which handles generation, parsing, checking and sanitization
    topic = "exploring space"
    result = run_song_flow(topic)

    # Print results (main does not perform processing)
    if result is None:
        print("No result returned from run_song_flow()")
    else:
        print(f"Generated Song (original):\n{result['song']}\n")
        print(f"Generated Song (sanitized, no headings):\n{result['sanitized_text']}\n")
        print(f"Parsed Song (stanzas -> lines -> words):\n{result['parsed_song']}\n")
        if not result['check_ok']:
            print(f"check_song failed: {result['check_error']}")



    







