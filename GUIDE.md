# Starfall Pocket: step-by-step guide

## 1. What you need

- **Python 3.9 or newer** from https://www.python.org/downloads/ (3.14 works).
- **Git** from https://git-scm.com/downloads.
- **A GitHub account**, only for putting the game online and building the apps.

On a Mac, type `python3` instead of `python`. On Windows, tick **Add python.exe to PATH** when installing.

## 2. Run the game

Open a terminal in the `starfall-pocket` folder and type these lines **one at a time**.

On a Mac:

```bash
python3 -m venv .venv
source .venv/bin/activate
python run.py
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
python run.py
```

The first run installs everything the game needs. Next time you only need the last two lines.

## 3. How it plays

1. Create an account with your **Gmail** address and a password. Other email addresses aren't accepted.
2. Connect Gmail (step 6). The game won't let you play until it's connected.
3. Enter the 6-digit code that arrives in your Gmail.
4. Tap **Pull 10 cards** (pulling is free).
5. A card flies into the sky. The flash tells you what's coming:
   - **No flash:** only common cards.
   - **Gold flash:** at least one Super Rare.
   - **Rainbow flash:** at least one ULTRA RARE.
6. Tap to slam each card onto the desk. Its stars pop in one at a time, from 1 star up to 6.
7. On the results screen, tapping **Pull 10 more** or **Home** emails all 10 cards to your Gmail. Tap a single card to send it with its own Gmail ability.

### Rarities and odds

From most common to rarest. Slots 1 to 8 and slots 9 to 10 use different odds.

| Stars | Rarity | Slots 1 to 8 | Slots 9 and 10 | Overall | Flash |
| --- | --- | --- | --- | --- | --- |
| ★ | What is this? | 48% | 10% | about 40% | none |
| ★★ | Cooked | 30% | 20% | about 28% | none |
| ★★★ | Medium Rare | 15% | 30% | about 18% | none |
| ★★★★ | Rare | 5% | 28% | about 9% | none |
| ★★★★★ | Super Rare | 2% | 12% | about 4% | gold |
| ★★★★★★ | ULTRA RARE | 1% | 1% | 1% | rainbow |

Super Rare also shakes and glows gold before it lands. To change the defaults for everyone, edit `RARITIES` in `starfall_pocket/content.py`; the list goes from most common to rarest.

### ULTRA RARE (1% per card)

Half of the ULTRA RARE hits are an ULTRA RARE version of a normal card, and half are the special ULTRA RARE video card.

