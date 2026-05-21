# summarizer.py
# ---------------------------------------------------------------
# What this file does:
#   Takes a raw meeting transcript (text) and uses AI (Groq) to
#   extract the key information into a structured dictionary.
#
# This is the FIRST file. Test this before anything else.
# ---------------------------------------------------------------

import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load your secret key from the .env file
load_dotenv()

# Connect to Groq AI using your API key
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ---------------------------------------------------------------
# MAIN FUNCTION: summarize_transcript
# ---------------------------------------------------------------
# Input:
#   transcript_text  — the raw meeting transcript as a string
#   meeting_name     — e.g. "Week 1 Strategy Meeting"
#
# Output: a Python dictionary with these keys:
#   decisions, blockers, action_items, people,
#   model_used, task_type, estimated_cost, success
# ---------------------------------------------------------------

def summarize_transcript(transcript_text, meeting_name):
    """
    Takes a meeting transcript and returns a structured summary.
    Uses a fast cheap model for short transcripts,
    smarter model for long ones.
    """

    # Count words to decide which model to use
    word_count = len(transcript_text.split())

    if word_count < 500:
        model = "llama-3.1-8b-instant"      # fast and cheap
        task_type = "simple summarization"
        estimated_cost = "$0.001"
    else:
        model = "llama-3.3-70b-versatile"   # smarter for long transcripts
        task_type = "complex summarization"
        estimated_cost = "$0.005"

    # Build the prompt — tell the AI exactly what we want back
    prompt = f"""
You are a professional meeting analyst. Analyze this meeting transcript and extract key information.

Meeting Name: {meeting_name}

Transcript:
{transcript_text}

Return ONLY a valid JSON object with exactly these keys (no extra text, no markdown, no backticks):
{{
  "decisions": ["list every concrete decision made, be specific"],
  "blockers": ["list every problem, blocker, or unresolved question"],
  "action_items": ["list every task with owner name, e.g. John will do X by Friday"],
  "people": ["list every person's name mentioned in the transcript"]
}}

Rules:
- Only include information explicitly stated in the transcript
- Do not invent or infer anything not directly mentioned
- Each list item should be a complete sentence
- If nothing fits a category, use an empty list []
"""

    # Call the AI and handle any errors
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1000,
            temperature=0.1
        )

        # Get the text response
        raw_text = response.choices[0].message.content.strip()

        # Clean up in case AI added backticks or "json" prefix
        clean_text = raw_text.replace("```json", "").replace("```", "").strip()

        # Convert text to Python dictionary
        summary_dict = json.loads(clean_text)

        # Add extra info to the result
        summary_dict["meeting_name"]    = meeting_name
        summary_dict["model_used"]      = model
        summary_dict["task_type"]       = task_type
        summary_dict["estimated_cost"]  = estimated_cost
        summary_dict["word_count"]      = word_count
        summary_dict["success"]         = True

        return summary_dict

    except json.JSONDecodeError:
        # AI did not return clean JSON — return a safe fallback
        print(f"Warning: AI returned non-JSON. Raw text was: {raw_text}")
        return {
            "decisions":      ["Could not parse — check the transcript format"],
            "blockers":       [],
            "action_items":   [],
            "people":         [],
            "meeting_name":   meeting_name,
            "model_used":     model,
            "task_type":      task_type,
            "estimated_cost": estimated_cost,
            "word_count":     word_count,
            "success":        False,
            "error":          "JSON parse failed"
        }

    except Exception as e:
        # Something else went wrong — network, wrong API key, etc.
        print(f"Error calling Groq API: {str(e)}")
        return {
            "decisions":      [],
            "blockers":       [],
            "action_items":   [],
            "people":         [],
            "meeting_name":   meeting_name,
            "model_used":     model,
            "task_type":      task_type,
            "estimated_cost": "$0",
            "word_count":     word_count,
            "success":        False,
            "error":          str(e)
        }


# ---------------------------------------------------------------
# TEST BLOCK
# ---------------------------------------------------------------
# Run this file directly to test it:
#   python summarizer.py
#
# You should see decisions, blockers, action items printed out.
# ---------------------------------------------------------------

if __name__ == "__main__":
    print("Testing summarizer.py...\n")

    sample_transcript = """
    Sarah: Good morning everyone. Let's get started. First agenda item — pricing.
    John: I've done the market research. I recommend we go with $19 per user per month.
    Sarah: That sounds right. John, you'll own the pricing page and finalize by Friday?
    John: Yes, confirmed. I'll have it done by Friday EOD.
    Maria: I finished the onboarding wireframes. Ready for review.
    Sarah: Great work Maria. Can you present them next Tuesday?
    Maria: Sure, Tuesday works.
    Sarah: One blocker — legal hasn't approved our terms of service yet. We can't launch without that.
    John: Who's following up with legal?
    Sarah: I'll send them a reminder today. If we don't hear back by Wednesday, we escalate.
    Maria: Also — we haven't decided which analytics tool to use. Mixpanel vs Amplitude is still open.
    Sarah: Let's table that for next week. John, add it to next meeting's agenda.
    John: Done.
    """

    result = summarize_transcript(sample_transcript, "Week 1 Strategy Meeting")

    if result["success"]:
        print("✅ Summarizer working!\n")
        print(f"Model used:     {result['model_used']}")
        print(f"Task type:      {result['task_type']}")
        print(f"Estimated cost: {result['estimated_cost']}")
        print(f"Word count:     {result['word_count']}\n")

        print("DECISIONS:")
        for d in result["decisions"]:
            print(f"  • {d}")

        print("\nBLOCKERS:")
        for b in result["blockers"]:
            print(f"  • {b}")

        print("\nACTION ITEMS:")
        for a in result["action_items"]:
            print(f"  • {a}")

        print("\nPEOPLE MENTIONED:")
        for p in result["people"]:
            print(f"  • {p}")

        print("\nNext step: run memory.py")

    else:
        print("❌ Summarizer failed.")
        print(f"Error: {result.get('error', 'Unknown error')}")
        print("\nTROUBLESHOOTING:")
        print("1. Open .env file in Notepad and check GROQ_API_KEY=your_key is there")
        print("2. Make sure you ran: pip install groq python-dotenv")
        print("3. Go to groq.com and confirm your API key is correct")
