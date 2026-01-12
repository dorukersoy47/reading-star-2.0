from models.generation import InstrumentalPrompt, GeneratedInstrumental

def generateMusic(prompt : InstrumentalPrompt) -> GeneratedInstrumental:
    return GeneratedInstrumental(
        title="test instrumental",
        prompt=prompt,
        music="this is the music"
    )