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

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE          = Path("/Users/asociaciondame/ugcpanorama")
SKILL_PATH    = Path("/Users/asociaciondame/.claude/skills/ugcfullcreation/SKILL.md")
CALENDAR_PATH = BASE / "las3x1_calendar.json"
ENV_PATH      = BASE / ".env"
LOG_PATH      = BASE / "daily_agent.log"

# ── Load env ──────────────────────────────────────────────────────────────────
env = dict(
    line.split("=", 1)
    for line in ENV_PATH.read_text().splitlines()
    if "=" in line
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
today = sys.argv[1] if len(sys.argv) > 1 else str(_date.today())
calendar = json.loads(CALENDAR_PATH.read_text())
entry = next((e for e in calendar["entries"] if e["date"] == today), None)

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

## EXECUTION CONTEXT

You are running HEADLESSLY from a cron job. There is NO user present. Make every decision autonomously:
- Apply SYSTEM 10 pre-flight checks and auto-fix any known-block patterns
- Build optimal prompts using SYSTEM 4 (6-layer), SYSTEM 2 (all 10 realism anchors), SYSTEM 3 (camera profile)
- Route to the correct provider using SYSTEM 8 + SYSTEM 10
- Execute generation via the Bash tool (write generate.py, run it)
- Write publish.py and campaign.json
- Send push notification via osascript

Use these tools:
- **bash**: run any shell command (python3, ffmpeg, ffprobe, osascript, etc.)
- **read_file**: read any file from disk
- **write_file**: write content to any file path

Key paths:
- Campaigns output: /Users/asociaciondame/ugcpanorama/campaigns/
- Actors: /Users/asociaciondame/ugcpanorama/actors/
- FAL_KEY env var is already set in the shell — do not hardcode it, read from .env
- All Python scripts must add these to sys.path at the very top:
  sys.path.insert(0, "/Users/asociaciondame/ugcpanorama")
  sys.path.insert(0, "/Users/asociaciondame/Library/Python/3.9/lib/python/site-packages")
- Use /usr/local/bin/python3 for all generation scripts (fal_client works via sys.path injection above)

IMPORTANT: PIL is broken — use ffmpeg/sips for image operations. Never import PIL.
IMPORTANT: Always crop CAROUSEL images to 4:5 with ffmpeg after download. Never publish uncropped images.
IMPORTANT: Always write campaign.json on completion even if some slides failed.
IMPORTANT: Log every auto-fix (SYSTEM 10 substitution) in your output.
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
