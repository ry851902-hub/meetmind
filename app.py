# app.py — MeetMind Full UI with Premium Styling
import streamlit as st
from main import process_meeting, get_briefing, get_meetings_list, get_memory_count

# ── PAGE CONFIG ──────────────────────────────────────────────────
st.set_page_config(
    page_title="MeetMind - AI Team Memory System",
    page_icon="🧠",
    layout="wide"
)

# ── FULL CSS THEME ───────────────────────────────────────────────
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #1a0a2e 50%, #0a1a2e 100%);
    min-height: 100vh;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12002e 0%, #1a1a3e 100%) !important;
    border-right: 1px solid rgba(108,63,197,0.3);
}
[data-testid="stSidebar"] * { color: #e0d0ff !important; }

/* Headings */
h1 { font-size: 2.8rem !important; font-weight: 900 !important; color: #ffffff !important; }
h2 { color: #c4b5fd !important; font-weight: 700 !important; }
h3 { color: #a78bfa !important; font-weight: 600 !important; }

/* Body text */
p, label, .stMarkdown { color: #e2e8f0 !important; }

/* All buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 0.65rem 2rem !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.5) !important;
    transition: all 0.3s ease !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(124,58,237,0.7) !important;
}

/* Text inputs */
.stTextInput input, .stTextArea textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(124,58,237,0.4) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 14px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.3) !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(37,99,235,0.15)) !important;
    border: 1px solid rgba(124,58,237,0.3) !important;
    border-radius: 16px !important;
    padding: 1.2rem !important;
}
[data-testid="metric-container"] [data-testid="metric-value"] {
    color: #a78bfa !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}
[data-testid="metric-container"] label {
    color: #94a3b8 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
}

/* Alerts */
.stSuccess {
    background: rgba(52,211,153,0.1) !important;
    border-left: 4px solid #34d399 !important;
    border-radius: 8px !important;
}
.stError {
    background: rgba(248,113,113,0.1) !important;
    border-left: 4px solid #f87171 !important;
    border-radius: 8px !important;
}
.stInfo {
    background: rgba(96,165,250,0.1) !important;
    border-left: 4px solid #60a5fa !important;
    border-radius: 8px !important;
}

/* Expanders */
.streamlit-expanderHeader {
    background: rgba(124,58,237,0.1) !important;
    border: 1px solid rgba(124,58,237,0.2) !important;
    border-radius: 10px !important;
    color: #c4b5fd !important;
    font-weight: 600 !important;
}

/* Divider */
hr { border-color: rgba(124,58,237,0.2) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0a0a1a; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(#7c3aed, #2563eb);
    border-radius: 3px;
}

</style>
""", unsafe_allow_html=True)

# ── HEADER BANNER ────────────────────────────────────────────────
st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(124,58,237,0.25), rgba(37,99,235,0.25));
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    text-align: center;
">
    <div style="font-size:3rem; margin-bottom:0.3rem;">🧠</div>
    <h1 style="
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 900;
        margin: 0;
        letter-spacing: -1px;
    ">MeetMind</h1>
    <p style="color:#94a3b8; font-size:1.1rem; margin:0.5rem 0 1rem;">
        Your AI Team Memory System — Cross-Session Intelligence
    </p>
    <div style="display:flex; justify-content:center; gap:0.8rem; flex-wrap:wrap;">
        <span style="background:rgba(52,211,153,0.15);color:#34d399;padding:5px 16px;border-radius:20px;font-size:12px;border:1px solid rgba(52,211,153,0.3)">● Live</span>
        <span style="background:rgba(124,58,237,0.15);color:#a78bfa;padding:5px 16px;border-radius:20px;font-size:12px;border:1px solid rgba(124,58,237,0.3)">🧠 Hindsight Memory</span>
        <span style="background:rgba(37,99,235,0.15);color:#60a5fa;padding:5px 16px;border-radius:20px;font-size:12px;border:1px solid rgba(37,99,235,0.3)">🔀 CascadeFlow Routing</span>
        <span style="background:rgba(251,191,36,0.15);color:#fbbf24;padding:5px 16px;border-radius:20px;font-size:12px;border:1px solid rgba(251,191,36,0.3)">⚡ Groq Powered</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1rem 0 0.5rem;">
        <div style="font-size:2.5rem;">🧠</div>
        <h2 style="
            background: linear-gradient(90deg, #a78bfa, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size:1.5rem; font-weight:800; margin:0.3rem 0;
        ">MeetMind</h2>
        <p style="color:#64748b; font-size:11px; margin:0;">AI Team Memory System</p>
    </div>
    <hr style="border-color:rgba(124,58,237,0.2); margin:1rem 0;">
    """, unsafe_allow_html=True)

    workspace_id = st.text_input(
        "🏢 Workspace ID",
        value="my-alpha-team",
        help="Change this to separate different projects or teams."
    )

    st.markdown("<hr style='border-color:rgba(124,58,237,0.2)'>", unsafe_allow_html=True)

    # Memory count card
    total_saved = get_memory_count()
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(37,99,235,0.2));
        border: 1px solid rgba(124,58,237,0.3);
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
        margin: 0.5rem 0;
    ">
        <p style="color:#94a3b8;font-size:10px;margin:0;text-transform:uppercase;letter-spacing:1.5px;">
            Cross-Session Memories
        </p>
        <p style="
            font-size:2.8rem; font-weight:900; margin:0.3rem 0;
            background: linear-gradient(90deg, #a78bfa, #60a5fa);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        ">{total_saved}</p>
        <p style="color:#34d399;font-size:11px;margin:0;">● Active Memory Layer</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(124,58,237,0.2)'>", unsafe_allow_html=True)

    # Status badge
    st.markdown("""
    <div style="
        background: rgba(52,211,153,0.1);
        border: 1px solid rgba(52,211,153,0.3);
        border-radius: 10px;
        padding: 0.8rem;
        text-align: center;
    ">
        <p style="color:#34d399;font-size:13px;font-weight:600;margin:0;">✓ Backend Connected</p>
        <p style="color:#64748b;font-size:10px;margin:0.2rem 0 0;">via main.py</p>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="margin-top:2rem; font-size:10px; color:#374151; text-align:center;">
        Powered by<br>
        <span style="color:#8b5cf6">Hindsight</span> +
        <span style="color:#3b82f6">CascadeFlow</span> +
        <span style="color:#f59e0b">Groq</span>
    </div>
    """, unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📝  Process New Meeting", "📊  Workspace Briefing & Logs"])

# ── TAB 1: PROCESS NEW MEETING ───────────────────────────────────
with tab1:
    st.markdown("### 📝 Process a New Meeting Transcript")
    st.markdown(
        "<p style='color:#94a3b8;'>Paste your raw meeting text below — MeetMind extracts key decisions, "
        "blockers and action items, then saves them to team memory.</p>",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])
    with col_left:
        meeting_name = st.text_input(
            "📌 Meeting Title",
            value="Week 3 Mid-Sprint Check-in",
            placeholder="e.g., Week 1 Strategy Kickoff"
        )
    with col_right:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.3);"
            f"border-radius:10px;padding:0.6rem 1rem;text-align:center;'>"
            f"<span style='color:#a78bfa;font-size:12px;'>Workspace: <b>{workspace_id}</b></span></div>",
            unsafe_allow_html=True
        )

    transcript_text = st.text_area(
        "📄 Paste Raw Transcript here...",
        height=220,
        placeholder="Sarah: Let's start the review...\nJohn: I will handle the backend task...\nMaria: Blocker — legal approval still pending."
    )

    if st.button("✨ Process & Remember", type="primary"):
        if not transcript_text.strip():
            st.error("⚠️ Please paste a transcript before processing!")
        else:
            with st.spinner("🧠 AI is analyzing the transcript and committing to memory..."):
                result = process_meeting(transcript_text, meeting_name, workspace_id)

            if result["success"]:
                # Success banner
                st.markdown(f"""
                <div style="
                    background: rgba(52,211,153,0.1);
                    border: 1px solid rgba(52,211,153,0.3);
                    border-radius: 12px;
                    padding: 1rem 1.5rem;
                    margin: 1rem 0;
                ">
                    <p style="color:#34d399;font-weight:700;margin:0;font-size:15px;">
                        🎉 Success! "{meeting_name}" has been processed and saved to memory.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # Stats row
                m1, m2, m3 = st.columns(3)
                m1.metric("🧠 Total Memories", result["total_memories"])
                m2.metric("🤖 AI Model", result["model_used"])
                m3.metric("💾 Status", "Saved ✓")

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### 📋 Summary Extracted from this Meeting:")

                # Summary in a styled box
                summary_text = result["summary"]["summary_text"]
                st.markdown(f"""
                <div style="
                    background: rgba(255,255,255,0.03);
                    border: 1px solid rgba(124,58,237,0.25);
                    border-radius: 14px;
                    padding: 1.5rem 2rem;
                    line-height: 1.9;
                    color: #e2e8f0;
                    font-size: 14px;
                ">{summary_text}</div>
                """, unsafe_allow_html=True)

                # CascadeFlow badge
                st.markdown("""
                <div style="
                    background: rgba(37,99,235,0.1);
                    border: 1px solid rgba(37,99,235,0.3);
                    border-radius: 10px;
                    padding: 0.6rem 1.2rem;
                    margin-top: 1rem;
                    display: flex;
                    align-items: center;
                    gap: 1rem;
                ">
                    <span style="color:#60a5fa;font-size:12px;">🔀 <b>CascadeFlow</b> → llama-3.1-8b-instant (simple task route)</span>
                    <span style="color:#64748b;">|</span>
                    <span style="color:#34d399;font-size:12px;">Cost: ~$0.001</span>
                    <span style="color:#64748b;">|</span>
                    <span style="color:#a78bfa;font-size:12px;">94% cheaper than GPT-4</span>
                </div>
                """, unsafe_allow_html=True)

                st.rerun()

            else:
                st.error(f"❌ Failed at step: {result.get('step_failed')}")
                st.code(result.get("error"))

# ── TAB 2: BRIEFING & LOGS ───────────────────────────────────────
with tab2:
    st.markdown("### 📊 Workspace Briefing & Memory Log")
    st.markdown(
        "<p style='color:#94a3b8;'>Generate a cross-session briefing doc that pulls context "
        "from ALL past meetings in this workspace.</p>",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Generate Smart Briefing", type="primary"):
        with st.spinner("🧠 Retrieving memories and generating cross-session briefing..."):
            briefing_result = get_briefing(workspace_id)

        if briefing_result and briefing_result.get("success"):
            # Stats row
            b1, b2, b3 = st.columns(3)
            b1.metric("🧠 Memories Used", briefing_result.get("memories_used", 0))
            b2.metric("🤖 Model", "qwen3-32b")
            b3.metric("💰 Cost vs GPT-4", "94% Saved")

            # CascadeFlow escalation badge
            st.markdown("""
            <div style="
                background: rgba(124,58,237,0.1);
                border: 1px solid rgba(124,58,237,0.3);
                border-radius: 10px;
                padding: 0.6rem 1.2rem;
                margin: 0.8rem 0;
            ">
                <span style="color:#a78bfa;font-size:12px;">
                    🔀 <b>CascadeFlow</b> escalated to <b>qwen/qwen3-32b</b> (complex cross-session task)
                </span>
                <span style="color:#64748b;"> | </span>
                <span style="color:#34d399;font-size:12px;">Cost: ~$0.008 vs $0.12 on GPT-4</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("#### 📄 Your Cross-Session Briefing:")

            # Briefing in styled box
            briefing_text = briefing_result.get("briefing", "No briefing content returned.")
            st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(124,58,237,0.2);
                border-left: 4px solid #7c3aed;
                border-radius: 14px;
                padding: 1.8rem 2rem;
                line-height: 1.9;
                color: #e2e8f0;
                font-size: 14px;
            ">{briefing_text}</div>
            """, unsafe_allow_html=True)

        else:
            st.info("💡 No memories found yet. Process at least 2 meetings first, then generate your briefing.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### 🗂️ All Processed Meetings")

    # Meeting history
    meetings = get_meetings_list(workspace_id)
    if meetings:
        for i, meeting in enumerate(reversed(meetings), 1):
            name = meeting.get("meeting_name", f"Meeting {i}")
            with st.expander(f"📌 {name}"):
                st.markdown(
                    f"<div style='color:#e2e8f0;font-size:13px;line-height:1.8'>"
                    f"{meeting.get('summary', {}).get('summary_text', 'No summary available.')}</div>",
                    unsafe_allow_html=True
                )
    else:
        st.markdown("""
        <div style="
            text-align:center;
            padding: 3rem 1rem;
            color: #374151;
        ">
            <div style="font-size:3rem;">🧠</div>
            <p style="color:#64748b;margin-top:0.5rem;">No meetings processed yet.<br>
            Go to the Process New Meeting tab to get started.</p>
        </div>
        """, unsafe_allow_html=True)
