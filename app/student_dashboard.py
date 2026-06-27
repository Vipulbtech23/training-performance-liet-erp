import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import datetime

# ================= CONFIG =================
st.set_page_config(
    page_title="LIET Student ERP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= CSS =================
with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ================= DATA =================
df = pd.read_excel("output/final_rankings.xlsx")
df.columns = df.columns.str.strip()

# ================= SESSION =================
if "login" not in st.session_state:
    st.session_state.login = False

if "student" not in st.session_state:
    st.session_state.student = None

# ================= LOGIN =================
if not st.session_state.login:

    st.markdown("<h1 style='text-align:center;'>🎓 LIET Student ERP</h1>", unsafe_allow_html=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = df[df["Email"].str.lower() == email.lower()]

        if len(user) > 0 and password == "Lloyd@2025":

            st.session_state.login = True
            st.session_state.student = user.iloc[0]
            st.rerun()

        else:
            st.error("Invalid Credentials")

    st.stop()

# ================= STUDENT =================
student = st.session_state.student

# ================= SIDEBAR =================
st.sidebar.image("assets/avatar.png", width=130)
st.sidebar.markdown(f"### {student['Name']}")
st.sidebar.write(student["Email"])

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        
        "Downloads",
        "🤖 AI Assistant",
        "👤 Profile",
        "⚙ Settings",
        "📌 Attendance"
    ]
)

# ================= FUNCTIONS =================
def get_gradecard(name):
    safe = name.strip().replace(" ", "_")
    return f"output/gradecards/{safe}_gradecard.pdf"

def get_certificate(name):
    safe = name.strip().replace(" ", "_")
    return f"output/certificates/{safe}_certificate.pdf"

# ================= DASHBOARD =================
if page == "🏠 Dashboard":

    st.title("🎓 Student Dashboard")
    st.success(f"Welcome {student['Name']} 👋")

    st.markdown("<div class='title'>Student Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Welcome Back</div>", unsafe_allow_html=True)

    # ================= METRICS =================
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rank", student["Rank"])
    c2.metric("Percentage", f"{student['Percentage']}%")
    c3.metric("CGPA", student["CGPA"])
    c4.metric("Attendance", f"{student['Attendance_%']}%")

    # ================= PROFILE =================
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image("assets/avatar.png", width=170)

    with col2:
        st.markdown(f"""
        <div class="glass">
            <h2>{student['Name']}</h2>
            <h4>{student['Email']}</h4>
            <p>CGPA : {student['CGPA']}</p>
            <p>Rank : {student['Rank']}</p>
            <p>Grade : {student['Grade']}</p>
        </div>
        """, unsafe_allow_html=True)

    # ================= PROGRESS =================
    st.subheader("📈 Performance")

    st.write("Overall Percentage")
    st.progress(int(student["Percentage"]))

    st.write("Attendance")
    st.progress(int(student["Attendance_%"]))

    cgpa_percent = int((student["CGPA"] / 10) * 100)
    st.write("CGPA Progress")
    st.progress(cgpa_percent)

    # ================= PROFILE CARD =================
    st.subheader("👤 Student Profile")

    left, right = st.columns([1, 3])

    with left:
        st.image(
            "https://api.dicebear.com/7.x/initials/png?seed=" + student["Name"],
            width=140
        )

    with right:
        st.write("###", student["Name"])
        st.write("📧", student["Email"])
        st.write("🎓 Grade :", student["Grade"])
        st.write("📊 Rank :", student["Rank"])

    # ================= BAR CHART =================
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=["Attendance", "Percentage", "CGPA"],
        y=[student["Attendance_%"], student["Percentage"], student["CGPA"] * 10]
    ))

    fig.update_layout(title="My Performance", height=420)

    st.plotly_chart(fig, use_container_width=True)

    # ================= RADAR =================
    fig2 = go.Figure()

    fig2.add_trace(go.Scatterpolar(
        r=[
            student["Attendance_%"],
            student["Percentage"],
            student["CGPA"] * 10,
            student["Percentage"]
        ],
        theta=["Attendance", "Percentage", "CGPA", "Performance"],
        fill="toself"
    ))

    fig2.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=500
    )

    st.plotly_chart(fig2, use_container_width=True)

    # ================= STATS =================
    stats1, stats2 = st.columns(2)

    with stats1:
        st.info(f"""
        ### Academic
        Rank : {student['Rank']}
        Grade : {student['Grade']}
        CGPA : {student['CGPA']}
        """)

    with stats2:
        st.success(f"""
        ### Training
        Attendance : {student['Attendance_%']}
        Percentage : {student['Percentage']}
        """)

    # ================= MODULE CHART =================
    marks_cols = [c for c in df.columns if "_Marks" in c]

    module_df = pd.DataFrame([
        {"Module": c.replace("_Marks", ""), "Marks": student[c]}
        for c in marks_cols
    ])

    fig3 = px.bar(module_df, x="Module", y="Marks", title="Module Performance")

    st.plotly_chart(fig3, use_container_width=True)

    # ================= PERCENTILE =================
    total = len(df)
    percentile = round((1 - (student["Rank"] / total)) * 100, 2)

    st.success(f"🏆 You are better than **{percentile}%** students")

    # ================= ACHIEVEMENTS =================
    st.subheader("🏅 Achievements")

    if student["Rank"] == 1:
        st.balloons()
        st.success("🥇 College Topper")
    elif student["Rank"] <= 3:
        st.success("🥈 Top 3 Performer")
    elif student["Rank"] <= 10:
        st.info("🥉 Top 10 Performer")
    else:
        st.warning("🏅 Participant")

