from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import datetime
import threading
import time
import os

from .database import SessionLocal, engine
from .models import Base, AudioSample, Audio1Min
from .audio import measure_peak_db
from .compress import compress_previous_minute, cleanup_raw

Base.metadata.create_all(bind=engine)

SAMPLE_INTERVAL = int(os.getenv("SAMPLE_INTERVAL", 5))

app = FastAPI()

def sampler():
    last_minute = None

    while True:
        db: Session = SessionLocal()
        try:
            peak = measure_peak_db()
            if peak is not None:
                db.add(AudioSample(peak_db=peak))
                db.commit()

            current_minute = datetime.utcnow().replace(second=0, microsecond=0)
            if current_minute != last_minute:
                compress_previous_minute(db)
                cleanup_raw(db)
                db.commit()
                last_minute = current_minute

        finally:
            db.close()

        time.sleep(SAMPLE_INTERVAL)

@app.on_event("startup")
def start_sampler():
    threading.Thread(target=sampler, daemon=True).start()

@app.get("/api/history")
def history(
    start: datetime | None = Query(None),
    end: datetime | None = Query(None)
):
    db = SessionLocal()
    q = db.query(Audio1Min)

    if start:
        q = q.filter(Audio1Min.minute >= start)
    if end:
        q = q.filter(Audio1Min.minute <= end)

    rows = q.order_by(Audio1Min.minute).all()
    db.close()
    return rows

@app.get("/")
def ui():
    with open("app/static/index.html") as f:
        return HTMLResponse(f.read())
