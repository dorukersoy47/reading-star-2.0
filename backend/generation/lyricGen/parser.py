import re
from typing import List

def remove_headings(song: str) -> str:
    heading_re = re.compile(r"^\s*\[?\s*(verse|chorus|bridge|refrain|stanza)\s*\]?\s*$", flags=re.I)
    lines = song.splitlines()
    kept = [ln for ln in lines if not heading_re.match(ln.strip())]
    return "\n".join(kept)


def remove_numbering(song: str) -> str:
    lines = []
    for ln in song.splitlines():
        ln = re.sub(r"^\s*\d+\s*[.)-]\s*", "", ln) 
        ln = re.sub(r"^\s*[\-\*]\s*", "", ln)
        lines.append(ln.strip())
    return "\n".join(lines)

def remove_paranthesis(song: str) -> str:
    lines = []
    for ln in song.splitlines():
        ln = re.sub(r"\s*\(.*?\)\s*", " ", ln)
        lines.append(ln.strip())
    return "\n".join(lines)
    

def strip_couplets(couplet: str) -> List[str]:
    match = re.search(r"<couplet[^>]*>(.*?)</couplet>", couplet, flags=re.I | re.S)
    if not match:
        return []
    inner = match.group(1)
    lines = [line.strip() for line in inner.split("\n") if line.strip()]
    return lines[:2]

def clean_couplet(couplet: str) -> List[str]:
    clean = strip_couplets(couplet)
    for i, line in enumerate(clean):
        line = remove_paranthesis(line)
        line = remove_numbering(line)
        line = remove_headings(line)
        clean[i] = line

    return clean


def format_song(raw_song: List[str]) -> List[str]:
    song = []

    for couplet in raw_song:
        clean = clean_couplet(couplet)
        song.extend(clean)

    return song