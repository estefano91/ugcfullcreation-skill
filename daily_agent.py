"""
las3x1.official — Daily autonomous generation agent
Calls Anthropic API with ugcfullcreation skill as system prompt.
Claude generates optimal prompts, executes generation, writes publish.py.

Usage:
  python3 daily_agent.py              # today's date
  python3 daily_agent.py 2026-05-01   # override date (testing)
"""
import sys
import os
import json
import subprocess
import traceback
from datetime import date as _date
from pathlib import Path

# ── Locate workspace.json ─────────────────────────────────────────────────────
SKILL_PATH = Path("/Users/asociaciondame/.claude/skills/ugcfullcreation/SKILL.md")

def find_workspace() -> Path:
    # 1. explicit arg: python3 daily_agent.py --workspace /path/to/workspace.json
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--workspace" and i < len(sys.argv):
            return Path(sys.argv[i + 1])
    # 2. workspace.json next to this script
    local = Path(__file__).parent / "workspace.json"
    if local.exists():
        return local
    # 3. fallback default
    default = Path("/Users/asociaciondame/ugcpanorama/workspace.json")
    if default.exists():
        return default
    print("ERROR: workspace.json not found. Run /ugcfullcreation setup first.")
    sys.exit(1)

WORKSPACE_PATH = find_workspace()
workspace      = json.loads(WORKSPACE_PATH.read_text())

BASE     = Path(workspace["root"])
ENV_PATH = BASE / workspace.get("env_file", ".env")
account  = workspace["accounts"][0]   # primary account

# ── Load env ──────────────────────────────────────────────────────────────────
env = dict(
    line.split("=", 1)
    for line in ENV_PATH.read_text().splitlines()
    if "=" in line and not line.startswith("#")
)

ANTHROPIC_API_KEY = env.get("ANTHROPIC_API_KEY", "")
if not ANTHROPIC_API_KEY:
    print("ERROR: ANTHROPIC_API_KEY not set in .env")
    sys.exit(1)

# ── Anthropic SDK ─────────────────────────────────────────────────────────────
try:
    import anthropic
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "anthropic", "-q"])
    import anthropic

# ── Calendar ──────────────────────────────────────────────────────────────────
today = next(
    (a for a in sys.argv[1:] if a != "--workspace" and not a.startswith("/")),
    str(_date.today())
)

CALENDAR_PATH = BASE / account["calendar_file"]
calendar      = json.loads(CALENDAR_PATH.read_text())
entry         = next((e for e in calendar["entries"] if e["date"] == today), None)

if not entry:
    upcoming = [e["date"] for e in calendar["entries"] if e["date"] > today][:5]
    print(f"\n  No entry for {today}. Next: {upcoming}\n")
    sys.exit(0)

# ── Load actor cards ──────────────────────────────────────────────────────────
actor_cards = {}
for actor_id in entry.get("actors", []):
    card_path = BASE / "actors" / actor_id / "actor_card.json"
    if card_path.exists():
        actor_cards[actor_id] = json.loads(card_path.read_text())

# ── Build system prompt from SKILL.md ────────────────────────────────────────
skill_content = SKILL_PATH.read_text()

SYSTEM_PROMPT = f"""You are executing Mode D of the ugcfullcreation skill — the autonomous calendar-driven generation mode.

{skill_content}

---

## WORKSPACE (loaded from workspace.json)

```json
{json.dumps(workspace, indent=2)}
```

Derived paths:
- ROOT:           {BASE}
- ACTORS_BASE:    {BASE}/actors/
- CAMPAIGNS_BASE: {BASE}/campaigns/
- ENV_FILE:       {ENV_PATH}
- CALENDAR:       {CALENDAR_PATH}
- ACCOUNT:        {account.get('instagram_handle')} ({account.get('id')})
- NICHE:          {account.get('niche')}
- LANGUAGE:       {account.get('language')}
- MONETIZATION:   {account.get('monetization')}
- CAPTION_VOICE:  {account.get('caption_voice')}
- BUDGET:         ${workspace['budget']['per_image_max_usd']}/img · ${workspace['budget']['per_video_max_usd']}/video · ${workspace['budget']['daily_max_usd']}/day max

---

## EXECUTION RULES

You are running HEADLESSLY from a cron job. NO user present. Make every decision autonomously:
- Apply SYSTEM 10 pre-flight checks and auto-fix any known-block patterns (log each substitution)
- Build optimal prompts using SYSTEM 4 (6-layer), SYSTEM 2 (all 10 realism anchors), SYSTEM 3 (camera profile)
- Route to the correct provider using SYSTEM 8 + SYSTEM 10 + budget constraints above
- Execute generation via the Bash tool (write generate.py to output folder, run it)
- Write publish.py and campaign.json
- Send push notification via osascript

Use these tools:
- **bash**: run any shell command (python3, ffmpeg, ffprobe, osascript, etc.)
- **read_file**: read any file from disk
- **write_file**: write content to any file path

Python generation scripts must start with:
  import sys
  sys.path.insert(0, "{BASE}")
  sys.path.insert(0, "/Users/asociaciondame/Library/Python/3.9/lib/python/site-packages")

Use /usr/local/bin/python3 to run them. Read FAL_KEY from {ENV_PATH} — never hardcode it.

IMPORTANT: PIL is broken on this machine — use ffmpeg/sips for image ops, never import PIL.
IMPORTANT: GPT Image 2 edit (fal.ai) outputs at ~576×1184 (~1:2 tall portrait) — NOT 4:5. ALWAYS crop every GPT image to 4:5 with ffmpeg before saving as -crop.png. Instagram feed rejects anything outside 0.75–1.91 ratio and will error on publish. Same rule applies to STATIC_POST and COLLAB_POST — not only CAROUSEL.
IMPORTANT: NBP fal.ai respects the aspect_ratio parameter — pass "4:5" and output is already correct. No crop needed.
IMPORTANT: Always write campaign.json on completion even if some slides failed.
IMPORTANT: Always write campaign.json on completion even if some slides failed.
IMPORTANT: Caption voice for this account: {account.get('caption_voice', 'casual and warm')}
IMPORTANT: Monetization CTA on CTA-type entries: use DM-based CTA matching the account's model.
"""

