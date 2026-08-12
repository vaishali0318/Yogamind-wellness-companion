"""
============================================================
YOGAMIND
Personalized Yoga & Mental Wellness Companion
============================================================

Features:
- User profile
- Wellness analysis
- Personalized 6-asana plan
- 30-asana library
- Yoga importance
- Breathing & mindfulness
- Performance analysis
- Session history
- Development graphs
- Date/time tracking

YOGAMIND is a wellness-support prototype.
It does not diagnose or treat medical conditions.
============================================================
"""

import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="YOGAMIND | Wellness Companion",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #050505;
        color: #F5F5F5;
    }

    section[data-testid="stSidebar"] {
        background: #0A0A0A;
        border-right: 1px solid #252525;
    }

    section[data-testid="stSidebar"] * {
        color: #E8E8E8 !important;
    }

    h1, h2, h3, h4 {
        color: #FFFFFF !important;
    }

    p, label {
        color: #CFCFCF !important;
    }

    .hero-box {
        background: linear-gradient(135deg, #111111, #080808);
        border: 1px solid #292929;
        border-radius: 22px;
        padding: 55px 45px;
        margin-bottom: 30px;
    }

    .hero-title {
        font-size: 55px;
        font-weight: 800;
        letter-spacing: 7px;
        color: #FFFFFF;
    }

    .hero-subtitle {
        font-size: 23px;
        color: #A7D8B5;
        margin-top: 8px;
        margin-bottom: 20px;
    }

    .hero-text {
        font-size: 17px;
        line-height: 1.8;
        max-width: 900px;
        color: #BDBDBD;
    }

    .section-title {
        font-size: 30px;
        font-weight: 700;
        color: #FFFFFF;
        margin-top: 25px;
        margin-bottom: 8px;
    }

    .section-subtitle {
        font-size: 16px;
        color: #A8A8A8;
        line-height: 1.7;
        margin-bottom: 20px;
    }

    .card-box {
        background: #101010;
        border: 1px solid #292929;
        border-radius: 16px;
        padding: 24px;
        margin: 15px 0;
    }

    .card-title {
        font-size: 21px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 10px;
    }

    .card-text {
        font-size: 15px;
        color: #BDBDBD;
        line-height: 1.7;
    }

    .info-box {
        background: #0D1510;
        border-left: 4px solid #78B88A;
        border-radius: 12px;
        padding: 22px;
        margin: 20px 0;
    }

    .info-title {
        font-size: 20px;
        font-weight: 700;
        color: #D8F1DE;
        margin-bottom: 8px;
    }

    .info-text {
        color: #B8C5BC;
        line-height: 1.7;
        font-size: 15px;
    }

    .asana-box {
        background: #0D0D0D;
        border: 1px solid #2B2B2B;
        border-radius: 17px;
        padding: 25px;
        margin: 18px 0;
    }

    .asana-number {
        color: #78B88A;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 7px;
    }

    .asana-name {
        font-size: 25px;
        font-weight: 700;
        color: #FFFFFF;
    }

    .asana-common {
        font-size: 15px;
        color: #9E9E9E;
        margin-top: 4px;
        margin-bottom: 18px;
    }

    .asana-heading {
        color: #9DD3AA;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-top: 15px;
        margin-bottom: 5px;
    }

    .asana-description {
        color: #C7C7C7;
        line-height: 1.7;
        font-size: 14px;
    }

    .sidebar-brand {
        text-align: center;
        padding: 15px 5px 25px 5px;
    }

    .sidebar-logo {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 4px;
        color: #FFFFFF;
    }

    .sidebar-caption {
        color: #8FAF98;
        font-size: 12px;
        margin-top: 6px;
    }

    .stButton > button {
        background: #78B88A;
        color: #071009;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        min-height: 45px;
    }

    .stButton > button:hover {
        background: #91C99F;
        color: #050505;
    }

    div[data-testid="stMetric"] {
        background: #101010;
        border: 1px solid #292929;
        padding: 18px;
        border-radius: 14px;
    }

    div[data-testid="stMetricValue"] {
        color: #FFFFFF;
    }

    div[data-testid="stMetricLabel"] {
        color: #9D9D9D;
    }

    hr {
        border-color: #292929;
    }

    .footer {
        text-align: center;
        color: #666666;
        font-size: 12px;
        padding: 40px 10px 15px 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "user_name": "",
    "user_age": 18,
    "analysis_done": False,
    "wellness_score": 0,
    "wellness_status": "",
    "stress": 5,
    "energy": 5,
    "mood": 5,
    "sleep": 5,
    "activity": 5,
    "plan_count": 0
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HISTORY FILE
# ============================================================

HISTORY_FILE = "yogamind_history.json"


def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except:

        return []


def save_history(history):

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4
        )


# ============================================================
# ASANA DATABASE
# ============================================================

ASANAS = [

    {
        "name": "Tādāsana",
        "common": "Mountain Pose",
        "benefits": "Encourages upright posture, balance and body awareness.",
        "steps": [
            "Stand comfortably with feet close together.",
            "Keep your spine tall and shoulders relaxed.",
            "Distribute your weight evenly across both feet.",
            "Breathe slowly and hold comfortably."
        ]
    },

    {
        "name": "Vṛkṣāsana",
        "common": "Tree Pose",
        "benefits": "Supports balance, concentration and steady body control.",
        "steps": [
            "Stand upright with feet together.",
            "Shift your weight onto one leg.",
            "Place the other foot against the inner leg at a comfortable height.",
            "Bring your hands together and breathe steadily."
        ]
    },

    {
        "name": "Trikoṇāsana",
        "common": "Triangle Pose",
        "benefits": "Encourages gentle stretching and body alignment awareness.",
        "steps": [
            "Stand with your feet comfortably wide.",
            "Turn one foot outward.",
            "Extend your arms sideways.",
            "Lean gently toward the extended leg."
        ]
    },

    {
        "name": "Vīrabhadrāsana I",
        "common": "Warrior I",
        "benefits": "Supports controlled lower-body movement and body awareness.",
        "steps": [
            "Stand with your feet apart.",
            "Step one foot forward.",
            "Bend the front knee gently.",
            "Raise your arms while keeping your torso upright."
        ]
    },

    {
        "name": "Vīrabhadrāsana II",
        "common": "Warrior II",
        "benefits": "Supports balance, controlled movement and lower-body engagement.",
        "steps": [
            "Stand with your feet wide apart.",
            "Turn one foot outward.",
            "Bend the front knee comfortably.",
            "Extend both arms sideways."
        ]
    },

    {
        "name": "Utkatāsana",
        "common": "Chair Pose",
        "benefits": "Supports controlled leg and core engagement.",
        "steps": [
            "Stand upright.",
            "Bend your knees slightly.",
            "Move your hips backward.",
            "Raise your arms while keeping your back comfortable."
        ]
    },

    {
        "name": "Adho Mukha Śvānāsana",
        "common": "Downward-Facing Dog",
        "benefits": "Provides a full-body stretch and coordinated movement.",
        "steps": [
            "Begin on your hands and knees.",
            "Place your hands firmly on the floor.",
            "Lift your hips upward.",
            "Keep your spine long and breathe comfortably."
        ]
    },

    {
        "name": "Bhujangāsana",
        "common": "Cobra Pose",
        "benefits": "Encourages gentle front-body opening and spinal mobility.",
        "steps": [
            "Lie on your stomach.",
            "Place your palms beside your chest.",
            "Gently lift your chest.",
            "Keep your shoulders relaxed."
        ]
    },

    {
        "name": "Balāsana",
        "common": "Child's Pose",
        "benefits": "Provides a gentle resting position and encourages relaxation.",
        "steps": [
            "Kneel comfortably.",
            "Lower your hips toward your heels.",
            "Fold your upper body forward.",
            "Rest your arms comfortably."
        ]
    },

    {
        "name": "Makarāsana",
        "common": "Crocodile Pose",
        "benefits": "Encourages physical relaxation and comfortable breathing.",
        "steps": [
            "Lie comfortably on your stomach.",
            "Place your arms in front of you.",
            "Rest your head comfortably.",
            "Relax your shoulders."
        ]
    },

    {
        "name": "Śavāsana",
        "common": "Corpse Pose",
        "benefits": "Encourages relaxation, stillness and mindful breathing.",
        "steps": [
            "Lie comfortably on your back.",
            "Relax your arms and legs.",
            "Close your eyes if comfortable.",
            "Observe your natural breathing."
        ]
    },

    {
        "name": "Sukhāsana",
        "common": "Easy Pose",
        "benefits": "Supports comfortable seated breathing and mindfulness.",
        "steps": [
            "Sit comfortably with legs crossed.",
            "Keep your spine naturally upright.",
            "Rest your hands on your knees.",
            "Breathe slowly."
        ]
    },

    {
        "name": "Vajrāsana",
        "common": "Thunderbolt Pose",
        "benefits": "Provides a stable seated position for breathing and mindfulness.",
        "steps": [
            "Kneel comfortably.",
            "Sit back toward your heels.",
            "Keep your spine upright.",
            "Rest your hands on your thighs."
        ]
    },

    {
        "name": "Paścimottānāsana",
        "common": "Seated Forward Bend",
        "benefits": "Encourages a gentle stretch along the back of the body.",
        "steps": [
            "Sit with your legs extended.",
            "Keep your spine comfortably long.",
            "Reach toward your legs.",
            "Fold only as far as comfortable."
        ]
    },

    {
        "name": "Setu Bandhāsana",
        "common": "Bridge Pose",
        "benefits": "Supports controlled movement of the hips, legs and back.",
        "steps": [
            "Lie on your back with knees bent.",
            "Keep your feet on the floor.",
            "Press gently through your feet.",
            "Lift your hips slowly."
        ]
    },

    {
        "name": "Marjaryāsana",
        "common": "Cat Pose",
        "benefits": "Encourages spinal mobility and coordinated breathing.",
        "steps": [
            "Start on your hands and knees.",
            "Keep your hands below your shoulders.",
            "Round your spine gently.",
            "Move slowly with your breathing."
        ]
    },

    {
        "name": "Bitilāsana",
        "common": "Cow Pose",
        "benefits": "Encourages gentle spinal movement and body awareness.",
        "steps": [
            "Start on your hands and knees.",
            "Keep your spine neutral.",
            "Gently open your chest.",
            "Move slowly without forcing."
        ]
    },

    {
        "name": "Anjaneyāsana",
        "common": "Low Lunge",
        "benefits": "Provides a gentle stretch through the hips and legs.",
        "steps": [
            "Step one foot forward.",
            "Lower the back knee comfortably.",
            "Keep the front foot stable.",
            "Maintain an upright posture."
        ]
    },

    {
        "name": "Baddha Koṇāsana",
        "common": "Butterfly Pose",
        "benefits": "Encourages gentle hip mobility.",
        "steps": [
            "Sit comfortably.",
            "Bring the soles of your feet together.",
            "Hold your feet gently.",
            "Allow your knees to move naturally."
        ]
    },

    {
        "name": "Ardha Matsyendrāsana",
        "common": "Half Spinal Twist",
        "benefits": "Encourages gentle rotational movement and spinal awareness.",
        "steps": [
            "Sit comfortably.",
            "Bend one knee.",
            "Turn your torso gently.",
            "Keep the movement controlled."
        ]
    },

    {
        "name": "Nāvāsana",
        "common": "Boat Pose",
        "benefits": "Supports controlled core engagement and balance.",
        "steps": [
            "Sit with your knees bent.",
            "Lean back slightly.",
            "Lift your feet if comfortable.",
            "Maintain steady breathing."
        ]
    },

    {
        "name": "Dhanurāsana",
        "common": "Bow Pose",
        "benefits": "Encourages coordinated movement of the back, legs and shoulders.",
        "steps": [
            "Lie on your stomach.",
            "Bend your knees.",
            "Reach toward your ankles if comfortable.",
            "Lift gently without forcing."
        ]
    },

    {
        "name": "Salabhāsana",
        "common": "Locust Pose",
        "benefits": "Supports controlled back-body and leg engagement.",
        "steps": [
            "Lie on your stomach.",
            "Keep your arms beside your body.",
            "Gently lift your chest or legs.",
            "Lower slowly."
        ]
    },

    {
        "name": "Gomukhāsana",
        "common": "Cow Face Pose",
        "benefits": "Encourages shoulder and hip mobility.",
        "steps": [
            "Sit comfortably.",
            "Position your legs comfortably.",
            "Bring your arms into a gentle shoulder stretch.",
            "Maintain relaxed breathing."
        ]
    },

    {
        "name": "Garuḍāsana",
        "common": "Eagle Pose",
        "benefits": "Challenges balance, concentration and coordinated movement.",
        "steps": [
            "Stand upright.",
            "Bend your knees slightly.",
            "Cross one leg over the other if comfortable.",
            "Balance with controlled breathing."
        ]
    },

    {
        "name": "Prasārita Pādottānāsana",
        "common": "Wide-Legged Forward Bend",
        "benefits": "Encourages a gentle stretch through the legs and back.",
        "steps": [
            "Stand with your feet comfortably wide.",
            "Keep your legs steady.",
            "Fold forward gently.",
            "Allow your shoulders to relax."
        ]
    },

    {
        "name": "Ustrāsana",
        "common": "Camel Pose",
        "benefits": "Encourages chest opening and controlled spinal extension.",
        "steps": [
            "Kneel comfortably.",
            "Keep your thighs upright.",
            "Place your hands on your hips or heels if comfortable.",
            "Open your chest gently."
        ]
    },

    {
        "name": "Matsyāsana",
        "common": "Fish Pose",
        "benefits": "Encourages gentle chest opening and mindful breathing.",
        "steps": [
            "Lie comfortably on your back.",
            "Position your arms beside your body.",
            "Gently lift your chest if comfortable.",
            "Return slowly."
        ]
    },

    {
        "name": "Pavanamuktāsana",
        "common": "Wind-Relieving Pose",
        "benefits": "Provides a gentle resting movement for the lower body.",
        "steps": [
            "Lie on your back.",
            "Bring one or both knees toward your chest.",
            "Hold comfortably.",
            "Breathe slowly and release."
        ]
    },

    {
        "name": "Supta Baddha Koṇāsana",
        "common": "Reclining Butterfly Pose",
        "benefits": "Provides a comfortable resting position and encourages relaxation.",
        "steps": [
            "Lie comfortably on your back.",
            "Bring the soles of your feet together.",
            "Allow your knees to open naturally.",
            "Rest and breathe comfortably."
        ]
    }

]


# ============================================================
# WELLNESS CALCULATION
# ============================================================

def calculate_wellness_score(
    stress,
    energy,
    mood,
    sleep,
    activity
):

    score = 100

    score -= stress * 4
    score += (energy - 5) * 3
    score += (mood - 5) * 3
    score += (sleep - 5) * 3
    score += (activity - 5) * 2

    score = max(
        0,
        min(100, int(score))
    )

    if score >= 75:
        status = "Balanced"

    elif score >= 50:
        status = "Moderate"

    else:
        status = "Needs Attention"

    return score, status


# ============================================================
# PERSONALIZED ASANAS
# ============================================================

def get_personalized_asanas():

    stress = st.session_state.stress
    energy = st.session_state.energy
    mood = st.session_state.mood
    sleep = st.session_state.sleep

    if stress >= 8 or mood <= 3:

        selected = [
            "Vṛkṣāsana",
            "Balāsana",
            "Makarāsana",
            "Sukhāsana",
            "Supta Baddha Koṇāsana",
            "Śavāsana"
        ]

        explanation = (
            "Your responses indicate that today's routine "
            "should emphasize calm movement, balance and relaxation."
        )

    elif energy <= 3 or sleep <= 3:

        selected = [
            "Tādāsana",
            "Vajrāsana",
            "Bhujangāsana",
            "Balāsana",
            "Makarāsana",
            "Śavāsana"
        ]

        explanation = (
            "Your responses indicate lower energy or reduced "
            "sleep quality, so today's plan uses gentle movement "
            "and relaxation."
        )

    elif energy >= 8 and mood >= 8:

        selected = [
            "Tādāsana",
            "Vṛkṣāsana",
            "Trikoṇāsana",
            "Vīrabhadrāsana II",
            "Bhujangāsana",
            "Śavāsana"
        ]

        explanation = (
            "Your responses indicate good energy and mood, "
            "so today's routine combines balance, movement "
            "and relaxation."
        )

    else:

        selected = [
            "Tādāsana",
            "Vṛkṣāsana",
            "Trikoṇāsana",
            "Bhujangāsana",
            "Balāsana",
            "Śavāsana"
        ]

        explanation = (
            "Your responses indicate a moderate wellness state, "
            "so today's routine focuses on balanced movement, "
            "gentle stretching and relaxation."
        )

    return selected, explanation


# ============================================================
# DURATION
# ============================================================

def get_duration(name):

    if name == "Śavāsana":
        return "3–5 minutes"

    if name in [
        "Balāsana",
        "Makarāsana",
        "Sukhāsana",
        "Vajrāsana",
        "Supta Baddha Koṇāsana"
    ]:
        return "1–2 minutes"

    return "20–30 seconds"


# ============================================================
# DISPLAY ASANA
# ============================================================

def display_asana(
    asana,
    number=None
):

    duration = get_duration(
        asana["name"]
    )

    number_html = ""

    if number:

        number_html = f"""
        <div class="asana-number">
        PERSONALIZED ROUTINE {number:02d}
        </div>
        """

    st.markdown(
        f"""
        <div class="asana-box">

        {number_html}

        <div class="asana-name">
        {asana["name"]}
        </div>

        <div class="asana-common">
        {asana["common"]}
        </div>

        <div class="asana-heading">
        ⏱ RECOMMENDED TIME
        </div>

        <div class="asana-description">
        {duration}
        </div>

        <div class="asana-heading">
        BENEFITS
        </div>

        <div class="asana-description">
        {asana["benefits"]}
        </div>

        <div class="asana-heading">
        SIMPLE STEPS
        </div>

        <div class="asana-description">
        {"<br>".join(
            [
                f"{i + 1}. {step}"
                for i, step in enumerate(asana["steps"])
            ]
        )}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">

        <div class="sidebar-logo">
        YOGAMIND
        </div>

        <div class="sidebar-caption">
        Personal Wellness Companion
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Analyze Wellness",
            "Personalized Plan",
            "Workout Library",
            "Performance Analysis",
            "Why Yoga?",
            "Breathing & Mindfulness",
            "About YOGAMIND"
        ]
    )

    st.divider()

    if st.session_state.user_name:

        st.markdown(
            f"""
            **USER**

            {st.session_state.user_name}

            Age: {st.session_state.user_age}
            """
        )

    else:

        st.caption(
            "Complete your profile on Dashboard."
        )


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.markdown(
        """
        <div class="hero-box">

        <div class="hero-title">
        YOGAMIND
        </div>

        <div class="hero-subtitle">
        Personalized Yoga & Mental Wellness Companion
        </div>

        <div class="hero-text">
        Understand your current wellness state, receive
        personalized guidance, and follow a structured routine
        combining movement, breathing and mindfulness.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Start Your Wellness Journey</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-subtitle">
        Enter your basic details before beginning your
        personalized wellness journey.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Your Name",
            value=st.session_state.user_name,
            placeholder="Enter your name"
        )

    with col2:

        age = st.number_input(
            "Your Age",
            min_value=10,
            max_value=100,
            value=int(
                st.session_state.user_age
            )
        )

    if st.button(
        "Save Profile & Continue",
        use_container_width=True
    ):

        if name.strip():

            st.session_state.user_name = name.strip()
            st.session_state.user_age = age

            st.success(
                f"Welcome to YOGAMIND, {name.strip()}!"
            )

        else:

            st.warning(
                "Please enter your name."
            )

    st.markdown(
        """
        <div class="info-box">

        <div class="info-title">
        How YOGAMIND Works
        </div>

        <div class="info-text">

        <b>01 — Understand</b><br>
        Enter your basic profile and daily wellness inputs.

        <br><br>

        <b>02 — Analyse</b><br>
        YOGAMIND generates a simple wellness indicator.

        <br><br>

        <b>03 — Personalise</b><br>
        Six suitable yoga practices are selected.

        <br><br>

        <b>04 — Practice</b><br>
        Follow the recommended steps and duration.

        <br><br>

        <b>05 — Track</b><br>
        Review your wellness development over multiple sessions.

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# ANALYZE WELLNESS
# ============================================================

elif page == "Analyze Wellness":

    st.markdown(
        '<div class="section-title">Analyze Your Wellness</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.user_name:

        st.warning(
            "Please enter your name and age on Dashboard first."
        )

    else:

        st.markdown(
            f"""
            <div class="section-subtitle">
            Hello <b>{st.session_state.user_name}</b>.
            Rate each area based on how you feel today.
            </div>
            """,
            unsafe_allow_html=True
        )

        stress = st.slider(
            "Current stress level",
            1,
            10,
            st.session_state.stress
        )

        energy = st.slider(
            "Current energy level",
            1,
            10,
            st.session_state.energy
        )

        mood = st.slider(
            "Current mood",
            1,
            10,
            st.session_state.mood
        )

        sleep = st.slider(
            "Sleep quality",
            1,
            10,
            st.session_state.sleep
        )

        activity = st.slider(
            "Physical activity today",
            1,
            10,
            st.session_state.activity
        )

        if st.button(
            "Analyze My Wellness",
            use_container_width=True
        ):

            score, status = calculate_wellness_score(
                stress,
                energy,
                mood,
                sleep,
                activity
            )

            # Save current values
            st.session_state.stress = stress
            st.session_state.energy = energy
            st.session_state.mood = mood
            st.session_state.sleep = sleep
            st.session_state.activity = activity

            st.session_state.wellness_score = score
            st.session_state.wellness_status = status
            st.session_state.analysis_done = True

            # ------------------------------------------------
            # CREATE HISTORY ENTRY
            # ------------------------------------------------

            history = load_history()

            now = datetime.now()

            entry = {
                "name": st.session_state.user_name,
                "age": st.session_state.user_age,
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M:%S"),
                "timestamp": now.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "score": score,
                "status": status,
                "stress": stress,
                "energy": energy,
                "mood": mood,
                "sleep": sleep,
                "activity": activity
            }

            history.append(entry)

            save_history(history)

            st.success(
                "Your wellness analysis has been recorded."
            )

        if st.session_state.analysis_done:

            st.divider()

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Wellness Indicator",
                    f"{st.session_state.wellness_score}/100"
                )

            with c2:

                st.metric(
                    "Current State",
                    st.session_state.wellness_status
                )

            with c3:

                st.metric(
                    "User",
                    st.session_state.user_name
                )

            st.info(
                "Open Performance Analysis from the sidebar "
                "to view your development over time."
            )


# ============================================================
# PERSONALIZED PLAN
# ============================================================

elif page == "Personalized Plan":

    st.markdown(
        '<div class="section-title">Your Personalized Plan</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.user_name:

        st.warning(
            "Please enter your name and age on Dashboard first."
        )

    elif not st.session_state.analysis_done:

        st.warning(
            "Please complete Analyze Wellness first."
        )

    else:

        selected_names, explanation = get_personalized_asanas()

        st.session_state.plan_count += 1

        st.markdown(
            f"""
            <div class="info-box">

            <div class="info-title">
            Hello, {st.session_state.user_name} 👋
            </div>

            <div class="info-text">

            <b>Age:</b> {st.session_state.user_age}<br>

            <b>Wellness Indicator:</b>
            {st.session_state.wellness_score}/100<br>

            <b>Current State:</b>
            {st.session_state.wellness_status}

            <br><br>

            {explanation}

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title">Today\'s 6-Asana Routine</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="section-subtitle">
            Complete the practices comfortably and in order.
            Do not force a movement.
            </div>
            """,
            unsafe_allow_html=True
        )

        for index, selected_name in enumerate(
            selected_names,
            start=1
        ):

            for asana in ASANAS:

                if asana["name"] == selected_name:

                    display_asana(
                        asana,
                        index
                    )

                    break

        st.markdown(
            """
            <div class="info-box">

            <div class="info-title">
            Finish With Relaxation
            </div>

            <div class="info-text">
            Complete the routine with a few quiet minutes
            of comfortable breathing and relaxation.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# WORKOUT LIBRARY
# ============================================================

elif page == "Workout Library":

    st.markdown(
        '<div class="section-title">Yoga Asana Library</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-subtitle">
        Explore all 30 yoga practices available in the
        YOGAMIND library.
        </div>
        """,
        unsafe_allow_html=True
    )

    search = st.text_input(
        "Search an asana",
        placeholder="Search by traditional or common name"
    )

    filtered = ASANAS

    if search.strip():

        query = search.lower()

        filtered = [
            a for a in ASANAS
            if query in a["name"].lower()
            or query in a["common"].lower()
        ]

    st.write(
        f"Showing {len(filtered)} of {len(ASANAS)} asanas"
    )

    for index, asana in enumerate(
        filtered,
        start=1
    ):

        with st.expander(
            f"{index:02d} | {asana['name']} — {asana['common']}"
        ):

            st.markdown(
                f"**Benefits:** {asana['benefits']}"
            )

            st.markdown("**Steps:**")

            for i, step in enumerate(
                asana["steps"],
                start=1
            ):

                st.write(
                    f"{i}. {step}"
                )

            st.caption(
                "Suggested comfortable duration: "
                + get_duration(asana["name"])
            )


# ============================================================
# PERFORMANCE ANALYSIS
# ============================================================

elif page == "Performance Analysis":

    st.markdown(
        '<div class="section-title">Performance Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-subtitle">
        Review your YOGAMIND usage and observe how your
        self-reported wellness indicators develop across
        recorded sessions.
        </div>
        """,
        unsafe_allow_html=True
    )

    history = load_history()

    # --------------------------------------------------------
    # NO HISTORY
    # --------------------------------------------------------

    if not history:

        st.info(
            "No analysis sessions have been recorded yet. "
            "Complete your first Wellness Analysis to begin tracking."
        )

    else:

        # ----------------------------------------------------
        # DATAFRAME
        # ----------------------------------------------------

        df = pd.DataFrame(history)

        df["datetime"] = pd.to_datetime(
            df["timestamp"]
        )

        df = df.sort_values(
            "datetime"
        )

        # ----------------------------------------------------
        # USER FILTER
        # ----------------------------------------------------

        if st.session_state.user_name:

            user_df = df[
                df["name"]
                == st.session_state.user_name
            ]

            if user_df.empty:

                user_df = df

        else:

            user_df = df

        # ----------------------------------------------------
        # MAIN METRICS
        # ----------------------------------------------------

        total_sessions = len(user_df)

        average_score = round(
            user_df["score"].mean(),
            1
        )

        highest_score = int(
            user_df["score"].max()
        )

        lowest_score = int(
            user_df["score"].min()
        )

        first_access = user_df[
            "datetime"
        ].min().strftime(
            "%d %b %Y, %I:%M %p"
        )

        last_access = user_df[
            "datetime"
        ].max().strftime(
            "%d %b %Y, %I:%M %p"
        )

        # ----------------------------------------------------
        # TOP METRICS
        # ----------------------------------------------------

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Total Sessions",
                total_sessions
            )

        with c2:

            st.metric(
                "Average Score",
                f"{average_score}/100"
            )

        with c3:

            st.metric(
                "Highest Score",
                f"{highest_score}/100"
            )

        with c4:

            st.metric(
                "Lowest Score",
                f"{lowest_score}/100"
            )

        st.divider()

        # ----------------------------------------------------
        # ACCESS INFORMATION
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">Usage Information</div>',
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2)

        with c1:

            st.markdown(
                f"""
                <div class="card-box">

                <div class="card-title">
                First Recorded Access
                </div>

                <div class="card-text">
                {first_access}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                f"""
                <div class="card-box">

                <div class="card-title">
                Most Recent Access
                </div>

                <div class="card-text">
                {last_access}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        # ----------------------------------------------------
        # WELLNESS DEVELOPMENT GRAPH
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">Wellness Development</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="section-subtitle">
            This graph shows the wellness indicator recorded
            during each completed analysis session.
            </div>
            """,
            unsafe_allow_html=True
        )

        score_chart = user_df[
            ["datetime", "score"]
        ].copy()

        score_chart = score_chart.set_index(
            "datetime"
        )

        st.line_chart(
            score_chart["score"],
            height=350
        )

        # ----------------------------------------------------
        # WELLNESS DIMENSION DEVELOPMENT
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">Wellness Dimensions</div>',
            unsafe_allow_html=True
        )

        dimension_chart = user_df[
            [
                "datetime",
                "stress",
                "energy",
                "mood",
                "sleep",
                "activity"
            ]
        ].copy()

        dimension_chart = dimension_chart.set_index(
            "datetime"
        )

        st.line_chart(
            dimension_chart,
            height=400
        )

        st.caption(
            "The graph represents your self-reported values "
            "from each recorded check-in."
        )

        # ----------------------------------------------------
        # AVERAGE DIMENSIONS
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">Average Check-in Profile</div>',
            unsafe_allow_html=True
        )

        avg_stress = round(
            user_df["stress"].mean(),
            1
        )

        avg_energy = round(
            user_df["energy"].mean(),
            1
        )

        avg_mood = round(
            user_df["mood"].mean(),
            1
        )

        avg_sleep = round(
            user_df["sleep"].mean(),
            1
        )

        avg_activity = round(
            user_df["activity"].mean(),
            1
        )

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            st.metric(
                "Avg. Stress",
                f"{avg_stress}/10"
            )

        with c2:
            st.metric(
                "Avg. Energy",
                f"{avg_energy}/10"
            )

        with c3:
            st.metric(
                "Avg. Mood",
                f"{avg_mood}/10"
            )

        with c4:
            st.metric(
                "Avg. Sleep",
                f"{avg_sleep}/10"
            )

        with c5:
            st.metric(
                "Avg. Activity",
                f"{avg_activity}/10"
            )

        # ----------------------------------------------------
        # SESSION TABLE
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">Complete Session History</div>',
            unsafe_allow_html=True
        )

        table = user_df[
            [
                "date",
                "time",
                "score",
                "status",
                "stress",
                "energy",
                "mood",
                "sleep",
                "activity"
            ]
        ].copy()

        table.columns = [
            "Date",
            "Time",
            "Score",
            "Status",
            "Stress",
            "Energy",
            "Mood",
            "Sleep",
            "Activity"
        ]

        table = table.sort_values(
            "Date",
            ascending=False
        )

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # USAGE SUMMARY
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="info-box">

            <div class="info-title">
            What Your Performance Analysis Means
            </div>

            <div class="info-text">

            <b>Total Sessions</b> shows how many wellness
            check-ins have been recorded.

            <br><br>

            <b>Average Score</b> represents the average
            wellness indicator across recorded sessions.

            <br><br>

            <b>Development Graph</b> allows you to visually
            compare your recorded check-ins over time.

            <br><br>

            <b>Access Time</b> records when a wellness analysis
            was submitted.

            <br><br>

            These values are intended for personal reflection
            and prototype demonstration. They should not be
            interpreted as medical measurements or diagnoses.

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # CLEAR HISTORY
        # ----------------------------------------------------

        st.divider()

        st.markdown(
            '<div class="section-title">History Management</div>',
            unsafe_allow_html=True
        )

        if st.button(
            "Clear All Recorded History"
        ):

            if os.path.exists(HISTORY_FILE):

                os.remove(
                    HISTORY_FILE
                )

            st.success(
                "All recorded YOGAMIND history has been cleared."
            )

            st.rerun()


# ============================================================
# WHY YOGA
# ============================================================

elif page == "Why Yoga?":

    st.markdown(
        '<div class="section-title">Why Yoga?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-box">

        <div class="hero-subtitle">
        Yoga connects movement, breathing and awareness.
        </div>

        <div class="hero-text">
        Yoga can be practiced as a mindful form of movement.
        A consistent and comfortable practice can support
        flexibility, balance, body awareness and relaxation.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            """
            <div class="card-box">

            <div class="card-title">
            Physical Wellbeing
            </div>

            <div class="card-text">
            Yoga practices can support flexibility,
            balance, mobility, posture awareness and
            controlled movement.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
            <div class="card-box">

            <div class="card-title">
            Mental Wellbeing
            </div>

            <div class="card-text">
            Breathing and mindfulness practices can encourage
            relaxation, concentration and present-moment awareness.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="info-box">

        <div class="info-title">
        The YOGAMIND Approach
        </div>

        <div class="info-text">

        <b>Movement</b> — Controlled physical practices.

        <br><br>

        <b>Breathing</b> — Comfortable breathing awareness.

        <br><br>

        <b>Mindfulness</b> — Attention to the present moment.

        <br><br>

        <b>Consistency</b> — Building sustainable wellness habits.

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# BREATHING & MINDFULNESS
# ============================================================

elif page == "Breathing & Mindfulness":

    st.markdown(
        '<div class="section-title">Breathing & Mindfulness</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-subtitle">
        Breathing and mindfulness complement physical yoga
        practices by encouraging attention, calmness and
        awareness.
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            """
            <div class="card-box">

            <div class="card-title">
            Comfortable Breathing
            </div>

            <div class="card-text">

            Sit or lie comfortably.

            <br><br>

            Breathe naturally.

            <br><br>

            Keep the breathing comfortable.

            <br><br>

            Continue for 2–3 minutes.

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
            <div class="card-box">

            <div class="card-title">
            Mindful Observation
            </div>

            <div class="card-text">

            Sit comfortably.

            <br><br>

            Notice your natural breathing.

            <br><br>

            If your attention wanders, gently return
            to the present moment.

            <br><br>

            Continue for 2–5 minutes.

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="info-box">

        <div class="info-title">
        Simple Practice Rule
        </div>

        <div class="info-text">
        Do not force the breath or hold it for long periods.
        Keep the practice comfortable. If you feel
        uncomfortable, stop and rest.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# ABOUT
# ============================================================

elif page == "About YOGAMIND":

    st.markdown(
        '<div class="section-title">About YOGAMIND</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-box">

        <div class="hero-title">
        YOGAMIND
        </div>

        <div class="hero-subtitle">
        From Check-in to Personalised Wellness
        </div>

        <div class="hero-text">
        YOGAMIND demonstrates how a digital wellness
        companion can combine user input, simple analysis,
        personalized yoga recommendations and longitudinal
        performance tracking.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="card-box">

        <div class="card-title">
        Core System
        </div>

        <div class="card-text">

        User Profile
        →
        Wellness Check-in
        →
        Analysis
        →
        Personalized Plan
        →
        Practice
        →
        Performance Tracking

        <br><br>

        The system stores completed check-ins locally and
        presents the recorded information through tables,
        metrics and development graphs.

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="info-box">

        <div class="info-title">
        Prototype Safety Note
        </div>

        <div class="info-text">
        YOGAMIND provides general wellness suggestions.
        It is not a medical diagnostic system and should
        not replace professional healthcare advice.

        Practice within your comfort level and stop if a
        movement causes pain, dizziness or discomfort.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

    🌿 YOGAMIND — Personalized Yoga & Mental Wellness Companion

    <br><br>

    Movement • Breathing • Mindfulness • Personalisation • Tracking

    <br><br>

    Wellness-support prototype — not a medical diagnostic system.

    </div>
    """,
    unsafe_allow_html=True
)