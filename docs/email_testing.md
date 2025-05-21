# Email Testing with MailDev

Smart Travel uses MailDev for testing email functionality. This document explains how to set up and use MailDev for email testing.

## What is MailDev?

MailDev is a simple SMTP server with a web-based UI for viewing and testing emails during development. It's perfect for testing email functionality without sending real emails to actual addresses.

## Setup

### Prerequisites

- Docker Desktop must be installed on your system
- PowerShell (for Windows)

### Starting MailDev

To start the MailDev server:

```powershell
# Run the provided start script
./start_maildev.ps1
```

This will:
1. Start the MailDev container
2. Run some basic email tests to verify the setup
3. Open the MailDev web interface in your browser

### Stopping MailDev

When you're done testing:

```powershell
docker compose -f docker/maildev-compose.yml down
```

## Using MailDev for Testing

### Web Interface

- The MailDev web interface is available at: http://localhost:1080
- You can view all emails sent during testing
- Features include viewing HTML content, raw message, plain text, and attachments

### SMTP Configuration

MailDev is configured with the following settings:

- SMTP Server: localhost
- SMTP Port: 1025
- No authentication required
- TLS disabled (for simplicity)

These settings are already configured in `app/core/config.py` for development mode.

## Running Email Tests

To run email verification tests with MailDev:

```powershell
./run_email_tests.ps1
```

This will:
1. Start MailDev if it's not already running
2. Run all email verification tests with real email sending to MailDev
3. Open the MailDev web interface to check the emails

## Manual Email Testing

You can also test email sending manually:

```powershell
python backend/scripts/test_maildev.py
```

This will:
1. Test direct SMTP connection to MailDev
2. Test email sending through the EmailService
3. Test sending a verification email

## Integration with CI/CD

For CI/CD pipelines, the email service can be mocked to prevent external dependencies. The verification email tests have been designed to use a mock service by default but can use a real MailDev instance when the `MAILDEV_TESTING=true` environment variable is set.
