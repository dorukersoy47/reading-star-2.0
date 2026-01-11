from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Request(BaseModel):
    prompt: str

@app.post("/sample")
def generate_lyrics(req: Request):
    print("ok!")
    return {
        "lyrics": "La la la"
    }