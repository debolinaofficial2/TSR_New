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
# LOAD SEMANTIC MODEL
# ------------------------------------------------

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()


# ------------------------------------------------
# SESSION STATE CONTROL
# ------------------------------------------------

if "step" not in st.session_state:
    st.session_state.step = 1

if "page" not in st.session_state:
    st.session_state.page = "form"


# ------------------------------------------------
# GLOBAL CSS (TUTRAIN BRANDING + MOTION UI)
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


/* PROGRESS PANEL */

.intake-panel {
background: rgba(255,255,255,0.95);
padding:28px;
border-radius:18px;
box-shadow:0px 12px 35px rgba(0,0,0,0.12);
animation: glowPanel 3s infinite ease-in-out;
}


/* PROGRESS BAR SHIMMER */

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
animation:pulseScore 2s infinite;
}


/* DESCRIPTION */

.description{
font-size:16px;
color:#4b5563;
margin-top:6px;
}


/* WHY SECTION */

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
animation:slideIn 0.6s ease-in;
}


/* CTA BUTTON */

.cta-button{
background:#ff7a18;
padding:12px 22px;
border-radius:10px;
color:white;
font-weight:600;
display:inline-block;
margin-top:14px;
text-decoration:none;
transition:0.3s ease;
}

.cta-button:hover{
background:#e66a0f;
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

@keyframes pulseScore {
0%{opacity:1;}
50%{opacity:.6;}
100%{opacity:1;}
}

@keyframes glowPanel {
0%{box-shadow:0px 12px 35px rgba(0,0,0,0.12);}
50%{box-shadow:0px 12px 55px rgba(47,164,169,0.35);}
100%{box-shadow:0px 12px 35px rgba(0,0,0,0.12);}
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

@keyframes slideIn{
from{opacity:0; transform:translateX(-12px);}
to{opacity:1; transform:translateX(0);}
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
# FORM PAGE
# ------------------------------------------------

if st.session_state.page == "form":

    TOTAL_STEPS = 5

    progress = min((st.session_state.step - 1)/TOTAL_STEPS,1.0)

    st.markdown('<div class="intake-panel">', unsafe_allow_html=True)

    st.progress(progress)

    st.write(f"Profile completion: {int(progress*100)}%")


    if st.session_state.step == 1:

        subject = st.selectbox(
            "Select subject",
            sorted(teachers["subject"].dropna().unique())
        )

        if subject:

            st.session_state.subject = subject
            st.session_state.step = 2
            st.rerun()


    elif st.session_state.step == 2:

        boards=set()

        for b in teachers["boards"].dropna():
            boards.update([x.strip() for x in b.split(",")])

        board = st.selectbox(
            "Select curriculum board",
            sorted(boards)
        )

        if board:

            st.session_state.board = board
            st.session_state.step = 3
            st.rerun()


    elif st.session_state.step == 3:

        goal = st.selectbox(
            "Learning objective",
            [
                "Conceptual Understanding",
                "Exam Preparation",
                "Assignment Support",
                "Research Guidance"
            ]
        )

        if goal:

            st.session_state.goal = goal
            st.session_state.step = 4
            st.rerun()


    elif st.session_state.step == 4:

        exp = st.slider(
            "Minimum experience required",
            0,20,5
        )

        st.session_state.experience = exp
        st.session_state.step = 5
        st.rerun()


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

        score = int(min(teacher["score"], 100))


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


        st.markdown(
            f'<a class="cta-button">📅 Book Demo with {teacher["name"]}</a>',
            unsafe_allow_html=True
        )


        st.markdown('</div>', unsafe_allow_html=True)