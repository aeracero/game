import sys
import subprocess
import importlib.util

NEEDED = {"pygame": "pygame-ce>=2.5.6", "PIL": "Pillow>=9.0", "certifi": "certifi", "pillow_heif": "pillow-heif"}


def ensure_dependencies():
    missing = [pkg for mod, pkg in NEEDED.items() if importlib.util.find_spec(mod) is None]
    if not missing:
        return
    print("Installing:", ", ".join(missing))
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
    except subprocess.CalledProcessError:
        print("\nAutomatic install failed. Run these lines one at a time, then try again:")
        if sys.platform.startswith("win"):
            print("  python -m venv .venv")
            print("  .venv\\Scripts\\activate")
        else:
            print("  python3 -m venv .venv")
            print("  source .venv/bin/activate")
        print("  python run.py")
        sys.exit(1)
    importlib.invalidate_caches()


if __name__ == "__main__":
    ensure_dependencies()
    from starfall_pocket.main import run
    run()