# ── User message ──────────────────────────────────────────────────────────────
USER_MESSAGE = f"""Execute Mode D from-calendar for date: {today}

Calendar entry:
{json.dumps(entry, indent=2)}

Actor cards loaded:
{json.dumps({k: {"consistency_anchor": v.get("consistency_anchor","")[:300], "prompt_seed": v.get("prompt_seed")} for k, v in actor_cards.items()}, indent=2)}

Proceed with full autonomous execution:
1. SYSTEM 10 pre-flight check on this entry
2. Build optimized prompts for each slide/shot
3. Write generate.py, execute it
4. Write publish.py and campaign.json
5. Send push notification
6. Print final summary
"""

# ── Tool definitions ──────────────────────────────────────────────────────────
tools = [
    {
        "name": "bash",
        "description": "Execute a bash shell command. Use for running Python scripts, ffmpeg, ffprobe, osascript, and any other shell operations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The bash command to execute"},
                "description": {"type": "string", "description": "Brief description of what this does"}
            },
            "required": ["command"]
        }
    },
    {
        "name": "read_file",
        "description": "Read a file from disk and return its contents.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Absolute path to the file"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file on disk (creates or overwrites).",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Absolute path to write"},
                "content": {"type": "string", "description": "Content to write"}
            },
            "required": ["path", "content"]
        }
    }
]


def execute_tool(name: str, inp: dict) -> str:
    try:
        if name == "bash":
            cmd = inp["command"]
            print(f"  [bash] {inp.get('description', cmd[:80])}")
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=600,
                env={**os.environ, "FAL_KEY": env.get("FAL_KEY", "")}
            )
            out = result.stdout
            if result.stderr:
                out += f"\n[stderr] {result.stderr[:500]}"
            print(f"  → {out[:300]}")
            return out or "(no output)"

        elif name == "read_file":
            path = inp["path"]
            return Path(path).read_text()

        elif name == "write_file":
            path = Path(inp["path"])
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(inp["content"])
            return f"Written {len(inp['content'])} chars to {path}"

        else:
            return f"Unknown tool: {name}"

    except subprocess.TimeoutExpired:
        return "ERROR: command timed out after 600s"
    except Exception as e:
        return f"ERROR: {traceback.format_exc()}"


# ── Agentic loop ──────────────────────────────────────────────────────────────
def run():
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    print(f"\n{'─'*62}")
    print(f"  las3x1 Daily Agent — {today}")
    print(f"  {entry['format']} / {entry.get('type','')} — {entry.get('concept','')}")
    print(f"{'─'*62}\n")

    messages = [{"role": "user", "content": USER_MESSAGE}]

    iteration = 0
    max_iterations = 40  # safety cap

    while iteration < max_iterations:
        iteration += 1

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=16000,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages
        )

        # Collect text output
        for block in response.content:
            if hasattr(block, "text"):
                print(block.text)

        # Append assistant turn
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            print(f"\n  ✓ Agent completed in {iteration} iteration(s).")
            break

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            messages.append({"role": "user", "content": tool_results})

        else:
            print(f"  Unexpected stop_reason: {response.stop_reason}")
            break

    else:
        print(f"  ⚠ Safety cap reached ({max_iterations} iterations).")


if __name__ == "__main__":
    run()
