# /ugcfullcreation — Full UGC Campaign Studio

A complete UGC production skill for [Claude Code](https://claude.ai/code). Takes you from zero to a fully-ready campaign folder with generation scripts, images, videos, and captions — engineered for maximum photorealism and scroll-stopping believability.

---

## Activation

```
/ugcfullcreation
```

---

## Formats

| Format | Aspect | Slides/Shots | Output |
|---|---|---|---|
| `STATIC_POST` | 4:5 | 1 | Single image + caption |
| `STORY` | 9:16 | 1 | Single image + caption |
| `COLLAB_POST` | 4:5 | 1 | Single image + caption + collab tag |
| `REEL` | 9:16 | 5–10 | Images → assembled video + caption |
| `STORY_VIDEO` | 9:16 | 2–8 | Images → assembled video + caption |
| `CAROUSEL` | 4:5 | 2–10 | Multi-slide images + caption |

---

## Wizard Steps

The skill runs an interactive wizard. Each step must be completed before moving to the next.

```
1.  FORMAT          → pick content type
2.  ACTOR           → select actor, loads identity + content profile
3.  CONCEPT         → optional trend research, lock the idea
4.  SCRIPT          → REEL/STORY_VIDEO only: hook + body beats + CTA
5.  ART DIRECTION   → location, time, outfit, mood, palette, camera style
6.  SHOTS           → shot cards: action, framing, camera, key moment
7.  PROMPTS         → full 6-layer prompts per shot
8.  GENERATE.PY     → dry-run → cost estimate → write script → execute
9.  REMOTION        → video formats only: render API payload
10. CAPTION         → hook + body + CTA + hashtag first comment
11. PUBLISH         → schedule, platform, notes
```

---

## Actor Roster

| actor_id | Description |
|---|---|
| `luna-21-caucasian-blonde` | Female, 21, Caucasian. Warm peachy skin, balayage blonde mid-back waves, warm brown eyes, freckle scatter, rosy flush. 1 ref. |
| `glacia-24-nordic-asian` | Female, 22–27, Finnish-born East Asian-Nordic mix. Glacial blue eyes, golden blonde waist-length hair, warm honey skin. 13 refs. |
| `mia-23-mediterranean` | Female, 23, Mediterranean. Warm olive skin, dark espresso wavy hair, dense freckles, bold dark brows. 1 ref. |
| `rowan-22-redhead` | Female, 22, very fair. Vivid copper-auburn waist-length hair, almond green-grey eyes, dense copper freckles. 1 ref. |
| `nova-22-caucasian-blonde` | Female, 22, Caucasian blonde. No refs — uses actor_card.json only. |

Multi-actor campaigns are supported — references are merged across actors.

---

## Internal Systems

### SYSTEM 2 — Realism Engine
10 anchors injected into every prompt: skin pores, loose hairs, under-eye texture, uneven skin tone, fabric drape, directional light, lens character, chromatic fringing, natural nail detail, jewelry gravity.

### SYSTEM 3 — iPhone Camera Profiles
Selfie front cam, rear cam, mirror selfie, overhead flatlay — exact technical specs injected into Layer 4.

### SYSTEM 4 — 6-Layer Prompt Architecture
Every image prompt is built in 6 layers:
1. **CHARACTER** — full identity anchor from actor_card.json
2. **SCENE** — location, time of day, light quality
3. **ACTION** — what the actor is doing, pose, expression
4. **CAMERA** — full camera profile from SYSTEM 9
5. **REALISM** — all 10 anchors from SYSTEM 2
6. **NEGATIVE** — explicit negatives to block AI artifacts

### SYSTEM 7 — Video Generation

**Face Consistency Rule — always 2-step:**
```
Step 0 — Dry-run (no refs, ~$0.02)      → verify prompt passes content filter
Step 1 — GPT Image 2 edit (~$0.07)      → generate face-locked frame
Step 2 — Kling O3 image-to-video (~$0.84) → animate that frame
```
Kling video-to-video/reference is reserved for scene/style transfers without a specific character.

### SYSTEM 8 — Model Routing

| Use case | Provider | Cost |
|---|---|---|
| Standard image (single actor, outdoor) | kie.ai Nano Banana Pro | ~$0.12/image |
| Complex scene / video frame anchor | GPT Image 2 edit (fal.ai) | ~$0.07/image |
| Video animation | Kling O3 Pro (fal.ai) | ~$0.168/s |

### SYSTEM 9 — 22 Camera Styles

**iPhone — Realistic / Candid**
| Code | Style |
|---|---|
| A | iPhone 15 Pro rear — default UGC, sharp, natural |
| B | iPhone 14 Pro rear — 48MP, slightly warmer |
| C | iPhone front selfie — Portrait Mode, arm-extended |
| D | Mirror selfie — phone visible in reflection |
| E | iPhone photo dump — mixed quality, casual |

**Film / Analog**
| Code | Style |
|---|---|
| F | 35mm Kodak Ultramax 400 — warm grain, slight orange cast |
| G | 35mm Fuji Superia 400 — cooler, green shadows, fine grain |
| H | Disposable camera — flash, harsh shadows, magenta, coarse grain |
| I | Polaroid — square format, washed colors, chemistry feel |
| J | Lomography LC-A — vignette, cross-process, saturated |

**Digital Cameras**
| Code | Style |
|---|---|
| K | Fujifilm X100VI — Classic Chrome film sim, SOOC JPEG |
| L | Sony A7 IV mirrorless — clinical sharp, full-frame |
| M | Canon 5D Mark IV — warm, creamy L-series bokeh |
| N | Y2K point & shoot — early 2000s digital, nostalgic |

**Aesthetic / Trend**
| Code | Style |
|---|---|
| O | Paparazzi / candid tele — compressed, slightly blurry, real |
| P | Night flash / party — harsh flash, dark background |
| Q | Golden hour editorial — warm cinematic, intentional |

**Vintage / Lo-fi / Authentic**
| Code | Style |
|---|---|
| R | Nokia N95 / early smartphone 2008–2011 — lo-res, blue-grey grain, found photo feel |
| S | Samsung Galaxy S3 era Android 2012–2014 — oversaturated, harsh auto-sharpening |
| T | 90s compact film (Olympus Stylus / Nikon L35) — soft, pastel grain, intimate |
| U | VSCO / Instagram 2013 era — faded, lifted blacks, warm midtones, tumblr |
| V | Super 8 / 8mm home movie — heavy grain, strong vignette, warm amber, organic |

---

## Content Policy Rules (GPT Image 2 + reference images)

### Dry-run before every generation
Before spending $0.07 on a ref-based generation, always run a cheap dry-run (~$0.02, no refs, low quality) to verify the prompt passes the content filter. A dry-run passing does **not** guarantee the edit mode (with refs) will pass — the ref-based filter is stricter.

### Known blocks (GPT Image 2 edit + refs)
- `"bikini"`, `"two-piece swimsuit"` — hard block regardless of phrasing
- `"crop top"` without a covering jacket — blocks
- `"leggings"` + suggestive pose (head back, eyes half-closed) — blocks
- `"sweat sheen on collarbone/chest"` — blocks
- `"damp clothing sticking to skin"` — blocks
- `"bodycon"` + `"club"` + `"flushed from dancing"` combined — blocks

### Known safe outfits
- Jeans (wide-leg, regular), linen skirt/shorts, denim mini skirt
- Athletic leggings + zip-up jacket (covered top required)
- Athletic jogger pants + long-sleeve top
- Tennis skirt + sleeveless polo
- Linen/cotton dresses, oversized shirts

### Pool / beach full body workaround
Do not mention `"swimsuit"`. Use `"cream linen pareo wrap tied at the hip over a white fitted crop top"` — same pool aesthetic, passes clean.

---

## Folder Structure

```
/campaigns/{actor}-{concept}_{YYYY-MM-DD}/
  generate.py       — generation script
  shot-deck.md      — all 6-layer prompts
  slide01-{name}.png
  slide02-{name}.png
  ...
  reel-{name}.mp4   — assembled video (if applicable)
  caption.txt
```

---

## Requirements

- [Claude Code](https://claude.ai/code)
- fal.ai API key (for GPT Image 2 + Kling O3)
- kie.ai API key (for Nano Banana Pro)
- Python 3.9+ with `fal_client`, `requests`
- Remotion (for video assembly) — optional

Set your keys:
```python
FAL_KEY = "YOUR_FAL_KEY_HERE"
KIE_KEY = "YOUR_KIE_KEY_HERE"
```

---

## Installation

Copy `SKILL.md` into your Claude Code skills folder:

```bash
mkdir -p ~/.claude/skills/ugcfullcreation
cp SKILL.md ~/.claude/skills/ugcfullcreation/SKILL.md
```

Then use `/ugcfullcreation` in any Claude Code session.
