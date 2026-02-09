from sqlalchemy import func
from datetime import datetime, timedelta
from .models import AudioSample, Audio1Min

def compress_previous_minute(db):
    minute = (
        datetime.utcnow()
        .replace(second=0, microsecond=0)
        - timedelta(minutes=1)
    )

    stats = (
        db.query(
            func.max(AudioSample.peak_db),
            func.avg(AudioSample.peak_db),
            func.count(AudioSample.id)
        )
        .filter(
            AudioSample.timestamp >= minute,
            AudioSample.timestamp < minute + timedelta(minutes=1)
        )
        .one()
    )

    if stats[2] == 0:
        return

    db.merge(Audio1Min(
        minute=minute,
        peak_max=stats[0],
        peak_avg=stats[1],
        sample_count=stats[2]
    ))


def cleanup_raw(db, hours=24):
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    db.query(AudioSample).filter(
        AudioSample.timestamp < cutoff
    ).delete()
