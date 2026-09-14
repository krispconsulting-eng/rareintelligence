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


def thud(length: float = 0.55, gain: float = 0.30) -> np.ndarray:
    """The weight of the landing: a short sine with the pitch dropping away. A few
    milliseconds of attack keep it a soft thump rather than a hit."""
    t = np.arange(int(length * SR)) / SR
    freq = 38.0 + 52.0 * np.exp(-t / 0.055)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    return np.sin(phase) * np.exp(-t / 0.16) * (1 - np.exp(-t / 0.006)) * gain


def knock(gain: float = 0.16) -> np.ndarray:
    """The midrange of the landing. Phone speakers roll off below about 500 Hz, so
    without this the impacts are felt on headphones and lost on a phone."""
    t = np.arange(int(0.14 * SR)) / SR
    rng = np.random.default_rng(11)
    noise = rng.standard_normal(t.size)
    band = lowpass(noise, 900.0) - lowpass(noise, 220.0)
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


BAR = 4 * (60.0 / 120.0)

# Bass root, pluck tones and pad tones per chord, in Hz. A minor with its VI and VII,
# plucks kept to notes that sit inside the pentatonic the landing bells use.
CHORDS = {
    "Am": (110.00, [220.00, 261.63, 329.63, 440.00], [220.00, 261.63, 329.63]),
    "F": (87.31, [174.61, 220.00, 261.63, 349.23], [174.61, 220.00, 261.63]),
    "G": (98.00, [196.00, 293.66, 392.00, 587.33], [196.00, 293.66, 392.00]),
}
PROGRESSION = ["Am", "Am", "F", "G"]
PLUCK_PATTERN = [0, 1, 2, 3, 2, 1, 0, 1]


def kick(gain: float = 0.13) -> np.ndarray:
    t = np.arange(int(0.28 * SR)) / SR
    freq = 44.0 + 60.0 * np.exp(-t / 0.03)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    return np.sin(phase) * np.exp(-t / 0.085) * (1 - np.exp(-t / 0.002)) * gain


def hat(length: float = 0.03, gain: float = 0.03, seed: int = 5) -> np.ndarray:
    t = np.arange(int(max(length * 4, 0.08) * SR)) / SR
    rng = np.random.default_rng(seed)
    noise = rng.standard_normal(t.size)
    high = noise - lowpass(noise, 5500.0)
    high /= np.abs(high).max() or 1.0
    return high * np.exp(-t / length) * gain


def pluck(freq: float, gain: float = 0.06, length: float = 0.35) -> np.ndarray:
    t = np.arange(int(length * SR)) / SR
    w = np.sin(2 * np.pi * freq * t)
    w += 0.28 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-t / 0.05)
    w += 0.08 * np.sin(2 * np.pi * 3 * freq * t)
    return w * np.exp(-t / 0.10) * (1 - np.exp(-t / 0.0012)) * gain


def bass(freq: float, gain: float = 0.09, length: float = 0.3) -> np.ndarray:
    t = np.arange(int(length * SR)) / SR
    w = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * 2 * freq * t)
    return w * np.exp(-t / 0.14) * (1 - np.exp(-t / 0.004)) * gain


def pad(freqs: list[float], length: float, gain: float = 0.026) -> np.ndarray:
    t = np.arange(int(length * SR)) / SR
    w = np.zeros_like(t)
    for f in freqs:
        for detune in (-0.4, 0.0, 0.4):
            w += np.sin(2 * np.pi * (f + detune) * t + detune)
    w /= 3 * len(freqs)
    attack = 1 - np.exp(-t / 0.5)
    release = np.clip((length - t) / 0.6, 0, 1)
    return w * attack * release * gain


def music() -> np.ndarray:
    """A quiet, driving bed at 120 bpm: four-on-the-floor kick, eighth-note hats, a
    syncopated bass and a rolling pentatonic pluck. It builds through the twelve labs,
    then drops to the pad alone under the closing card."""
    buf = np.zeros((int(TOTAL * SR), 2), dtype=np.float64)
    bars = int(TOTAL / BAR)
    first_lab_bar = int(INTRO / BAR)
    last_lab_bar = first_lab_bar + len(LABS)

    for bar in range(bars):
        start = bar * BAR
        in_labs = first_lab_bar <= bar < last_lab_bar
        chord = PROGRESSION[(bar - first_lab_bar) % len(PROGRESSION)] if in_labs else "Am"
        root, tones, pad_tones = CHORDS[chord]
        build = 0.85 + 0.15 * min(1.0, max(0.0, (bar - first_lab_bar) / (len(LABS) - 1)))

        add(buf, start, pad(pad_tones, BAR + 0.6))

        if bar >= first_lab_bar - 1 and bar < last_lab_bar:
            for eighth in range(8):
                at = start + eighth * BAR / 8
                is_open = eighth in (3, 7)
                add(buf, at, hat(0.07 if is_open else 0.03, (0.038 if is_open else 0.028) * build, seed=eighth), 0.25)

        if not in_labs:
            continue

        for beat in (0, 1, 2):          # beat 4 belongs to the landing thud
            add(buf, start + beat * BAR / 4, kick(0.13 * build))
        for at in (0.0, 0.75, 1.0, 1.75):
            add(buf, start + at, bass(root, 0.09 * build))
        for eighth, idx in enumerate(PLUCK_PATTERN):
            at = start + eighth * BAR / 8
            add(buf, at, pluck(tones[idx], 0.06 * build), -0.2)
            if bar >= first_lab_bar + 6 and eighth % 2 == 1:
                add(buf, at, pluck(tones[idx] * 2, 0.028 * build, 0.25), 0.35)

    t = np.arange(buf.shape[0]) / SR
    duck = np.ones_like(t)
    for at in LANDINGS + [FINAL]:
        age = t - at
        duck = np.minimum(duck, np.where(age >= 0, 1 - 0.55 * np.exp(-age / 0.16), 1.0))
    outro = np.clip((TOTAL - 1.0 - t) / 3.0, 0, 1)
    outro = np.where(t < FINAL, 1.0, outro)
    return buf * (duck * outro)[:, None]


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
    tune = music()
    buf += tune
    music_rms = float(np.sqrt((tune ** 2).mean()))
    print(f"music bed rms {20*np.log10(music_rms):.1f} dBFS before normalisation")

    add(buf, 0.1, riser(0.9, 0.09))
    add(buf, 1.0, thud(0.7, 0.34))
    add(buf, 1.0, bell(110.0, 2.4, 0.13))

    for i, at in enumerate(LANDINGS):
        pan = ((i % 5) - 2) / 6.0
        add(buf, at - 0.42, whoosh(), pan * 0.6)
        add(buf, at, thud())
        add(buf, at, knock(), pan * 0.4)
        add(buf, at, tick(0.025), pan)
        add(buf, at, bell(NOTES[i]), pan)

    for at in POPS:
        add(buf, at, tick(0.028), 0.0)

    add(buf, FINAL - 1.1, riser(1.1, 0.13))
    add(buf, FINAL, thud(0.9, 0.40))
    add(buf, FINAL, knock(0.22))
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
