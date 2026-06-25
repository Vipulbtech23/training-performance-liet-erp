import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
import zipfile

# ================= ROOT =================
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from scripts.send_email import Emailer

# ================= CONFIG =================
st.set_page_config(page_title="LIET ERP", layout="wide")

df = pd.read_excel("output/final_rankings.xlsx")
df.columns = df.columns.str.strip()

# CLEAN DATA
df["Email"] = df["Email"].astype(str).str.strip().str.lower()
df["Name"] = df["Name"].astype(str).str.strip()
df["Badge"] = df["Rank"].apply(
    lambda x:
        "🥇 Gold" if x == 1
        else "🥈 Silver" if x <= 3
        else "🥉 Bronze" if x <= 10
        else "🏅 Participant"
)
# ================= GRADE DISTRIBUTION DATA =================

grade_count = (
    df["Grade"]
    .value_counts()
    .reset_index()
)

grade_count.columns = ["Grade", "Students"]

# ================= PATH FUNCTIONS =================
def get_pdf_path(name):
    safe = name.strip().replace(" ", "_")
    return os.path.join("output", "gradecards", f"{safe}_gradecard.pdf")

def get_certificate(name):
    safe = name.strip().replace(" ", "_")
    return f"output/certificates/{safe}_certificate.pdf"

def get_gradecard(name):
    safe = name.strip().replace(" ", "_")
    return f"output/gradecards/{safe}_gradecard.pdf"

# ================= AI INSIGHT =================
def ai_insight(row):
    if row["Rank"] <= 5:
        return "🏆 Outstanding performer. Ready for advanced projects."
    elif row["Percentage"] >= 75:
        return "🔥 Strong performance. Focus on projects."
    elif row["Percentage"] >= 60:
        return "👍 Good progress. Improve consistency."
    return "⚠️ Needs revision and practice."

# ================= EMAILER =================
EMAILER = None

# ================= ROLE (NO LOGIN) =================
role = "admin"

# ================= MENU =================
menu = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Leaderboard",
        "Analytics",
        "Module Analysis",
        "Low Performers",
        "Student Search",
        "Reports",
        "Certificates",
        "Email Center",
        "Top Performers",
        "AI Insights",
        "Placement Readiness",
        "Download Center"
    ]
)

# ================= HOME =================
if menu == "Home":

    st.title("🏫 LIET Training ERP Dashboard")

    # METRICS
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Students", len(df))
    c2.metric("Avg %", round(df["Percentage"].mean(), 2))
    c3.metric("Top Score", df["Total"].max())
    c4.metric("Top CGPA", df["CGPA"].max())

    # ALL STUDENTS
    st.subheader("👨‍🎓 All Students List")
    if st.button("🚀 Run Complete Pipeline"):

     os.system("python scripts/merge_quizzes.py")
     os.system("python scripts/calculate_scores.py")
     os.system("python scripts/generate_gradecards.py")
     os.system("python scripts/certificate_generator.py")

    st.success(
        "All Reports Generated Successfully"
    )
    st.dataframe(df.sort_values("Rank"))
    st.dataframe(
    df[
        ["Name",
         "Rank",
         "Badge",
         "Grade"]
    ]
)

    # PIE CHART (PERCENTILE DISTRIBUTION)
    st.subheader("📊 Performance Distribution")

    bins = [0, 40, 60, 75, 90, 100]
    labels = ["0-40", "40-60", "60-75", "75-90", "90-100"]

    df["Percentile Range"] = pd.cut(df["Percentage"], bins=bins, labels=labels, include_lowest=True)

    pie_data = df["Percentile Range"].value_counts().reset_index()
    pie_data.columns = ["Range", "Students"]

    fig = px.pie(
        pie_data,
        names="Range",
        values="Students",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)
elif menu == "Top Performers":

    st.title("🏆 Hall of Fame")

    top3 = df.sort_values("Rank").head(3)

    c1,c2,c3 = st.columns(3)

    with c1:
        st.success(f"🥇 {top3.iloc[0]['Name']}")
        st.metric("Percentage", top3.iloc[0]["Percentage"])

    with c2:
        st.info(f"🥈 {top3.iloc[1]['Name']}")
        st.metric("Percentage", top3.iloc[1]["Percentage"])

    with c3:
        st.warning(f"🥉 {top3.iloc[2]['Name']}")
        st.metric("Percentage", top3.iloc[2]["Percentage"])

    st.dataframe(df.sort_values("Rank").head(10))
    

# ================= LEADERBOARD =================
elif menu == "Leaderboard":

    st.title("🏆 Top 10 Performers")

    top10 = df.sort_values("Rank").head(10)

    st.success(f"🥇 {top10.iloc[0]['Name']}")
    st.info(f"🥈 {top10.iloc[1]['Name']}")
    st.warning(f"🥉 {top10.iloc[2]['Name']}")

    st.dataframe(top10)
elif menu == "AI Insights":

    st.title("🤖 AI Performance Insights")

    insights = []

    for _, row in df.iterrows():

        insights.append({
            "Name": row["Name"],
            "Insight": ai_insight(row)
        })

    st.dataframe(pd.DataFrame(insights))
