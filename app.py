# =========================================================
# SMARTLEARN CONNECT
# FINAL COMPLETE VERSION
# =========================================================

import streamlit as st
import pandas as pd
import time
import smtplib
import streamlit.components.v1 as components

from datetime import (
    date,
    timedelta,
    datetime
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
# SESSION STATES
# =========================================================

defaults = {

    "page": "form",
    "step": 1,

    "subject": None,
    "board": None,
    "goal": None,
    "experience": 5,
    "expectation": "",

    "global_booking_done": False,

    "booking_success": False,

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
        "TSR.xlsx"
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
# EMAIL FUNCTION
# =========================================================
def send_academic_buddy_alert():

    try:

        sender_email = (
            "debolinaofficial2@gmail.com"
        )

        sender_password = (
            st.secrets["EMAIL_PASSWORD"]
        )

        academic_buddy_email = (
            "debolinabhanjaofficial@gmail.com"
        )

        msg = MIMEMultipart("alternative")

        msg["From"] = sender_email

        msg["To"] = academic_buddy_email

        msg["Subject"] = (
            "No Exact Tutor Match Found"
        )

        html_body = f"""
        <html>

        <body style="
        font-family:Arial;
        background:#f5f7fb;
        padding:30px;
        ">

        <div style="
        max-width:650px;
        margin:auto;
        background:white;
        border-radius:20px;
        overflow:hidden;
        ">

            <div style="
            background:linear-gradient(
            90deg,
            #f59e0b,
            #d97706
            );
            padding:30px;
            text-align:center;
            color:white;
            ">

                <h1>
                Academic Buddy Escalation
                </h1>

            </div>

            <div style="padding:35px;">

                <h2>
                No Exact Match Found
                </h2>

                <p style="
                font-size:17px;
                line-height:1.8;
                ">

                A learner request requires manual academic review.

                </p>

                <div style="
                background:#f8fbfc;
                border-radius:16px;
                padding:24px;
                margin-top:25px;
                ">

                    <p>
                    <strong>Subject:</strong>
                    {st.session_state.subject}
                    </p>

                    <p>
                    <strong>Board:</strong>
                    {st.session_state.board}
                    </p>

                    <p>
                    <strong>Goal:</strong>
                    {st.session_state.goal}
                    </p>

                    <p>
                    <strong>Expected Experience:</strong>
                    {st.session_state.experience} years
                    </p>

                    <p>
                    <strong>Learner Expectations:</strong>
                    <br><br>
                    {st.session_state.expectation}
                    </p>

                    <p>
                    <strong>Parent Name:</strong>
                    {st.session_state.parent_name}
                    </p>

                    <p>
                    <strong>Parent Email:</strong>
                    {st.session_state.parent_email}
                    </p>

                </div>

            </div>

        </div>

        </body>
        </html>
        """

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
            academic_buddy_email,
            msg.as_string()
        )

        server.quit()

    except Exception as e:

        print(e)

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

        msg["Cc"] = "debolinabhanjaofficial@gmail.com"

        msg["Subject"] = (
            "SmartLearn Connect Demo Confirmation"
        )

        html_body = f"""
        <html>

        <body style="
        font-family:Arial;
        background:#f5f7fb;
        padding:30px;
        ">

        <div style="
        max-width:650px;
        margin:auto;
        background:white;
        border-radius:22px;
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

        recipients = [

            parent_email,

            "debolinabhanjaofficial@gmail.com"
        ]

        server.sendmail(
            sender_email,
            recipients,
            msg.as_string()
        )

        server.quit()

        return True

    except Exception as e:

        print(e)

        return False

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet"href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
""", unsafe_allow_html=True)

# =========================================================
# CSS
# =========================================================


