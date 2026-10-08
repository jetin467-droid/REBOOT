import streamlit as st
import pandas as pd
import math
from datetime import date, timedelta
from pathlib import Path

# ============================================================
# REBOOT — Your Personal Rhythm
# ============================================================

APP_NAME = "REBOOT"
VERSION = "1.0.0"
TAGLINE = "Your Personal Rhythm"
MOTIVATION = "Small steps. Better days. Reboot yourself."

ICON_PATH = Path("reboot_icon.png")

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------

st.set_page_config(
    page_title="REBOOT — Your Personal Rhythm",
    page_icon=str(ICON_PATH) if ICON_PATH.exists() else "🔄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------------------

st.markdown(
    """
    <style>

    /* Remove unnecessary Streamlit top spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
        margin: auto;
    }

    /* Prevent content from hiding behind Streamlit elements */
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Main background */
    .stApp {
        background: #f7f9fa;
    }

    /* REBOOT header */
    .reboot-header {
        text-align: center;
        padding: 15px 10px 25px 10px;
    }

    .reboot-logo {
        width: 76px;
        height: 76px;
        object-fit: contain;
        margin-bottom: 8px;
    }

    .reboot-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: 5px;
        margin: 0;
        color: #111820;
    }

    .reboot-tagline {
        font-size: 18px;
        color: #4b5b63;
        margin-top: 4px;
    }

    .reboot-motivation {
        font-size: 14px;
        color: #1aa7a1;
        margin-top: 10px;
        font-weight: 600;
    }

    /* Cards */
    .metric-card {
        background: white;
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 12px;
        border: 1px solid #e6ebed;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
        min-height: 125px;
    }

    .metric-name {
        font-size: 14px;
        color: #64727a;
        font-weight: 600;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 750;
        color: #18242b;
        margin-top: 8px;
    }

    .metric-status {
        font-size: 13px;
        margin-top: 5px;
        color: #1aa7a1;
    }

    .section-title {
        font-size: 25px;
        font-weight: 750;
        color: #18242b;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    .attention-card {
        background: #ffffff;
        border-left: 5px solid #20b7ae;
        border-radius: 14px;
        padding: 18px;
        margin: 10px 0 20px 0;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }

    .attention-title {
        font-weight: 750;
        font-size: 18px;
        color: #17242b;
    }

    .attention-text {
        margin-top: 6px;
        color: #59676e;
        line-height: 1.5;
    }

    .sync-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 20px;
        border: 1px solid #e4eaec;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }

    .sync-title {
        font-size: 21px;
        font-weight: 750;
        color: #18242b;
    }

    .sync-text {
        color: #637078;
        line-height: 1.5;
        margin-top: 7px;
    }

    .status-good {
        color: #139c86;
        font-weight: 650;
    }

    .status-fair {
        color: #9a7a16;
        font-weight: 650;
    }

    .status-attention {
        color: #b35d5d;
        font-weight: 650;
    }

    .footer {
        text-align: center;
        color: #7a878d;
        font-size: 12px;
        padding: 30px 0 10px 0;
    }

    /* Mobile */
    @media (max-width: 600px) {

        .block-container {
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .reboot-title {
            font-size: 32px;
            letter-spacing: 4px;
        }

        .reboot-tagline {
            font-size: 16px;
        }

        .reboot-logo {
            width: 64px;
            height: 64px;
        }

        .section-title {
            font-size: 22px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------

if "data" not in st.session_state:
    st.session_state.data = {
        "sleep": 7.0,
        "steps": 6000,
        "study": 2.0,
        "exercise": 30,
        "screen": 4.0,
        "mood": 4,
        "energy": 4
    }

if "history" not in st.session_state:
    st.session_state.history = {
        str(date.today() - timedelta(days=6)): 72,
        str(date.today() - timedelta(days=5)): 75,
        str(date.today() - timedelta(days=4)): 70,
        str(date.today() - timedelta(days=3)): 81,
        str(date.today() - timedelta(days=2)): 78,
        str(date.today() - timedelta(days=1)): 84,
        str(date.today()): 0
    }

# ------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------

def get_status(value, good_min, attention_max=None, reverse=False):
    if reverse:
        if value <= good_min:
            return "Good"
        elif attention_max is not None and value >= attention_max:
            return "Needs attention"
        return "Fair"

    if value >= good_min:
        return "Good"

    if attention_max is not None and value <= attention_max:
        return "Needs attention"

    return "Fair"


def calculate_score(data):
    # Sleep: 8 hours = full points
    sleep_score = min(data["sleep"] / 8, 1) * 20

    # Steps: 10000 = full points
    step_score = min(data["steps"] / 10000, 1) * 15

    # Study: 4 hours = full points
    study_score = min(data["study"] / 4, 1) * 15

    # Exercise: 60 minutes = full points
    exercise_score = min(data["exercise"] / 60, 1) * 15

    # Screen time: lower is better
    if data["screen"] <= 2:
        screen_score = 15
    elif data["screen"] <= 4:
        screen_score = 12
    elif data["screen"] <= 6:
        screen_score = 7
    else:
        screen_score = 3

    # Mood
    mood_score = (data["mood"] / 5) * 10

    # Energy
    energy_score = (data["energy"] / 5) * 10

    total = (
        sleep_score
        + step_score
        + study_score
        + exercise_score
        + screen_score
        + mood_score
        + energy_score
    )

    return max(0, min(100, round(total)))


def score_status(score):
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Fair"
    return "Needs attention"


def get_attention(data):
    issues = []

    if data["sleep"] < 7:
        issues.append(
            (
                "Sleep",
                "Your sleep was a little low today. Try giving yourself some extra time to rest tonight."
            )
        )

    if data["steps"] < 5000:
        issues.append(
            (
                "Steps",
                "Your activity was lower today. A short walk or some movement could help you stay active."
            )
        )

    if data["study"] < 1.5:
        issues.append(
            (
                "Study",
                "You could use a little more focused study time. Try one short distraction-free session."
            )
        )

    if data["exercise"] < 20:
        issues.append(
            (
                "Exercise",
                "Your activity was a little low today. Some simple movement could help."
            )
        )

    if data["screen"] > 6:
        issues.append(
            (
                "Screen Time",
                "Your screen time was a little high today. Try taking a few short screen-free breaks."
            )
        )

    if data["energy"] <= 2:
        issues.append(
            (
                "Energy",
                "Your energy seems a little low today. Give yourself some time to rest and recharge."
            )
        )

    if data["mood"] <= 2:
        issues.append(
            (
                "Mood",
                "Your mood seems lower today. Take some time for something relaxing or enjoyable."
            )
        )

    if issues:
        return issues[0]

    return (
        "You're doing well",
        "Your main daily areas are looking balanced. Keep building your routine with small consistent steps."
    )


def circular_score(score):
    radius = 82
    circumference = 2 * math.pi * radius
    progress = circumference * (score / 100)
    remaining = circumference - progress

    html = f"""
    <div style="
        display:flex;
        justify-content:center;
        align-items:center;
        width:100%;
        margin:5px 0 25px 0;
    ">
        <div style="
            position:relative;
            width:230px;
            height:230px;
        ">

            <svg width="230" height="230"
                 viewBox="0 0 230 230"
                 style="transform:rotate(-90deg);">

                <circle
                    cx="115"
                    cy="115"
                    r="{radius}"
                    fill="none"
                    stroke="#dfe5e7"
                    stroke-width="15"
                />

                <circle
                    cx="115"
                    cy="115"
                    r="{radius}"
                    fill="none"
                    stroke="#18b8b0"
                    stroke-width="15"
                    stroke-linecap="round"
                    stroke-dasharray="{progress} {remaining}"
                    style="
                        transition:stroke-dasharray 1.2s ease-out;
                    "
                />

            </svg>

            <div style="
                position:absolute;
                inset:0;
                display:flex;
                flex-direction:column;
                justify-content:center;
                align-items:center;
            ">
                <div style="
                    font-size:52px;
                    font-weight:800;
                    color:#18242b;
                    line-height:1;
                ">
                    {score}
                </div>

                <div style="
                    font-size:15px;
                    color:#718087;
                    margin-top:5px;
                ">
                    / 100
                </div>
            </div>

        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


def metric_card(name, value, status):
    status_class = "status-good"

    if status == "Fair":
        status_class = "status-fair"
    elif status == "Needs attention":
        status_class = "status-attention"

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-name">{name}</div>
            <div class="metric-value">{value}</div>
            <div class="{status_class}">{status}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------

logo_html = ""

if ICON_PATH.exists():
    logo_html = f"""
    <img src="data:image/png;base64,PLACEHOLDER"
         class="reboot-logo">
    """

# Streamlit image is more reliable than embedding manually.
st.markdown('<div class="reboot-header">', unsafe_allow_html=True)

if ICON_PATH.exists():
    st.image(str(ICON_PATH), width=76)

st.markdown(
    f"""
    <div class="reboot-title">{APP_NAME}</div>
    <div class="reboot-tagline">{TAGLINE}</div>
    <div class="reboot-motivation">{MOTIVATION}</div>
    """,
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# CURRENT DATA
# ------------------------------------------------------------

data = st.session_state.data

score = calculate_score(data)
st.session_state.history[str(date.today())] = score

# ------------------------------------------------------------
# NAVIGATION
# ------------------------------------------------------------

page = st.radio(
    "",
    ["HOME", "TODAY", "HEALTH", "PROGRESS"],
    horizontal=True,
    label_visibility="collapsed"
)

# ============================================================
# HOME
# ============================================================

if page == "HOME":

    st.markdown(
        '<div class="section-title">Your Reboot Score</div>',
        unsafe_allow_html=True
    )

    circular_score(score)

    st.markdown(
        f"""
        <div style="text-align:center;margin-top:-10px;margin-bottom:25px;">
            <div style="
                font-size:20px;
                font-weight:700;
                color:#18242b;
            ">
                {score_status(score)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    attention_title, attention_text = get_attention(data)

    st.markdown(
        f"""
        <div class="attention-card">
            <div class="attention-title">What needs attention?</div>
            <div style="
                margin-top:8px;
                font-size:16px;
                font-weight:700;
                color:#18a9a2;
            ">
                {attention_title}
            </div>
            <div class="attention-text">
                {attention_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Today\'s Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            "Sleep",
            f"{data['sleep']:.1f} h",
            get_status(data["sleep"], 7)
        )

    with col2:
        metric_card(
            "Steps",
            f"{data['steps']:,}",
            get_status(data["steps"], 7000)
        )

    with col3:
        metric_card(
            "Study",
            f"{data['study']:.1f} h",
            get_status(data["study"], 2)
        )

    with col4:
        metric_card(
            "Exercise",
            f"{data['exercise']} min",
            get_status(data["exercise"], 30)
        )

    col5, col6, col7 = st.columns(3)

    with col5:
        metric_card(
            "Screen Time",
            f"{data['screen']:.1f} h",
            get_status(
                data["screen"],
                2,
                6,
                reverse=True
            )
        )

    with col6:
        metric_card(
            "Mood",
            f"{data['mood']}/5",
            get_status(data["mood"], 4)
        )

    with col7:
        metric_card(
            "Energy",
            f"{data['energy']}/5",
            get_status(data["energy"], 4)
        )

# ============================================================
# TODAY
# ============================================================

elif page == "TODAY":

    st.markdown(
        '<div class="section-title">Quick Daily Check-In</div>',
        unsafe_allow_html=True
    )

    st.write("Update your values for today.")

    col1, col2 = st.columns(2)

    with col1:

        data["sleep"] = st.slider(
            "Sleep (hours)",
            min_value=0.0,
            max_value=14.0,
            value=float(data["sleep"]),
            step=0.5
        )

        data["steps"] = st.number_input(
            "Steps",
            min_value=0,
            max_value=50000,
            value=int(data["steps"]),
            step=500
        )

        data["study"] = st.slider(
            "Study / Focus (hours)",
            min_value=0.0,
            max_value=12.0,
            value=float(data["study"]),
            step=0.5
        )

        data["exercise"] = st.slider(
            "Exercise / Activity (minutes)",
            min_value=0,
            max_value=300,
            value=int(data["exercise"]),
            step=5
        )

    with col2:

        data["screen"] = st.slider(
            "Screen Time (hours)",
            min_value=0.0,
            max_value=16.0,
            value=float(data["screen"]),
            step=0.5
        )

        data["mood"] = st.slider(
            "Mood",
            min_value=1,
            max_value=5,
            value=int(data["mood"]),
            step=1
        )

        data["energy"] = st.slider(
            "Energy",
            min_value=1,
            max_value=5,
            value=int(data["energy"]),
            step=1
        )

    if st.button("Save Today's Check-In", use_container_width=True):
        new_score = calculate_score(data)
        st.session_state.history[str(date.today())] = new_score
        st.success("Today's check-in has been saved.")

# ============================================================
# HEALTH
# ============================================================

elif page == "HEALTH":

    st.markdown(
        '<div class="section-title">Health Data</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sync-card">
            <div class="sync-title">Sync Health Data</div>
            <div class="sync-text">
                REBOOT is ready for future automatic health-data integration.
                A normal Streamlit web app cannot directly access Android
                Health Connect data.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.button(
        "Sync Health Data",
        use_container_width=True
    ):
        st.info(
            "Automatic Health Connect syncing requires the future "
            "Android version of REBOOT. For now, use manual entry."
        )

    st.markdown(
        '<div class="section-title">Manual Health Data</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Until automatic syncing is available, you can enter your "
        "daily health and activity information manually."
    )

    col1, col2 = st.columns(2)

    with col1:

        data["sleep"] = st.number_input(
            "Sleep",
            min_value=0.0,
            max_value=14.0,
            value=float(data["sleep"]),
            step=0.5
        )

        data["steps"] = st.number_input(
            "Steps",
            min_value=0,
            max_value=50000,
            value=int(data["steps"]),
            step=500
        )

        data["exercise"] = st.number_input(
            "Exercise / Activity (minutes)",
            min_value=0,
            max_value=500,
            value=int(data["exercise"]),
            step=5
        )

    with col2:

        data["screen"] = st.number_input(
            "Screen Time (hours)",
            min_value=0.0,
            max_value=24.0,
            value=float(data["screen"]),
            step=0.5
        )

        data["study"] = st.number_input(
            "Study / Focus (hours)",
            min_value=0.0,
            max_value=16.0,
            value=float(data["study"]),
            step=0.5
        )

    if st.button(
        "Save Health Data",
        use_container_width=True
    ):
        st.session_state.history[str(date.today())] = calculate_score(data)
        st.success("Health data saved.")

# ============================================================
# PROGRESS
# ============================================================

elif page == "PROGRESS":

    st.markdown(
        '<div class="section-title">Weekly Progress</div>',
        unsafe_allow_html=True
    )

    history = st.session_state.history

    dates = list(history.keys())
    scores = list(his