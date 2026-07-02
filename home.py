import streamlit as st
from PIL import Image
import os

# ======================================
# CONFIG
# ======================================
st.set_page_config(
    page_title="LIET Smart ERP Portal",
    page_icon="🎓",
    layout="wide"
)

# ======================================
# CSS DESIGN
# ======================================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(140deg, #e0f7fa, #e3f2fd, #ede7f6);
}

/* HERO */
.hero {
    text-align:center;
    padding:40px;
    border-radius:20px;
    background: linear-gradient(135deg,#003366,#0056b3,#00bcd4);
    color:white;
    box-shadow:0px 10px 25px rgba(0,0,0,0.2);
}

/* CARD */
.card {
    padding:20px;
    border-radius:15px;
    background:white;
    box-shadow:0px 5px 15px rgba(0,0,0,0.1);
}

/* CONTACT */
.contact-card {
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0px 8px 20px rgba(0,0,0,0.15);
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg,#0056b3,#00bcd4);
    color:white;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ======================================
# SIDEBAR MENU (MAIN NAVIGATION)
# ======================================
st.sidebar.title("🎓 LIET ERP MENU")

menu = st.sidebar.selectbox(
    "Navigate",
    [
        "🏠 Home",
        "🏫 About",
        "📚 Courses",
        "📞 Contact",
      
    ]
)

st.sidebar.divider()

# SIDEBAR ERP BUTTONS
st.sidebar.subheader("🚀 ERP Access")

st.sidebar.link_button(
    "🎓 Student ERP",
    "https://training-performance-liet-erp-std1.streamlit.app/"
)

st.sidebar.link_button(
    "👨‍💼 Admin ERP",
    "https://training-performance-liet-dash1.streamlit.app/"
)

st.sidebar.divider()

st.sidebar.info("LIET Smart ERP System 2026")

# ======================================
# HEADER
# ======================================
col1, col2 = st.columns([1, 6])

with col1:
    if os.path.exists("assets/mllogo.png"):
        st.image("assets/mllogo.png", width=80)

with col2:
    st.title("LLOYD INSTITUTE OF ENGINEERING & TECHNOLOGY")
    st.caption("Greater Noida, Uttar Pradesh")

st.divider()

# ======================================
# HOME PAGE
# ======================================
if menu == "🏠 Home":

    st.markdown("""
    <div class="hero">
        <h1>🎓 LIET SMART ERP PORTAL</h1>
        <h3>AI Powered Academic Management System</h3>
        <p>Learn • Analyze • Improve</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.success("Welcome to LIET ERP Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Students", "1200+")
    c2.metric("Courses", "12")
    c3.metric("Attendance", "87%")
    c4.metric("Placements", "450+")

# ======================================
# ABOUT
# ======================================
elif menu == "🏫 About":

    st.header("🏫 About LIET")

    c1, c2 = st.columns([2, 3])

    with c1:
        if os.path.exists("assets/avatar.png"):
            st.image("assets/avatar.png")

    with c2:
        st.write("""
LIET focuses on modern technical education with AI, ML, Data Science.

✔ Quality Education  
✔ Practical Learning  
✔ Industry Exposure  
✔ ERP Based Training System  
        """)

# ======================================
# COURSES
# ======================================
elif menu == "📚 Courses":

    st.header("📚 Courses Offered")

    st.success("""
    - B.Tech Computer Science
    - B.Tech AI & ML
    - B.Tech Data Science
    - MBA
    - Diploma Engineering
    """)

    st.info("Industry oriented curriculum with AI integration")

# ======================================
# CONTACT
# ======================================
elif menu == "📞 Contact":

    st.header("📞 Contact Centre")

    st.markdown("""
    <div class="contact-card">
        <h3>📍 Greater Noida, Uttar Pradesh</h3>
        <p>Email: info@liet.in</p>
        <p>Phone: +91-XXXXXXXXXX</p>
        <p>Website: www.lloydcollege.in</p>
    </div>
    """, unsafe_allow_html=True)

# ======================================
# AI CHATBOT UI (OPTIONAL SECTION)
# ======================================

# ======================================
# FOOTER
# ======================================
st.divider()

st.markdown("""
<div style="text-align:center; color:gray;">
© 2026 LIET Smart ERP Portal | Developed by Vipul
</div>
""", unsafe_allow_html=True)
