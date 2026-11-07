import os
import sys
import wave
import shutil
import subprocess
import numpy as np

SR = 22050
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "starfall_pocket", "assets", "music")
NOTES = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}


def midi(name):
    pitch, octave = name[:-1], int(name[-1])
    return 12 * (octave + 1) + NOTES[pitch]


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env(n, attack=0.005, release=0.05, decay=0.0):
    t = np.arange(n) / SR
    e = np.minimum(1.0, t / max(attack, 1e-4))
    if decay:
        e *= np.exp(-decay * t)
    r = int(release * SR)
    if r and r < n:
        e[-r:] *= np.linspace(1, 0, r)
    return e


def osc(kind, f, n, duty=0.5, vib=0.0):
    t = np.arange(n) / SR
    phase = f * t + (vib * np.sin(2 * np.pi * 5.5 * t) / (2 * np.pi * 5.5) * f if vib else 0)
    p = phase % 1.0
    if kind == "square":
        return np.where(p < duty, 1.0, -1.0)
    if kind == "saw":
        return 2 * p - 1
    if kind == "tri":
        return 4 * np.abs(p - 0.5) - 1
    return np.sin(2 * np.pi * phase)


def lowpass(x, a):
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += a * (x[i] - acc)
        y[i] = acc
    return y


