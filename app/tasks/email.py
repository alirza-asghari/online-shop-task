from celery import Celery # type: ignore
from app.config import config
import smtplib
from email.mime.text import MIMEText

celery = Celery(
    "worker",
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_RESULT_BACKEND
)

@celery.task
def send_verification_email(email: str):
    """
    Task to send verification email asynchronously.
    """
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    sender_email = config.SENDER_EMAIL
    sender_password = config.EMAIL_PASSWORD

    subject = "Verify Your Account"
    body = (
        f"Hello!\n\n"
        f"Please verify your account for {email}. "
        f"Thank you!"
    )

    try:
        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = email

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
        print(f"Verification email has been sent to {email}")
    except Exception as e:
        print(f"Error sending email to {email}: {str(e)}")