st.markdown("""
<style>
       
body{
font-family:'Poppins';
}

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
margin-bottom:25px;
box-shadow:0px 10px 35px rgba(0,0,0,0.08);
}

.nav-title{
font-size:34px;
font-weight:800;
color:white;
}

.nav-links{
font-size:18px;
font-weight:700;
color:white;
}

/* HERO */

.hero{
background:white;
padding:55px;
border-radius:30px;
box-shadow:0px 12px 40px rgba(0,0,0,0.08);
margin-bottom:25px;
animation:fadeUp 1s ease;
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
margin-top:18px;
color:#4b5563;
}

.tag{
display:inline-block;
padding:12px 22px;
background:#f8fbfc;
border-radius:30px;
margin-right:12px;
margin-top:20px;
font-weight:700;
color:#167b7f;
}

/* FORM */

.form-box{
background:white;
padding:35px;
border-radius:24px;
box-shadow:0px 12px 40px rgba(0,0,0,0.08);
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
font-weight:700;
border:none;
border-radius:14px;
height:50px;
padding:0px 26px;
}

.stButton>button:hover{
background:#ff8f38;
}

/* TEACHER CARD */

.teacher-card{
background:rgba(255,255,255,0.75);
backdrop-filter:blur(10px);
border:1px solid rgba(255,255,255,0.6);
border-radius:28px;
box-shadow:0 10px 30px rgba(0,0,0,0.04);
}

.teacher-name{
font-size:36px;
font-weight:800;
color:#1f2937;
font-family:'Poppins',sans-serif;
}

.teacher-desc{
font-size:17px;
line-height:1.9;
font-weight:500;
color:#4b5563;
max-width:92%;
}

.score{
font-size:54px;
font-weight:800;
color:#167b7f;
text-align:right;
}

.reason{
background:#f8fbfc;
padding:14px 18px;
border-left:6px solid #2fa4a9;
border-radius:12px;
margin-bottom:12px;
}

/* SUCCESS */

.success-card{
background:white;
padding:40px;
border-radius:24px;
margin-top:35px;
box-shadow:0px 12px 40px rgba(0,0,0,0.08);
border:2px solid #2fa4a9;
text-align:center;
animation:fadeUp 0.8s ease;
}

.success-title{
font-size:42px;
font-weight:800;
color:#167b7f;
margin-bottom:18px;
}

.success-sub{
font-size:20px;
line-height:1.8;
color:#4b5563;
}

.meet-btn{
display:inline-block;
background:#ff7a18;
padding:16px 28px;
border-radius:14px;
text-decoration:none;
color:white !important;
font-weight:700;
font-size:18px;
margin-top:25px;
}

/* ANIMATION */

@keyframes moveProgress{
0%{background-position:200% 0;}
100%{background-position:-200% 0;}
}

@keyframes fadeUp{
from{
opacity:0;
transform:translateY(30px);
}
to{
opacity:1;
transform:translateY(0px);
}
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
# PROGRESS LOOKUP
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

    back_col,_ = st.columns([1,8])

    with back_col:

        if st.session_state.step > 1:

            if st.button("⬅ Back"):

                st.session_state.step -= 1
                st.rerun()

    # STEP 1

    if st.session_state.step == 1:

        subject_list = []

        for item in teachers[
            "subject_specialization"
        ].dropna():

            parts = str(item).split("&")

            for p in parts:

                cleaned = p.strip()

                if cleaned not in subject_list:

                    subject_list.append(cleaned)

        subject_list = sorted(subject_list)

        selected_subject = st.selectbox(

            "Select Subject",

            subject_list,

            index=(
                subject_list.index(
                    st.session_state.subject
                )
                if st.session_state.subject
                in subject_list
                else None
            ),

            placeholder="Choose subject"
        )

        if selected_subject:

            if (
                st.session_state.subject
                != selected_subject
            ):

                st.session_state.subject = (
                    selected_subject
                )

                st.session_state.step = 2

                st.rerun()

    # STEP 2

    elif st.session_state.step == 2:

        boards = set()

        for b in teachers[
            "boards"
        ].dropna():

            boards.update(
                [
                    x.strip()
                    for x in str(b).split(",")
                ]
            )

        board_list = sorted(boards)

        selected_board = st.selectbox(

            "Select Curriculum Board",

            board_list,

            index=(
                board_list.index(
                    st.session_state.board
                )
                if st.session_state.board
                in board_list
                else None
            )
        )

        if selected_board:

            if (
                st.session_state.board
                != selected_board
            ):

                st.session_state.board = (
                    selected_board
                )

                st.session_state.step = 3

                st.rerun()

    # STEP 3

    elif st.session_state.step == 3:

        goals = [

            "Conceptual Understanding",

            "Exam Preparation",

            "Assignment Support",

            "Research Guidance"
        ]

        selected_goal = st.selectbox(

            "Learning Objective",

            goals,

            index=(
                goals.index(
                    st.session_state.goal
                )
                if st.session_state.goal
                in goals
                else None
            )
        )

        if selected_goal:

            if (
                st.session_state.goal
                != selected_goal
            ):

                st.session_state.goal = (
                    selected_goal
                )

                st.session_state.step = 4

                st.rerun()

    # STEP 4

    elif st.session_state.step == 4:

        experience = st.slider(

            "Minimum Teaching Experience",

            0,
            20,

            value=st.session_state.experience
        )

        st.session_state.experience = (
            experience
        )

        if st.button(
            "Continue"
        ):

            st.session_state.step = 5

            st.rerun()

    # STEP 5

    elif st.session_state.step == 5:

        expectation = st.text_area(

            "Describe learner expectations",

            value=st.session_state.expectation
        )

        st.session_state.expectation = (
            expectation
        )

        if st.button(
            "Generate Recommendations"
        ):

            with st.spinner(
                "Matching best tutors..."
            ):

                time.sleep(2)

            st.session_state.page = (
                "results"
            )

            st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <hr style="
    margin-top:30px;
    margin-bottom:30px;
    border:none;
    border-top:1px solid #e5e7eb;
    ">
    """, unsafe_allow_html=True)


