"""
run_from_json.py — Mode B execution engine for /ugcfullcreation skill.
Reads a campaign.json and generates images (and optionally video) directly.

Usage:
    python3 run_from_json.py campaigns/luna-pool-kling_2026-04-23/campaign.json

Supports:
    - gpt-image-2-edit  → fal.ai openai/gpt-image-2/edit
    - kie-nano-banana-pro → kie.ai Nano Banana Pro
    - kling-o3 video    → fal.ai kling-video/o3/pro/image-to-video (2-step)
"""

import sys
import os
import json
import requests

sys.path.insert(0, "/Users/asociaciondame/ugcpanorama")

import fal_client
from kie_client import generate_image, save_image

FAL_KEY = "930975a9-c25c-497d-b0a1-01f27317680a:21d6ce06c9e934ab27fc427d4e4748e1"
KIE_KEY = "sk-k2FRdFRaEWBnlz0WJiLO_CxJcRPBiXf4KFo3Ah8r4-I"
os.environ["FAL_KEY"] = FAL_KEY


# ── helpers ─────────────────────────────────────────────────────────────────

def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


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
        vid_provider = campaign["provider"]["video"]["provider"]
        duration = int(campaign["provider"]["video"].get("duration", "5"))
        if vid_provider == "kling-o3":
            vid_cost = n_shots * (duration * 0.168)

    return img_cost + vid_cost


# ── generation backends ──────────────────────────────────────────────────────

def generate_gpt_image_2_edit(prompt: str, ref_urls: list, quality: str, seed: int) -> str:
    """Returns CDN URL of generated image."""
    result = fal_client.subscribe("openai/gpt-image-2/edit", arguments={
        "prompt": prompt,
        "image_urls": ref_urls,
        "quality": quality,
        "seed": seed,
    })
    return result["images"][0]["url"]


def generate_kie(prompt: str, ref_urls: list, aspect_ratio: str, seed: int) -> str:
    """Returns CDN URL of generated image."""
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
    """Uploads image to CDN, animates with Kling O3. Returns CDN URL of video."""
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


# ── main ─────────────────────────────────────────────────────────────────────

def run(json_path: str):
    campaign = load_json(json_path)
    campaign_id = campaign["campaign_id"]
    out_dir = os.path.join("/Users/asociaciondame/ugcpanorama/campaigns", campaign_id)
    ensure_dir(out_dir)

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

    generated_frames = []  # (shot_name, local_path)

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

        frame_path = os.path.join(out_dir, f"{name}.png")
        download(img_url, frame_path)
        print(f"    ✓ Frame saved → {frame_path}")

        generated_frames.append((name, frame_path, shot))

    # Video pass (2-step: frame already generated above)
    if has_video:
        print(f"\n── Animating {n} shot(s) with {vid_cfg.get('provider')} ──\n")
        vid_provider = vid_cfg.get("provider", "kling-o3")
        vid_duration = vid_cfg.get("duration", "5")
        vid_aspect = vid_cfg.get("aspect_ratio", "9:16")

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
            else:
                raise ValueError(f"Unknown video provider: {vid_provider}")

            vid_path = os.path.join(out_dir, f"{name}.mp4")
            download(vid_url, vid_path)
            print(f"    ✓ Video saved → {vid_path}")

    print(f"\n{'─'*60}")
    print(f"  Done — {campaign_id}")
    print(f"{'─'*60}\n")

    # List output files
    files = sorted(os.listdir(out_dir))
    for fname in files:
        print(f"  {fname}")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 run_from_json.py <path/to/campaign.json>")
        sys.exit(1)
    run(sys.argv[1])
