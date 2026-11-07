import os
import sys
import shutil
import subprocess
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEOS = os.path.join(ROOT, "starfall_pocket", "assets", "videos")


def ffmpeg():
    path = shutil.which("ffmpeg")
    if path:
        return path
    if importlib.util.find_spec("imageio_ffmpeg") is None:
        print("Installing imageio-ffmpeg (one time)...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "imageio-ffmpeg"])
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/import_video.py <video.mp4> [name]")
        sys.exit(1)
    src = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(os.path.basename(src))[0]
    out = os.path.join(VIDEOS, name)
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    exe = ffmpeg()
    scale = "scale=450:800:force_original_aspect_ratio=decrease,pad=450:800:(ow-iw)/2:(oh-ih)/2:black,fps=29.97"
    subprocess.check_call([exe, "-v", "error", "-y", "-i", src, "-vf", scale, "-q:v", "5", os.path.join(out, "%04d.jpg")])
    try:
        subprocess.check_call([exe, "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "22050", "-c:a", "libvorbis", "-q:a", "4",
                               os.path.join(out, "audio.ogg")])
    except subprocess.CalledProcessError:
        print("No audio track found, saved frames only")
    frames = len([f for f in os.listdir(out) if f.endswith(".jpg")])
    print(f"Saved {frames} frames to {out}")
    print(f'Use it in content.py with "videos": ["{name}"]')


if __name__ == "__main__":
    main()
