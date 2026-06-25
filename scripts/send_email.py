import smtplib
from email.message import EmailMessage
import os

class Emailer:

    def __init__(self, sender_email, app_password):
        self.sender = sender_email
        self.password = app_password

    # =====================================================
    # 📧 UNIVERSAL EMAIL FUNCTION (GRADECARD + CERTIFICATE)
    # =====================================================
    def send_pdf(self, receiver_email, pdf_path, student_name, doc_type="Gradecard"):

        msg = EmailMessage()

        # ================= SUBJECT (DYNAMIC) =================
        if doc_type == "Certificate":
            msg["Subject"] = "🏆 Your LIET Training Certificate"
        else:
            msg["Subject"] = "📄 Your LIET Bootcamp Report Card"

        msg["From"] = self.sender
        msg["To"] = receiver_email

        # ================= BODY MESSAGE =================
        msg.set_content(f"""
Hello {student_name},

Congratulations 🎉

Please find your {doc_type} attached.

This document contains your ML & Agentic AI performance report.

Keep learning and growing 🚀

Regards,  
LIET Bootcamp Training Team
""")

        # ================= ATTACH PDF =================
        try:
            with open(pdf_path, "rb") as f:
                file_data = f.read()

            msg.add_attachment(
                file_data,
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(pdf_path)
            )

        except Exception as e:
            print(f"❌ File error: {e}")
            return

        # ================= SEND EMAIL =================
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.sender, self.password)
                smtp.send_message(msg)

            print(f"✅ {doc_type} sent to {student_name}")

        except Exception as e:
            print(f"❌ Email failed for {student_name}: {e}")