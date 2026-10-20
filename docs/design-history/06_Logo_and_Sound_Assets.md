# 06 — Logo and Sound Assets

## A. Logo

### Two versions — DECIDED: current 2025 icon (README decision #2)
| | 2019–2025 "classic" (`assets/teams_logo_2019-2025.*`) | 2025–present (`assets/teams_logo_2025-present.*`) |
|---|---|---|
| Look | Big indigo rounded square with a large white **T**; two purple people to the right. | Two blue-violet people (heads + torsos); a small indigo **T** tile at the bottom-left. |
| Aspect (w:h) | 1.075 : 1 (viewBox 2228.8 × 2073.3) | 0.947 : 1 (viewBox 36 × 38) |
| Colors | Square gradient **#5A62C3 → #4D55BD → #3940AB**; big person **#7B83EB**; small person **#5059C9**; T **#FFFFFF**; subtle 10–20 % black shadow overlays. | Big person torso **#85C2FF → #7588FF → #6459FE**, head **#8282FF → #3923B1**; second person **#A98AFF → #8C75FF → #5F50E2 → #3C2CB8**, head **#6868F7 → #3923B1**; T tile **#688EFF → #230F94** (+ #8F8FFF highlight); T **#FFFFFF**. |
| Silhouette for the cut | Square + two round heads + two rounded torsos merging on the right. | Two heads + two rounded torsos + a small square at the bottom-left. |
| Decision | Not used (was my recommendation for street legibility). The SVG stays in `assets/` if it's ever wanted. | **Ben's choice — the icon everyone sees today.** The print template now carries only this version. |

The 2019 SVG's `T` glyph, for reference: a bar 500 units wide × 100 tall at the top of the square, stem 121 wide × 517 tall — i.e. the T occupies roughly the middle 44 % of the square's width and 54 % of its height (bar 500 × 100, stem 121 × 517 in SVG units; square 1140 × 1140).

### Print template — `assets/print_template.html`
Open in Safari/Chrome → the controls at the top are pre-set to Ben's measured pumpkin (logo **125 mm**, face **178 × 203 mm**, window scale 0.93, logo top 20 mm) → File › Print at **100 % / "Actual size"**, Letter, portrait. **Three pages, all needed:**
1. **INSERT — current logo, full color.** Print at **FedEx Office**: 2 copies on white cardstock (stack them) + 1 on plain paper for comparison. Save as PDF from the browser's print dialog; email it or bring it on a USB stick.
2. **WINDOW CUT TEMPLATE** — the silhouette in solid black at 93 %. Home B&W laser.
3. **FACE LAYOUT, full size** — the 178 × 203 mm usable face with the window *and* the 24 mm PIR hole in position, plus a centre line. Home B&W laser. Tape this one on the pumpkin and trace both cuts from it.
Every page has a **100 mm scale bar** — check it with a ruler on each printer before cutting anything ("fit to page" must be off, at home and at FedEx).

**Sizing — settled 2026-10-13.** Ben's pumpkin measures **178 × 203 mm (7 × 8 in)** of usable face, wider than the 125–150 mm I had assumed. Chosen logo width **125 mm** → logo 125 × 131.9 mm, leaving **26 mm clear each side** and 71 mm of vertical slack (20 mm above the logo, 51 mm below for the PIR). The window is cut at 93 % → 116.2 × 122.7 mm, so the printed logo overhangs the opening by **4.4 mm all round**: no white halo at the edge, and the tape job can be 4 mm off-centre without showing. Going bigger is possible (140 mm still leaves 19 mm each side) but 125 mm keeps a comfortable margin from the moulding seams and the curvature.

### Cutting note — the heads are islands
In the current icon the two round heads do not touch the torsos. The silhouette is **three separate holes**. At the chosen 125 mm width, cut at 93 %:

| Hole | Size in the window |
|---|---|
| Big head | Ø ≈ 38.8 mm |
| Small head | Ø ≈ 32.3 mm |
| Body (both torsos + T tile, overlapping) | ≈ 116 mm wide |
| Foam bridge, each head → body | **≈ 6.5 mm** |

Keep the bridges — they are what makes it read as "people" in daylight, and a hot-knife tip handles 6.5 mm fine. If one breaks, the print insert restores the shape; just widen the opening to join head and torso.

### Materials test (do this before the final cut)
Backlight three candidates with a flashlight through a sheet of white diffuser, in the dark, from 20 ft:
1. Inkjet transparency, **two copies stacked** (expected winner: saturated purples, crisp white T).
2. Inkjet vellum (softer, doubles as its own diffuser).
3. Plain paper (cheapest; washes out at high brightness, not weatherproof).
Print with the printer's "best/photo" quality. If the purple still looks pale at full flash, lower `NOTIFY_BRIGHTNESS` — a bright print at 50 % beats a washed-out one at 70 %.

### If the logo were done in neon (documented for completeness, not recommended)
Line-art version of the classic logo at 150 mm: rounded-square outline ≈ 4 × 110 mm sides (one continuous 4117 loop only if the corners are opened up to ≥40 mm radius); T bar ≈ 65 × 10 mm and stem ≈ 16 × 68 mm as two cut-and-soldered cold-white pieces; big head Ø 45 mm and small head Ø 31 mm cannot be bent from 5 × 12 mm flex — use purple nOOd loops or backlit dots; torsos need ≥40 mm corner radii. Needs a flatter/larger face than a 13" pumpkin offers.

### nOOd red + blue "purple"
Equal current → magenta (hue ≈ 300°); Teams indigo #5059C9 ≈ hue 235°. Approximate it with blue at 50 mA and red at ≈12 mA (e.g. 40 Ω and 160 Ω from 5 V), filaments touching, behind a diffuser. Reads as two lines up close. Not used.

### Trademark
Microsoft's mark. Personal, non-commercial decoration only. See `assets/NOTICE.md`.

---

## B. Sound

### What we have (2026-09-21)
`TeamsCallSound.mp3` (Ben-supplied): the Teams **incoming-call ringtone**, 12.1 s, stereo 44.1 kHz MP3, ripped from a video (container tags say DASH/ffmpeg). Two ring cycles at 0.4–3.6 s and 4.2–7.4 s, then 4.7 s of silence. Peaks at −10.2 dBFS (quiet).

Firmware-ready conversions (already in `assets/`, PCM 16-bit mono 22,050 Hz, peak −1 dBFS):
- `teams_call_1ring_22k_mono.wav` — 3.45 s, 152 KB (one ring cycle). **DECIDED — this is the v1 sound** (copied to `firmware/sounds/teams_call_1ring.wav`).
- `teams_call_2rings_22k_mono.wav` — 7.20 s, 318 KB (both rings).

Note the difference from the Slack build: Slack's gag used the ~1-second *message* chime. The ringtone is longer and arguably scarier ("someone is calling you"). The firmware plays a weighted list, so both can coexist once we have the chime.

### Getting the short "new message" chime (not planned for v1; kept for reference)
Ranked by cleanliness:
1. **Personal Mac, free Teams**: install *Microsoft Teams (free)* on this Mac, then run `find` for audio assets under `/Applications/Microsoft Teams.app` and `~/Library/Containers/com.microsoft.teams2*` — I can do this with you here. Personal device, no corporate policy questions.
2. **Work PC (Windows, new Teams)**: `C:\Program Files\WindowsApps\MSTeams_<version>\Audio\*.mp3`. Protected folder; needs admin/ownership. Copying a UI sound off a corporate laptop may trip DLP/policy — check before doing it.
3. **iPhone**: start an iOS Screen Recording (captures app audio), have someone send you a Teams message, stop; AirDrop the .mp4 to the Mac and trim with the commands below.
4. **Browser**: teams.microsoft.com in Chrome → DevTools › Network › Media filter → trigger the sound preview in Settings › Notifications; open the media URL and save it.

### Conversion commands (Mac; `ffmpeg` and `afconvert` are both installed here)
```bash
# 1) measure peak
ffmpeg -i in.mp3 -af volumedetect -f null - 2>&1 | grep max_volume
```
```bash
# 2) trim (start, duration), normalize to -1 dBFS (gain = -1 - max_volume), mono 22.05 kHz 16-bit, click-free edges
ffmpeg -y -i in.mp3 -ss 0.35 -t 3.45 -ac 1 -ar 22050 -sample_fmt s16 -af "volume=9.2dB,afade=t=in:d=0.005,afade=t=out:st=3.35:d=0.1" out.wav
```
```bash
# Apple-native alternative (no trim/normalize): 
afconvert -f WAVE -d LEI16@22050 -c 1 in.mp3 out.wav
```
```bash
# 3) verify
ffprobe -v error -show_entries stream=codec_name,sample_rate,channels,bits_per_sample:format=duration -of default=noprint_wrappers=1 out.wav
```

### Licensing
Microsoft assets; personal use only; keep them local; never push them to a public repo.
