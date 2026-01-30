from pydantic import BaseModel
from typing import List

class LyricRhythm(BaseModel):
    initial_delay: float
    on_beat_timings: List[List[float]]
    polyrhythm_timings: List[List[float]]
    final_delay: float
    total_song_length: float