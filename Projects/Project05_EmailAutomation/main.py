import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path

BASE_DIR = Path(__file__).parent
ATTACHMENTS_DIR = BASE_DIR / "attachments"
ATTACHMENTS_DIR.mkdir(exist_ok=True)


def create_email(sender: str, recipients: list[str], subject: str, html_body: str, attachments: list[Path]) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg.set_content("This email is sent with HTML formatting. Please view it in an HTML-capable client.")
    msg.add_alternative(html_body, subtype="html")

    for attachment in attachments:
        if not attachment.exists():
            raise FileNotFoundError(f"Attachment not found: {attachment}")
        maintype, subtype = "application", "octet-stream"
        with open(attachment, "rb") as f:
            data = f.read()
        msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=attachment.name)

    return msg


def send_email(smtp_server: str, smtp_port: int, username: str, password: str, msg: EmailMessage) -> None:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
    print("Email sent successfully.")


def main() -> None:
    print("Email Automation Demo")
    sender = "sender@example.com"
    recipients = ["recipient1@example.com", "recipient2@example.com"]
    subject = "Automated Email from Python"
    html_body = """
    <html>
      <body>
        <h1>Hello from Email Automation</h1>
        <p>This email is <strong>automatically generated</strong> and includes attachments.</p>
      </body>
    </html>
    """

    attachments = [ATTACHMENTS_DIR / "sample_attachment.txt"]
    for attachment in attachments:
        if not attachment.exists():
            attachment.write_text("This is a sample attachment.", encoding="utf-8")

    message = create_email(sender, recipients, subject, html_body, attachments)
    print("Email message created.")
    print("Update SMTP settings and uncomment send_email() to actually send.")
    # Uncomment and configure the lines below to send email.
    # smtp_server = "smtp.example.com"
    # smtp_port = 587
    # username = "your_username"
    # password = "your_password"
    # send_email(smtp_server, smtp_port, username, password, message)


if __name__ == "__main__":
    main()
