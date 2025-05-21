# Smart Travel API Endpoint Tester
# This script helps you test specific API endpoints

# Set base URL for API
$baseUrl = "http://localhost:8000"
$apiPrefix = "/api/v1"

# Store the token after login
$global:authToken = $null

function Write-Title($title) {
    Write-Host "`n===== $title =====" -ForegroundColor Cyan
}

function Invoke-ApiEndpoint {
    param (
        [string]$endpoint,
        [string]$method = "GET",
        [object]$body = $null,
        [hashtable]$headers = @{},
        [switch]$useAuth = $false,
        [switch]$isFormData = $false
    )
    
    # Build full URL
    $url = "$baseUrl$apiPrefix$endpoint"
    
    # Add auth header if needed
    if ($useAuth -and $global:authToken) {
        $headers["Authorization"] = "Bearer $global:authToken"
    }
    
    Write-Host "Calling: $method $url" -ForegroundColor Yellow
    
    $params = @{
        Uri = $url
        Method = $method
        Headers = $headers
        ErrorAction = "Stop"
    }
    
    # Add body if provided
    if ($body) {
        if ($isFormData) {
            $params["Form"] = $body
        } else {
            $params["Body"] = ($body | ConvertTo-Json)
            $params["ContentType"] = "application/json"
        }
    }
    
    try {
        $response = Invoke-RestMethod @params
        Write-Host "Success!" -ForegroundColor Green
        return $response
    }
    catch {
        Write-Host "Error: $_" -ForegroundColor Red
        Write-Host $_.Exception.Response.StatusCode
        try {
            $errorContent = $_.ErrorDetails.Message | ConvertFrom-Json
            Write-Host "API Error: $($errorContent.detail)" -ForegroundColor Red
        }
        catch {
            Write-Host "Failed to parse error response" -ForegroundColor Red
        }
        return $null
    }
}

function Test-Register {
    Write-Title "Register New User"
    
    $email = Read-Host "Enter email (e.g. test@example.com)"
    $password = Read-Host "Enter password" -AsSecureString
    $plainPassword = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))
    $fullName = Read-Host "Enter full name"
    
    $body = @{
        email = $email
        password = $plainPassword
        full_name = $fullName
    }
    
    Invoke-ApiEndpoint -endpoint "/auth/register" -method "POST" -body $body
}

function Test-Login {
    Write-Title "Login"
    
    $email = Read-Host "Enter email"
    $password = Read-Host "Enter password" -AsSecureString
    $plainPassword = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))
    
    $body = @{
        username = $email
        password = $plainPassword
    }
    
    $response = Invoke-ApiEndpoint -endpoint "/auth/login/access-token" -method "POST" -body $body -isFormData
    
    if ($response -and $response.access_token) {
        $global:authToken = $response.access_token
        Write-Host "Authentication successful! Token stored for subsequent requests." -ForegroundColor Green
    }
}

function Test-GetUser {
    Write-Title "Get Current User"
    
    if (-not $global:authToken) {
        Write-Host "You need to login first!" -ForegroundColor Red
        return
    }
    
    Invoke-ApiEndpoint -endpoint "/users/me" -useAuth
}

function Test-UpdateUser {
    Write-Title "Update User"
    
    if (-not $global:authToken) {
        Write-Host "You need to login first!" -ForegroundColor Red
        return
    }
    
    $fullName = Read-Host "Enter new full name"
    $body = @{ full_name = $fullName }
    
    Invoke-ApiEndpoint -endpoint "/users/me" -method "PATCH" -body $body -useAuth
}

