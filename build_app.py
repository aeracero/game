import os
import sys
import shutil
import platform
import subprocess
import importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))
NAME = "Starfall Pocket"
ASSETS = os.path.join(ROOT, "build_assets")
DIST = os.path.join(ROOT, "dist")
RELEASE = os.path.join(DIST, "release")
NEEDED = {"PyInstaller": "pyinstaller", "pygame": "pygame-ce>=2.5.6", "PIL": "Pillow>=9.0", "certifi": "certifi", "pillow_heif": "pillow-heif"}


def ensure_tools():
    missing = [pkg for mod, pkg in NEEDED.items() if importlib.util.find_spec(mod) is None]
    if missing:
        print("Installing:", ", ".join(missing))
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
        importlib.invalidate_caches()


def make_icons():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    sys.path.insert(0, ROOT)
    import pygame
    from PIL import Image
    from starfall_pocket.render import app_icon
    pygame.init()
    os.makedirs(ASSETS, exist_ok=True)
    png = os.path.join(ASSETS, "icon.png")
    pygame.image.save(app_icon(1024), png)
    pygame.quit()
    img = Image.open(png).convert("RGBA")
    ico = os.path.join(ASSETS, "icon.ico")
    icns = os.path.join(ASSETS, "icon.icns")
    img.save(ico, sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    img.save(icns)
    return icns if sys.platform == "darwin" else ico


def build(icon):
    args = [
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--windowed",
        "--name", NAME, "--icon", icon, "--collect-data", "certifi",
        "--add-data", os.path.join(ROOT, "starfall_pocket", "assets") + os.pathsep + os.path.join("starfall_pocket", "assets"),
        "--collect-submodules", "starfall_pocket.animations", "--collect-all", "pillow_heif",
        "--distpath", DIST, "--workpath", os.path.join(ROOT, "build"), "--specpath", ASSETS,
    ]
    if sys.platform == "darwin":
        args += ["--onedir", "--osx-bundle-identifier", "com.starfall.pocket"]
    else:
        args += ["--onefile"]
    args.append(os.path.join(ROOT, "starfall_app.py"))
    subprocess.check_call(args, cwd=ROOT)


def package():
    if os.path.exists(RELEASE):
        shutil.rmtree(RELEASE)
    os.makedirs(RELEASE)
    arch = platform.machine().lower()
    if sys.platform.startswith("win"):
        out = os.path.join(RELEASE, "StarfallPocket-Windows.exe")
        shutil.copy2(os.path.join(DIST, NAME + ".exe"), out)
    elif sys.platform == "darwin":
        out = os.path.join(RELEASE, f"StarfallPocket-macOS-{arch}.zip")
        app = os.path.join(DIST, NAME + ".app")
        if shutil.which("ditto"):
            subprocess.check_call(["ditto", "-c", "-k", "--keepParent", app, out])
        else:
            shutil.make_archive(out[:-4], "zip", DIST, NAME + ".app")
    else:
        out = shutil.make_archive(os.path.join(RELEASE, f"StarfallPocket-Linux-{arch}"), "gztar", DIST, NAME)
    print("\nBuilt:", out)


if __name__ == "__main__":
    ensure_tools()
    build(make_icons())
    package()
