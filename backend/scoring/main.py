from backend.scoring.scoreWords import get_recognized_words

def scoring_system(lyrics, duration=10):
    print(f"Listening for {duration} seconds...")
    recognized_words = get_recognized_words(duration)
    print(f"Recognized words: {recognized_words}")

    # Count matching words
    lyrics_words = set(lyrics.lower().split())
    matching_words = [word for word in recognized_words if word in lyrics_words]
    score = len(matching_words)

    score = 0
    for word in matching_words:
        score += len(word)

    return score

# Example usage
if __name__ == "__main__":
    lyrics = "twinkle twinkle little star how I wonder what you are"
    print(scoring_system(lyrics.lower(), duration=10))
