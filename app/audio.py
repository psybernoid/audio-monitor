import subprocess
import numpy as np
import math
import os

RTSP_URL = os.getenv("RTSP_URL")

def measure_peak_db(duration=1):
    cmd = [
        "ffmpeg",
        "-rtsp_transport", "tcp",
        "-i", RTSP_URL,
        "-t", str(duration),
        "-vn",
        "-ac", "1",
        "-ar", "44100",
        "-f", "s16le",
        "pipe:1"
    ]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    raw = proc.stdout.read()
    proc.wait()

    if not raw:
        return None

    audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    peak = np.max(np.abs(audio))

    if peak == 0:
        return -float("inf")

    return 20 * math.log10(peak)
