"""Build the sound design for the toolkit video.

Not music: a whoosh on each drop and an impact on each landing, sitting on a very quiet
bed. The twelve landings are tuned to an ascending A minor pentatonic, so the bag fills
up audibly as well as visually. It stands on its own, and it also sits under a music
track if one gets added later.

Timings are derived from the same constants as render.py, so the two stay in step.

    python3 make_audio.py          # writes out/toolkit-audio.wav
    python3 make_audio.py --mux    # and muxes it onto the rendered video
"""

from __future__ import annotations

import argparse
import subprocess
import wave
from pathlib import Path

import numpy as np

from render import FPS, IMPACT, INTRO, LABS, OUTRO, PER_BUTTON, TOTAL

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
SR = 48_000

LANDINGS = [INTRO + i * PER_BUTTON + IMPACT for i in range(len(LABS))]
POPS = [INTRO + i * PER_BUTTON for i in range(len(LABS))]
FINAL = INTRO + len(LABS) * PER_BUTTON

# A minor pentatonic, one note per lab, climbing.
NOTES = [220.00, 261.63, 293.66, 329.63, 392.00, 440.00,
         523.25, 587.33, 659.25, 783.99, 880.00, 1046.50]


def lowpass(x: np.ndarray, cutoff: np.ndarray | float) -> np.ndarray:
    """One-pole lowpass; cutoff may be a per-sample array for a sweep."""
    fc = np.broadcast_to(np.asarray(cutoff, dtype=np.float64), x.shape)
    a = 1.0 - np.exp(-2.0 * np.pi * np.clip(fc, 20.0, SR / 2.2) / SR)
    out = np.empty_like(x)
    y = 0.0
    for i in range(x.size):
        y += a[i] * (x[i] - y)
        out[i] = y
    return out


def add(buf: np.ndarray, at: float, sound: np.ndarray, pan: float = 0.0) -> None:
    start = int(at * SR)
    if start < 0:
        sound, start = sound[-start:], 0
    end = min(buf.shape[0], start + sound.size)
    if end <= start:
        return
    chunk = sound[: end - start]
    left, right = np.sqrt(0.5 * (1.0 - pan)), np.sqrt(0.5 * (1.0 + pan))
    buf[start:end, 0] += chunk * left * np.sqrt(2)
    buf[start:end, 1] += chunk * right * np.sqrt(2)


def bell(freq: float, length: float = 1.6, gain: float = 0.32) -> np.ndarray:
    """A struck tone: fundamental plus two quiet partials, exponential decay."""
    t = np.arange(int(length * SR)) / SR
    body = np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.42)
    body += 0.34 * np.sin(2 * np.pi * freq * 2.01 * t) * np.exp(-t / 0.17)
    body += 0.12 * np.sin(2 * np.pi * freq * 3.02 * t) * np.exp(-t / 0.08)
    body *= 1.0 - np.exp(-t / 0.0015)          # soften the attack click
    return body * gain


def thud(length: float = 0.55, gain: float = 0.42) -> np.ndarray:
    """The weight of the landing: a short sine with the pitch dropping away."""
    t = np.arange(int(length * SR)) / SR
    freq = 38.0 + 52.0 * np.exp(-t / 0.055)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    return np.sin(phase) * np.exp(-t / 0.13) * gain


def knock(gain: float = 0.30) -> np.ndarray:
    """The midrange of the landing. Phone speakers roll off below about 500 Hz, so
    without this the impacts are felt on headphones and lost on a phone."""
    t = np.arange(int(0.14 * SR)) / SR
    rng = np.random.default_rng(11)
    noise = rng.standard_normal(t.size)
    band = lowpass(noise, 1500.0) - lowpass(noise, 260.0)
    band /= np.abs(band).max() or 1.0
    tone = np.sin(2 * np.pi * (520.0 + 240.0 * np.exp(-t / 0.02)) * t)
    return (band * 0.75 + tone * 0.45) * np.exp(-t / 0.038) * gain


