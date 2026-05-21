# summarizer.py
# ---------------------------------------------------------------
# FIXED AND SAFE AI SUMMARIZER
# ---------------------------------------------------------------

import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def summarize_transcript(transcript_text, meeting_name="Meeting"):
    """
    Takes a transcript, sends it to Groq API, and returns a fixed dictionary format.
    """
    try:
        # Initialize Groq client
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return {
                "success": False,
                "error": "GROQ_API_KEY missing from environment/secrets",
                "summary_text": "Error: API Key missing"
            }
            
        client = Groq(api_key=api_key)
        
        # System instructions for AI
        system_prompt = (
            "You are an expert project manager. Analyze the meeting transcript and provide a clean, "
            "structured summary with DECISIONS MADE and ACTION ITEMS. Use clear markdown bullet points."
        )
        
        # API Call using the correct current model
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Meeting: {meeting_name}\n\nTranscript:\n{transcript_text}"}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        # Extract the text
        ai_response_text = response.choices[0].message.content
        
        # EXACT FORMAT THAT APP.PY AND MAIN.PY EXPECTS
        return {
            "success": True,
            "summary_text": ai_response_text,
            "model_used": "llama-3.1-8b-instant",
            "estimated_cost": "$0.00 (Free Tier)"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "summary_text": f"Error during processing: {str(e)}"
        }