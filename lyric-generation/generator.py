# ========================
# SONG GENERATION MODULE
# ========================
# Handles song generation with LLM - generates stanzas one-by-one

from config import (
    SONG_TOPIC, STANZA_COUNT, LINE_COUNT, SEQUENCE, SYLLABLE_COUNT,
)
from model import generate_text


def generate_stanza(topic: str, stanza_number: int, line_count: int = LINE_COUNT,
                    sequence: str = SEQUENCE, syllable_count: int = SYLLABLE_COUNT,
                    previous_stanzas: list[str] = None) -> str:
    """
    Generate a single stanza of song lyrics.
    
    Args:
        topic: The topic/theme for the song
        stanza_number: Which stanza this is (1-indexed)
        line_count: Number of lines in this stanza
        sequence: Rhyme scheme (e.g., "AABB", "ABAB")
        syllable_count: Target syllables per line
        previous_stanzas: List of previously generated stanzas for context
        
    Returns:
        Generated stanza text (line_count lines)
    """
    # Build context from previous stanzas
    context = ""
    if previous_stanzas:
        context = f"\n\nPrevious verses (for context, continue the theme):\n"
        for i, stanza in enumerate(previous_stanzas, 1):
            context += f"\nVerse {i}:\n{stanza}\n"
    
    chat = [
        {
            "role": "system",
            "content": "You are a creative assistant that writes simple, child-friendly song lyrics. Output exactly the number of lines requested, nothing more."
        },
        {
            "role": "user",
            "content": f"""Write verse {stanza_number} of a children's song about "{topic}".
{context}
REQUIREMENTS for this verse:
- Exactly {line_count} lines
- {sequence} rhyme scheme  
- {syllable_count} syllables per line

Output ONLY the {line_count} lines for this verse. No titles, no "Verse {stanza_number}:", no annotations."""
        },
    ]

    return generate_text(chat)


def generate_song(topic: str = SONG_TOPIC, stanza_count: int = STANZA_COUNT, line_count: int = LINE_COUNT, 
                  sequence: str = SEQUENCE, syllable_count: int = SYLLABLE_COUNT) -> str:
    """
    Generate song lyrics by creating each stanza one-by-one and combining them.
    
    Args:
        topic: The topic/theme for the song
        stanza_count: Number of stanzas to generate
        line_count: Number of lines per stanza
        sequence: Rhyme scheme (e.g., "AABB", "ABAB")
        syllable_count: Target syllables per line
        
    Returns:
        Complete song text with all stanzas
    """
    stanzas = []
    
    for i in range(1, stanza_count + 1):
        print(f"   Generating stanza {i}/{stanza_count}...")
        
        stanza = generate_stanza(
            topic=topic,
            stanza_number=i,
            line_count=line_count,
            sequence=sequence,
            syllable_count=syllable_count,
            previous_stanzas=stanzas if stanzas else None
        )
        
        # Clean up the stanza (remove extra blank lines, strip whitespace)
        stanza_lines = [ln.strip() for ln in stanza.splitlines() if ln.strip()]
        stanza = "\n".join(stanza_lines[:line_count])  # Ensure only line_count lines
        
        stanzas.append(stanza)
    
    # Combine all stanzas with blank line between them
    return "\n\n".join(stanzas)