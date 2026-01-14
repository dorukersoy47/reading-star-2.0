import re
from generation.config import LINE_COUNT


def remove_headings(song: str) -> str:
    lines = song.splitlines()
    heading_re = re.compile(r"^\s*(?:\(?\s*(?:verse|chorus|bridge|refrain|stanza)\b.*\)?)\s*$", re.I)
    filtered = [ln for ln in lines if not heading_re.match(ln)]
    return "\n".join(filtered)


def remove_empty_lines(song: str) -> str:
    lines = song.splitlines()
    filtered = [ln for ln in lines if ln.strip()]
    return "\n".join(filtered)


def remove_numbering(song: str) -> str:
    lines = song.splitlines()
    cleaned = []
    for ln in lines:
        cleaned_line = re.sub(r"^\s*[\d]+[.\):\-]\s*", "", ln)
        cleaned_line = re.sub(r"^\s*[\-\*]\s*", "", cleaned_line)
        cleaned.append(cleaned_line)
    return "\n".join(cleaned)

def remove_paranthesis(song: str) -> str:
    lines = song.splitlines()
    cleaned = []
    for ln in lines:
        cleaned_line = re.sub(r"\s*\(.*?\)\s*", "", ln)
        cleaned.append(cleaned_line)
    return "\n".join(cleaned)

def crop_to_expected_lines(song: str, stanza_count: int, 
                           line_count: int = LINE_COUNT) -> str:
    lines = [ln for ln in song.splitlines() if ln.strip()]
    expected_total = stanza_count * line_count
    cropped = lines[:expected_total]
    return "\n".join(cropped)


def parse_to_lines(song: str) -> list[str]:
    return [ln.strip() for ln in song.splitlines() if ln.strip()]


def format_song(song: str, stanza_count: int, 
                line_count: int = LINE_COUNT) -> str:
    song = remove_headings(song)
    song = remove_empty_lines(song)
    song = remove_numbering(song)
    song = crop_to_expected_lines(song, stanza_count, line_count)
    return song