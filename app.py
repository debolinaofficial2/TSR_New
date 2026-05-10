# =========================================================
# SMARTLEARN CONNECT
# COMPLETE FINAL VERSION
# =========================================================

import streamlit as st
import pandas as pd
import time
import smtplib

from datetime import (
    date,
    timedelta
)

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
# SESSION STATE
# =========================================================

defaults = {

    "page": "form",
    "step": 1,

    "subject": None,
    "board": None,
    "goal": None,
    "experience": 5,
    "expectation": "",

    "booking_success": False,
    "global_booking_done": False,

    "booked_teacher": "",
    "booked_date": "",
    "booked_time": ""
}

for k,v in defaults.items():

    if k not in st.session_state:

        st.session_state[k] = v


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
# MODEL
# =========================================================

@st.cache_resource
def load_model():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


model = load_model()


# =========================================================
# EMAIL FUNCTION
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

        msg = MIMEMultipart(
            "alternative"
        )

        msg["From"] = sender_email

        msg["To"] = parent_email

        msg["Subject"] = (
            "SmartLearn Connect Demo Confirmation"
        )

        html = f"""
        <html>

        <body style="
        background:#f5f7fb;
        font-family:Arial;
        padding:25px;
        ">

        <div style="
        max-width:650px;
        margin:auto;
        background:white;
        border-radius:24px;
        overflow:hidden;
        box-shadow:0 10px 35px rgba(0,0,0,0.08);
        ">

        <div style="
        background:linear-gradient(
        90deg,
        #2fa4a9,
        #167b7f
        );
        color:white;
        padding:40px;
        text-align:center;
        ">

        <h1>
        SmartLearn Connect
        </h1>

        <p>
        Demo Session Confirmation
        </p>

        </div>

        <div style="padding:35px;">

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
        margin-top:20px;
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

        msg.attach(
            MIMEText(
                html,
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
border-radius:22px;
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:30px;
box-shadow:0 10px 35px rgba(0,0,0,0.08);
}

.logo{
font-size:34px;
font-weight:800;
color:white;
}

.links{
font-size:18px;
font-weight:700;
color:white;
}

/* HERO */

.hero{
background:white;
padding:55px;
border-radius:28px;
box-shadow:0 10px 35px rgba(0,0,0,0.08);
margin-bottom:30px;
}

.hero-title{
font-size:72px;
font-weight:800;
line-height:1.1;
color:#1f2937;
}

.highlight{
color:#ff7a18;
}

.hero-sub{
font-size:22px;
margin-top:20px;
line-height:1.8;
color:#4b5563;
}

.tag{
display:inline-block;
padding:12px 22px;
background:#f8fbfc;
border-radius:40px;
margin-top:22px;
margin-right:10px;
font-weight:700;
color:#167b7f;
}

/* FORM */

.form-box{
background:white;
padding:35px;
border-radius:24px;
box-shadow:0 10px 35px rgba(0,0,0,0.08);
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

/* BUTTON */

.stButton>button{

background:#ff7a18;
color:white;
border:none;
height:50px;
padding:0px 26px;
border-radius:14px;
font-weight:700;
font-size:16px;
}

.stButton>button:hover{
background:#ff8f38;
}

/* TEACHER CARD */

.teacher-card{

background:white;

padding:35px;

border-radius:28px;

margin-bottom:35px;

box-shadow:0 10px 35px rgba(0,0,0,0.08);

border:1px solid #eef2f7;

transition:0.3s ease;
}

.teacher-card:hover{

transform:translateY(-6px);

box-shadow:0 18px 45px rgba(0,0,0,0.12);
}

.teacher-header{

display:flex;

justify-content:space-between;

align-items:center;

margin-bottom:25px;
}

.teacher-profile{

display:flex;

align-items:center;

gap:18px;
}

.teacher-avatar{

width:80px;
height:80px;

border-radius:24px;

background:linear-gradient(
135deg,
#2fa4a9,
#167b7f
);

display:flex;

align-items:center;

justify-content:center;

overflow:hidden;
}

.teacher-name{

font-size:34px;

font-weight:800;

color:#1f2937;
}

.teacher-meta{

font-size:16px;

color:#6b7280;

margin-top:6px;
}

.score-circle{

width:120px;
height:120px;

border-radius:50%;

background:linear-gradient(
135deg,
#2fa4a9,
#167b7f
);

display:flex;

flex-direction:column;

align-items:center;

justify-content:center;

color:white;
}

.score-value{

font-size:34px;

font-weight:800;
}

.score-label{

font-size:14px;
}

.teacher-description{

font-size:17px;

line-height:1.9;

color:#4b5563;

margin-bottom:28px;
}

.recommend-title{

font-size:24px;

font-weight:800;

margin-bottom:18px;
}

.recommend-grid{

display:grid;

grid-template-columns:1fr 1fr;

gap:16px;
}

.reason-card{

background:#f8fbfc;

padding:18px;

border-radius:18px;

display:flex;

align-items:center;

gap:15px;

border:1px solid #eef2f7;
}

.reason-icon{

width:52px;
height:52px;

border-radius:14px;

background:linear-gradient(
135deg,
#2fa4a9,
#167b7f
);

display:flex;

align-items:center;

justify-content:center;

font-size:24px;

color:white;
}

.reason-heading{

font-size:17px;

font-weight:700;

color:#1f2937;
}

.reason-sub{

font-size:14px;

color:#6b7280;

margin-top:4px;
}

/* ANIMATION */

@keyframes moveProgress{

0%{
background-position:200% 0;
}

100%{
background-position:-200% 0;
}

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# RESULTS PAGE
# =========================================================

st.markdown("""
<h1 style="
font-size:54px;
font-weight:800;
margin-bottom:25px;
color:#1f2937;
">
Top 3 Recommended Teachers
</h1>
""", unsafe_allow_html=True)


ranked = []

for _,teacher in teachers.iterrows():

    teacher_subjects = str(
        teacher["subject_specialization"]
    ).lower()

    student_subject = (
        str(st.session_state.subject)
        .lower()
    )

    subject_score = 35 if (
        student_subject
        in teacher_subjects
    ) else 0

    board_score = 20 if (
        str(st.session_state.board)
        .lower()
        in str(
            teacher["boards"]
        ).lower()
    ) else 0

    teacher_exp = teacher.get(
        "teaching_experience_years",
        0
    )

    try:

        teacher_exp = int(
            teacher_exp
        )

    except:

        teacher_exp = 0

    exp_score = 10 if (
        teacher_exp
        >= st.session_state.experience
    ) else 0

    teacher_profile = " ".join([

        str(
            teacher.get(
                "description",
                ""
            )
        ),

        str(
            teacher.get(
                "highest_qualification",
                ""
            )
        )

    ])

    semantic = util.cos_sim(

        model.encode(
            st.session_state.expectation
        ),

        model.encode(
            teacher_profile
        )

    ).item()

    semantic = (
        (semantic + 1) / 2
    ) * 35

    total_score = (

        subject_score
        + board_score
        + exp_score
        + semantic

    )

    teacher_dict = (
        teacher.to_dict()
    )

    teacher_dict[
        "final_score"
    ] = total_score

    teacher_dict[
        "subject_score"
    ] = subject_score

    teacher_dict[
        "board_score"
    ] = board_score

    teacher_dict[
        "exp_score"
    ] = exp_score

    teacher_dict[
        "semantic_score"
    ] = semantic

    ranked.append(
        teacher_dict
    )


ranked = sorted(

    ranked,

    key=lambda x:
    x["final_score"],

    reverse=True

)[:3]


for teacher in ranked:

    teacher_name = teacher.get(
        "name",
        "Tutor"
    )

    score = int(
        min(
            teacher["final_score"],
            98
        )
    )

    st.markdown(f"""
    <div class="teacher-card">

        <div class="teacher-header">

            <div class="teacher-profile">

                <div class="teacher-avatar">

                <img
                src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                width="42"
                />

                </div>

                <div>

                    <div class="teacher-name">
                    {teacher_name}
                    </div>

                    <div class="teacher-meta">

                    {teacher.get('teaching_experience_years',0)}+ Years Experience

                    </div>

                </div>

            </div>

            <div class="score-circle">

                <div class="score-value">
                {score}%
                </div>

                <div class="score-label">
                Compatibility
                </div>

            </div>

        </div>

        <div class="teacher-description">

        {teacher.get('description','')}

        </div>

        <div class="recommend-title">

        Why this tutor matches

        </div>

        <div class="recommend-grid">
    """, unsafe_allow_html=True)

    if teacher["subject_score"] > 0:

        st.markdown("""
        <div class="reason-card">

        <div class="reason-icon">
        ✓
        </div>

        <div>

        <div class="reason-heading">
        Subject Expertise
        </div>

        <div class="reason-sub">
        Strong subject alignment
        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)

    if teacher["board_score"] > 0:

        st.markdown("""
        <div class="reason-card">

        <div class="reason-icon">
        ✓
        </div>

        <div>

        <div class="reason-heading">
        Board Compatibility
        </div>

        <div class="reason-sub">
        Matches selected curriculum
        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)

    if teacher["exp_score"] > 0:

        st.markdown("""
        <div class="reason-card">

        <div class="reason-icon">
        ✓
        </div>

        <div>

        <div class="reason-heading">
        Experience Match
        </div>

        <div class="reason-sub">
        Meets experience preference
        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)

    if teacher["semantic_score"] > 0:

        st.markdown("""
        <div class="reason-card">

        <div class="reason-icon">
        ✓
        </div>

        <div>

        <div class="reason-heading">
        Learner Expectation Match
        </div>

        <div class="reason-sub">
        Aligned with learner goals
        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander(
        f"Book Demo with {teacher_name}"
    ):

        parent_name = st.text_input(
            "Parent Name",
            key=f"name_{teacher_name}"
        )

        parent_email = st.text_input(
            "Parent Email",
            key=f"email_{teacher_name}"
        )

        selected_date = st.date_input(

            "Preferred Date",

            min_value=(
                date.today()
                + timedelta(days=1)
            ),

            key=f"date_{teacher_name}"
        )

        selected_time = st.selectbox(

            "Preferred Time",

            [
                "10:00 AM",
                "12:00 PM",
                "03:00 PM",
                "05:00 PM",
                "07:00 PM"
            ],

            key=f"time_{teacher_name}"
        )

        already_booked = (
            st.session_state
            .global_booking_done
        )

        if already_booked:

            st.button(
                "Demo Already Booked",
                disabled=True,
                key=f"disabled_{teacher_name}"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="
            background:linear-gradient(
            90deg,
            #f8fbfc,
            #eefaf9
            );
            border:1px solid #d9eceb;
            border-radius:16px;
            padding:22px;
            margin-top:8px;
            ">

                <div style="
                display:flex;
                align-items:center;
                gap:14px;
                ">

                    <div style="
                    width:42px;
                    height:42px;
                    border-radius:12px;
                    background:#dff6f4;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:20px;
                    color:#167b7f;
                    ">

                    📅

                    </div>

                    <div>

                        <div style="
                        font-size:22px;
                        font-weight:800;
                        color:#374151;
                        ">

                        Demo Scheduled:
                        <span style="color:#167b7f;">

                        {st.session_state.booked_date}

                        at

                        {st.session_state.booked_time}

                        </span>

                        </div>

                        <div style="
                        margin-top:6px;
                        font-size:16px;
                        color:#6b7280;
                        ">

                        Confirmed with
                        <strong>
                        {st.session_state.booked_teacher}
                        </strong>

                        </div>

                    </div>

                </div>

            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            col1,col2,col3 = st.columns([1,1,1])

            with col2:

                st.link_button(
                    "Join Google Meet",
                    "https://meet.google.com/ypj-jhkz-gta",
                    use_container_width=True
                )

        else:

            if st.button(

                f"Confirm Demo with {teacher_name}",

                key=f"confirm_{teacher_name}"
            ):

                if (
                    not parent_name
                    or not parent_email
                ):

                    st.error(
                        "Please fill all fields"
                    )

                else:

                    with st.spinner(
                        "Booking demo..."
                    ):

                        time.sleep(2)

                        success = (
                            send_demo_email(
                                parent_name,
                                parent_email,
                                teacher_name,
                                selected_date,
                                selected_time
                            )
                        )

                    if success:

                        st.session_state[
                            "global_booking_done"
                        ] = True

                        st.session_state[
                            "booking_success"
                        ] = True

                        st.session_state[
                            "booked_teacher"
                        ] = teacher_name

                        st.session_state[
                            "booked_date"
                        ] = selected_date

                        st.session_state[
                            "booked_time"
                        ] = selected_time

                        st.rerun()

                    else:

                        st.error(
                            "Email sending failed"
                        )


st.markdown("<br><br>", unsafe_allow_html=True)

center1,center2,center3 = st.columns([2,2,2])

with center2:

    if st.button(
        "Start New Search",
        use_container_width=True
    ):

        st.session_state.clear()

        st.rerun()