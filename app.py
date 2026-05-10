# ------------------------------------------------
# IMPORTS
# ------------------------------------------------

import streamlit as st
import pandas as pd
import time
import smtplib

from sentence_transformers import SentenceTransformer, util
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="SmartLearn Connect",
    layout="wide"
)


# ------------------------------------------------
# SESSION STATES
# ------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "form"

if "step" not in st.session_state:
    st.session_state.step = 1

if "show_popup" not in st.session_state:
    st.session_state.show_popup = False

if "global_booking_done" not in st.session_state:
    st.session_state.global_booking_done = False


# ------------------------------------------------
# LOAD DATASET
# ------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_excel("Dataset_TSR.xlsx")

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


teachers = load_data()


# ------------------------------------------------
# LOAD MODEL
# ------------------------------------------------

@st.cache_resource
def load_model():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


model = load_model()


# ------------------------------------------------
# EMAIL FUNCTION
# ------------------------------------------------

def send_demo_email(
    parent_name,
    parent_email,
    teacher_name,
    selected_date,
    selected_time
):

    try:

        parent_email = parent_email.strip()

        sender_email = "debolinaofficial1@gmail.com"

        sender_password = st.secrets["EMAIL_PASSWORD"]

        meet_link = (
            "https://meet.google.com/ypj-jhkz-gta"
        )

        subject = (
            "SmartLearn Connect Demo Confirmation"
        )

        body = f"""
Hello {parent_name},

Your demo session has been booked successfully.

Teacher: {teacher_name}

Date: {selected_date}

Time: {selected_time}

Google Meet Link:
{meet_link}

Regards,
SmartLearn Connect
"""

        msg = MIMEMultipart()

        msg["From"] = sender_email

        msg["To"] = parent_email

        msg["Subject"] = subject

        msg.attach(
            MIMEText(body, "plain")
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


# ------------------------------------------------
# CSS
# ------------------------------------------------

st.markdown("""
<style>

/* APP */

.main {
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
border-radius:18px;
display:flex;
justify-content:space-between;
align-items:center;
box-shadow:0px 10px 30px rgba(0,0,0,0.08);
animation:navbarGlow 6s ease infinite;
}

.nav-title{
font-size:32px;
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
padding:50px;
border-radius:26px;
margin-top:25px;
box-shadow:0px 12px 40px rgba(0,0,0,0.08);
overflow:hidden;
}

.hero-title{
font-size:68px;
font-weight:800;
line-height:1.1;
color:#1f2937;
animation:floatTitle 4s ease infinite;
}

.highlight{
color:#ff7a18;
}

.hero-sub{
font-size:22px;
margin-top:20px;
color:#4b5563;
}


/* TAGS */

.tag{
display:inline-block;
padding:12px 22px;
border-radius:30px;
background:#f8fbfc;
margin-right:10px;
margin-top:22px;
font-weight:700;
color:#167b7f;
box-shadow:0px 5px 15px rgba(0,0,0,0.05);
}


/* FORM */

.form-box{
background:white;
padding:35px;
border-radius:24px;
margin-top:25px;
box-shadow:0px 12px 40px rgba(0,0,0,0.08);
animation:fadeIn 0.8s ease;
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
animation:progressMove 2s linear infinite;
height:18px;
border-radius:20px;
}


/* RECOMMENDATION CARD */

.teacher-card{
background:white;
padding:35px;
border-radius:24px;
box-shadow:0px 12px 35px rgba(0,0,0,0.08);
margin-bottom:30px;
animation:cardUp 0.8s ease;
border:1px solid #edf2f7;
}

.teacher-name{
font-size:34px;
font-weight:800;
color:#1f2937;
}

.teacher-desc{
font-size:17px;
line-height:1.8;
color:#4b5563;
margin-top:12px;
}

.score{
font-size:52px;
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


/* BUTTONS */

.stButton>button{
background:#ff7a18;
color:white;
font-weight:700;
border:none;
border-radius:14px;
height:50px;
padding:0px 26px;
transition:0.3s;
}

.stButton>button:hover{
transform:translateY(-2px);
background:#ff8f38;
}


/* POPUP */

.popup-overlay{
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background:rgba(0,0,0,0.55);
backdrop-filter:blur(8px);
display:flex;
justify-content:center;
align-items:center;
z-index:999999;
animation:fadeOverlay 0.4s ease;
}

.popup-modal{
width:650px;
background:linear-gradient(
135deg,
#2fa4a9,
#167b7f
);
padding:55px;
border-radius:30px;
text-align:center;
box-shadow:0px 25px 80px rgba(0,0,0,0.35);
animation:popupScale 0.4s ease;
}

.popup-title{
font-size:46px;
font-weight:800;
color:white;
margin-bottom:18px;
}

.popup-sub{
font-size:21px;
color:white;
line-height:1.7;
margin-bottom:35px;
}

.popup-btn{
display:inline-block;
background:white;
color:#167b7f !important;
padding:16px 30px;
border-radius:14px;
font-size:18px;
font-weight:800;
text-decoration:none;
}


/* ANIMATIONS */

@keyframes popupScale{
from{
opacity:0;
transform:scale(0.75);
}
to{
opacity:1;
transform:scale(1);
}
}

@keyframes fadeOverlay{
from{opacity:0;}
to{opacity:1;}
}

@keyframes cardUp{
from{
opacity:0;
transform:translateY(20px);
}
to{
opacity:1;
transform:translateY(0px);
}
}

@keyframes progressMove{
0%{background-position:200% 0;}
100%{background-position:-200% 0;}
}

@keyframes floatTitle{
0%{transform:translateY(0px);}
50%{transform:translateY(-10px);}
100%{transform:translateY(0px);}
}

@keyframes navbarGlow{
0%{filter:brightness(1);}
50%{filter:brightness(1.08);}
100%{filter:brightness(1);}
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------
# NAVBAR
# ------------------------------------------------

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


# ------------------------------------------------
# HERO
# ------------------------------------------------

left, right = st.columns([1.2,1])

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


# ------------------------------------------------
# PROGRESS LOOKUP
# ------------------------------------------------

progress_lookup = {
    1:0.0,
    2:0.2,
    3:0.4,
    4:0.6,
    5:0.8
}


# ------------------------------------------------
# FORM PAGE
# ------------------------------------------------

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

            st.session_state.page = (
                "results"
            )

            st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ------------------------------------------------
# RESULTS PAGE
# ------------------------------------------------

if st.session_state.page == "results":

    st.progress(1.0)

    st.write(
        "Profile completion: 100%"
    )

    st.markdown(
        "## 🎯 Top 3 Recommended Teachers"
    )

    student = {
        "subject":
        st.session_state.subject,

        "board":
        st.session_state.board,

        "experience":
        st.session_state.experience
    }

    ranked = []


    for _, teacher in teachers.iterrows():

        subject_score = 35 if (
            student["subject"]
            in str(
                teacher[
                    "subject_specialization"
                ]
            )
        ) else 0

        board_score = 20 if (
            student["board"]
            in str(
                teacher["boards"]
            )
        ) else 0

        exp_score = 10 if (
            teacher[
                "teaching_experience_years"
            ]
            >= student["experience"]
        ) else 0


        teacher_profile = " ".join([

            str(teacher["description"]),

            str(
                teacher[
                    "highest_qualification"
                ]
            ),

            str(
                teacher[
                    "field_of_study"
                ]
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
        ) * 30


        total = (
            subject_score
            + board_score
            + exp_score
            + semantic
        )

        teacher_dict = (
            teacher.to_dict()
        )

        teacher_dict["score"] = total

        teacher_dict["reasons"] = {

            "Subject alignment":
            subject_score,

            "Curriculum familiarity":
            board_score,

            "Experience alignment":
            exp_score,

            "Learner expectation match":
            semantic
        }

        ranked.append(
            teacher_dict
        )


    ranked = sorted(
        ranked,
        key=lambda x:x["score"],
        reverse=True
    )[:3]


    for teacher in ranked:

        teacher_name = teacher["name"]

        score = int(
            min(
                teacher["score"],
                100
            )
        )

        st.markdown(
            '<div class="teacher-card">',
            unsafe_allow_html=True
        )

        left, right = st.columns([5,1])

        with left:

            st.markdown(
                f"""
                <div class="teacher-name">
                👩‍🏫 {teacher_name}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="teacher-desc">
                {teacher["description"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        with right:

            st.markdown(
                f"""
                <div class="score">
                {score}%
                </div>
                """,
                unsafe_allow_html=True
            )


        st.markdown(
            "### Why recommended"
        )

        for label,val in (
            teacher["reasons"]
            .items()
        ):

            if val > 0:

                confidence = int(
                    (val/35)*100
                )

                st.markdown(
                    f"""
                    <div class="reason">
                    {confidence}% — {label}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


        # ----------------------------------------
        # BOOK DEMO
        # ----------------------------------------

        with st.expander(
            f"📅 Book Demo with {teacher_name}"
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
                key=f"date_{teacher_name}"
            )

            selected_time = st.time_input(
                "Preferred Time",
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

                            st.session_state.global_booking_done = True

                            st.session_state.show_popup = True

                            st.rerun()

                        else:

                            st.error(
                                "Email sending failed"
                            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# ------------------------------------------------
# POPUP MODAL
# ------------------------------------------------

if st.session_state.show_popup:

    st.markdown(
        """
        <div class="popup-overlay">

            <div class="popup-modal">

                <div class="popup-title">
                ✅ Demo Booked Successfully!
                </div>

                <div class="popup-sub">
                Demo confirmation email has been
                sent successfully.
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
        """,
        unsafe_allow_html=True
    )

    _,center,_ = st.columns([2,1,2])

    with center:

        if st.button("Close"):

            st.session_state.show_popup = False

            st.rerun()


# ------------------------------------------------
# RESET
# ------------------------------------------------

st.divider()

if st.button("Start New Search"):

    st.session_state.clear()

    st.rerun()