function Test-CreateSearch {
    Write-Title "Create Search"
    
    if (-not $global:authToken) {
        Write-Host "You need to login first!" -ForegroundColor Red
        return
    }
    
    $origin = Read-Host "Enter origin airport code (e.g. NYC)"
    $destination = Read-Host "Enter destination airport code (e.g. LON)"
    $departureDate = Read-Host "Enter departure date (YYYY-MM-DD)"
    $returnDate = Read-Host "Enter return date (YYYY-MM-DD)"
    $adults = Read-Host "Enter number of adults"
    $children = Read-Host "Enter number of children"
    $cabinClass = Read-Host "Enter cabin class (economy, premium_economy, business, first)"
    
    $body = @{
        origin = $origin
        destination = $destination
        departure_date = $departureDate
        return_date = $returnDate
        adults = [int]$adults
        children = [int]$children
        cabin_class = $cabinClass
    }
    
    Invoke-ApiEndpoint -endpoint "/search/" -method "POST" -body $body -useAuth
}

function Test-GetSearchHistory {
    Write-Title "Get Search History"
    
    if (-not $global:authToken) {
        Write-Host "You need to login first!" -ForegroundColor Red
        return
    }
    
    Invoke-ApiEndpoint -endpoint "/search/history" -useAuth
}

function Test-GetRecommendations {
    Write-Title "Get Recommendations"
    
    if (-not $global:authToken) {
        Write-Host "You need to login first!" -ForegroundColor Red
        return
    }
    
    Invoke-ApiEndpoint -endpoint "/recommendations/" -useAuth
}

function Test-GetDeals {
    Write-Title "Get Deals"
    
    if (-not $global:authToken) {
        Write-Host "You need to login first!" -ForegroundColor Red
        return
    }
    
    Invoke-ApiEndpoint -endpoint "/deals/" -useAuth
}

function Test-SaveDeal {
    Write-Title "Save Deal"
    
    if (-not $global:authToken) {
        Write-Host "You need to login first!" -ForegroundColor Red
        return
    }
    
    $dealId = Read-Host "Enter deal ID to save"
    
    Invoke-ApiEndpoint -endpoint "/deals/$dealId/save" -method "POST" -useAuth
}

function Test-GetSavedDeals {
    Write-Title "Get Saved Deals"
    
    if (-not $global:authToken) {
        Write-Host "You need to login first!" -ForegroundColor Red
        return
    }
    
    Invoke-ApiEndpoint -endpoint "/deals/saved" -useAuth
}

function Show-Menu {
    Write-Host "`n=======================================================" -ForegroundColor Yellow
    Write-Host "             SMART TRAVEL API ENDPOINT TESTER          " -ForegroundColor Yellow
    Write-Host "=======================================================" -ForegroundColor Yellow
    Write-Host "1: Register new user"
    Write-Host "2: Login"
    Write-Host "3: Get current user"
    Write-Host "4: Update user"
    Write-Host "5: Create search"
    Write-Host "6: Get search history"
    Write-Host "7: Get recommendations"
    Write-Host "8: Get deals"
    Write-Host "9: Save deal"
    Write-Host "10: Get saved deals"
    Write-Host "Q: Quit"
    Write-Host "=======================================================" -ForegroundColor Yellow
    
    if ($global:authToken) {
        Write-Host "Authentication: " -NoNewline
        Write-Host "ACTIVE" -ForegroundColor Green
    } else {
        Write-Host "Authentication: " -NoNewline
        Write-Host "NONE" -ForegroundColor Red
    }
}

# Main menu loop
do {
    Show-Menu
    $selection = Read-Host "`nEnter your choice"
    
    switch ($selection) {
        '1' { Test-Register }
        '2' { Test-Login }
        '3' { Test-GetUser }
        '4' { Test-UpdateUser }
        '5' { Test-CreateSearch }
        '6' { Test-GetSearchHistory }
        '7' { Test-GetRecommendations }
        '8' { Test-GetDeals }
        '9' { Test-SaveDeal }
        '10' { Test-GetSavedDeals }
        'q' { exit }
        default {
            Write-Host "Invalid selection!" -ForegroundColor Red
        }
    }
    
    Write-Host "`nPress any key to continue..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
} until ($selection -eq 'q')
