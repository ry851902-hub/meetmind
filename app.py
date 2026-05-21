# app.py
# ---------------------------------------------------------------
# FRONTEND / USER INTERFACE (UI) CODE
# ---------------------------------------------------------------

import streamlit as st
from main import process_meeting, get_briefing, get_meetings_list, get_memory_count

# Page Setup
st.set_page_config(
    page_title="MeetMind - AI Team Memory System",
    page_icon="🧠",
    layout="wide"
)

# Header
st.title("🧠 MeetMind Dashboard")
st.subheader("Your AI Team Memory System — Built Solo")
st.markdown("---")

# Sidebar for Stats
st.sidebar.header("Workspace Settings")
workspace_id = st.sidebar.text_input("Workspace ID", value="hackathon-team")

st.sidebar.markdown("---")
st.sidebar.header("System Status")
total_saved = get_memory_count()
st.sidebar.metric(label="Total Saved Memories", value=total_saved)
st.sidebar.success("Backend Connected! 🔥")

# Tabs
tab1, tab2 = st.tabs(["📝 Input New Meeting", "📊 View Team Briefing & Logs"])

# ---------------------------------------------------------------
# TAB 1: INPUT TRANSCRIPT
# ---------------------------------------------------------------
with tab1:
    st.header("Upload or Paste Meeting Transcript")
    st.write("Paste your meeting text here to let AI extract decisions and save them.")
    
    meeting_name = st.text_input("Meeting Title", value="Week 1 — Strategy Kickoff")
    transcript_text = st.text_area("Paste Transcript Text Here...", height=250)
    
    if st.button("✨ Process & Save to Memory", type="primary"):
        if not transcript_text.strip():
            st.error("Please enter a meeting transcript before processing.")
        else:
            with st.spinner("AI is thinking and remembering..."):
                result = process_meeting(transcript_text, meeting_name, workspace_id)
                
                if result["success"]:
                    st.success(f"🎉 Success! '{meeting_name}' saved to team memory.")
                    st.markdown("### 📋 AI Summary Extracted:")
                    st.markdown(result["summary"]["summary_text"])
                    st.rerun()
                else:
                    st.error("Something went wrong!")
                    st.code(result.get("error"))

# ---------------------------------------------------------------
# TAB 2: BRIEFING LOGS
# ---------------------------------------------------------------
with tab2:
    st.header(f"Workspace History: `{workspace_id}`")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🚀 Generate Cross-Session Briefing")
        st.write("This button merges all past meetings to show project progress and blockers.")
        
        upcoming_topic = st.text_input("Next Meeting Topic (Optional)", value="")
        
        if st.button("🔥 Generate Magic Briefing"):
            with st.spinner("Fetching memories and generating document..."):
                briefing_result = get_briefing(workspace_id, upcoming_topic)
                
                if briefing_result["success"]:
                    st.markdown("---")
                    st.markdown(briefing_result["briefing_text"])
                else:
                    st.error("Briefing failed. Check if you have added meetings first!")
                    st.code(briefing_result.get("error"))
                    
    with col2:
        st.subheader("🗄️ Saved Meeting Logs")
        past_meetings = get_meetings_list(workspace_id)
        
        if past_meetings:
            for mtg in past_meetings:
                st.info(f"📁 {mtg}")
        else:
            st.warning("No meetings saved in this workspace yet.")
