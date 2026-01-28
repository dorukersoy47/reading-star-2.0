from fastapi import FastAPI
import uvicorn
from api import router as api_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

# register routers
app.include_router(api_router, prefix="/instrumentals")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)