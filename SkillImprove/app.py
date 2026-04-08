import streamlit as st
from auth import signup, login
from career_engine import analyze_skills
import base64
import os

# ---------- SAFE BACKGROUND FUNCTION ---------- #
def set_bg(image):
    if not os.path.exists(image):
        st.warning(f"Image not found: {image}")
        return

    with open(image, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---------- BASE PATH ---------- #
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

login_img = os.path.join(BASE_DIR, "assets", "login_bg.jpg")
dashboard_img = os.path.join(BASE_DIR, "assets", "dashboard_bg.jpg")

# ---------- SESSION ---------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------- LOGIN / SIGNUP PAGE ---------- #
if not st.session_state.logged_in:

    set_bg(login_img)

    st.title("SkillImprove")

    option = st.selectbox("Choose", ["Login", "Signup"])

    # -------- SIGNUP -------- #
    if option == "Signup":
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        password = st.text_input("Password", type="password")

        if st.button("Signup"):
            success, msg = signup(name, email, phone, password)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    # -------- LOGIN -------- #
    else:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            success, user = login(email, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid credentials")

# ---------- DASHBOARD ---------- #
else:

    set_bg(dashboard_img)

    user = st.session_state.user

    st.title(f"Welcome {user['name']}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    skills_input = st.text_input("Enter skills (comma separated)")

    if st.button("Analyze"):
        skills = skills_input.split(",")

        careers, courses, materials, projects = analyze_skills(skills)

        # -------- CAREERS -------- #
        st.subheader("Careers")
        for c in careers:
            st.write("-", c)

        # -------- COURSES -------- #
        st.subheader("Courses")
        for c in courses:
            st.markdown(f"[Open]({c})")
            st.write(c)
            st.write("---")

        # -------- MATERIALS -------- #
        st.subheader("Materials")
        for m in materials:
            st.markdown(f"[Read]({m})")
            st.write(m)
            st.write("---")

        # -------- PROJECTS -------- #
        st.subheader("Projects")
        for p in projects:
            st.write("-", p)
