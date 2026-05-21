# briefing.py
# ---------------------------------------------------------------
# What this file does:
#   This is the WOW MOMENT of MeetMind.
#
#   It reads ALL past meeting memories (from memory.py),
#   sends them to the AI, and gets back a professional
#   briefing document that knows everything discussed before.
#
#   This is what makes judges say "oh wow" —
#   the Week 3 briefing automatically knows what happened
#   in Week 1 and Week 2 without you typing anything extra.
#
# Solo: this is the THIRD file you build.
#   Make sure both summarizer.py AND memory.py work first.
# ---------------------------------------------------------------

import os
from groq import Groq
from dotenv import load_dotenv
from memory import get_meeting_context   # reads memories from memory.py

# Load your secret API key from the .env file
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ---------------------------------------------------------------
# MAIN FUNCTION: generate_briefing
# ---------------------------------------------------------------
# What it does:
#   1. Reads all past meeting memories for your workspace
#   2. Sends them to the AI with a detailed prompt
#   3. Gets back a full professional briefing document
#   4. Returns the briefing as formatted text
#
# Inputs:
#   workspace_id           — e.g. "demo-team" (must match what
#                            you used when storing memories)
#   upcoming_meeting_topic — optional, e.g. "Q3 planning"
#                            leave it empty ("") if you don't have one
#
# Output: a dictionary with:
#   briefing_text   — the full briefing document as a string
#   memory_count    — how many past meetings were used
#   model_used      — which AI model generated this
#   success         — True or False
# ---------------------------------------------------------------

def generate_briefing(workspace_id, upcoming_meeting_topic=""):
    """
    Reads all past meeting memories and generates a professional
    briefing document using the AI.
    """

    # --- STEP 1: Get all past meeting context ---
    print(f"Reading memories for workspace: {workspace_id}...")
    past_context, memory_count = get_meeting_context(workspace_id)

    # If no memories exist yet, return a helpful message
    if memory_count == 0:
        return {
            "briefing_text": (
                "# No Meeting History Found\n\n"
                "There are no past meetings stored for this workspace yet.\n\n"
                "**What to do:**\n"
                "1. Go to the 'Process Meeting' page\n"
                "2. Paste a meeting transcript and click Process\n"
                "3. Do this for at least 2 meetings\n"
                "4. Then come back here to generate your briefing\n\n"
                "The magic happens when there are multiple meetings to remember!"
            ),
            "memory_count": 0,
            "model_used": "none",
            "success": False,
            "error": "No memories found"
        }

    # --- STEP 2: Build the prompt ---
    # This is what we send to the AI.
    # We give it all the past context and tell it exactly
    # what kind of document to produce.

    topic_line = ""
    if upcoming_meeting_topic:
        topic_line = f"The upcoming meeting topic is: {upcoming_meeting_topic}"
    else:
        topic_line = "Generate a general briefing for the next team meeting."

    prompt = f"""
You are an expert meeting facilitator and executive assistant.
You have been given the complete history of a team's past meetings.
Your job is to generate a professional pre-meeting briefing document.

{topic_line}

Here is everything discussed in all past meetings:

{past_context}

---

Generate a detailed, professional Meeting Briefing Document with these exact sections:

# Meeting Briefing Document

## Quick Summary
Write 2-3 sentences summarizing the overall project status and where the team stands right now.

## Decisions Already Made
List every decision that was confirmed in past meetings. For each one, mention WHO made it and WHEN (which meeting). These do not need to be discussed again.

## Still Unresolved — Needs Decision
List every open question, blocker, or topic that was raised but NOT resolved yet. These must be addressed in the next meeting. Mark anything that is urgent or blocking progress.

## Action Items Status
List every action item from past meetings. For each one say:
- What the task is
- Who owns it
- Whether it appears completed or still pending (based on whether it was mentioned again)

## Key People & Their Roles
List every person mentioned across all meetings and what they are responsible for.

## Recommended Agenda for Next Meeting
Based on what is unresolved and what is pending, suggest a specific agenda with time estimates. Example: "5 min — Legal approval update (Sarah)".

## Watch Out For
List 2-3 risks or things the team should be careful about based on the history of discussions.

---

Rules for writing this document:
- Be specific. Use real names, real numbers, real decisions from the transcripts.
- Do not make up anything that was not in the meeting history.
- Write in a professional but clear tone — not academic, not casual.
- Use markdown formatting (## headers, bullet points) for clean presentation.
- This document should feel like it was written by a senior chief of staff.
"""

    # --- STEP 3: Call the AI ---
    # We use a smarter model here because this is a complex task —
    # it needs to reason across multiple meetings and synthesize everything.
    model = "llama-3.3-70b-versatile"   # smarter model for complex cross-session reasoning

    try:
        print(f"Generating briefing using {model}...")
        print(f"Using context from {memory_count} past meeting(s)...")

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.2   # low = more focused and consistent output
        )

        briefing_text = response.choices[0].message.content.strip()

        # Add a footer showing how many memories powered this briefing
        footer = f"\n\n---\n*This briefing was generated from {memory_count} past meeting(s). Powered by MeetMind.*"
        briefing_text += footer

        print(f"✅ Briefing generated successfully!")

        return {
            "briefing_text": briefing_text,
            "memory_count": memory_count,
            "model_used": model,
            "task_type": "complex cross-session briefing",
            "estimated_cost": "$0.008",
            "success": True
        }

    except Exception as e:
        print(f"❌ Error generating briefing: {str(e)}")
        return {
            "briefing_text": f"Error generating briefing: {str(e)}\n\nCheck that your GROQ_API_KEY in .env is correct.",
            "memory_count": memory_count,
            "model_used": model,
            "success": False,
            "error": str(e)
        }


