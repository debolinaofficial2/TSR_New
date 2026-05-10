# =========================================================
# SMARTLEARN CONNECT
# FINAL PROFESSIONAL VERSION
# =========================================================

import streamlit as st
import pandas as pd
import time
import smtplib

from datetime import date

from sentence_transformers import (
    SentenceTransformer,
    util
)

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SmartLearn Connect",
    layout="wide"
)


# =========================================================
# SESSION STATES
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "form"

if "step" not in st.session_state:
    st.session_state.step = 1

if "show_popup" not in st.session_state:
    st.session_state.show_popup = False

if "global_booking_done" not in st.session_state:
    st.session_state.global_booking_done = False


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_excel(
        "Dataset_TSR.xlsx"
    )

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


teachers = load_data()


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


model = load_model()


# =========================================================
# SEND EMAIL
# =========================================================

def send_demo_email(
    parent_name,
    parent_email,
    teacher_name,
    selected_date,
    selected_time
):

    try:

        sender_email = (
            "debolinaofficial2@gmail.com"
        )

        sender_password = (
            st.secrets["EMAIL_PASSWORD"]
        )

        meet_link = (
            "https://meet.google.com/ypj-jhkz-gta"
        )

        subject = (
            "SmartLearn Connect Demo Session Confirmation"
        )

        html_body = f"""
        <html>

        <body style="
        font-family:Arial;
        background:#f5f7fb;
        padding:20px;
        ">

        <div style="
        max-width:650px;
        margin:auto;
        background:white;
        border-radius:20px;
        overflow:hidden;
        box-shadow:0px 10px 35px rgba(0,0,0,0.08);
        ">

            <div style="
            background:linear-gradient(
            90deg,
            #2fa4a9,
            #167b7f
            );
            padding:35px;
            text-align:center;
            color:white;
            ">

                <h1>
                🎓 SmartLearn Connect
                </h1>

                <p>
                Demo Session Confirmation
                </p>

            </div>


            <div style="
            padding:35px;
            ">

                <h2>
                Hello {parent_name},
                </h2>

                <p style="
                font-size:18px;
                line-height:1.8;
                ">

                Your demo session has been booked successfully.

                </p>


                <div style="
                background:#f8fbfc;
                padding:22px;
                border-radius:16px;
                margin-top:25px;
                ">

                    <p>
                    <strong>Teacher:</strong>
                    {teacher_name}
                    </p>

                    <p>
                    <strong>Date:</strong>
                    {selected_date}
                    </p>

                    <p>
                    <strong>Time:</strong>
                    {selected_time}
                    </p>

                </div>


                <div style="
                text-align:center;
                margin-top:35px;
                ">

                    <a
                    href="{meet_link}"
                    target="_blank"
                    style="
                    background:#ff7a18;
                    color:white;
                    padding:16px 30px;
                    border-radius:12px;
                    text-decoration:none;
                    font-weight:700;
                    font-size:18px;
                    "
                    >

                    Join Google Meet

                    </a>

                </div>


                <p style="
                margin-top:40px;
                line-height:1.8;
                ">

                Regards,
                <br>

                <strong>
                SmartLearn Connect
                </strong>

                </p>

            </div>

        </div>

        </body>

        </html>
        """

        msg = MIMEMultipart("alternative")

        msg["From"] = sender_email

        msg["To"] = parent_email

        msg["Subject"] = subject

        msg.attach(
            MIMEText(
                html_body,
                "html"
            )
        )

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            sender_email,
            sender_password
        )

        server.sendmail(
            sender_email,
            [parent_email],
            msg.as_string()
        )

        server.quit()

        return True

    except Exception as e:

        print(e)

        return False


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

/* MAIN */

.main{
background:#f5f7fb;
}


/* NAVBAR */

.navbar{
background:linear-gradient(
90deg,
#2fa4a9,
#167b7f
);

padding:20px 40px;

border-radius:20px;

display:flex;

justify-content:space-between;

align-items:center;

box-shadow:
0px 10px 35px rgba(0,0,0,0.08);

margin-bottom:25px;
}

.nav-title{
font-size:34px;
font-weight:800;
color:white;
}

.nav-links{
font-size:18px;
font-weight:600;
color:white;
}


/* HERO */

.hero{
background:white;

padding:55px;

border-radius:30px;

box-shadow:
0px 12px 40px rgba(0,0,0,0.08);

margin-bottom:25px;
}

.hero-title{
font-size:74px;
font-weight:800;
line-height:1.1;
color:#1f2937;
}

.highlight{
color:#ff7a18;
}

.hero-sub{
font-size:22px;
margin-top:18px;
color:#4b5563;
}


/* TAG */

.tag{
display:inline-block;

padding:12px 22px;

background:#f8fbfc;

border-radius:30px;

margin-right:12px;

margin-top:20px;

font-weight:700;

color:#167b7f;

box-shadow:
0px 5px 15px rgba(0,0,0,0.05);
}


/* FORM */

.form-box{
background:white;

padding:35px;

border-radius:24px;

box-shadow:
0px 12px 40px rgba(0,0,0,0.08);

margin-top:25px;
}


/* PROGRESS */

div[data-testid="stProgress"] > div > div > div{

background:linear-gradient(
90deg,
#2fa4a9,
#6be0da,
#2fa4a9
);

background-size:200% 100%;

animation:moveProgress 2s linear infinite;

height:18px;

border-radius:20px;
}

@keyframes moveProgress{
0%{
background-position:200% 0;
}
100%{
background-position:-200% 0;
}
}


/* TEACHER CARD */

.teacher-card{
background:white;

padding:35px;

border-radius:26px;

box-shadow:
0px 12px 35px rgba(0,0,0,0.08);

margin-bottom:35px;

border:1px solid #eef2f7;
}

