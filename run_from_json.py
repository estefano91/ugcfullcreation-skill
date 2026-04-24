"""
run_from_json.py — execution engine for /ugcfullcreation skill.

Mode B — run as-is:
    python3 run_from_json.py campaigns/luna-pool/campaign.json

Mode C — swap actor, then run:
    python3 run_from_json.py campaigns/luna-pool/campaign.json --actor glacia-24-nordic-asian

Mode C saves a modified campaign.json to a new folder and names output files
as {original_shot_name}--{new_actor_short}.ext so the source JSON is always traceable.

Supports:
    - gpt-image-2-edit     → fal.ai openai/gpt-image-2/edit
    - kie-nano-banana-pro   → kie.ai Nano Banana Pro
    - kling-o3 video        → fal.ai kling-video/o3/pro/image-to-video (2-step)
    - seedance video        → fal.ai bytedance/seedance/v1/pro/image-to-video (2-step)
"""

import sys
import os
import json
import argparse
import requests
from datetime import date

sys.path.insert(0, "/Users/asociaciondame/ugcpanorama")

import fal_client
from kie_client import generate_image, save_image

FAL_KEY = "930975a9-c25c-497d-b0a1-01f27317680a:21d6ce06c9e934ab27fc427d4e4748e1"
KIE_KEY = "sk-k2FRdFRaEWBnlz0WJiLO_CxJcRPBiXf4KFo3Ah8r4-I"
os.environ["FAL_KEY"] = FAL_KEY

ACTORS_BASE = "/Users/asociaciondame/ugcpanorama/actors"
CAMPAIGNS_BASE = "/Users/asociaciondame/ugcpanorama/campaigns"


# ── helpers ──────────────────────────────────────────────────────────────────