def whoosh(length: float = 0.42, gain: float = 0.17) -> np.ndarray:
    """Air moving past a falling object: noise closing down, swelling to the impact."""
    n = int(length * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(7)
    cutoff = 5200.0 * np.exp(-t / 0.20) + 220.0
    body = lowpass(rng.standard_normal(n), cutoff)
    body /= np.abs(body).max() or 1.0
    swell = (t / length) ** 2.1
    return body * swell * gain


def riser(length: float, gain: float = 0.12) -> np.ndarray:
    n = int(length * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(19)
    cutoff = 300.0 + 5200.0 * (t / length) ** 2.4
    body = lowpass(rng.standard_normal(n), cutoff)
    body /= np.abs(body).max() or 1.0
    return body * (t / length) ** 2.0 * gain


def tick(gain: float = 0.05) -> np.ndarray:
    t = np.arange(int(0.05 * SR)) / SR
    rng = np.random.default_rng(3)
    body = lowpass(rng.standard_normal(t.size), 5200.0)
    return body / (np.abs(body).max() or 1.0) * np.exp(-t / 0.008) * gain


def bed(length: float) -> np.ndarray:
    """Barely-there drone, so the cut is not dead silent between hits."""
    t = np.arange(int(length * SR)) / SR
    drone = np.sin(2 * np.pi * 55.0 * t) + 0.7 * np.sin(2 * np.pi * 82.41 * t)
    drone += 0.5 * np.sin(2 * np.pi * 110.0 * t + 0.4)
    breathe = 0.7 + 0.3 * np.sin(2 * np.pi * t / 9.0)
    fade = np.clip(t / 1.2, 0, 1) * np.clip((length - t) / 2.0, 0, 1)
    return drone * breathe * fade * 0.011


def build() -> np.ndarray:
    buf = np.zeros((int(TOTAL * SR), 2), dtype=np.float64)
    add(buf, 0.0, bed(TOTAL))

    add(buf, 0.1, riser(0.9, 0.09))
    add(buf, 1.0, thud(0.7, 0.34))
    add(buf, 1.0, bell(110.0, 2.4, 0.13))

    for i, at in enumerate(LANDINGS):
        pan = ((i % 5) - 2) / 6.0
        add(buf, at - 0.42, whoosh(), pan * 0.6)
        add(buf, at, thud())
        add(buf, at, knock(), pan * 0.4)
        add(buf, at, tick(), pan)
        add(buf, at, bell(NOTES[i]), pan)

    for at in POPS:
        add(buf, at, tick(0.028), 0.0)

    add(buf, FINAL - 1.1, riser(1.1, 0.13))
    add(buf, FINAL, thud(0.9, 0.50))
    add(buf, FINAL, knock(0.34))
    for freq, pan in ((220.0, -0.3), (261.63, 0.0), (329.63, 0.3), (440.0, -0.15)):
        add(buf, FINAL, bell(freq, 3.2, 0.20), pan)

    tail = np.clip((TOTAL - np.arange(buf.shape[0]) / SR) / 0.9, 0, 1)
    buf *= tail[:, None]
    peak = np.abs(buf).max()
    if peak:
        buf *= 0.89 / peak
    return buf


def write_wav(buf: np.ndarray, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (np.clip(buf, -1.0, 1.0) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mux", action="store_true", help="mux onto the rendered video")
    args = ap.parse_args()

    buf = build()
    wav = OUT / "toolkit-audio.wav"
    write_wav(buf, wav)
    rms = float(np.sqrt((buf ** 2).mean()))
    print(f"{wav}  {TOTAL:.1f}s  peak {np.abs(buf).max():.3f}  rms {rms:.4f} ({20*np.log10(rms):.1f} dBFS)")

    if args.mux:
        video = HERE.parent / "kris-pierce-toolkit.mp4"
        out = HERE.parent / "kris-pierce-toolkit-sound.mp4"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-i", str(wav),
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
             "-movflags", "+faststart", str(out)],
            check=True,
        )
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