# =========================================================
# RESULTS PAGE
# =========================================================

if st.session_state.page == "results":

    st.progress(1.0)

    st.write(
        "Profile completion: 100%"
    )

    st.markdown("""
    <h1 style="
    font-size:52px;
    font-weight:800;
    color:#1f2937;
    margin-top:20px;
    ">
    <i class="fa-solid fa-bullseye"></i> Top 3 Recommended Teachers
    </h1>
    """, unsafe_allow_html=True)

    ranked = []

    for _,teacher in teachers.iterrows():

        teacher_subjects = str(
            teacher[
                "subject_specialization"
            ]
        ).lower()

        student_subject = (
            st.session_state.subject
            .lower()
        )

        subject_score = 35 if (
            student_subject
            in teacher_subjects
        ) else 0

        board_score = 20 if (
            st.session_state.board.lower()
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
            ),

            str(
                teacher.get(
                    "field_of_study",
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

    # ==========================================
    # STRICT FILTER
    # ==========================================

    filtered_ranked = [

        r for r in ranked

        if r["final_score"] >= 80
    ]

    # ==========================================
    # FALLBACK FILTER
    # ==========================================

    if len(filtered_ranked) < 3:

        filtered_ranked = [

            r for r in ranked

            if r["final_score"] >= 70
        ]

    # ==========================================
    # FINAL SORT
    # ==========================================

    ranked = sorted(

        filtered_ranked,

        key=lambda x:
        x["final_score"],

        reverse=True

    )[:3]

    # ==========================================
    # NO MATCH FOUND
    # ==========================================

    if len(ranked) == 0:

        if "academic_alert_sent" not in st.session_state:

            send_academic_buddy_alert()

            st.session_state[
                "academic_alert_sent"
            ] = True

        reference_id = (
            "LC-"
            + datetime.now().strftime("%Y%m%d-%H%M%S")
        )

        no_match_html = f"""
        <div style="
        background:#fffdf8;
        border:1px solid #f4dfb3;
        border-radius:18px;
        overflow:hidden;
        margin-top:25px;
        font-family:'Poppins', sans-serif;
        ">

            <div style="
            background:#fff7e6;
            padding:20px 24px;
            border-bottom:1px solid #f4ead2;
            ">

                <div style="
                font-size:30px;
                font-weight:700;
                color:#374151;
                display:flex;
                align-items:center;
                gap:12px;
                ">

                ⚠️ No Exact Match Found

                </div>

            </div>

            <div style="
            padding:28px;
            ">

                <div style="
                font-size:20px;
                color:#4b5563;
                line-height:1.8;
                ">

                We are reviewing your request to ensure the best pedagogical alignment.

                <br><br>

                Your query need to be escalated to an Academic Buddy and it will be resolved within 12 working hours.

                </div>

                <div style="
                margin-top:24px;
                background:white;
                border:1px solid #e5e7eb;
                border-radius:14px;
                padding:18px;
                ">

                    <div style="
                    font-size:22px;
                    font-weight:700;
                    color:#4b5563;
                    ">

                    🔄 Status:
                    <span style="color:#374151;">

                    Under Priority Review

                    </span>

                    </div>

                    <div style="
                    margin-top:8px;
                    font-size:16px;
                    color:#6b7280;
                    ">

                    Reference ID:
                    {reference_id}

                    </div>

                </div>

            </div>

        </div>
        """

        components.html(
            no_match_html,
            height=340
        )

        st.markdown("### Connect with Academic Buddy")

        with st.form("academic_buddy_form"):

            parent_name = st.text_input(
                "Parent/Child Name"
            )

            parent_email = st.text_input(
                "Parent/Child Email"
            )

            submitted = st.form_submit_button(
                "Request Academic Buddy Support"
            )

            if submitted:

                parent_name = parent_name.strip()

                parent_email = parent_email.strip()

                if (
                    parent_name == ""
                    or parent_email == ""
                ):

                    st.error(
                        "Please fill all fields"
                    )

                else:

                    st.session_state[
                        "parent_name"
                    ] = parent_name

                    st.session_state[
                        "parent_email"
                    ] = parent_email

                    send_academic_buddy_alert()

                    st.success(
                        "Academic Buddy has been notified successfully."
                    )

        st.markdown("<br><br>", unsafe_allow_html=True)

        col1,col2,col3 = st.columns([2,2,2])

        with col2:

            if st.button(
                "Start New Search",
                use_container_width=True,
                key="restart_no_match"
            ):

                st.session_state.clear()

                st.rerun()

        st.stop()

    for teacher in ranked:

        teacher_name = teacher.get(
            "name",
            "Tutor"
        )

        score = int(
            min(
                teacher[
                    "final_score"
                ],
                98
            )
        )

        st.markdown(
            '<div class="teacher-card">',
            unsafe_allow_html=True
        )

        qualification = teacher.get(
            "highest_qualification",
            "Experienced Educator"
        )

        experience = teacher.get(
            "teaching_experience_years",
            "N/A"
        )

        field = teacher.get(
            "field_of_study",
            "Academic Mentoring"
        )

        teacher_desc = teacher.get(
            "description",
            ""
        )

        top_section = f"""
        <div style="
        position:relative;
        margin-bottom:20px;
        ">

            <div style="
            width:100%;
            ">

                <div style="
                font-size:34px;
                font-weight:800;
                color:#1f2937;
                margin-bottom:22px;
                font-family:'Poppins',sans-serif;
                ">

                <div style="
                display:flex;
                align-items:center;
                gap:14px;
                ">

                <i class="fa-solid fa-chalkboard-user"
                style="
                color:#0f766e;
                margin-right:10px;
                "></i>
                {teacher_name}

                </div>

                </div>

                <div style="
                display:flex;
                flex-wrap:wrap;
                gap:12px;
                margin-bottom:24px;
                ">

                    <div style="
                    background:#ecfeff;
                    color:#0f766e;
                    padding:10px 18px;
                    border-radius:30px;
                    font-size:14px;
                    font-weight:700;
                    ">

                    {qualification}

                    </div>

                    <div style="
                    background:#f8fafc;
                    color:#475569;
                    padding:10px 18px;
                    border-radius:30px;
                    font-size:14px;
                    font-weight:700;
                    ">

                    {experience} Years Experience

                    </div>

                    <div style="
                    background:#fff7ed;
                    color:#ea580c;
                    padding:10px 18px;
                    border-radius:30px;
                    font-size:14px;
                    font-weight:700;
                    ">

                    {field}

                    </div>

                </div>

                <div style="
                background:#fafafa;
                padding:28px 190px 28px 28px;
                border-radius:24px;
                border-left:6px solid #2fa4a9;
                border:1px solid #edf2f7;
                box-shadow:0px 6px 20px rgba(0,0,0,0.04);
                position:relative;
                min-height:auto;
                ">

                    <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:flex-start;
                    gap:24px;
                    margin-bottom:20px;
                    ">

                        <div style="
                        font-size:17px;
                        line-height:1.75;
                        color:#4b5563;
                        text-align:justify;
                        width:100%;
                        font-family:'Poppins',sans-serif;
                        ">

                        {teacher_desc}

                        </div>

                        <div style="
                        position:absolute;
                        right:36px;
                        top:0;
                        bottom:0;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        ">

                            <div style="
                            width:108px;
                            height:108px;
                            border-radius:28px;
                            background:linear-gradient(
                            135deg,
                            #14b8a6,
                            #0ea5e9
                            );
                            display:flex;
                            flex-direction:column;
                            align-items:center;
                            justify-content:center;
                            box-shadow:0px 12px 25px rgba(20,184,166,0.20);
                            ">

                                <div style="
                                font-size:32px;
                                font-weight:800;
                                color:white;
                                line-height:1;
                                font-family:'Poppins',sans-serif;
                                ">

                                {score}%

                                </div>

                                <div style="
                                margin-top:8px;
                                font-size:11px;
                                letter-spacing:1px;
                                color:white;
                                font-weight:700;
                                text-transform:uppercase;
                                font-family:'Poppins',sans-serif;
                                ">

                                Match

                                </div>

                            </div>

                        </div>

                    </div>

                </div>

            </div>

        </div>
        """

        desc_length = len(teacher_desc)

        if desc_length < 350:
            dynamic_height = 220

        elif desc_length < 550:
            dynamic_height = 255

        elif desc_length < 750:
            dynamic_height = 290

        else:
            dynamic_height = 340

        components.html(
            top_section,
            height=dynamic_height,
            scrolling=False
        )

        recommendation_items = []

        if teacher["subject_score"] > 0:

            recommendation_items.append(
                ("fa-book-open", "Subject Alignment"),
            )

        if teacher["board_score"] > 0:

            recommendation_items.append(
                ("fa-school", "Curriculum Compatibility")
            )

        if teacher["exp_score"] > 0:

            recommendation_items.append(
                ("fa-star", "Experience Match")
            )

        if teacher["semantic_score"] > 0:

            recommendation_items.append(
                ("fa-brain", "Learner Expectation Match")
            )

        recommendation_html = """
        <link rel="stylesheet"href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        <div style="
        font-family:'Poppins', sans-serif;
        ">

        <div style="
        font-size:22px;
        font-weight:700;
        color:#374151;
        margin-bottom:16px;
        ">

        Why Recommended

        </div>

        <div style="
        display:grid;
        grid-template-columns:1fr 1fr;
        gap:14px;
        margin-bottom:8px;
        ">
        """

        for icon, label in recommendation_items:

            recommendation_html += f"""
            <div style="
            background:#f8fbfc;
            border:1px solid #e2e8f0;
            border-radius:16px;
            padding:12px 16px;
            display:flex;
            align-items:center;
            gap:12px;
            ">

                <div style="
                width:34px;
                height:34px;
                border-radius:12px;
                background:#e8faf8;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:18px;
                ">

                <i class="fa-solid {icon}"
                style="
                color:#0f766e;
                font-size:16px;
                "></i>

                </div>

                <div style="
                font-size:16px;
                font-weight:600;
                color:#374151;
                font-family:'Poppins',sans-serif;
                ">

                {label}

                </div>

            </div>
            """

        recommendation_html += "</div></div>"

        card_count = len(
            recommendation_items
        )

        dynamic_height = 170

        if card_count > 2:

            dynamic_height = 190

        components.html(
            recommendation_html,
            height=dynamic_height,
            scrolling=False
        )

        with st.expander(
            f"📅 Book Demo with {teacher_name}"
        ):

                with st.form(
                    key=f"demo_form_{teacher_name}"
                ):

                    parent_name = st.text_input(
                        "Parent/Child Name",
                        key=f"name_{teacher_name}"
                    )

                    parent_email = st.text_input(
                        "Parent/Child Email",
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

                    # =====================================================
                    # ALREADY BOOKED
                    # =====================================================

                    if already_booked:

                        st.form_submit_button(
                            "Demo Already Booked",
                            disabled=True
                        )

                        if (
                            st.session_state.booked_teacher
                            == teacher_name
                        ):

                            scheduled_card = f"""
                            <div style="
                            background:#f8fbfc;
                            border:1px solid #e5e7eb;
                            border-radius:16px;
                            padding:20px;
                            margin-top:18px;
                            font-family:'Poppins', sans-serif;
                            ">

                                <div style="
                                display:flex;
                                align-items:center;
                                gap:14px;
                                ">

                                    <div style="
                                    width:44px;
                                    height:44px;
                                    border-radius:12px;
                                    background:#e8faf8;
                                    display:flex;
                                    align-items:center;
                                    justify-content:center;
                                    font-size:22px;
                                    color:#167b7f;
                                    flex-shrink:0;
                                    ">

                                    📅

                                    </div>

                                    <div>

                                        <div style="
                                        font-size:24px;
                                        font-weight:700;
                                        color:#374151;
                                        font-family:'Poppins',sans-serif;
                                        line-height:1.3;
                                        ">

                                        Demo Scheduled:
                                        <span style="
                                        color:#4b5563;
                                        font-weight:600;
                                        ">

                                        {st.session_state.booked_date}

                                        at

                                        {st.session_state.booked_time}

                                        </span>

                                        </div>

                                        <div style="
                                        margin-top:6px;
                                        font-size:17px;
                                        color:#6b7280;
                                        ">

                                        Confirmed with
                                        <strong>
                                        {st.session_state.booked_teacher}
                                        </strong>

                                        </div>

                                        <div style="
                                        margin-top:6px;
                                        font-size:15px;
                                        color:#9ca3af;
                                        ">

                                        Confirmation email sent successfully.

                                        </div>

                                    </div>

                                </div>

                            </div>
                            """

                            components.html(
                            scheduled_card,
                            height=135
                            )

                    # =====================================================
                    # NEW BOOKING
                    # =====================================================

                    else:

                        submitted = st.form_submit_button(
                            f"Confirm Demo with {teacher_name}"
                        )

                        if submitted:

                            parent_name = parent_name.strip()

                            parent_email = parent_email.strip()

                            if (
                                parent_name == ""
                                or parent_email == ""
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


# =========================================================
# RESET
# =========================================================

st.divider()

if st.button(
    "Start New Search"
):

    st.session_state.clear()
    st.rerun()