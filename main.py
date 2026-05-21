# main.py
# ---------------------------------------------------------------
# What this file does:
#   This is the CONNECTOR. It imports the 3 files you already
#   built and provides 2 simple functions that the UI (app.py)
#   will call.
#
# Solo: this is the FOURTH file. Build it after briefing.py works.
# ---------------------------------------------------------------

from summarizer import summarize_transcript
from memory import store_meeting_memory, get_all_meetings_list, get_total_memory_count
from briefing import generate_briefing


# ---------------------------------------------------------------
# FUNCTION 1: process_meeting
# ---------------------------------------------------------------
def process_meeting(transcript_text, meeting_name, workspace_id):
    """
    Full pipeline: transcript → AI summary → saved to memory.
    This is called when the user clicks 'Process & Remember'.
    """
    print(f"\n--- Processing meeting: {meeting_name} ---")

    # Step 1: Summarize the transcript using AI
    print("Step 1: Summarizing transcript...")
    summary = summarize_transcript(transcript_text, meeting_name)

    if not summary["success"]:
        return {
            "success": False,
            "error": summary.get("error", "Summarization failed"),
            "step_failed": "summarization"
        }

    print(f"  ✅ Summary done — model used: {summary['model_used']}")

    # Step 2: Save the summary into memory
    print("Step 2: Saving to memory...")
    memory_result = store_meeting_memory(summary, meeting_name, workspace_id)

    if not memory_result["success"]:
        return {
            "success": False,
            "error": memory_result.get("error", "Memory storage failed"),
            "step_failed": "memory storage",
            "summary": summary
        }

    print(f"  ✅ Memory saved — total memories: {memory_result['total_memories']}")

    # Step 3: Return everything to the UI
    return {
        "success": True,
        "meeting_name": meeting_name,
        "workspace_id": workspace_id,
        "summary": summary,
        "memory_id": memory_result["memory_id"],
        "total_memories": memory_result["total_memories"],
        "model_used": summary["model_used"],
        "estimated_cost": summary["estimated_cost"]
    }


# ---------------------------------------------------------------
# FUNCTION 2: get_briefing
# ---------------------------------------------------------------
def get_briefing(workspace_id, upcoming_meeting_topic=""):
    """
    Generates a cross-session briefing document from all past memories.
    This is called when the user clicks 'Generate Briefing'.
    """
    print(f"\n--- Generating briefing for workspace: {workspace_id} ---")
    result = generate_briefing(workspace_id, upcoming_meeting_topic)
    return result


# ---------------------------------------------------------------
# FUNCTION 3: get_meetings_list
# ---------------------------------------------------------------
def get_meetings_list(workspace_id):
    """Returns list of all meetings for this workspace."""
    return get_all_meetings_list(workspace_id)


# ---------------------------------------------------------------
# FUNCTION 4: get_memory_count
# ---------------------------------------------------------------
def get_memory_count():
    """Returns total memory count across all workspaces."""
    return get_total_memory_count()


# ---------------------------------------------------------------
# TEST BLOCK
# ---------------------------------------------------------------
if __name__ == "__main__":
    print("Testing main.py — full pipeline test\n")
    print("=" * 60)

    from memory import clear_memories
    TEST_WORKSPACE = "main-test-workspace"
    clear_memories(TEST_WORKSPACE)

    # --- Test transcript 1 ---
    transcript_1 = """
    Sarah: Let's get started. First item — pricing model.
    John: I recommend $19 per user per month based on competitor research.
    Sarah: Agreed. John you own the pricing page — get it done by Friday.
    John: Confirmed, Friday EOD.
    Maria: I finished the onboarding wireframes, ready for review next Tuesday.
    Sarah: Great. One blocker — legal still hasn't approved our terms of service.
    John: Who is following up?
    Sarah: I will email them today. If no reply by Wednesday we escalate.
    Maria: Also we haven't picked an analytics tool yet — Mixpanel or Amplitude?
    Sarah: Table that for next week. John add it to the agenda.
    """

    # --- Test transcript 2 ---
    transcript_2 = """
    Sarah: Quick update everyone. Marcus closed the Mixpanel deal yesterday.
    Marcus: Yes, API limits are fine. We are good to go with Mixpanel.
    Sarah: Great. Legal is still pending though — I escalated to the CEO this morning.
    Priya: I have 12 beta users ready and waiting. When can I reach out to them?
    Sarah: As soon as legal approves. Should be this week.
    Marcus: One concern — our staging server is slow. Might affect beta experience.
    Sarah: Marcus can you fix that before beta? By end of this week?
    Marcus: Yes I can do that.
    Priya: I will prepare the beta welcome email in the meantime.
    Sarah: Perfect. Legal is the only blocker now. Everything else is on track.
    """

    # Process both meetings
    print("PROCESSING MEETING 1...")
    result1 = process_meeting(transcript_1, "Week 1 — Project Kickoff", TEST_WORKSPACE)
    if result1["success"]:
        print(f"✅ Meeting 1 processed — {result1['total_memories']} memory saved\n")
    else:
        print(f"❌ Meeting 1 failed: {result1['error']}\n")

    print("PROCESSING MEETING 2...")
    result2 = process_meeting(transcript_2, "Week 2 — Progress Review", TEST_WORKSPACE)
    if result2["success"]:
        print(f"✅ Meeting 2 processed — {result2['total_memories']} memories saved\n")
    else:
        print(f"❌ Meeting 2 failed: {result2['error']}\n")

    # Generate briefing from both
    print("=" * 60)
    print("GENERATING BRIEFING FROM BOTH MEETINGS...")
    print("=" * 60)
    briefing = get_briefing(TEST_WORKSPACE, "Week 3 mid-sprint check-in")

    if briefing["success"]:
        print("\n" + briefing["briefing_text"])
        print("\n" + "=" * 60)
        print(f"✅ main.py is working perfectly!")
        print(f"Memories used:  {briefing['memory_count']}")
        print(f"Model used:     {briefing['model_used']}")
        print("\nAll 4 backend files are working. You are officially ready to build app.py!")
    else:
        print(f"❌ Briefing failed: {briefing.get('error')}")