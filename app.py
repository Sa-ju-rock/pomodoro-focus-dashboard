"""Personal Pomodoro & Focus Dashboard.

A Streamlit web application providing a 25-minute Pomodoro countdown timer,
visual progress tracking, and ambient focus sounds (Rain, Café, Forest, White Noise).
"""

import time
import streamlit as st

# --- Pure Logic & Helper Functions (Unit Testable) ---

DEFAULT_POMODORO_SECONDS: int = 25 * 60  # 25 minutes = 1500 seconds

AMBIENT_SOUNDS: dict[str, dict[str, str | None]] = {
    "🌧️ Rain": {
        "url": "https://actions.google.com/sounds/v1/weather/rain_heavy.ogg",
        "description": "Gentle, steady rainfall to calm your mind and wash away distractions.",
        "type": "audio/ogg",
    },
    "☕ Café": {
        "url": "https://actions.google.com/sounds/v1/ambiences/coffee_shop.ogg",
        "description": "Warm coffee shop ambiance with gentle background chatter and espresso sounds.",
        "type": "audio/ogg",
    },
    "🌲 Forest": {
        "url": "https://actions.google.com/sounds/v1/ambiences/outdoor_summer_day_in_forest.ogg",
        "description": "Peaceful woodland atmosphere with soft breeze and cheerful birdsong.",
        "type": "audio/ogg",
    },
    "📻 White Noise": {
        "url": "https://actions.google.com/sounds/v1/ambiences/white_noise.ogg",
        "description": "Continuous soothing static frequencies for deep concentration.",
        "type": "audio/ogg",
    },
    "🔇 Silence (Mute)": {
        "url": None,
        "description": "Pure silence for deep, undistracted concentration.",
        "type": None,
    },
}


def format_time(seconds: int) -> str:
    """Format total seconds into MM:SS format string."""
    seconds = max(0, int(seconds))
    mins, secs = divmod(seconds, 60)
    return f"{mins:02d}:{secs:02d}"


def calculate_progress(remaining_seconds: int, total_seconds: int) -> float:
    """Calculate progress from 0.0 (start) to 1.0 (completed)."""
    if total_seconds <= 0:
        return 0.0
    elapsed = total_seconds - max(0, remaining_seconds)
    return min(1.0, max(0.0, elapsed / total_seconds))


def get_timer_status(remaining_seconds: int, is_running: bool) -> str:
    """Return current human-readable status for the timer."""
    if remaining_seconds <= 0:
        return "Session Complete! Take a break ☕"
    elif is_running:
        return "Focus Mode Active 🎯"
    else:
        return "Paused / Ready to Focus ⏳"


# --- Streamlit Dashboard UI ---

def init_session_state() -> None:
    """Initialize state variables for the timer and user session."""
    if "total_duration" not in st.session_state:
        st.session_state.total_duration = DEFAULT_POMODORO_SECONDS
    if "remaining_seconds" not in st.session_state:
        st.session_state.remaining_seconds = DEFAULT_POMODORO_SECONDS
    if "is_running" not in st.session_state:
        st.session_state.is_running = False
    if "sessions_completed" not in st.session_state:
        st.session_state.sessions_completed = 0


def render_ui() -> None:
    """Render the dashboard UI components."""
    st.set_page_config(
        page_title="Pomodoro & Focus Dashboard",
        page_icon="🍅",
        layout="centered",
    )

    init_session_state()

    # Custom styling
    st.markdown(
        """
        <style>
            .main-title {
                text-align: center;
                font-size: 2.3rem;
                font-weight: 700;
                margin-bottom: 0.2rem;
            }
            .subtitle {
                text-align: center;
                color: #888888;
                font-size: 1rem;
                margin-bottom: 1.5rem;
            }
            .timer-box {
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                border: 2px solid #334155;
                border-radius: 16px;
                padding: 2rem;
                text-align: center;
                margin-bottom: 1.5rem;
                box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            }
            .timer-digits {
                font-family: 'Courier New', Courier, monospace;
                font-size: 4.5rem;
                font-weight: bold;
                letter-spacing: 4px;
                color: #38bdf8;
                margin: 0.5rem 0;
            }
            .status-badge {
                display: inline-block;
                padding: 0.4rem 1rem;
                border-radius: 9999px;
                font-size: 0.95rem;
                font-weight: 600;
                background-color: #1e3a8a;
                color: #e0f2fe;
            }
            .sound-card {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 1rem;
                margin-top: 0.5rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<h1 class='main-title'>🍅 Personal Pomodoro & Focus Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Stay organized, eliminate distractions, and track deep work cycles.</p>", unsafe_allow_html=True)

    # Metrics row
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric(label="Sessions Completed", value=f"{st.session_state.sessions_completed} 🏆")
    with col_m2:
        total_focus_min = st.session_state.sessions_completed * 25
        st.metric(label="Total Deep Work", value=f"{total_focus_min} mins ⚡")

    # Current focus task input
    st.text_input("🎯 What are you focusing on right now?", placeholder="e.g., Implementing new feature / reading documentation", key="focus_task")

    st.write("---")

    # Timer Card
    time_str = format_time(st.session_state.remaining_seconds)
    status_text = get_timer_status(st.session_state.remaining_seconds, st.session_state.is_running)

    st.markdown(
        f"""
        <div class='timer-box'>
            <div class='status-badge'>{status_text}</div>
            <div class='timer-digits'>{time_str}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Progress bar
    progress_val = calculate_progress(st.session_state.remaining_seconds, st.session_state.total_duration)
    st.progress(progress_val)
    st.caption(f"Progress: {int(progress_val * 100)}% ({time_str} remaining of {format_time(st.session_state.total_duration)})")

    # Controls
    col_start, col_pause, col_reset = st.columns([1, 1, 1])

    with col_start:
        if st.button("▶️ Start", use_container_width=True, type="primary", disabled=st.session_state.is_running):
            if st.session_state.remaining_seconds <= 0:
                st.session_state.remaining_seconds = st.session_state.total_duration
            st.session_state.is_running = True
            st.rerun()

    with col_pause:
        if st.button("⏸️ Pause", use_container_width=True, disabled=not st.session_state.is_running):
            st.session_state.is_running = False
            st.rerun()

    with col_reset:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.is_running = False
            st.session_state.remaining_seconds = st.session_state.total_duration
            st.rerun()

    st.write("---")

    # Ambient Sound Section
    st.subheader("🎧 Focus Ambient Sound")
    sound_choice = st.selectbox(
        "Choose background atmosphere to boost immersion:",
        options=list(AMBIENT_SOUNDS.keys()),
        index=0,
    )

    sound_info = AMBIENT_SOUNDS[sound_choice]
    st.markdown(f"**Atmosphere Details:** *{sound_info['description']}*")

    if sound_info["url"]:
        st.audio(sound_info["url"], format=sound_info["type"], loop=True)
    else:
        st.info("Silence selected. Enjoy pure quiet focus.")

    # Timer countdown loop execution
    if st.session_state.is_running and st.session_state.remaining_seconds > 0:
        time.sleep(1)
        st.session_state.remaining_seconds -= 1
        if st.session_state.remaining_seconds <= 0:
            st.session_state.is_running = False
            st.session_state.sessions_completed += 1
            st.balloons()
            st.success("🎉 Pomodoro complete! Take a well-deserved 5-minute break.")
        st.rerun()


if __name__ == "__main__":
    render_ui()
