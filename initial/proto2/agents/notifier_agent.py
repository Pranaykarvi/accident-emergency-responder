import smtplib
import ssl
import os
from email.message import EmailMessage

class NotifierAgent:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=465):
        """
        Expects two environment variables:
        EMAIL_ADDRESS  – your “from” email address
        EMAIL_PASSWORD – an app‐specific password or token for SMTP
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = os.getenv("EMAIL_ADDRESS")
        self.sender_pass = os.getenv("EMAIL_PASSWORD")
        if not self.sender_email or not self.sender_pass:
            raise EnvironmentError("Set EMAIL_ADDRESS and EMAIL_PASSWORD in environment variables.")

    def send_email(self, to_email, subject, body, image_path=None):
        """
        Sends an email with optional image attachment.
        """
        msg = EmailMessage()
        msg["From"] = self.sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        if image_path and os.path.isfile(image_path):
            with open(image_path, "rb") as img_file:
                img_data = img_file.read()
                img_name = os.path.basename(image_path)
            maintype, subtype = "image", "jpeg" if image_path.lower().endswith((".jpg", ".jpeg")) else "png"
            msg.add_attachment(img_data, maintype=maintype, subtype=subtype, filename=img_name)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            server.login(self.sender_email, self.sender_pass)
            server.send_message(msg)
        print(f"Email sent to {to_email} with subject '{subject}'")
