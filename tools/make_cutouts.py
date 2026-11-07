import os
import sys
import subprocess
import importlib.util

EXTS = (".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif")


def ensure():
    if importlib.util.find_spec("rembg") is None:
        print("Installing rembg (one time, this can take a few minutes)...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "rembg[cpu]", "pillow-heif"])


def main():
    if len(sys.argv) < 3:
        print("Usage: python tools/make_cutouts.py <input folder or image> <output folder>")
        sys.exit(1)
    ensure()
    from PIL import Image, ImageChops, ImageOps
    from rembg import remove, new_session
    try:
        from pillow_heif import register_heif_opener
        register_heif_opener()
    except ImportError:
        pass
    src, out = sys.argv[1], sys.argv[2]
    files = [src] if os.path.isfile(src) else [os.path.join(src, f) for f in sorted(os.listdir(src)) if f.lower().endswith(EXTS)]
    os.makedirs(out, exist_ok=True)
    images = {f: ImageOps.exif_transpose(Image.open(f)).convert("RGB") for f in files}
    for img in images.values():
        img.thumbnail((1400, 1400))
    masks = {}
    for model in ("isnet-general-use", "u2net_human_seg"):
        print(f"Running {model}...")
        session = new_session(model)
        for f, img in images.items():
            m = remove(img, session=session, only_mask=True).convert("L")
            masks[f] = m if f not in masks else ImageChops.lighter(masks[f], m)
        del session
    for f, img in images.items():
        stem = os.path.splitext(os.path.basename(f))[0]
        mask = masks[f]
        if "kakuhen" not in stem and "確変" not in stem:
            mask = mask.point(lambda v: 0 if v < 20 else min(255, int((v - 20) * 2.2)))
        cut = img.convert("RGBA")
        cut.putalpha(mask)
        box = mask.point(lambda v: 255 if v > 40 else 0).getbbox()
        if box:
            pad = 12
            cut = cut.crop((max(0, box[0] - pad), max(0, box[1] - pad), min(cut.width, box[2] + pad), min(cut.height, box[3] + pad)))
        path = os.path.join(out, stem + ".png")
        cut.save(path, optimize=True)
        print("Saved", path)


if __name__ == "__main__":
    main()
