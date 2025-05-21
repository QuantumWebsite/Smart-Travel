import logging
from typing import Dict, List, Optional
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """
    Service for sending emails
    """
    def __init__(self):
        self.from_email = settings.EMAILS_FROM_EMAIL
        self.smtp_server = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.use_tls = settings.SMTP_TLS
        
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        reply_to: Optional[str] = None,
    ) -> bool:
        """
        Send an email
        
        Args:
            to_email: Email address of the recipient
            subject: Subject of the email
            html_content: HTML content of the email
            text_content: Plain text content of the email (optional)
            cc: List of CC recipients (optional)
            bcc: List of BCC recipients (optional)
            reply_to: Reply-to email address (optional)
            
        Returns:
            True if the email was sent successfully, False otherwise
        """        # In development, still log the email but also send it to MailDev
        if settings.ENVIRONMENT == "development":
            logger.info(f"Email will be sent to: {to_email}")
            logger.info(f"Subject: {subject}")
            logger.info(f"Content: {html_content}")
            # Continue to send the email to MailDev

        # For production, send the actual email
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.from_email
            message["To"] = to_email
            
            if cc:
                message["Cc"] = ", ".join(cc)
            if reply_to:
                message["Reply-To"] = reply_to
                
            # Attach parts
            if text_content:
                message.attach(MIMEText(text_content, "plain"))
            message.attach(MIMEText(html_content, "html"))
            
            # Connect to SMTP server
            if self.use_tls:
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            else:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                
            # Login if credentials are provided
            if self.smtp_user and self.smtp_password:
                server.login(self.smtp_user, self.smtp_password)
                
            # Send email
            all_recipients = [to_email]
            if cc:
                all_recipients.extend(cc)
            if bcc:
                all_recipients.extend(bcc)
                
            server.sendmail(self.from_email, all_recipients, message.as_string())
            server.quit()
            
            logger.info(f"Email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
            
    def send_verification_email(self, email: str, token: str) -> bool:
        """
        Send an email verification link to a user
        
        Args:
            email: Email address of the user
            token: Verification token
            
        Returns:
            True if the email was sent successfully, False otherwise
        """
        subject = "Verify your Smart Travel account"
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        
        # HTML content
        html_content = f"""
        <html>
            <body>
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2>Welcome to Smart Travel!</h2>
                    <p>Thank you for registering. Please verify your email address by clicking the button below:</p>
                    <p style="text-align: center;">
                        <a href="{verification_url}" 
                           style="background-color: #4F46E5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            Verify Email
                        </a>
                    </p>
                    <p>If the button doesn't work, you can also copy and paste the following link into your browser:</p>
                    <p>{verification_url}</p>
                    <p>This link will expire in 24 hours.</p>
                    <p>If you didn't create an account, you can safely ignore this email.</p>
                    <p>Best regards,<br>The Smart Travel Team</p>
                </div>
            </body>
        </html>
        """
        
        # Plain text content as fallback
        text_content = f"""
        Welcome to Smart Travel!
        
        Thank you for registering. Please verify your email address by clicking the link below:
        
        {verification_url}
        
        This link will expire in 24 hours.
        
        If you didn't create an account, you can safely ignore this email.
        
        Best regards,
        The Smart Travel Team
        """
        
        return self.send_email(
            to_email=email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )


# Create a global instance
email_service = EmailService()