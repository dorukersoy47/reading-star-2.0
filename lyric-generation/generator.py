from config import (
    SONG_TOPIC, STANZA_COUNT, LINE_COUNT, SEQUENCE, SYLLABLE_COUNT,
)
from model import generate_text


def generate_stanza(topic: str, line_count: int = LINE_COUNT,
                    sequence: str = SEQUENCE, syllable_count: int = SYLLABLE_COUNT) -> str:    
    chat = [
        {
            "role": "system",
            "content": "You are a creative assistant that writes simple, child-friendly song lyrics. Output exactly the number of lines requested, nothing more."
        },
        {
            "role": "user",
            "content": f"""Write a verse of a children's song about "{topic}".
REQUIREMENTS for this verse:
- Exactly {line_count} lines
- '{sequence}' rhyme scheme  
- {syllable_count} syllables per line

Output ONLY the {line_count} lines for this verse. No titles, no annotations."""
        },
    ]

    return generate_text(chat)


def generate_song(topic: str = SONG_TOPIC, stanza_count: int = STANZA_COUNT, line_count: int = LINE_COUNT, 
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