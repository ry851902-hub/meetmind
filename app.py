import os
import time
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# =====================================================================
# 1. PAGE CONFIGURATION & SESSION STATE INITIALIZATION
# =====================================================================
st.set_page_config(
    page_title="MeetMind - AI Meeting Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize persistent session states so app doesn't reset on re-renders
if "transcription" not in st.session_state:
    st.session_state.transcription = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "action_items" not in st.session_state:
    st.session_state.action_items = []
if "processing" not in st.session_state:
    st.session_state.processing = False

# =====================================================================
# 2. SIDEBAR - CONFIGURATION & CREDENTIALS
# =====================================================================
with st.sidebar:
    st.title("⚙️ MeetMind Settings")
    st.markdown("Configure your AI credentials and preferences below.")
    
    # Secure API Key input
    api_key = st.text_input(
        "Enter Gemini API Key:", 
        type="password", 
        placeholder="AIzaSy...",
        help="Get your key from Google AI Studio. Left empty, it will check your local system environment variables."
    )
    
    # Model Selection Strategy
    model_choice = st.selectbox(
        "Select AI Engine Model:",
        options=["gemini-2.5-flash", "gemini-2.5-pro"],
        index=0,
        help="Use flash for fast, low-latency audio processing and pro for deep complex conceptual summaries."
    )
    
    st.divider()
    st.markdown("### 📋 Application Sections")
    st.info("💡 **Tip:** Upload clear meeting audio files (MP3/WAV) or paste pre-existing transcripts directly in the main panel.")

# Initialize the Gemini Client safely
def get_gemini_client(user_key):
    # Prioritize user input token, fallback to environment variable
    final_key = user_key if user_key else os.environ.get("GEMINI_API_KEY")
    if not final_key:
        return None
    return genai.Client(api_key=final_key)

client = get_gemini_client(api_key)

# =====================================================================
# 3. MAIN UI LAYOUT & FLOW
# =====================================================================
st.title("🧠 MeetMind: AI-Powered Meeting Intelligence")
st.caption("Streamline your engineering syncs, standups, and team documentation instantly.")

# Tab structure avoids vertical clutter and improves user cognitive load
tab_upload, tab_results, tab_qa = st.tabs(["📥 Source Input", "📝 Minutes & Actions", "💬 Ask Your Notes"])

# --- TAB 1: SOURCE INPUT & PROCESSING ---
with tab_upload:
    st.subheader("Provide Meeting Details")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload Meeting Audio (MP3, WAV, M4A) or Video", 
            type=["mp3", "wav", "m4a", "mp4"],
            help="Direct audio processing uses advanced multimodal inputs."
        )
        
    with col2:
        manual_transcript = st.text_area(
            "Or Paste Text Transcript Directly:",
            height=150,
            placeholder="Speaker 1: Let's discuss the solar drone hardware filters...\nSpeaker 2: Right, we need to finalize the passive airflow system..."
        )

    # Core Action Processing Trigger
    process_btn = st.button("🚀 Generate Meeting Intelligence", use_container_width=True)

    if process_btn:
        if not client:
            st.error("❌ API Authentication Failed. Please enter a valid API Key in the sidebar or check your server environment.")
        elif not uploaded_file and not manual_transcript.strip():
            st.warning("⚠️ Please provide a source! Either upload an audio/video file or paste a textual meeting script.")
        else:
            st.session_state.processing = True
            
            # Context-aware user prompt engineering for rich extraction
            prompt_template = """
            You are an elite, professional executive meeting assistant. Analyze the provided meeting data completely and output three distinct structural blocks:
            
            1. **EXECUTIVE SUMMARY**: A tight high-level narrative summary of what transpired.
            2. **DETAILED DISCUSSION POINTS**: Bulleted summaries of technical milestones, debates, and design pathways.
            3. **ACTION ITEMS**: A clear list of exact tasks explicitly mapped to individual assignees where possible, with priority flags.
            """
            
            try:
                with st.spinner("🧠 MeetMind is analyzing your meeting files... Please wait."):
                    # Case A: Handling Native Multimodal Audio File Uploads
                    if uploaded_file:
                        # Write out temporary byte buffer safely
                        bytes_data = uploaded_file.read()
                        
                        # Use Gemini's clean files API upload mechanics
                        # For extremely large files, use client.files.upload(file=...)
                        # Short/Medium files can be passed cleanly as inline bytes metadata depending on the structure
                        # To ensure absolute runtime reliability across web containers:
                        response = client.models.generate_content(
                            model=model_choice,
                            contents=[
                                types.Part.from_bytes(
                                    data=bytes_data,
                                    mime_type=uploaded_file.type,
                                ),
                                prompt_template
                            ]
                        )
                    # Case B: Standard Text Processing
                    else:
                        response = client.models.generate_content(
                            model=model_choice,
                            contents=[f"{prompt_template}\n\nMeeting Data Content:\n{manual_transcript}"]
                        )
                    
                    # Update global application state safely
                    st.session_state.summary = response.text
                    st.success("✅ Analysis Complete! Switch to the 'Minutes & Actions' tab to review.")
                    
            except APIError as e:
                st.error(f"API Error detected: {e.message}")
            except Exception as e:
                st.error(f"An unexpected runtime pipeline error occurred: {str(e)}")
            finally:
                st.session_state.processing = False

# --- TAB 2: MINUTES & ACTIONS (THE VISUAL RESULTS) ---
with tab_results:
    st.subheader("📋 Extracted Meeting Minutes")
    
    if not st.session_state.summary:
        st.info("Nothing generated yet. Submit your inputs in the 'Source Input' tab to initialize.")
    else:
        # Structured container presentation layer
        st.markdown(st.session_state.summary)
        
        st.divider()
        # Enable quick downloads for documentation management
        st.download_button(
            label="📥 Download Clean Minutes (.txt)",
            data=st.session_state.summary,
            file_name="meetmind_meeting_minutes.txt",
            mime="text/plain"
        )

# --- TAB 3: ASK YOUR NOTES (INTERACTIVE Q&A CHAT COMPONENT) ---
with tab_qa:
    st.subheader("💬 Interactive Context QA")
    st.write("Query specific decisions, edge cases, or ask follow-up questions directly to the meeting memory bank.")
    
    if not st.session_state.summary:
        st.warning("⚠️ Please process a meeting source first before initializing semantic search Q&A.")
    else:
        user_query = st.text_input("Ask a question about this meeting (e.g., 'What timeline did we agree on?'):")
        
        if user_query:
            if not client:
                st.error("API client not authenticated.")
            else:
                with st.spinner("🔍 Reviewing internal transcript structure..."):
                    qa_prompt = f"""
                    You are answering questions about a meeting based entirely on the following meeting summary data:
                    
                    {st.session_state.summary}
                    
                    User Question: {user_query}
                    
                    Provide an accurate, concise, factual response based strictly on the context provided above.
                    """
                    try:
                        qa_response = client.models.generate_content(
                            model=model_choice,
                            contents=qa_prompt
                        )
                        st.chat_message("assistant").write(qa_response.text)
                    except Exception as e:
                        st.error(f"Error resolving query: {e}")

# =====================================================================
# 4. FOOTER & COMPLIANCE BRANDING
# =====================================================================
st.divider()
st.caption("MeetMind Workspace v1.2 • Engineered for seamless productivity flow.")
