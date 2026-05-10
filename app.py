import streamlit as st
import pandas as pd
import time
from sentence_transformers import SentenceTransformer, util


# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="SmartLearn Connect",
    layout="wide"
)


# ------------------------------------------------
# SESSION STATE INIT
# ------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "form"

if "step" not in st.session_state:
    st.session_state.step = 1


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
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()


# ------------------------------------------------
# GLOBAL CSS
# ------------------------------------------------

st.markdown("""
<style>

/* NAVBAR */

.navbar {
background: linear-gradient(270deg,#2fa4a9,#1e7f80,#2fa4a9);
background-size:400% 400%;
animation: gradientMove 8s ease infinite;
padding:18px 40px;
border-radius:14px;
color:white;
font-size:22px;
font-weight:600;
display:flex;
justify-content:space-between;
}


/* HERO TITLE */

.hero-title {
font-size:56px;
font-weight:700;
color:#1f2937;
animation: floatTitle 4s ease-in-out infinite;
}

.highlight {
color:#ff7a18;
}


/* PANEL */

.intake-panel {
background:white;
padding:28px;
border-radius:18px;
box-shadow:0px 12px 35px rgba(0,0,0,0.12);
}


/* PROGRESS BAR */

div[data-testid="stProgress"] > div > div > div {
background: linear-gradient(
90deg,
#2fa4a9,
#6be0da,
#2fa4a9
);
background-size:200% 100%;
animation: shimmer 2s linear infinite;
}


/* RECOMMENDATION CARD */

.recommendation-container{
background:#ffffff;
padding:32px;
border-radius:18px;
box-shadow:0px 10px 40px rgba(0,0,0,0.08);
margin-bottom:28px;
animation:fadeIn 0.8s ease-in;
}


/* TEACHER NAME */

.teacher-name{
font-size:26px;
font-weight:600;
color:#1f2937;
}


/* SCORE */

.score{
font-size:42px;
font-weight:700;
color:#2fa4a9;
text-align:right;
}


/* DESCRIPTION */

.description{
font-size:16px;
color:#4b5563;
margin-top:6px;
}


/* SECTION */

.section-title{
font-size:18px;
font-weight:600;
margin-top:18px;
margin-bottom:10px;
color:#111827;
}


/* MATCH ROW */

.reason-row{
background:#f8fafc;
border-left:5px solid #2fa4a9;
padding:12px 16px;
border-radius:10px;
margin-bottom:10px;
font-size:15px;
color:#374151;
}


/* BUTTONS */

.stButton>button {
background:#ff7a18;
color:white;
border-radius:10px;
font-weight:600;
height:45px;
border:none;
}


/* ANIMATIONS */

@keyframes gradientMove {
0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}
}

@keyframes shimmer {
0%{background-position:200% 0;}
100%{background-position:-200% 0;}
}

@keyframes fadeIn {
from{opacity:0;}
to{opacity:1;}
}

@keyframes floatTitle {
0%{transform:translateY(0);}
50%{transform:translateY(-6px);}
100%{transform:translateY(0);}
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------
# NAVBAR
# ------------------------------------------------

st.markdown("""
<div class="navbar">
<span>🎓 SmartLearn Connect</span>
<span>Home &nbsp;&nbsp; Academic &nbsp;&nbsp; Exam Prep &nbsp;&nbsp; Mentors</span>
</div>
""", unsafe_allow_html=True)


# ------------------------------------------------
# HERO SECTION
# ------------------------------------------------

left, right = st.columns([1.2,1])

with left:

    st.markdown("""
<div class="hero-title">
Find the Right <span class="highlight">Tutor Match</span><br>
for Your Child Instantly
</div>
""", unsafe_allow_html=True)

with right:

    st.image(
        "https://images.unsplash.com/photo-1588072432836-e10032774350",
        use_container_width=True
    )


# ------------------------------------------------
# PROGRESS BAR
# ------------------------------------------------

progress_lookup = {
    1: 0.0,
    2: 0.2,
    3: 0.4,
    4: 0.6,
    5: 0.8
}


# ------------------------------------------------
# FORM PAGE
# ------------------------------------------------

if st.session_state.page == "form":

    progress = progress_lookup.get(st.session_state.step, 0)

    st.markdown('<div class="intake-panel">', unsafe_allow_html=True)

    st.progress(progress)

    st.write(f"Profile completion: {int(progress*100)}%")


    # STEP 1

    if st.session_state.step == 1:

        subject = st.selectbox(
            "Select subject",
            sorted(teachers["subject"].dropna().unique()),
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
            boards.update([x.strip() for x in b.split(",")])

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

        if st.button("Generate Recommendations"):

            st.session_state.expectation = expectation

            with st.spinner("Matching best tutors using AI engine..."):

                time.sleep(2)

            st.session_state.page = "results"

            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------
# RESULTS PAGE
# ------------------------------------------------

if st.session_state.page == "results":

    st.progress(1.0)

    st.write("Profile completion: 100%")

    st.markdown("## 🎯 Top 3 Recommended Teachers")


    student = {
        "subject": st.session_state.subject,
        "board": st.session_state.board,
        "experience": st.session_state.experience
    }


    ranked = []


    for _, teacher in teachers.iterrows():

        subject_score = 35 if student["subject"] in teacher["subject_specialization"] else 0

        board_score = 20 if student["board"] in teacher["boards"] else 0

        exp_score = 10 if teacher["teaching_experience_years"] >= student["experience"] else 0


        teacher_profile = " ".join([
            str(teacher["description"]),
            str(teacher["highest_qualification"]),
            str(teacher["field_of_study"])
        ])


        semantic = util.cos_sim(
            model.encode(st.session_state.expectation),
            model.encode(teacher_profile)
        ).item()

        semantic = ((semantic + 1) / 2) * 30


        total = subject_score + board_score + exp_score + semantic


        teacher_dict = teacher.to_dict()

        teacher_dict["score"] = total

        teacher_dict["reasons"] = {
            "Subject alignment": subject_score,
            "Curriculum familiarity": board_score,
            "Matches experience requirement": exp_score,
            "Aligned with learner expectations": semantic
        }

        ranked.append(teacher_dict)


    ranked = sorted(ranked, key=lambda x: x["score"], reverse=True)[:3]


    for teacher in ranked:

        score = int(min(teacher["score"],100))

        st.markdown('<div class="recommendation-container">', unsafe_allow_html=True)

        left, right = st.columns([5,1])

        with left:

            st.markdown(
                f'<div class="teacher-name">👩‍🏫 {teacher["name"]}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="description">{teacher["description"]}</div>',
                unsafe_allow_html=True
            )

        with right:

            st.markdown(
                f'<div class="score">{score}%</div>',
                unsafe_allow_html=True
            )


        st.markdown(
            '<div class="section-title">Why recommended</div>',
            unsafe_allow_html=True
        )


        for label, val in teacher["reasons"].items():

            if val > 0:

                confidence = int((val / 35) * 100)

                st.markdown(
                    f'<div class="reason-row">{confidence}% — {label}</div>',
                    unsafe_allow_html=True
                )


        # ------------------------------------------------
        # BOOK DEMO SECTION
        # ------------------------------------------------

        with st.expander(f"📅 Book Demo with {teacher['name']}"):

            parent_name = st.text_input(
                "Parent Name",
                key=f"name_{teacher['name']}"
            )

            parent_email = st.text_input(
                "Parent Email",
                key=f"email_{teacher['name']}"
            )

            selected_date = st.date_input(
                "Preferred Date",
                key=f"date_{teacher['name']}"
            )

            selected_time = st.time_input(
                "Preferred Time",
                key=f"time_{teacher['name']}"
            )


            if st.button(
                f"Confirm Demo with {teacher['name']}",
                key=f"confirm_{teacher['name']}"
            ):

                with st.spinner("Booking your demo session..."):

                    time.sleep(2)

                st.success("Demo booked successfully!")

                st.markdown("### 📍 Google Meet Link")

                st.markdown(
                    "[Join Google Meet](https://meet.google.com/ypj-jhkz-gta)"
                )

                st.info(
                    f"""
Demo details sent successfully.

Teacher: {teacher['name']}
Date: {selected_date}
Time: {selected_time}
Meeting Link:
https://meet.google.com/ypj-jhkz-gta
"""
                )

        st.markdown('</div>', unsafe_allow_html=True)


    st.divider()


    if st.button("Start New Search"):

        st.session_state.clear()

        st.rerun()