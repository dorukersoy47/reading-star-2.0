from fastapi import FastAPI
from api.lyrics import router as lyrics_router
from api.instrumentals import router as instrumental_router

app = FastAPI()

# register routers
app.include_router(instrumental_router, prefix="/instrumentals")
app.include_router(lyrics_router, prefix="/instrumentals")