import math
from models.rhythm import LyricRhythm

def flatten_lyrics(lyrics_3d):
    """Flatten 3D lyrics structure (lines -> words -> syllables) into 2D (lines -> syllables)."""
    flattened = []
    for line in lyrics_3d:
        line_syllables = []
        for word in line:
            line_syllables.extend(word)
        flattened.append(line_syllables)
    return flattened


def generate_syllable_timings(song_lines, bpm):
    """Generate timing delays for each syllable in each line.
    
    Args:
        song_lines: 2D array [lines][syllables] - use flatten_lyrics() if you have 3D structure
        bpm: Beats per minute (tempo)
    
    Returns:
        Tuple: (initial_delay, on_beat_timings, polyrhythm_timings, final_delay, total_song_length)
        - initial_delay: float (milliseconds) - 1 bar count-in before all lyrics
        - on_beat_timings: 2D array [[delays per line]] - on-beat delays for each line
        - polyrhythm_timings: 2D array [[delays per line]] - polyrhythm delays for each line
        - final_delay: float (milliseconds) - 1 bar count-out after all lyrics
        - total_song_length: float (milliseconds) - total time including count in/out
    """
    beat_duration = 60000 / bpm  
    count_bar_duration = 4 * beat_duration  # 1 bar = 4 beats
    
    on_beat_timings = []
    polyrhythm_timings = []
    total_lyrics_time = 0
    
    for line in song_lines:
        num_syllables = len(line)
        
        num_beats = math.ceil(num_syllables / 4) * 4
        total_time = num_beats * beat_duration
        total_lyrics_time += total_time
        
        # On-beat delays: each syllable on a beat, last one includes tail
        on_beat_delays = [beat_duration] * num_syllables
        on_beat_time_used = num_syllables * beat_duration
        on_beat_tail = total_time - on_beat_time_used
        on_beat_delays[-1] += on_beat_tail
        
        # Polyrhythm delays: evenly distributed, last one includes tail
        polyrhythm_delay = total_time / num_syllables
        polyrhythm_delays = [polyrhythm_delay] * num_syllables
        
        on_beat_timings.append(on_beat_delays)
        polyrhythm_timings.append(polyrhythm_delays)
    
    # Calculate total song length: count-in + all lyrics + count-out
    total_song_length = count_bar_duration + total_lyrics_time + count_bar_duration
    
    return LyricRhythm(
        initial_delay=count_bar_duration, 
        on_beat_timings=on_beat_timings, 
        polyrhythm_timings=polyrhythm_timings, 
        final_delay=count_bar_duration, 
        total_song_length=total_song_length
    )

def get_syllable_timings(lyrics: list[list[list[str]]], bpm) -> LyricRhythm:
    return generate_syllable_timings(flatten_lyrics(lyrics), bpm)


# ===== USAGE EXAMPLE =====

#given:
# lyrics_3d = [
#     [["hel", "lo"], ["world"]],           # Line 1: 2 words, 3 syllables
#     [["this"], ["is"], ["a"], ["test"]]   # Line 2: 4 words, 4 syllables
# ]

# bpm = 120

#first, flatten to a 2D array (where each line is only syllable separated with no word distinction)
# lyrics_2d = flatten_lyrics(lyrics_3d)

#next, generate syllable timings for both on-beat and polyrhythm approach
# result = generate_syllable_timings(lyrics_2d, bpm)

#next, parse the output which is a 5-tuple in the following structure
# initial_delay, on_beat_timings, polyrhythm_timings, final_delay, total_song_length = result

#initial_delay is the amount of time to count in before the lyrics should come in
#final_delay is the amount of time to count out after the final line is complete
#total_song_length is the total length of the song including initial and final delay and lyric timings
#on_beat_timings will play each syllable on beat, with a delay at the end to close out the rest of the line
#polyrhythm_timings will divide the syllables to the length of the line

#to use all of this together:
#count in for the length of the initial delay
#print word, wait for associated delay
#repeat for all lines
#count out for the length of the final delay