class Track:
    def __init__(self, bpm, bars):
        self.beat = 60 / bpm
        self.n = int(round(bars * 4 * self.beat * SR))
        self.buf = np.zeros(self.n)

    def add(self, start_beat, sound, vol):
        i = int(start_beat * self.beat * SR)
        if i >= self.n:
            return
        end = min(self.n, i + len(sound))
        self.buf[i:end] += sound[: end - i] * vol

    def note(self, start, beats, name, kind, vol, duty=0.5, vib=0.0, attack=0.005, release=0.05, decay=0.0):
        n = int(beats * self.beat * SR)
        f = hz(midi(name) if isinstance(name, str) else name)
        self.add(start, osc(kind, f, n, duty, vib) * env(n, attack, release, decay), vol)

    def kick(self, start, vol=0.9):
        n = int(0.28 * SR)
        t = np.arange(n) / SR
        f = 45 + 110 * np.exp(-t * 28)
        self.add(start, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9), vol)

    def snare(self, start, vol=0.5, rng=np.random.default_rng(1)):
        n = int(0.18 * SR)
        t = np.arange(n) / SR
        noise = np.diff(rng.uniform(-1, 1, n + 1))
        self.add(start, (noise * 0.8 + np.sin(2 * np.pi * 185 * t) * 0.5) * np.exp(-t * 22), vol)

    def hat(self, start, vol=0.18, length=0.045, rng=np.random.default_rng(2)):
        n = int(length * SR)
        noise = np.diff(np.diff(rng.uniform(-1, 1, n + 2)))
        self.add(start, noise * np.exp(-np.arange(n) / SR * 70), vol)

    def crash(self, start, vol=0.25, rng=np.random.default_rng(3)):
        n = int(1.4 * SR)
        noise = np.diff(rng.uniform(-1, 1, n + 1))
        self.add(start, noise * np.exp(-np.arange(n) / SR * 3), vol)

    def save(self, name):
        x = self.buf / max(1e-6, np.max(np.abs(self.buf))) * 0.85
        data = (x * 32767).astype(np.int16).tobytes()
        os.makedirs(OUT, exist_ok=True)
        wav = os.path.join(OUT, name + ".wav")
        with wave.open(wav, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(data)
        exe = shutil.which("ffmpeg")
        if exe:
            subprocess.check_call([exe, "-v", "error", "-y", "-i", wav, "-c:a", "libvorbis", "-q:a", "5", os.path.join(OUT, name + ".ogg")])
            os.remove(wav)
            print("Saved", os.path.join(OUT, name + ".ogg"))
        else:
            print("Saved", wav)


def chord_tones(root, minor):
    r = midi(root)
    return [r, r + (3 if minor else 4), r + 7]


def bgm():
    tr = Track(104, 16)
    prog = [("C3", 0), ("G2", 0), ("A2", 1), ("F2", 0), ("C3", 0), ("G2", 0), ("F2", 0), ("G2", 0)] * 2
    melody = [
        ("E5", 1), ("G5", 1), ("A5", 1.5), ("G5", 0.5), ("D5", 1), ("G5", 1), ("B5", 2),
        ("C6", 1), ("B5", 0.5), ("A5", 0.5), ("E5", 2), ("F5", 1), ("A5", 1), ("C6", 1), ("A5", 1),
        ("G5", 1.5), ("E5", 0.5), ("C5", 2), ("D5", 1), ("G5", 1), ("B5", 1), ("D6", 1),
        ("C6", 1), ("A5", 1), ("F5", 1), ("A5", 1), ("G5", 3), (None, 1),
    ]
    for bar, (root, minor) in enumerate(prog):
        b = bar * 4
        tones = chord_tones(root, minor)
        for i in range(8):
            tr.note(b + i * 0.5, 0.45, tones[0] - (0 if i % 2 == 0 else -12), "tri", 0.32, release=0.05)
        for tone in tones:
            tr.note(b, 4, tone + 12, "square", 0.035, duty=0.25, attack=0.08, release=0.4)
        for i in range(16):
            tr.note(b + i * 0.25, 0.22, tones[i % 3] + 24 + (12 if i % 8 >= 4 else 0), "sine", 0.06, decay=6)
        tr.kick(b, 0.6)
        tr.kick(b + 2, 0.6)
        tr.snare(b + 1, 0.22)
        tr.snare(b + 3, 0.22)
        for i in range(8):
            tr.hat(b + i * 0.5, 0.09)
    start = 32
    for name, beats in melody:
        if name:
            tr.note(start, beats * 0.92, name, "square", 0.08, duty=0.5, vib=0.004, attack=0.01, release=0.08)
        start += beats
    tr.save("bgm")


def battle():
    tr = Track(156, 16)
    prog = [("A2", 1), ("F2", 0), ("G2", 0), ("E2", 0), ("A2", 1), ("F2", 0), ("D2", 1), ("E2", 0)] * 2
    lead = [
        ("A4", 0.5), ("C5", 0.5), ("E5", 1), ("A5", 1), ("G5", 0.5), ("E5", 0.5),
        ("F5", 1), ("E5", 0.5), ("D5", 0.5), ("C5", 1), ("A4", 1),
        ("B4", 0.5), ("D5", 0.5), ("G5", 1), ("F5", 0.5), ("E5", 0.5), ("D5", 1),
        ("E5", 1.5), ("G#5", 0.5), ("B5", 2),
        ("C6", 1), ("B5", 0.5), ("A5", 0.5), ("E5", 1), ("C5", 1),
        ("F5", 1), ("A5", 1), ("C6", 1), ("A5", 1),
        ("D6", 1), ("C6", 0.5), ("A5", 0.5), ("F5", 1), ("D5", 1),
        ("E5", 1), ("G#5", 1), ("B5", 1), ("E6", 1),
    ]
    for bar, (root, minor) in enumerate(prog):
        b = bar * 4
        r = midi(root)
        for i in range(8):
            tr.note(b + i * 0.5, 0.42, r + (12 if i % 2 else 0), "saw", 0.22, release=0.03)
        tones = chord_tones(root, minor)
        for i in range(16):
            tr.note(b + i * 0.25, 0.2, tones[i % 3] + 24, "square", 0.045, duty=0.125, decay=8)
        for beat in range(4):
            tr.kick(b + beat, 0.85)
        tr.snare(b + 1, 0.5)
        tr.snare(b + 3, 0.5)
        if bar % 4 == 3:
            tr.snare(b + 3.5, 0.35)
            tr.snare(b + 3.75, 0.35)
        for i in range(16):
            tr.hat(b + i * 0.25, 0.1 if i % 2 else 0.16)
        if bar % 8 == 0:
            tr.crash(b, 0.3)
    for rep in range(2):
        start = rep * 32
        for name, beats in lead:
            tr.note(start, beats * 0.9, name, "square", 0.11, duty=0.5, vib=0.006, attack=0.005, release=0.05)
            tr.note(start, beats * 0.9, midi(name) - 12, "saw", 0.04, attack=0.005, release=0.05)
            start += beats
    tr.buf = lowpass(tr.buf, 0.55) * 0.5 + tr.buf * 0.5
    tr.save("battle")


if __name__ == "__main__":
    which = sys.argv[1:] or ["bgm", "battle"]
    if "bgm" in which:
        bgm()
    if "battle" in which:
        battle()