- **ULTRA RARE version of a card** (no warning, it's a surprise):
  1. The card slams down looking like a normal card, using the blurry 確変 photo.
  2. It cracks and shatters into pieces.
  3. The ULTRA RARE version slams down in its place with a rainbow frame and 6 stars.
- **The special ULTRA RARE card:**
  1. `ultra_start` plays while the card back charges up.
  2. The line "Its me, PayPay" appears with `ultra_start_2`.
  3. The card waits for you to **tap it**.
  4. Battle music starts, video 1 plays and fades into video 2 (the videos' own sound is off).
  5. The last frame shrinks into the ULTRA RARE card, which slams down while its 6 stars appear. The battle music keeps going until you tap to the next card.

Tap during the videos to skip to the card. In the collection, the special card has a **Replay** button.

### Testing the odds (code 0510)

1. Open the **gear** on the home screen.
2. Tap **Test code** at the top right and enter `0510`.
3. Adjust the odds:
   - The weight of each rarity, for slots 1 to 8 and for the last 2 slots.
   - The ULTRA RARE chance.
   - How often an ULTRA RARE is the video card.
   - **Every pull**: put a Super Rare or an ULTRA RARE into every pull, which is handy for testing the animations.
4. Tap **Save**. The screen shows the resulting chance per card.

These settings are saved only on that computer. **Reset** puts the defaults back. To change the code, edit `TEST_CODE` in `content.py`.

## 4. Put it on GitHub

These photos show real people. Use a **private** repository unless everyone in them is fine with the photos being public.

1. On GitHub, click **New repository**, name it `starfall-pocket`, and don't add a README.
2. In the `starfall-pocket` folder, run each line:

   ```bash
   git init
   git add .
   git commit -m "Starfall Pocket"
   git branch -M main
   git remote add origin https://github.com/aeracero/starfall-pocket.git
   git push -u origin main
   ```

## 5. Turn it into an app

```bash
git tag v1.0.0
git push origin v1.0.0
```

After about 5 minutes, the Windows, Mac and Linux apps appear on the repository's **Releases** page.

- **Windows:** the first time, click **More info**, then **Run anyway**.
- **Mac:** the first time, right-click the app and choose **Open**.

To build only for your own computer, run `python build_app.py`; the result is in `dist/release`.

## 6. Connect Gmail

1. Turn on **2-Step Verification** for your Google account.
2. Create an App Password at https://myaccount.google.com/apppasswords.
3. In the game, tap the **gear** on the home screen (or the Gmail link on the sign-in screen).
4. Paste your address and the App Password, then tap **Save** and **Send test email**.

Gmail is required to play. If it isn't connected, the game opens this screen right after you log in, and **Save and play** continues once it's filled in.

## 7. Add or change cards

Cards live in `starfall_pocket/assets/cards/`. The file name sets the rarity:

| File name | Result |
| --- | --- |
| `Rare.png` | A Rare card |
| `Rare__Taro.png` (two underscores) | Another Rare card, called "Taro" |
| `Rare_kakuhen.png` or `Rare_確変.png` | The disguise card that shatters before Rare's ULTRA RARE version appears |

Use **PNG with a transparent background**, so a background can be added later (step 10). Two ways to make one:

- **On a Mac (easiest):** open the photo in Preview or Photos, right-click the person and choose **Copy Subject**. In Preview, choose **File > New from Clipboard**, then save it as PNG.
- **Automatically:** put your photos in a folder and run:

  ```bash
  python tools/make_cutouts.py my_photos starfall_pocket/assets/cards
  ```

  It downloads a background-removal model the first time, so it's slow once. It handles people well; thin props sometimes come out faded. `originals/` has the original photos if you want to redo a cutout.

Normal JPG photos also work; they just keep their background.

## 8. Change the ULTRA RARE card

Everything is in `ULTRA_CARDS` in `starfall_pocket/content.py`:

```python
ULTRA_CARDS = [
    {
        "id": "Ultra_Rare",
        "name": "ULTRA RARE",
        "image": "Ultra_Rare.png",
        "intro_sound": "ultra_start",
        "line": "Its me, PayPay",
        "line_sound": "ultra_start_2",
        "videos": ["Ultra_Rare1", "Ultra_Rare2"],
        "video_sound": False,
        "music": "battle",
        "tap_to_play": True,
        "crossfade": 0.4,
        "ability": "mirage",
    },
]
```

| Setting | What it does |
| --- | --- |
| `line` | The text shown with `line_sound` |
| `image` | The final card picture, in `assets/ultra/` |
| `videos` | Played in order; `crossfade` is the fade between them in seconds |
| `video_sound` | `True` plays the videos' own sound |
| `music` | The music file (in `assets/music/`) played with the videos |
| `tap_to_play` | `True` waits for a tap on the card before the videos start |

**To add a video**, convert your MP4 first (this also keeps its sound):

```bash
python tools/import_video.py my_clip.mp4 My_Clip
```

Then add `"My_Clip"` to `videos`.

**To add another special card,** copy the whole `{ ... }` block, give it a new `id`, and put its image in `assets/ultra/`.

**Other ULTRA settings** are in the `ULTRA` block:

- `chance`: 0.01 = 1%.
- `special_share`: how often a hit is a special card instead of a card's ULTRA version.

## 9. Sounds and music

**Sounds** go in `starfall_pocket/assets/sounds/` (`.mp3`, `.ogg` or `.wav`).

- Set each rarity's sound with `"sound"` in `RARITIES` (in `content.py`), using the file name without the extension.
- A list such as `["what_is_this_1", "what_is_this_2"]` picks one at random each time.

**Music** goes in `starfall_pocket/assets/music/`:

- `bgm.ogg` is the background music for every screen.
- `battle.ogg` plays with the ULTRA RARE videos.

Both are original tracks generated by `tools/make_music.py`. To use your own, replace the file with one of the same name, or point screens at other files with `MUSIC` in `content.py`. Music pauses during the ULTRA RARE videos. **Ctrl+M** (Cmd+M on Mac) mutes it.

## 10. Backgrounds

Put images in `starfall_pocket/assets/backgrounds/`:

| File name | Shows |
| --- | --- |
| `app.png` | Behind the whole app |
| `card.png` | Behind every card's cutout |
| `Rare.png` (or any rarity key) | Behind that rarity only |
| `ULTRA_RARE.png` | Behind ULTRA RARE cards |

## 11. Add animations

Animations are small Python files in `starfall_pocket/animations/`. `examples/my_animations.py` shows one of each kind.

| Kind | What it does | Set with |
| --- | --- | --- |
| `@card_effect` | Draws on the card every frame | `"animation"` |
| `@motion` | Moves the whole card | `"animation"` |
| `@reveal` | Plays when a card lands | `"reveal"` |

- The built-ins are in `starfall_pocket/animations/builtin.py`:
  - Card effects: `stars`, `shine`, `rainbow`
  - Motions: `float`, `wobble`
  - Reveals: `slam`, `slam_stars`, `slam_big`, `ultra`
- Combine several with `+`, like `"stars+shine"`.

A reveal example:

```python
from starfall_pocket.animations import reveal

@reveal("big_flash")
def big_flash(ctx):
    if ctx.first:
        ctx.flash(1.0)
        ctx.shake(0.5)
        ctx.burst(80, colors="rainbow", shape="star")
```

What `ctx` gives you:

| Name | Meaning |
| --- | --- |
| `ctx.first` | `True` only on the frame the card lands |
| `ctx.elapsed` | Seconds since it landed |
| `ctx.screen` | The game screen to draw on |
| `ctx.x`, `ctx.y`, `ctx.w`, `ctx.h` | The card's center and size |
| `ctx.burst(...)` | Throw particles (`shape="circle"`, `"star"` or `"confetti"`) |
| `ctx.flash(amount)`, `ctx.shake(amount)` | Screen flash and shake, from 0 to 1 |
| `ctx.play(name)` | Play a sound |

## 12. Publish an update

```bash
git add .
git commit -m "New cards"
git push
git tag v1.0.1
git push origin v1.0.1
```

## 13. Troubleshooting

| Problem | Fix |
| --- | --- |
| `command not found: python` | On a Mac, use `python3` for the first command, then activate `.venv` |
| pygame fails to install | You have an old copy of the project; this version uses pygame-ce, which supports Python 3.14 |
| A card doesn't appear | Check the file name and that it's in `assets/cards` |
| Gmail login fails | Use the 16-letter App Password, not your normal password |
| "Couldn't reach Gmail" or "Connection unexpectedly closed" | The network is blocking email sending (common on school or office Wi-Fi, and some VPNs or antivirus apps). Try a phone hotspot or home Wi-Fi |
