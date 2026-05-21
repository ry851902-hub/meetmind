# memory.py
# ---------------------------------------------------------------
# What this file does:
#   Saves meeting summaries to a file on your laptop called
#   demo_memories.json — and reads them back when needed.
#
#   Think of it like a notebook that never forgets.
#   Every meeting you process gets written into this notebook.
#   When you ask for a briefing, this notebook is read to find
#   everything that was discussed before.
#
# Ranjan/Solo: this is the SECOND file you build.
#   Make sure summarizer.py works before starting this one.
# ---------------------------------------------------------------

import os
import json
from datetime import datetime

# This is the file where all memories are saved on your laptop.
# It will be created automatically the first time you save a memory.
MEMORY_FILE = "demo_memories.json"


# ---------------------------------------------------------------
# FUNCTION 1: store_meeting_memory
# ---------------------------------------------------------------
# What it does: saves one meeting summary into the memory file
#
# Inputs:
#   summary_dict  — the dictionary returned by summarize_transcript()
#   meeting_name  — e.g. "Week 1 Strategy Meeting"
#   workspace_id  — a name for your team, e.g. "demo-team"
#                   (this lets you keep different teams separate)
#
# Output: a dictionary saying success: True or False
# ---------------------------------------------------------------

def store_meeting_memory(summary_dict, meeting_name, workspace_id):
    """
    Saves a meeting summary into demo_memories.json on your laptop.
    Creates the file if it doesn't exist yet.
    """

    # Step 1: Load whatever memories we already have saved
    existing_memories = _load_all_memories()

    # Step 2: Build the new memory entry we want to save
    new_memory = {
        "id": len(existing_memories) + 1,           # give it a unique number
        "meeting_name": meeting_name,
        "workspace_id": workspace_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "summary": {
            "decisions":    summary_dict.get("decisions", []),
            "blockers":     summary_dict.get("blockers", []),
            "action_items": summary_dict.get("action_items", []),
            "people":       summary_dict.get("people", [])
        },
        "model_used":       summary_dict.get("model_used", "unknown"),
        "estimated_cost":   summary_dict.get("estimated_cost", "$0")
    }

    # Step 3: Add the new memory to the list
    existing_memories.append(new_memory)

    # Step 4: Save the updated list back to the file
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(existing_memories, f, indent=2)

        print(f"✅ Memory saved! Total memories: {len(existing_memories)}")
        return {
            "success": True,
            "memory_id": new_memory["id"],
            "total_memories": len(existing_memories)
        }

    except Exception as e:
        print(f"❌ Failed to save memory: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


# ---------------------------------------------------------------
# FUNCTION 2: get_meeting_context
# ---------------------------------------------------------------
# What it does: reads all past meeting memories for a workspace
#               and returns them as one big block of text.
#
# Inputs:
#   workspace_id — must match what you used when storing memories
#
# Output:
#   context_text  — a long string with all past meeting info
#   memory_count  — how many memories were found (a number)
# ---------------------------------------------------------------

def get_meeting_context(workspace_id):
    """
    Reads all saved memories for this workspace and returns them
    as a single formatted text block for the AI to use.
    """

    all_memories = _load_all_memories()

    # Filter: only keep memories for this workspace
    relevant = [m for m in all_memories if m["workspace_id"] == workspace_id]

    if not relevant:
        return "No past meeting memories found for this workspace.", 0

    # Build a nicely formatted text block from all memories
    context_parts = []

    for memory in relevant:
        s = memory["summary"]

        # Format decisions as bullet points
        decisions_text = "\n".join(
            [f"  - {d}" for d in s["decisions"]]
        ) if s["decisions"] else "  - None recorded"

        blockers_text = "\n".join(
            [f"  - {b}" for b in s["blockers"]]
        ) if s["blockers"] else "  - None recorded"

        actions_text = "\n".join(
            [f"  - {a}" for a in s["action_items"]]
        ) if s["action_items"] else "  - None recorded"

        people_text = ", ".join(s["people"]) if s["people"] else "None recorded"

        part = f"""
=== {memory['meeting_name']} ===
Date: {memory['timestamp']}

DECISIONS MADE:
{decisions_text}

BLOCKERS & OPEN QUESTIONS:
{blockers_text}

ACTION ITEMS:
{actions_text}

PEOPLE INVOLVED: {people_text}
"""
        context_parts.append(part)

    # Join all memories into one big text block
    full_context = "\n\n---\n".join(context_parts)

    return full_context, len(relevant)


# ---------------------------------------------------------------
# FUNCTION 3: get_all_meetings_list
# ---------------------------------------------------------------
# What it does: returns a simple list of all meetings stored,
#               used by the Memory Log page in the UI.
#
# Input:  workspace_id (string)
# Output: list of meeting entries (each is a dictionary)
# ---------------------------------------------------------------

def get_all_meetings_list(workspace_id):
    """
    Returns a list of all meetings stored for this workspace.
    Used by the Memory Log page to show meeting history.
    """
    all_memories = _load_all_memories()
    relevant = [m for m in all_memories if m["workspace_id"] == workspace_id]
    return relevant


# ---------------------------------------------------------------
# FUNCTION 4: get_total_memory_count
# ---------------------------------------------------------------
# What it does: returns the total number of memories saved
#               across ALL workspaces (used for stats display)
# ---------------------------------------------------------------

def get_total_memory_count():
    """Returns total number of memories saved across all workspaces."""
    return len(_load_all_memories())


# ---------------------------------------------------------------
# HELPER: _load_all_memories  (private — only used inside this file)
# ---------------------------------------------------------------
# What it does: reads demo_memories.json from disk and returns
#               the list of memories inside it.
#               If the file doesn't exist yet, returns empty list.
# ---------------------------------------------------------------

def _load_all_memories():
    """
    Reads the memory file and returns its contents as a Python list.
    Returns an empty list if the file doesn't exist yet.
    The underscore at the start means: only use this inside memory.py.
    """
    if not os.path.exists(MEMORY_FILE):
        return []   # file doesn't exist yet — that's fine, return empty

    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception):
        # File exists but is corrupted or empty — start fresh
        return []


