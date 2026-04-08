import streamlit as st
from auth import signup, login
from career_engine import analyze_skills
import base64

def set_bg(image):
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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# LOGIN
if not st.session_state.logged_in:

    set_bg("assets/login_bg.jpg")

    st.title("SkillImprove")

    option = st.selectbox("Choose", ["Login", "Signup"])

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

# DASHBOARD
else:

    set_bg("assets/dashboard_bg.jpg")

    user = st.session_state.user

    st.title(f"Welcome {user['name']}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    skills_input = st.text_input("Enter skills")

    if st.button("Analyze"):
        skills = skills_input.split(",")

        careers, courses, materials, projects = analyze_skills(skills)

        st.subheader("Careers")
        for c in careers:
            st.write("-", c)

        st.subheader("Courses")
        for c in courses:
            st.markdown(f"[Open]({c})")

        st.subheader("Materials")
        for m in materials:
            st.markdown(f"[Read]({m})")

        st.subheader("Projects")
        for p in projects:
            st.write("-", p)
