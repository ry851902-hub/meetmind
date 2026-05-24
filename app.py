# app.py
# ---------------------------------------------------------------
# What this file does:
#   This is the Frontend / User Interface (UI). It uses Streamlit
#   to create a clean web dashboard that opens in your browser.
#
# Solo: This is the FIFTH and final file. Run it using:
#   streamlit run app.py
# ---------------------------------------------------------------

import streamlit as st
from main import process_meeting, get_briefing, get_meetings_list, get_memory_count

# Page Configuration (Sets the browser tab title and layout)
st.set_page_config(
    page_title="MeetMind - AI Team Memory System",
    page_icon="🧠",
    layout="wide"
)

# App Header
st.title("🧠 MeetMind")
st.subheader("Your AI Team Memory System — Cross-Session Intelligence")
st.markdown("---")

# Sidebar for Workspace and Quick Stats
st.sidebar.header("Workspace Settings")
workspace_id = st.sidebar.text_input("Enter Workspace ID", value="my-alpha-team", help="Change this to separate different projects or teams.")

st.sidebar.markdown("---")
st.sidebar.header("System Status")
total_saved = get_memory_count()
st.sidebar.metric(label="Total Cross-Session Memories", value=total_saved)
st.sidebar.success("Backend Connected via main.py")

# Create Two Tabs for the Dashboard
tab1, tab2 = st.tabs(["📝 Process New Meeting", "📊 Workspace Briefing & Logs"])

# ---------------------------------------------------------------
# TAB 1: PROCESS NEW MEETING
# ---------------------------------------------------------------
with tab1:
    st.header("Process a New Meeting Transcript")
    st.write("Paste your raw meeting text below to extract key takeaways and save them to team memory.")
    
    # Input Fields
    meeting_name = st.text_input("Meeting Title", value="Week 3 Mid-Sprint Check-in", placeholder="e.g., Week 1 Strategy Kickoff")
    transcript_text = st.text_area("Paste Raw Transcript here...", height=250, placeholder="Sarah: Let's start...\nJohn: I will handle the backend task...")
    
    if st.button("✨ Process & Remember", type="primary"):
        if not transcript_text.strip():
            st.error("Please paste a transcript before processing!")
        else:
            with st.spinner("AI is analyzing the transcript and committing key items to memory..."):
                # Call Function 1 from main.py
                result = process_meeting(transcript_text, meeting_name, workspace_id)
                
                if result["success"]:
                    st.success(f"🎉 Success! '{meeting_name}' has been processed and safely remembered.")
                    
                    # Display Stats
                    col1, col2 = st.columns(2)
                    col1.metric("Workspace Memories", result["total_memories"])
                    col2.metric("AI Model Used", result["model_used"])
                    
                    # Show the summary markdown directly in the UI
                    st.markdown("### 📋 Meeting Summary Extracted:")
                    st.markdown(result["summary"]["summary_text"])
                    
                    # Force a refresh of the total metric on next click
                    st.rerun()
                else:
                    st.error(f"❌ Failed during step: {result.get('step_failed')}")
                    st.code(result.get("error"))

# ---------------------------------------------------------------
# TAB 2: WORKSPACE BRIEFING & LOGS
# ---------------------------------------------------------------
with tab2:
    st.header(f"Workspace: `{workspace_id}`")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("🤖 Generate Cross-Session Briefing")
        st.write("This reads *all* past summaries for this workspace to find project changes, action items, and resolved decisions over time.")
        
        upcoming_topic = st.text_input("Next Meeting Focus (Optional)", placeholder="e.g., Discussing pricing or architecture blockages")
        
        if st.button("🚀 Generate Briefing", type="secondary"):
            with st.spinner("Reading past history and synthesizing document..."):
                # Call Function 2 from main.py
                briefing_result = get_briefing(workspace_id, upcoming_topic)
                
                if briefing_result["success"]:
                    st.markdown("---")
                    st.markdown(briefing_result["briefing_text"])
                    st.info(f"Generated using {briefing_result['memory_count']} past meetings.")
                else:
                    st.error("Could not generate briefing.")
                    st.code(briefing_result.get("error"))
                    
    with col_right:
        st.subheader("🗄️ Saved Meeting Logs")
        st.write("Meetings currently saved in this workspace:")
        
        # Call Function 3 from main.py
        past_meetings = get_meetings_list(workspace_id)
        
        if past_meetings:
            for idx, mtg in enumerate(past_meetings):
                with st.expander(f"📁 {mtg}"):
                    st.write("Memory compiled in database.")
        else:
            st.warning("No meetings found in this workspace yet. Go to Tab 1 to add some!")