# ---------------------------------------------------------------
# BONUS: clear_memories  (useful for resetting your demo)
# ---------------------------------------------------------------

def clear_memories(workspace_id=None):
    """
    Clears memories. If workspace_id is given, only clears that
    workspace. If not given, clears ALL memories.
    Useful for resetting before a demo.
    """
    if workspace_id is None:
        # Clear everything
        if os.path.exists(MEMORY_FILE):
            os.remove(MEMORY_FILE)
        print("✅ All memories cleared.")
        return True
    else:
        # Clear only this workspace
        all_memories = _load_all_memories()
        kept = [m for m in all_memories if m["workspace_id"] != workspace_id]
        with open(MEMORY_FILE, "w") as f:
            json.dump(kept, f, indent=2)
        print(f"✅ Cleared memories for workspace: {workspace_id}")
        return True


# ---------------------------------------------------------------
# TEST BLOCK
# ---------------------------------------------------------------
# Run this file directly to test it:
#   python memory.py
#
# It will save 2 fake memories and then read them back.
# ---------------------------------------------------------------

if __name__ == "__main__":
    print("Testing memory.py...\n")

    TEST_WORKSPACE = "test-workspace-1"

    # Clean up any old test data first
    clear_memories(TEST_WORKSPACE)

    # --- TEST 1: Save a memory ---
    print("--- Test 1: Saving Week 1 memory ---")
    fake_summary_1 = {
        "decisions": [
            "Pricing set at $19 per user per month — owned by John",
            "Launch timeline confirmed as 8 weeks from today"
        ],
        "blockers": [
            "Legal has not approved the Terms of Service yet",
            "Analytics tool not decided — Mixpanel vs Amplitude still open"
        ],
        "action_items": [
            "John will finalize the pricing page by Friday",
            "Sarah will follow up with legal by Wednesday"
        ],
        "people": ["Sarah", "John", "Maria"],
        "model_used": "llama-3.1-8b-instant",
        "estimated_cost": "$0.001"
    }

    result1 = store_meeting_memory(fake_summary_1, "Week 1 Strategy Meeting", TEST_WORKSPACE)
    print(f"Result: {result1}\n")

    # --- TEST 2: Save a second memory ---
    print("--- Test 2: Saving Week 2 memory ---")
    fake_summary_2 = {
        "decisions": [
            "Decided to go with Mixpanel for analytics",
            "Marcus will negotiate API rate limits with Mixpanel by Friday"
        ],
        "blockers": [
            "Legal approval still pending — now on critical path",
            "Mixpanel API rate limits may be too low for our usage"
        ],
        "action_items": [
            "Marcus to close Mixpanel deal by end of week",
            "Sarah to escalate legal approval — blocking launch"
        ],
        "people": ["Sarah", "Marcus", "Priya"],
        "model_used": "llama-3.1-8b-instant",
        "estimated_cost": "$0.001"
    }

    result2 = store_meeting_memory(fake_summary_2, "Week 2 Progress Review", TEST_WORKSPACE)
    print(f"Result: {result2}\n")

    # --- TEST 3: Read memories back ---
    print("--- Test 3: Reading all memories back ---")
    context, count = get_meeting_context(TEST_WORKSPACE)
    print(f"Found {count} memories. Here is the context:\n")
    print(context)

    # --- TEST 4: Get meetings list ---
    print("\n--- Test 4: Meeting list ---")
    meetings = get_all_meetings_list(TEST_WORKSPACE)
    for m in meetings:
        print(f"  [{m['id']}] {m['meeting_name']} — {m['timestamp']}")

    print("\n✅ memory.py is working correctly!")
    print("You should see a file called demo_memories.json in your meetmind folder.")
    print("\nNext step: build briefing.py")

    # Clean up test data
    clear_memories(TEST_WORKSPACE)