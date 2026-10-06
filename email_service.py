"""
Email notification service for the Portfolio application.
Sends HTML-formatted email notifications when a new contact form message is received.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config


def build_email_html(name, email, subject, message):
    """
    Build an HTML email template for a new contact notification.

    Args:
        name: Sender's name
        email: Sender's email
        subject: Message subject
        message: Message body

    Returns:
        HTML string for the email body
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: #0f1013; color: #f8fafc; padding: 0; margin: 0; }}
            .container {{ max-width: 600px; margin: 20px auto; background: #1a1c23; border-radius: 16px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1); }}
            .header {{ background: linear-gradient(135deg, #2563eb, #1d4ed8); padding: 30px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 22px; color: #fff; }}
            .header p {{ margin: 5px 0 0; color: rgba(255,255,255,0.8); font-size: 14px; }}
            .body {{ padding: 30px; }}
            .field {{ margin-bottom: 20px; }}
            .field-label {{ font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; color: #60a5fa; font-weight: 600; margin-bottom: 6px; }}
            .field-value {{ font-size: 15px; color: #cbd5e1; line-height: 1.6; padding: 12px 16px; background: rgba(255,255,255,0.05); border-radius: 10px; border: 1px solid rgba(255,255,255,0.08); }}
            .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #64748b; border-top: 1px solid rgba(255,255,255,0.06); }}
            a {{ color: #60a5fa; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📬 New Contact Message</h1>
                <p>Someone reached out through your portfolio</p>
            </div>
            <div class="body">
                <div class="field">
                    <div class="field-label">From</div>
                    <div class="field-value">{name}</div>
                </div>
                <div class="field">
                    <div class="field-label">Email</div>
                    <div class="field-value"><a href="mailto:{email}">{email}</a></div>
                </div>
                <div class="field">
                    <div class="field-label">Subject</div>
                    <div class="field-value">{subject}</div>
                </div>
                <div class="field">
                    <div class="field-label">Message</div>
                    <div class="field-value">{message}</div>
                </div>
            </div>
            <div class="footer">
                Leroy Matienga Portfolio &mdash; Automated Notification
            </div>
        </div>
    </body>
    </html>
    """


def send_notification(name, email, subject, message):
    """
    Send an email notification for a new contact form submission.
    Fails gracefully — logs errors but never crashes the request.

    Args:
        name: Sender's name
        email: Sender's email
        subject: Message subject
        message: Message body

    Returns:
        True if email sent successfully, False otherwise
    """
    # Skip if SMTP is not configured
    if not Config.SMTP_EMAIL or not Config.SMTP_PASSWORD:
        print("[EMAIL] SMTP not configured — skipping email notification.")
        return False

    recipient = Config.NOTIFICATION_EMAIL or Config.SMTP_EMAIL

    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = Config.SMTP_EMAIL
        msg["To"] = recipient
        msg["Subject"] = f"Portfolio Contact: {subject}"

        # Plain text fallback
        plain_text = (
            f"New message from your portfolio:\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Subject: {subject}\n"
            f"Message:\n{message}\n"
        )
        msg.attach(MIMEText(plain_text, "plain"))

        # HTML version
        html_body = build_email_html(name, email, subject, message)
        msg.attach(MIMEText(html_body, "html"))

        # Connect and send
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(Config.SMTP_EMAIL, Config.SMTP_PASSWORD)
            server.sendmail(Config.SMTP_EMAIL, recipient, msg.as_string())

        print(f"[EMAIL] Notification sent to {recipient}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("[EMAIL ERROR] SMTP authentication failed. Check your email/password (use App Password for Gmail).")
        return False
    except smtplib.SMTPException as e:
        print(f"[EMAIL ERROR] SMTP error: {e}")
        return False
    except Exception as e:
        print(f"[EMAIL ERROR] Unexpected error: {e}")
        return False
