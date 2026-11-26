from fastapi import FastAPI

app = FastAPI(title="InternTrack")


@app.get("/health")
def health():
    return {"status": "ok"}
