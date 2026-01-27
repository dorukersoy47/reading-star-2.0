from generation.lyricGen.model import generate_text
from generation.config import TITLE_MAX_TOKENS
import re
from typing import List, Optional

ROLE_DESCRIPTION = "You are a special education teacher that writes simple, child-friendly song lyrics for autistic children."

def generate_couplet(topic: str, keyword: Optional[str], syllable_count: int, complexity: str) -> str:    
    chat = [
        {
            "role": "system",
            "content": ROLE_DESCRIPTION
        },
        {
            "role": "user",
            "content": (
                f"Write a rhyming couplet for autistic children about: \"{topic}\".\n"
                + (f"Keyword: {keyword} (use exactly once total)\n" if keyword else "")
                + f"Syllables per line: {syllable_count}\n"
                + f"Complexity: {complexity}\n\n"
                + "Rules:\n"
                + "- Exactly 2 lines only\n"
                + "- Last words must rhyme\n"
                + "- Simple concrete words, calming and positive\n"
                + "- No quotes, no extra lines\n"
                + "Output exactly:\n<couplet>\nLINE1\nLINE2\n</couplet>"
            )
        }
    ]

    return generate_text(chat)


def generate_song(topic: str, keywords: List[str], syllable_count: int, couplet_count: int, complexity: str) -> List[str]:
    couplets = []
    
    for i in range(0, couplet_count):
        print(f"Generating couplet {i + 1}...")

        couplet = generate_couplet(
            topic=topic,
            keyword=keywords[i] if i < len(keywords) else None,
            syllable_count=syllable_count,
            complexity=complexity,
        )
        
        couplets.append(couplet)
    
    return couplets

def generate_title(topic: str) -> str:
    chat = [
        {
            "role": "system",
            "content": ROLE_DESCRIPTION
        },
        {
            "role": "user",
            "content": f"Suggest a short (2-4 words), creative, and engaging title for a children's song about the topic: \"{topic}\". You should output one title and only the title."
        },
    ]

    title = generate_text(chat, max_tokens=TITLE_MAX_TOKENS)
    title = re.sub(r'[^\w\s]', '', title).strip().title()
    return title

def generate_instrumental_title(genre: str, keywords: str) -> str:
    chat = [
        {
            "role": "system",
            "content": ROLE_DESCRIPTION
        },
        {
            "role": "user",
            "content": f"Suggest a short title for a backing track. "
                        + f"The track is in the \"{genre}\" genre of and evokes the following qualities: {keywords}. "
                        + f"Choose a single descriptive keyword based on \"{keywords}\" and output the title in the format: \"<Keyword> <Genre>\" and no other words. You should output one title and only the title."
        },
    ]

    title = generate_text(chat, max_tokens=TITLE_MAX_TOKENS)
    title = re.sub(r'[^\w\s]', '', title).strip().title()
    return title