def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(data: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def download(url: str, dest: str):
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    with open(dest, "wb") as f:
        f.write(r.content)


def cost_estimate(campaign: dict) -> float:
    provider = campaign["provider"]["image"]
    n_shots = len(campaign["shots"])
    has_video = "video" in campaign.get("provider", {})

    if provider == "gpt-image-2-edit":
        img_cost = n_shots * 0.07
    elif provider == "kie-nano-banana-pro":
        img_cost = n_shots * 0.12
    else:
        img_cost = n_shots * 0.07

    vid_cost = 0.0
    if has_video:
        vid_cfg = campaign["provider"]["video"]
        duration = int(vid_cfg.get("duration", "5"))
        vid_provider = vid_cfg.get("provider", "kling-o3")
        if vid_provider in ("kling-o3", "seedance"):
            vid_cost = n_shots * (duration * 0.168)

    return img_cost + vid_cost


# ── actor swap (Mode C) ───────────────────────────────────────────────────────

def find_refs(actor_id: str, max_refs: int = 2) -> list:
    """Returns up to max_refs absolute paths from hero_shots/ (fallback: references/)."""
    actor_dir = os.path.join(ACTORS_BASE, actor_id)
    hero_dir = os.path.join(actor_dir, "hero_shots")
    ref_dir = os.path.join(actor_dir, "references")

    # prefer hero_shots if non-empty
    for folder in (hero_dir, ref_dir):
        if not os.path.isdir(folder):
            continue
        files = sorted([
            f for f in os.listdir(folder)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ])
        if not files:
            continue
        # put reference-01 first if present
        if "reference-01.jpg" in files:
            files.remove("reference-01.jpg")
            files.insert(0, "reference-01.jpg")
        chosen = files[:max_refs]
        return [os.path.join(folder, f) for f in chosen]

    raise FileNotFoundError(f"No reference images found for actor '{actor_id}'")


def build_shared_context(actor_card: dict) -> str:
    anchor = actor_card["consistency_anchor"]
    return f"The woman in the reference images is in this scene: {anchor}"


def swap_actor(campaign: dict, new_actor_id: str) -> dict:
    """
    Returns a deep copy of campaign with actor identity swapped.
    Replaces: actor field, refs, shared_context, and the context prefix
    embedded in each shot's prompt.
    """
    import copy
    c = copy.deepcopy(campaign)

    actor_card_path = os.path.join(ACTORS_BASE, new_actor_id, "actor_card.json")
    if not os.path.exists(actor_card_path):
        raise FileNotFoundError(f"actor_card.json not found for '{new_actor_id}'")

    actor_card = load_json(actor_card_path)
    new_context = build_shared_context(actor_card)
    new_refs = find_refs(new_actor_id)

    old_context = c.get("shared_context", "")

    # Update top-level fields
    c["actor"] = new_actor_id
    c["shared_context"] = new_context
    c["refs"] = new_refs

    # Swap context prefix in every shot's prompt
    for shot in c["shots"]:
        prompt = shot.get("prompt", "")
        if old_context and prompt.startswith(old_context):
            shot["prompt"] = new_context + prompt[len(old_context):]
        # If prompt doesn't start with old_context, prepend new context anyway
        # (handles JSONs where context is not perfectly embedded)
        elif not prompt.startswith("The woman in the reference images"):
            shot["prompt"] = new_context + " " + prompt

    return c


def actor_short(actor_id: str) -> str:
    """'glacia-24-nordic-asian' → 'glacia'"""
    return actor_id.split("-")[0]


# ── generation backends ───────────────────────────────────────────────────────

def generate_gpt_image_2_edit(prompt: str, ref_urls: list, quality: str, seed: int) -> str:
    result = fal_client.subscribe("openai/gpt-image-2/edit", arguments={
        "prompt": prompt,
        "image_urls": ref_urls,
        "quality": quality,
        "seed": seed,
    })
    return result["images"][0]["url"]


def generate_kie(prompt: str, ref_urls: list, aspect_ratio: str, seed: int) -> str:
    result = generate_image(
        prompt=prompt,
        ref_urls=ref_urls,
        aspect_ratio=aspect_ratio,
        resolution="2K",
        seed=seed,
    )
    return result["images"][0]["url"]


def generate_kling_video(image_path: str, motion_prompt: str, negatives: str,
                          duration: str, aspect_ratio: str) -> str:
    print(f"    Uploading frame to CDN...")
    frame_cdn_url = fal_client.upload_file(image_path)
    print(f"    Submitting to Kling O3... (2-4 min)")
    result = fal_client.subscribe("fal-ai/kling-video/o3/pro/image-to-video", arguments={
        "prompt": motion_prompt,
        "negative_prompt": negatives,
        "image_url": frame_cdn_url,
        "duration": duration,
        "aspect_ratio": aspect_ratio,
    })
    return result["video"]["url"]


def generate_seedance_video(image_path: str, motion_prompt: str,
                             duration: str, aspect_ratio: str) -> str:
    print(f"    Uploading frame to CDN...")
    frame_cdn_url = fal_client.upload_file(image_path)
    print(f"    Submitting to Seedance... (2-4 min)")
    result = fal_client.subscribe("fal-ai/bytedance/seedance/v1/pro/image-to-video", arguments={
        "prompt": motion_prompt,
        "image_url": frame_cdn_url,
        "duration": duration,
        "resolution": "1080p",
        "aspect_ratio": aspect_ratio,
    })
    return result["video"]["url"]


# ── main ──────────────────────────────────────────────────────────────────────

def run(json_path: str, actor_override: str = None):
    campaign = load_json(json_path)
    today = date.today().isoformat()

    # ── Mode C: swap actor ──
    if actor_override:
        original_id = campaign["campaign_id"]
        new_short = actor_short(actor_override)

        print(f"\n  Swapping actor: {campaign['actor']} → {actor_override}")
        campaign = swap_actor(campaign, actor_override)

        # New campaign_id: {new_actor_short}-from-{original_id}
        new_campaign_id = f"{new_short}-from-{original_id}"
        campaign["campaign_id"] = new_campaign_id
        campaign["created"] = today

        # Save modified JSON to new campaign folder
        out_dir = os.path.join(CAMPAIGNS_BASE, new_campaign_id)
        ensure_dir(out_dir)
        save_json(campaign, os.path.join(out_dir, "campaign.json"))
        print(f"  ✓ Modified JSON → {out_dir}/campaign.json\n")

        # Output files will be named {original_shot_name}--{new_short}.ext
        file_suffix = f"--{new_short}"
    else:
        out_dir = os.path.join(CAMPAIGNS_BASE, campaign["campaign_id"])
        ensure_dir(out_dir)
        file_suffix = ""

    campaign_id = campaign["campaign_id"]
    provider_img = campaign["provider"]["image"]
    quality = campaign["provider"].get("quality", "medium")
    aspect_ratio = campaign["provider"].get("aspect_ratio", "4:5")
    refs = campaign["refs"]
    negatives = campaign.get("negatives", "")

    has_video = "video" in campaign.get("provider", {})
    vid_cfg = campaign["provider"].get("video", {})

    total = cost_estimate(campaign)
    n = len(campaign["shots"])

    print(f"\n{'─'*60}")
    print(f"  Campaign:  {campaign_id}")
    print(f"  Actor:     {campaign['actor']}")
    print(f"  Format:    {campaign['format']}")
    print(f"  Provider:  {provider_img}")
    if has_video:
        print(f"  Video:     {vid_cfg.get('provider')} {vid_cfg.get('duration')}s")
    print(f"  Shots:     {n}")
    print(f"  Est. cost: ~${total:.2f}")
    print(f"{'─'*60}\n")

    # Upload refs once
    print(f"── Uploading {len(refs)} reference image(s) ──")
    ref_urls = []
    for ref_path in refs:
        url = fal_client.upload_file(ref_path)
        ref_urls.append(url)
        print(f"  ✓ {os.path.basename(ref_path)}")

    print(f"\n── Generating {n} shot(s) ──\n")

    generated_frames = []

    for i, shot in enumerate(campaign["shots"], 1):
        name = shot["name"]
        seed = shot.get("seed", 42 + i)
        prompt = shot["prompt"]

        print(f"  [{i}/{n}] {name}")

        if provider_img == "gpt-image-2-edit":
            img_url = generate_gpt_image_2_edit(prompt, ref_urls, quality, seed)
        elif provider_img == "kie-nano-banana-pro":
            img_url = generate_kie(prompt, ref_urls, aspect_ratio, seed)
        else:
            raise ValueError(f"Unknown image provider: {provider_img}")

        out_name = f"{name}{file_suffix}.png"
        frame_path = os.path.join(out_dir, out_name)
        download(img_url, frame_path)
        print(f"    ✓ Saved → {frame_path}")

        generated_frames.append((name, frame_path, shot))

    # Video pass
    if has_video:
        vid_provider = vid_cfg.get("provider", "kling-o3")
        vid_duration = vid_cfg.get("duration", "5")
        vid_aspect = vid_cfg.get("aspect_ratio", "9:16")

        print(f"\n── Animating {n} shot(s) with {vid_provider} ──\n")

        for name, frame_path, shot in generated_frames:
            motion_prompt = shot.get("motion_prompt", "")
            if not motion_prompt:
                print(f"  ⚠ No motion_prompt for {name} — skipping video")
                continue

            print(f"  [{name}] Animating...")

            if vid_provider == "kling-o3":
                vid_url = generate_kling_video(
                    frame_path, motion_prompt, negatives, vid_duration, vid_aspect
                )
            elif vid_provider == "seedance":
                vid_url = generate_seedance_video(
                    frame_path, motion_prompt, vid_duration, vid_aspect
                )
            else:
                raise ValueError(f"Unknown video provider: {vid_provider}")

            out_name = f"{name}{file_suffix}.mp4"
            vid_path = os.path.join(out_dir, out_name)
            download(vid_url, vid_path)
            print(f"    ✓ Video saved → {vid_path}")

    print(f"\n{'─'*60}")
    print(f"  Done — {campaign_id}")
    print(f"{'─'*60}\n")

    files = sorted(os.listdir(out_dir))
    for fname in files:
        print(f"  {fname}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run campaign JSON generation. Add --actor to swap subject."
    )
    parser.add_argument("json_path", help="Path to campaign.json")
    parser.add_argument(
        "--actor",
        metavar="ACTOR_ID",
        help="Swap the actor (e.g. glacia-24-nordic-asian). "
             "Saves modified JSON to a new campaign folder.",
    )
    args = parser.parse_args()
    run(args.json_path, actor_override=args.actor)
