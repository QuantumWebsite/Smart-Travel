# Start MailDev and test email functionality
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Smart Travel - MailDev Email Testing Setup" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Check if Docker is installed
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker is installed: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not installed or not in your PATH!" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Start MailDev container
Write-Host "`nStarting MailDev container..." -ForegroundColor Cyan
docker compose -f docker/maildev-compose.yml up -d

# Check if container started successfully
$containerStatus = docker ps --filter "name=smart_travel_maildev" --format "{{.Status}}"
if ($containerStatus) {
    Write-Host "✓ MailDev container started successfully: $containerStatus" -ForegroundColor Green
    Write-Host "  • SMTP Server: localhost:1025" -ForegroundColor Green
    Write-Host "  • Web Interface: http://localhost:1080" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to start MailDev container!" -ForegroundColor Red
    exit 1
}

# Wait for container to be fully operational
Write-Host "`nWaiting for MailDev to be fully operational..." -ForegroundColor Cyan
Start-Sleep -Seconds 3

# Run the email test script
Write-Host "`nRunning email tests..." -ForegroundColor Cyan
python scripts/test_maildev.py

# Open MailDev web interface
Write-Host "`nOpening MailDev web interface..." -ForegroundColor Cyan
Start-Process "http://localhost:1080"

Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host "To stop MailDev when done testing, run:" -ForegroundColor Yellow
Write-Host "docker compose -f docker/maildev-compose.yml down" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan
