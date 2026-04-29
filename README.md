# ugcfullcreation — AI UGC Production Studio

A Claude Code skill that turns you into a one-person content studio. You describe what you want, it generates the images and videos, writes the captions, and prepares everything for publishing to Instagram.

No design tools. No photographers. No agencies.

---

## What it can do

- Generate **photorealistic lifestyle and fashion images** of AI actors using reference photos
- Create **Instagram Reels** (animated 5-second clips) from a single generated frame
- Publish directly to Instagram through Zernio — no manual upload needed
- Run **every day automatically** at a time you choose, generating content from a calendar you set up once
- All of this without you writing a single prompt

---

## Who it's for

- Creators who want to run an AI model page on Instagram (lifestyle, fashion, aesthetics)
- Agencies managing multiple accounts and actors
- Anyone who wants to produce a month of content in an afternoon

---

## Setup — first time

When you run `/ugcfullcreation` for the first time, it detects that you haven't set up a workspace yet and walks you through 7 questions:

1. **Where is your project folder?** (the folder where your actors and content will live)
2. **What Instagram account are you publishing to?** (handle + your Zernio account ID)
3. **What kind of content?** Lifestyle, fashion, fitness, beauty, travel, product UGC — or describe your own
4. **What language and audience?** English/international, Spanish/LatAm, etc.
5. **What's your monetization?** Content packs via DM, affiliate, brand deals, subscription
6. **What's your budget per piece?** You decide how much per image and per video — the skill routes to the cheapest model that delivers the quality you need
7. **Do you want the daily agent?** It can generate content for you every morning and send you a notification to approve before it publishes

At the end it writes a `workspace.json` that remembers all of this. Every future run reads that file — you never answer these questions again.

---

## Your actors

An actor is a folder with a reference photo and an identity card. The skill reads the card to keep the face consistent across every image it generates.

You can have as many actors as you want. Examples of what an actor looks like:

- **Luna** — 21, blonde, warm peachy skin, round brown eyes, light freckles. Lifestyle and fashion content.
- **Mia** — 23, Mediterranean, dark wavy hair, golden olive skin, bold brows. Bold fashion and beauty.
- **Rowan** — 22, redhead, very fair skin, copper-auburn hair, green-grey eyes, freckle scatter. Editorial and autumn tones.

If you have a new actor, just give the skill a reference image. It extracts the identity card from the photo automatically.

---

## What you can ask it to do

### Create a carousel for your Instagram

You say `/ugcfullcreation` and answer a few questions — which actor, what concept, how many slides. It builds the full prompt, generates each slide, crops everything to the right ratio, and hands you a folder ready to publish.

**Example:**
> "6-slide carousel for Luna — outdoor terrace, golden hour, white linen outfit, mix of full body and close-up shots"

What you get: 6 cropped images + caption + hashtags + a one-command publish script.

---

### Make a Reel

You pick the actor and describe the vibe. The skill generates a base image first (to lock the face), then animates it into a 5-second clip.

**Examples:**

> "Mia — outdoor terrace, rust wrap dress, hair moving in the breeze, warm and magnetic energy"

> "Luna — POV text reel, outdoor, golden hour, text overlay: 'POV: you found her'"

> "Rowan — copper hair catching the backlight, very atmospheric, slow and dreamy"

What you get: a `.mp4` ready to post, plus the still frame it was built from.

---

### Use the same concept but with a different actor

You have a campaign that worked well for Luna — say it's an outdoor café session in a linen outfit. You want the exact same shoot but with Mia's face.

The skill swaps the identity anchor, keeps everything else identical (scene, outfit, camera style, lighting), and generates a new set. Same art direction, different face.

One concept × four actors = four times the content at a fraction of the work.

---

### Put your actor's face into any scene or prompt

You found a scene you like — a prompt from somewhere, a brief a client sent, a description you wrote. You drop the file and the skill reads it, flags any content risks before spending anything, asks which actor to use, and generates.

---

### Generate content for you every day without doing anything

You build a content calendar once — one row per day with format, actor, concept, and caption. The skill reads it every morning and generates that day's content automatically. You get a notification when it's ready, review it for 2 minutes, and run one command to publish.

