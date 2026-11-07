# Starfall Pocket

A card-pulling game written entirely in Python. Sign in with your email, pull cards for free, watch them slam onto the desk, collect them all, and send any card to your Gmail.

**New here? Read [GUIDE.md](GUIDE.md).**

- Cards are cut-out photos. The image name decides the rarity: Medium Rare, Rare, Super Rare, Cooked and What is this?
- Pull 10 at a time. A gold or rainbow flash shows a Super Rare or ULTRA RARE is coming, and each card's stars (1 to 6) pop in one by one.
- Every card has a 1% chance to be ULTRA RARE, disguised as a normal card that shatters to reveal it.
- The special ULTRA RARE card plays a sound, a line of text, and two videos before it appears.
- Sounds, music, backgrounds, videos and animations are all files you can add or swap.

## Download the app

No Python needed. Go to the **Releases** page of this repo and download the file for your computer:

| Computer | File | How to open |
| --- | --- | --- |
| Windows | `StarfallPocket-Windows.exe` | Double-click. If Windows SmartScreen appears, click **More info**, then **Run anyway** |
| Mac (Apple Silicon) | `StarfallPocket-macOS-arm64.zip` | Unzip, then right-click **Starfall Pocket** and choose **Open** the first time |
| Linux | `StarfallPocket-Linux-x86_64.tar.gz` | Extract, then run `./"Starfall Pocket"` |

The warnings appear because the app isn't signed with a paid developer certificate. They only show the first time.

### Publishing a new version

The apps are built automatically by GitHub Actions. To publish a release:

```bash
git tag v1.0.0
git push origin v1.0.0
```

After a few minutes the Windows, Mac, and Linux apps appear on the Releases page. You can also run the workflow by hand from the **Actions** tab; the files then appear as downloads on that run.

To build the app for your own computer locally, run `python build_app.py`. The result goes in `dist/release`.

## Run from source

You need Python 3.9 or newer.

**Option 1: install straight from GitHub**

```bash
pip install git+https://github.com/aeracero/starfall-pocket.git
starfall-pocket
```

If the `starfall-pocket` command isn't found, run `python -m starfall_pocket` instead.

**Option 2: clone and run**

```bash
git clone https://github.com/aeracero/starfall-pocket.git
cd starfall-pocket
python run.py
```

`run.py` installs pygame and Pillow automatically if they're missing.

## Send cards to Gmail

Without Gmail set up, the game still works: sign-up verification is skipped and card emails are saved as `.eml` files in the outbox folder.

To send real emails:

1. Turn on 2-Step Verification for your Google account.
2. Create an App Password at https://myaccount.google.com/apppasswords.
3. Either set environment variables:

   ```bash
   export GMAIL_ADDRESS="you@gmail.com"
   export GMAIL_APP_PASSWORD="abcd efgh ijkl mnop"
   ```

   or, easiest, open **Gmail settings** in the app (the gear on the home screen, or the link at the bottom of the sign-in screen) and paste them there. They're saved in `mail_settings.py` in the data folder:

   | OS | Data folder |
   | --- | --- |
   | Windows | `C:\Users\<you>\.starfall_pocket` |
   | macOS / Linux | `~/.starfall_pocket` |

Your password never goes into the repository. Set `STARFALL_HOME` to use a different data folder.

## Customizing

| What | Where |
| --- | --- |
| Cards | `starfall_pocket/assets/cards/` |
| ULTRA RARE card image | `starfall_pocket/assets/ultra/` |
| Videos | `starfall_pocket/assets/videos/` (convert with `tools/import_video.py`) |
| Sounds and music | `starfall_pocket/assets/sounds/`, `starfall_pocket/assets/music/` |
| Backgrounds | `starfall_pocket/assets/backgrounds/` |
| Rarities, odds, ULTRA RARE | `starfall_pocket/content.py` |
| Animations | `starfall_pocket/animations/` |

## Card abilities

| Ability | What arrives in your inbox |
| --- | --- |
| Quick Strike | The card as a glowing inline image |
| Shatter Burst | 4 emails, one quarter of the card each |
| Cipher Veil | The card encrypted with a Python decoder, then the key in a second email |
| Time Capsule | The card, 30 seconds after you send it |
| Mirage Shimmer | A looping animated GIF of the card |
| Pixel Rain | The card rebuilt from colored text blocks |
| Royal Vault | A ZIP with the card, its data, and a numbered certificate |

## Project layout

```
starfall_pocket/
  content.py   rarities, odds, ULTRA RARE, music (edit this)
  assets/      cards, ultra card, videos, sounds, music, backgrounds, font
  animations/  card effects, motions and reveals
  main.py      game UI and scenes
  render.py    card, pack and effect drawing
  cards.py     finds card images and rolls pulls
  mailer.py    Gmail abilities (separate from the UI)
  audio.py     sound effects and music
  assets.py    finds and loads asset files
  storage.py   accounts and saving
  config.py    data folder and Gmail settings
examples/      example animation file
tools/         make_cutouts.py (remove photo backgrounds), import_video.py (MP4 to frames)
originals/     the original photos before background removal
starfall_app.py   entry point used for the standalone app
build_app.py      builds the app with PyInstaller
run.py            clone-and-run launcher
setup.py          lets pip install from GitHub
.github/workflows/build.yml   builds Windows, Mac, and Linux apps on GitHub
```