elif menu == "Placement Readiness":

    st.title("🎯 Placement Readiness Score")

    df["Placement Score"] = (
        (df["CGPA"] * 4) +
        (df["Percentage"] * 0.4) +
        (df["Attendance_%"] * 0.2)
    )

    st.dataframe(
        df[
            ["Name",
             "Placement Score",
             "CGPA",
             "Percentage",
             "Rank"]
        ].sort_values(
            "Placement Score",
            ascending=False
        )
    )
elif menu == "Download Center":

    st.title("📥 Download Center")

    zip_path = "output/all_gradecards.zip"

    if st.button("Create Gradecard ZIP"):

        with zipfile.ZipFile(zip_path, "w") as zipf:

            for _, row in df.iterrows():

                pdf = get_gradecard(row["Name"])

                if os.path.exists(pdf):
                    zipf.write(
                        pdf,
                        os.path.basename(pdf)
                    )

        with open(zip_path, "rb") as f:

            st.download_button(
                "Download All Gradecards",
                f,
                file_name="all_gradecards.zip"
            )   
# ================= ANALYTICS =================
elif menu == "Analytics":

    st.title("📊 Analytics")

    fig = px.bar(df.sort_values("Percentage", ascending=False),
                 x="Name", y="Percentage",
                 color="Grade")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(df, x="CGPA", y="Percentage", color="Rank")
    st.plotly_chart(fig2, use_container_width=True)
    st.subheader("🎓 Grade Distribution")

    fig3 = px.pie(
    grade_count,
    names="Grade",
    values="Students",
    hole=0.4,
    title="Grade Distribution"
)

    st.plotly_chart(fig3, use_container_width=True)

# ================= MODULE ANALYSIS =================
elif menu == "Module Analysis":

    st.title("📚 Module Analysis")

    marks_cols = [c for c in df.columns if "_Marks" in c]

    module_avg = df[marks_cols].mean().reset_index()
    module_avg.columns = ["Module", "Avg Score"]

    st.dataframe(module_avg)

    fig = px.bar(module_avg, x="Module", y="Avg Score")
    st.plotly_chart(fig, use_container_width=True)

# ================= LOW PERFORMERS =================
elif menu == "Low Performers":

    st.title("⚠️ Low Performers")

    low = df[df["Percentage"] < 60]
    st.dataframe(low[["Name", "Percentage", "CGPA", "Grade", "Suggestion"]])

# ================= STUDENT SEARCH =================
elif menu == "Student Search":

    st.title("🔍 Search Student")

    name = st.text_input("Enter Name")

    if name:
        res = df[df["Name"].str.contains(name, case=False)]
        st.dataframe(res)

# ================= REPORTS =================
elif menu == "Reports":

    st.title("📄 Reports")

    student = st.selectbox("Select Student", df["Name"])
    path = get_pdf_path(student)

    if os.path.exists(path):
        with open(path, "rb") as f:
            st.download_button("Download PDF", f, file_name=os.path.basename(path))
    else:
        st.error("PDF not found")

    with open("output/final_rankings.xlsx", "rb") as f:
        st.download_button("Download Excel", f, file_name="report.xlsx")

# ================= CERTIFICATES =================
elif menu == "Certificates":

    st.title("🏆 Certificates Center")

    df["Badge"] = df["Rank"].apply(lambda x: "🥇 Gold" if x == 1 else "🥈 Silver" if x <= 3 else "🥉 Bronze" if x <= 10 else "🏅 Participant")

    st.dataframe(df[["Name", "Rank", "Badge", "Percentage", "CGPA"]])

    student = st.selectbox("Select Student", df["Name"])
    cert_path = get_certificate(student)

    if os.path.exists(cert_path):
        with open(cert_path, "rb") as f:
            st.download_button("Download Certificate", f, file_name=os.path.basename(cert_path))
    else:
        st.warning("Certificate not generated yet")

    # ZIP DOWNLOAD
    st.subheader("📦 Bulk Download")

    if st.button("Generate ZIP"):
        zip_path = "output/certificates_all.zip"

        with zipfile.ZipFile(zip_path, "w") as zipf:
            for _, row in df.iterrows():
                cert = get_certificate(row["Name"])
                if os.path.exists(cert):
                    zipf.write(cert, os.path.basename(cert))

        with open(zip_path, "rb") as f:
            st.download_button("Download ZIP", f, file_name="all_certificates.zip")

# ================= EMAIL CENTER =================
elif menu == "Email Center":

    st.title("📧 Email System")

    sender = st.text_input("Gmail")
    app_pass = st.text_input("App Password", type="password")

    if sender and app_pass:
        EMAILER = Emailer(sender, app_pass)

    student = st.selectbox("Student", df["Name"])
    email_type = st.radio("Document Type", ["Gradecard", "Certificate"])

    if st.button("Send Email") and EMAILER:

        row = df[df["Name"] == student].iloc[0]

        pdf_path = get_gradecard(student) if email_type == "Gradecard" else get_certificate(student)

        if os.path.exists(pdf_path):
            EMAILER.send_pdf(row["Email"], pdf_path, student)
            st.success("Email sent successfully")
        else:
            st.error("File not found")