.teacher-name{
font-size:38px;
font-weight:800;
color:#1f2937;
}

.teacher-desc{
font-size:17px;
line-height:1.8;
color:#4b5563;
margin-top:14px;
}

.score{
font-size:60px;
font-weight:800;
color:#167b7f;
text-align:right;
}


/* WHY */

.reason{
background:#f8fbfc;

padding:14px 18px;

border-left:6px solid #2fa4a9;

border-radius:12px;

margin-bottom:12px;

font-size:16px;

color:#374151;
}


/* BUTTON */

.stButton>button{

background:#ff7a18;

color:white;

font-weight:700;

border:none;

border-radius:14px;

height:52px;

padding:0px 28px;

transition:0.3s;
}

.stButton>button:hover{

background:#ff8f38;

transform:translateY(-2px);
}


/* POPUP */

.popup-overlay{

position:fixed;

top:0;
left:0;

width:100vw;
height:100vh;

background:rgba(0,0,0,0.55);

backdrop-filter:blur(8px);

display:flex;

justify-content:center;

align-items:center;

z-index:999999;
}

.popup-card{

width:650px;

background:white;

border-radius:28px;

padding:55px;

text-align:center;

box-shadow:
0px 20px 60px rgba(0,0,0,0.25);

border:3px solid #2fa4a9;
}

.popup-title{

font-size:42px;

font-weight:800;

color:#167b7f;

margin-bottom:22px;
}

.popup-sub{

font-size:20px;

line-height:1.8;

color:#4b5563;

margin-bottom:35px;
}

.popup-btn{

display:inline-block;

background:#ff7a18;

color:white !important;

text-decoration:none;

padding:16px 34px;

border-radius:14px;

font-size:18px;

font-weight:700;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# NAVBAR
# =========================================================

st.markdown("""
<div class="navbar">

<div class="nav-title">
🎓 SmartLearn Connect
</div>

<div class="nav-links">
Home &nbsp;&nbsp;&nbsp;
Academic &nbsp;&nbsp;&nbsp;
Exam Prep &nbsp;&nbsp;&nbsp;
Mentors
</div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# HERO
# =========================================================

left,right = st.columns([1.2,1])

with left:

    st.markdown("""
    <div class="hero">

    <div class="hero-title">

    Find the Right

    <span class="highlight">
    Tutor Match
    </span>

    <br>

    for Your Child Instantly

    </div>

    <div class="hero-sub">

    AI-powered tutor recommendation
    across CBSE, ICSE, IB,
    IGCSE & State Boards

    </div>

    <div class="tag">CBSE</div>
    <div class="tag">ICSE</div>
    <div class="tag">IB</div>
    <div class="tag">IGCSE</div>
    <div class="tag">State Boards</div>

    </div>
    """, unsafe_allow_html=True)

with right:

    st.image(
        "https://images.unsplash.com/photo-1588072432836-e10032774350",
        use_container_width=True
    )


# =========================================================
# PROGRESS
# =========================================================

progress_lookup = {
    1:0.0,
    2:0.2,
    3:0.4,
    4:0.6,
    5:0.8
}


# =========================================================
# FORM PAGE
# =========================================================

if st.session_state.page == "form":

    progress = progress_lookup.get(
        st.session_state.step,
        0
    )

    st.markdown(
        '<div class="form-box">',
        unsafe_allow_html=True
    )

    st.progress(progress)

    st.write(
        f"Profile completion: {int(progress*100)}%"
    )


    # STEP 1

    if st.session_state.step == 1:

        subject = st.selectbox(
            "Select subject",
            sorted(
                teachers["subject"].dropna().unique()
            ),
            index=None
        )

        if subject:

            st.session_state.subject = subject

            st.session_state.step = 2

            st.rerun()


    # STEP 2

    elif st.session_state.step == 2:

        boards = set()

        for b in teachers["boards"].dropna():

            boards.update(
                [x.strip() for x in b.split(",")]
            )

        board = st.selectbox(
            "Select curriculum board",
            sorted(boards),
            index=None
        )

        if board:

            st.session_state.board = board

            st.session_state.step = 3

            st.rerun()


    # STEP 3

    elif st.session_state.step == 3:

        goal = st.selectbox(
            "Learning objective",
            [
                "Conceptual Understanding",
                "Exam Preparation",
                "Assignment Support",
                "Research Guidance"
            ],
            index=None
        )

        if goal:

            st.session_state.goal = goal

            st.session_state.step = 4

            st.rerun()


    # STEP 4

    elif st.session_state.step == 4:

        exp = st.slider(
            "Minimum experience required",
            0,
            20,
            5
        )

        st.session_state.experience = exp

        st.session_state.step = 5

        st.rerun()


    # STEP 5

    elif st.session_state.step == 5:

        expectation = st.text_area(
            "Describe learner expectations"
        )

        if st.button(
            "Generate Recommendations"
        ):

            st.session_state.expectation = (
                expectation
            )

            with st.spinner(
                "Matching best tutors..."
            ):

                time.sleep(2)

            st.session_state.page = "results"

            st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# POPUP
# =========================================================

if st.session_state.show_popup:

    st.markdown("""
    <div class="popup-overlay">

        <div class="popup-card">

            <div class="popup-title">
            ✅ Demo Booked Successfully!
            </div>

            <div class="popup-sub">

            Demo confirmation email
            has been sent successfully.

            <br><br>

            Your Google Meet session
            is now ready.

            </div>

            <a
            href="https://meet.google.com/ypj-jhkz-gta"
            target="_blank"
            class="popup-btn"
            >

            Join Google Meet

            </a>

        </div>

    </div>
    """, unsafe_allow_html=True)