# ---------------------------------------------------------------
# TEST BLOCK
# ---------------------------------------------------------------
# Run this file directly to test it:
#   python briefing.py
#
# It will:
#   1. Save 2 fake memories using memory.py
#   2. Generate a briefing from those memories
#   3. Print the full briefing document
#
# If the briefing mentions Sarah's pricing decision from Week 1
# AND the legal blocker from Week 2 — it is working perfectly.
# ---------------------------------------------------------------

if __name__ == "__main__":
    print("Testing briefing.py...\n")
    print("=" * 60)

    # We need to save some test memories first
    # so the briefing has something to read
    from memory import store_meeting_memory, clear_memories

    TEST_WORKSPACE = "briefing-test-workspace"

    # Clean up old test data
    clear_memories(TEST_WORKSPACE)

    # Save Week 1 memory
    print("Setting up test data: saving Week 1 memory...")
    store_meeting_memory(
        summary_dict={
            "decisions": [
                "Pricing confirmed at $19 per user per month — John owns this",
                "Launch timeline set to 8 weeks — Sarah confirmed"
            ],
            "blockers": [
                "Legal has not approved Terms of Service — Sarah to follow up",
                "Analytics tool not decided — Mixpanel vs Amplitude still open"
            ],
            "action_items": [
                "John will finalize pricing page by Friday",
                "Sarah will email legal team by Wednesday",
                "Maria will prototype onboarding flow by next Tuesday"
            ],
            "people": ["Sarah", "John", "Maria"],
            "model_used": "llama-3.1-8b-instant",
            "estimated_cost": "$0.001"
        },
        meeting_name="Week 1 — Project Kickoff",
        workspace_id=TEST_WORKSPACE
    )

    # Save Week 2 memory
    print("Setting up test data: saving Week 2 memory...")
    store_meeting_memory(
        summary_dict={
            "decisions": [
                "Decided to go with Mixpanel for analytics — Marcus to close deal",
                "Beta launch pushed by 1 week due to legal delay"
            ],
            "blockers": [
                "Legal approval STILL pending — now blocking launch critical path",
                "Mixpanel API rate limits may be insufficient — Marcus negotiating"
            ],
            "action_items": [
                "Marcus to close Mixpanel deal by end of week",
                "Sarah to escalate legal to CEO if no response by Thursday",
                "Priya has 12 beta users ready — needs green light to reach out"
            ],
            "people": ["Sarah", "Marcus", "Priya"],
            "model_used": "llama-3.1-8b-instant",
            "estimated_cost": "$0.001"
        },
        meeting_name="Week 2 — Progress Review",
        workspace_id=TEST_WORKSPACE
    )

    print("\nTest data saved. Now generating briefing...\n")
    print("=" * 60)

    # Generate the briefing
    result = generate_briefing(
        workspace_id=TEST_WORKSPACE,
        upcoming_meeting_topic="Week 3 mid-sprint check-in"
    )

    if result["success"]:
        print("\n" + "=" * 60)
        print("GENERATED BRIEFING DOCUMENT:")
        print("=" * 60)
        print(result["briefing_text"])
        print("=" * 60)
        print(f"\nMemories used:  {result['memory_count']}")
        print(f"Model used:     {result['model_used']}")
        print(f"Estimated cost: {result['estimated_cost']}")
        print("\n✅ briefing.py is working!")
        print("\nCheck the briefing above.")
        print("It should mention Sarah's pricing decision from Week 1")
        print("AND the legal blocker that is still unresolved from Week 2.")
        print("If it does — the cross-session memory is working perfectly.")
        print("\nNext step: build main.py")
    else:
        print(f"\n❌ Briefing generation failed.")
        print(f"Error: {result.get('error')}")
        print("\nTROUBLESHOOTING:")
        print("1. Check your .env file has GROQ_API_KEY=your_key")
        print("2. Make sure memory.py is in the same folder")
        print("3. Try running: python memory.py first to confirm it works")

    # Clean up test data
    clear_memories(TEST_WORKSPACE)