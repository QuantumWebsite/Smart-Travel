import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.email.email_service import EmailService


def test_maildev_connection():
    """Test direct SMTP connection to MailDev without using our service"""
    print("Testing direct SMTP connection to MailDev...")
    
    try:
        # Connect to MailDev SMTP server
        server = smtplib.SMTP('localhost', 1025)
        
        # Create test email
        message = MIMEMultipart("alternative")
        message["Subject"] = "Test MailDev Direct Connection"
        message["From"] = "test@example.com"
        message["To"] = "recipient@example.com"
        
        html_content = """
        <html>
            <body>
                <h1>MailDev Test Email</h1>
                <p>This is a test email sent directly via SMTP to MailDev.</p>
            </body>
        </html>
        """
        message.attach(MIMEText(html_content, "html"))
        
        # Send email
        server.sendmail("test@example.com", ["recipient@example.com"], message.as_string())
        server.quit()
        
        print("✓ Direct SMTP connection test successful!")
        return True
    except Exception as e:
        print(f"✗ Direct SMTP connection test failed: {str(e)}")
        return False


def test_email_service():
    """Test the email service with MailDev"""
    print("\nTesting email service with MailDev...")
    
    try:
        email_service = EmailService()
        result = email_service.send_email(
            to_email="test@example.com",
            subject="Test Email Service with MailDev",
            html_content="""
            <html>
                <body>
                    <h1>Email Service Test</h1>
                    <p>This is a test email sent via the EmailService to MailDev.</p>
                </body>
            </html>
            """,
            text_content="This is a test email sent via the EmailService to MailDev."
        )
        
        if result:
            print("✓ Email Service test successful!")
            return True
        else:
            print("✗ Email Service test failed!")
            return False
    except Exception as e:
        print(f"✗ Email Service test failed: {str(e)}")
        return False


def test_verification_email():
    """Test sending a verification email"""
    print("\nTesting verification email with MailDev...")
    
    try:
        email_service = EmailService()
        result = email_service.send_verification_email(
            email="newuser@example.com",
            token="test-verification-token-12345"
        )
        
        if result:
            print("✓ Verification email test successful!")
            return True
        else:
            print("✗ Verification email test failed!")
            return False
    except Exception as e:
        print(f"✗ Verification email test failed: {str(e)}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("MAILDEV EMAIL TEST SCRIPT")
    print("=" * 50)
    print("Make sure MailDev is running with: docker compose -f docker/maildev-compose.yml up -d")
    print("Access the MailDev web interface at: http://localhost:1080")
    print("=" * 50)
    
    direct_test = test_maildev_connection()
    service_test = test_email_service()
    verification_test = test_verification_email()
    
    print("\n" + "=" * 50)
    print("TEST RESULTS:")
    print(f"Direct SMTP Connection: {'✓ PASS' if direct_test else '✗ FAIL'}")
    print(f"Email Service:          {'✓ PASS' if service_test else '✗ FAIL'}")
    print(f"Verification Email:     {'✓ PASS' if verification_test else '✗ FAIL'}")
    print("=" * 50)
    
    if direct_test and service_test and verification_test:
        print("\n✓ All tests PASSED! MailDev is working correctly.")
        sys.exit(0)
    else:
        print("\n✗ Some tests FAILED! Check your MailDev setup.")
        sys.exit(1)
