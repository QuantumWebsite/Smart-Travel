# Run Email Verification Tests with MailDev
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Smart Travel - Email Verification Tests with MailDev" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Check if MailDev is running
$containerStatus = docker ps --filter "name=smart_travel_maildev" --format "{{.Status}}"
if (-not $containerStatus) {
    Write-Host "MailDev container is not running. Starting it now..." -ForegroundColor Yellow
    docker compose -f docker/maildev-compose.yml up -d
    Start-Sleep -Seconds 3
} else {
    Write-Host "✓ MailDev container is running: $containerStatus" -ForegroundColor Green
}

Write-Host "`nRunning email verification tests with MailDev..."
Write-Host "You can view the test emails at: http://localhost:1080" -ForegroundColor Cyan
Write-Host ""

# Set environment variable for tests to use MailDev
$env:MAILDEV_TESTING = "true"

# Run the tests
cd backend
python -m pytest tests/test_email_verification.py tests/test_email_verification_flow.py -v

# Reset environment variable
$env:MAILDEV_TESTING = ""

Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host "Don't forget to check your test emails at:" -ForegroundColor Yellow
Write-Host "http://localhost:1080" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan
