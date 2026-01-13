from lyricGen.config import (
    STANZA_COUNT, LINE_COUNT, SEQUENCE, SYLLABLE_COUNT,
)
from lyricGen.model import generate_text


def generate_stanza(topic: str, line_count: int = LINE_COUNT,
                    sequence: str = SEQUENCE, syllable_count: int = SYLLABLE_COUNT) -> str:    
    chat = [
        {
            "role": "system",
            "content": "You are a creative assistant that writes simple, child-friendly song lyrics. Output only the raw lyrics, no labels or annotations."
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


def generate_song(topic, stanza_count: int = STANZA_COUNT, line_count: int = LINE_COUNT, 
                  sequence: str = SEQUENCE, syllable_count: int = SYLLABLE_COUNT) -> str:
    stanzas = []
    
    for i in range(1, stanza_count + 1):
        print(f"   Generating stanza {i}/{stanza_count}...")
        
        stanza = generate_stanza(
            topic=topic,
            line_count=line_count,
            sequence=sequence,
            syllable_count=syllable_count,
        )
        
        stanza_lines = [ln.strip() for ln in stanza.splitlines() if ln.strip()]
        stanza = "\n".join(stanza_lines[:line_count])
        
        stanzas.append(stanza)
    
    return "\n\n".join(stanzas)