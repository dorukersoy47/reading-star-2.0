import speech_recognition as sr

def recognize_for_duration(duration=60):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Adjusting for ambient noise... Please wait.")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print(f"Listening for {duration} seconds...")

        try:
            audio = recognizer.record(source, duration=duration)
            print("Processing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""

def get_recognized_words(duration=60):
    text = recognize_for_duration(duration).lower()
    words = text.split()
    return words