# ================= DOWNLOADS =================
elif page == "Downloads":

    st.subheader("👤 Student Info")

    c1, c2, c3 = st.columns(3)

    c1.metric("Rank", student["Rank"])
    c2.metric("Grade", student["Grade"])
    c3.metric("Percentage", f"{student['Percentage']}%")

    st.title("📥 Download Center")

    col1, col2 = st.columns(2)

    gradecard = get_gradecard(student["Name"])
    certificate = get_certificate(student["Name"])

    with col1:
        if os.path.exists(gradecard):
            with open(gradecard, "rb") as f:
                st.download_button("📄 Gradecard", f, file_name=os.path.basename(gradecard))

    with col2:
        if os.path.exists(certificate):
            with open(certificate, "rb") as f:
                st.download_button("🏆 Certificate", f, file_name=os.path.basename(certificate))

    st.subheader("📂 Document Status")

    status = pd.DataFrame([
        {"Document": "Gradecard", "Status": "✅ Available" if os.path.exists(gradecard) else "❌ Missing"},
        {"Document": "Certificate", "Status": "✅ Available" if os.path.exists(certificate) else "❌ Missing"}
    ])

    st.table(status)
elif page == "⚙ Settings":

    st.title("⚙ Settings Panel")

    

    # ================= THEME SWITCH =================
    st.subheader("🎨 Theme Settings")

    theme = st.selectbox("Choose Theme", ["Light", "Dark"])

    if theme == "Dark":
        st.markdown(
            """
            <style>
            body { background-color: #0e1117; color: white; }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.success("Dark theme applied")

    else:
        st.success("Light theme active")

    st.markdown("---")

    

    # ================= LOGOUT =================
    st.subheader("🚪 Logout")

    if st.button("Logout Now"):
        st.session_state.login = False
        st.session_state.student = None

        st.success("Logged out successfully!")

        st.rerun()    
elif page == "🤖 AI Assistant":
    st.subheader("🤖 AI Insights")

    rank = student["Rank"]
    cgpa = student["CGPA"]
    attendance = student["Attendance_%"]

    if rank == 1:
        st.success("🔥 You are College Topper — maintain consistency")
    elif rank <= 3:
        st.info("⭐ You are in Top 3 — push for Rank 1")
    elif cgpa < 7:
        st.warning("📉 Improve CGPA for better placement chances")
    elif attendance < 75:
        st.error("⚠ Attendance is low — risk of eligibility issue")
    else:
        st.success("✅ Performance is stable — keep improving")

    st.markdown("---")
elif page == "👤 Profile":
    st.subheader("👤 Profile Overview")

    st.write("Name:", student["Name"])
    st.write("Email:", student["Email"])
    st.write("Grade:", student["Grade"])
    st.write("Rank:", student["Rank"])
    st.write("CGPA:", student["CGPA"])
    st.markdown("---")

  