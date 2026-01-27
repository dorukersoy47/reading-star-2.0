from generation.config import LINE_COUNT, SEQUENCE
from generation.lyricGen.model import generate_text
import re


def generate_stanza(topic: str, syllable_count: int, line_count: int = LINE_COUNT,
                    sequence: str = SEQUENCE) -> str:    
    chat = [
        {
            "role": "system",
            "content": "You are a special education teacher that writes simple, child-friendly song lyrics for autistic children."
        },
        {
            "role": "user",
            "content": f"""Write a {line_count}-line verse of a children's song about "{topic}".

Rules:
- Follow the {sequence} rhyme scheme (do NOT write the letters, just make the lines rhyme accordingly)
- Each line should have approximately {syllable_count} syllables

Output ONLY the {line_count} lines of lyrics. No titles, no letter labels like (A) or (B), no explanations."""
        },
    ]

    return generate_text(chat)


def generate_song(topic, stanza_count: int, syllable_count: int, line_count: int = LINE_COUNT, sequence: str = SEQUENCE) -> str:
    stanzas = []
    
    for i in range(1, stanza_count + 1):
        print(f"   Generating stanza {i}/{stanza_count}...")
        
        stanza = generate_stanza(
            topic=topic,
            syllable_count=syllable_count,
            line_count=line_count,
            sequence=sequence,
        )
        
        stanza_lines = [ln.strip() for ln in stanza.splitlines() if ln.strip()]
        stanza = "\n".join(stanza_lines[:line_count])
        
        stanzas.append(stanza)
    
    return "\n\n".join(stanzas)

def generate_title(topic: str) -> str:
    chat = [
        {
            "role": "system",
            "content": "You are a creative assistant that writes simple, child-friendly song titles. Output only the raw title, no labels or annotations."
        },
        {
            "role": "user",
            "content": f"""Suggest a short (2-4 words), creative, and engaging title for a children's song about "{topic}"."""
        },
    ]

    title = generate_text(chat, max_tokens=10)
    title = re.sub(r'[^\w\s]', '', title).strip()
    return title.strip()