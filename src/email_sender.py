import os
import smtplib
from dotenv import load_dotenv, find_dotenv
from email.mime.text import MIMEText
import markdown

load_dotenv(find_dotenv())

def send_digest_email(digest_content: str, subject: str) -> bool:

    sender = os.getenv("SENDER_EMAIL")
    recipient = os.getenv("RECIPIENT_EMAIL")
    password = os.getenv("EMAIL_APP_PASSWORD")


    html_body = markdown.markdown(digest_content)
    msg = MIMEText(html_body, "html")

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            print("Email sent successfully")
            return True
    except Exception as e:
        print(f"Email failed:{e}")
        return False