**What a typical day looks like:**

- **07:33** — your Mac generates today's content in the background
- **08:00** — you get a desktop notification: *"6 images ready for Luna carousel. Publish at 09:00."*
- **08:45** — you open the folder and look at the images
- **09:00** — you run one command and it posts to Instagram

Total time: under 5 minutes a day.

---

## Formats

| Format | What it is | Best for |
|---|---|---|
| **Carousel** | 2–10 images, swipeable feed post | Storytelling, fashion sessions, product education |
| **Static Post** | Single image, feed | Strong hero shot, product reveal, editorial look |
| **Reel — Ambient** | 3–5s loop, environment moves | Golden hour, pool, café, outdoor lifestyle |
| **Reel — Portrait** | 3–5s close-up, one slow gesture | Beauty, skincare, magnetic eye contact |
| **Reel — POV** | 5–8s direct-to-camera | Aspirational lifestyle, "you found her" energy |
| **Reel — Text Reel** | 5–8s frame + bold text overlay | Viral "POV:" content, quotes, lifestyle statements |
| **Reel — Product** | 5–8s product interaction | Launches, unboxings, application moments |
| **Story** | Single vertical image | Stories, try-on moments, intimate lifestyle |
| **Collab Post** | Single image with brand element | Partnerships, affiliate content, gifting |

---

## Content quality

Every image is built with a 6-layer prompt system: character identity, scenario, environment, camera profile, realism details, and negative constraints. Each layer is filled automatically — you never see or touch the prompts unless you want to.

The skill also injects 10 realism anchors into every image: skin pores, stray hairs, natural under-eye texture, fabric drape, light imperfections, lens aberrations, jewelry following gravity. The goal is images that look like they were shot on a phone by a real person.

---

## Content policy

The skill knows which scene and outfit combinations will get blocked by each AI provider before it spends anything. It routes around known blocks automatically and logs what it changed.

If something does get blocked mid-generation, it retries with a safe alternative automatically — no wasted spend, no manual intervention needed.

---

## What it costs to use

These are AI generation costs paid directly to the providers. The skill itself is free.

| Content type | Approximate cost |
|---|---|
| 1 carousel slide (image) | $0.07 – $0.15 |
| Full 6-slide carousel | $0.40 – $0.70 |
| 1 Reel (frame + 5s video) | $0.90 – $1.00 |
| 1 month of daily content (24 posts) | $15 – $25 |

You set your budget in `workspace.json` and the skill stays within it when choosing which model to use.

---

## The autonomous daily agent

Once set up, a script runs every morning on your Mac at the time you chose. It reads your content calendar, calls Claude via the Anthropic API, gets back a full generation plan, executes it, crops everything to the right format, and sends you a push notification.

It runs whether Claude Code is open or not. Your Mac just needs to be on.

---

## Getting started

1. Install [Claude Code](https://claude.ai/code)
2. Download this skill into your Claude skills folder (`~/.claude/skills/ugcfullcreation/`)
3. Open Claude Code in your project folder
4. Type `/ugcfullcreation` — the setup wizard starts automatically
5. Follow the 7 setup questions
6. Add reference photos for your actors and start creating

---

## FAQ

**Do I need to write prompts?**
No. You describe the concept in plain language and the skill handles everything.

**How consistent is the face across slides?**
Very consistent. With 1 reference photo the face holds well across 5–6 slides. With more photos it holds even tighter.

**Can I use my own actors?**
Yes. Any person with at least one clear face photo can become an actor. The skill extracts the identity card from the photo automatically.

**What AI models does it use?**
It routes automatically based on your budget and the content type — GPT Image 2, Nano Banana Pro, Flux LoRA, or Ideogram v2 for images; Kling O3 or Seedance 2.0 for video. You don't need to know which model to pick.

**Can I run multiple Instagram accounts?**
Yes. `workspace.json` supports multiple accounts. The daily agent can be configured per account.

**Does it publish automatically?**
It prepares everything for publishing. By default you approve first, then run one command. Full auto-publish without approval is possible but off by default.

**Does it work if my computer is sleeping?**
No — the Mac needs to be on for the scheduled generation to run. It works fine with the lid closed as long as it's plugged in.
