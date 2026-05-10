# =========================================================
# SMARTLEARN CONNECT
# FINAL CLEAN VERSION
# =========================================================

import streamlit as st
import pandas as pd
import time
import smtplib
import streamlit.components.v1 as components

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

        msg = MIMEMultipart("alternative")

        msg["From"] = sender_email

        msg["To"] = parent_email

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

.teacher-card{
background:white;
padding:35px;
border-radius:24px;
box-shadow:0px 10px 35px rgba(0,0,0,0.08);
margin-bottom:35px;
}

.teacher-name{
font-size:36px;
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

.stButton>button{
background:#ff7a18;
color:white;
border:none;
border-radius:14px;
height:50px;
font-weight:700;
}

.stButton>button:hover{
background:#ff8f38;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# RESULTS PAGE
# =========================================================

st.title(
    "🎯 Top 3 Recommended Teachers"
)

ranked = []

for _,teacher in teachers.iterrows():

    teacher_subjects = str(
        teacher["subject_specialization"]
    ).lower()

    student_subject = str(
    st.session_state.subject or "").lower()

    subject_score = 35 if (
        student_subject
        in teacher_subjects
    ) else 0

    board_score = 20 if (
    str(
        st.session_state.board or ""
    ).lower()
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

    st.markdown(
        '<div class="teacher-card">',
        unsafe_allow_html=True
    )

    left,right = st.columns([5,1])

    with left:

        st.markdown(f"""
        <div class="teacher-name">

        {teacher_name}

        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="teacher-desc">

        {teacher.get('description','')}

        </div>
        """, unsafe_allow_html=True)

    with right:

        st.markdown(f"""
        <div class="score">

        {score}%

        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        "### Why recommended"
    )

    if teacher["subject_score"] > 0:

        st.markdown("""
        <div class="reason">
        ✓ Subject Alignment
        </div>
        """, unsafe_allow_html=True)

    if teacher["board_score"] > 0:

        st.markdown("""
        <div class="reason">
        ✓ Curriculum Compatibility
        </div>
        """, unsafe_allow_html=True)

    if teacher["exp_score"] > 0:

        st.markdown("""
        <div class="reason">
        ✓ Experience Match
        </div>
        """, unsafe_allow_html=True)

    if teacher["semantic_score"] > 0:

        st.markdown("""
        <div class="reason">
        ✓ Learner Expectation Match
        </div>
        """, unsafe_allow_html=True)

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
                font-family:'Source Sans Pro', sans-serif;
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

                st.components.v1.html(
                    scheduled_card,
                    height=120
                )

        else:

            if st.button(

                f"Confirm Demo with {teacher_name}",

                key=f"confirm_{teacher_name}"
            ):

                parent_name = (
                    parent_name.strip()
                )

                parent_email = (
                    parent_email.strip()
                )

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

    st.markdown(
        "</div>",
        unsafe_allow_html=True
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