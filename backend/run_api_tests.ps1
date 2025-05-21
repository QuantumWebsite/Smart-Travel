# Smart Travel API Test Runner
# This PowerShell script provides an easy way to run tests for the Smart Travel API

function Write-ColorOutput($ForegroundColor) {
    # Save the current colors
    $fc = $host.UI.RawUI.ForegroundColor

    # Set the new colors
    $host.UI.RawUI.ForegroundColor = $ForegroundColor

    # Pass the remaining arguments through
    if ($args) {
        Write-Output $args
    }
    else {
        # Write a space if no args
        Write-Output ' '
    }

    # Restore the original colors
    $host.UI.RawUI.ForegroundColor = $fc
}

function Show-Menu {
    Clear-Host
    Write-Host "=======================================================" -ForegroundColor Yellow
    Write-Host "             SMART TRAVEL API TEST RUNNER              " -ForegroundColor Yellow
    Write-Host "=======================================================" -ForegroundColor Yellow
    Write-Host "1: Run all tests"
    Write-Host "2: Run specific test module"
    Write-Host "3: Run tests with coverage report"
    Write-Host "4: Validate CRUD operations"
    Write-Host "5: Run HTTP server and test with Swagger UI"
    Write-Host "Q: Quit"
    Write-Host "=======================================================" -ForegroundColor Yellow
}

function Run-AllTests {
    Write-ColorOutput Green "Running all tests..."
    python -m pytest -v
}

function Select-TestModule {
    $testFiles = Get-ChildItem -Path ".\tests" -Filter "test_*.py" | ForEach-Object { $_.Name -replace '\.py$','' }
    
    Write-Host "Available test modules:" -ForegroundColor Yellow
    for ($i=0; $i -lt $testFiles.Count; $i++) {
        Write-Host "$($i+1): $($testFiles[$i])"
    }
    
    $selection = Read-Host "Select a test module to run (1-$($testFiles.Count))"
    $index = [int]$selection - 1
    
    if ($index -ge 0 -and $index -lt $testFiles.Count) {
        $testModule = $testFiles[$index]
        Write-ColorOutput Green "Running tests for $testModule..."
        python -m pytest -v ".\tests\$testModule.py"
    } else {
        Write-ColorOutput Red "Invalid selection!"
    }
}

function Run-TestsWithCoverage {
    Write-ColorOutput Green "Running tests with coverage report..."
    python -m pytest --cov=app tests/
    
    $genHtml = Read-Host "Generate HTML coverage report? (y/n)"
    if ($genHtml -eq "y" -or $genHtml -eq "Y") {
        python -m pytest --cov=app --cov-report=html tests/
        Write-ColorOutput Green "HTML coverage report generated in htmlcov/ directory"
        
        $openReport = Read-Host "Open coverage report in browser? (y/n)"
        if ($openReport -eq "y" -or $openReport -eq "Y") {
            Start-Process ".\htmlcov\index.html"
        }
    }
}

function Validate-CRUD {
    Write-ColorOutput Green "Validating CRUD operations..."
    python .\tests\validate_crud.py
}

function Run-Server {
    Write-ColorOutput Green "Starting the API server for testing..."
    $serverProcess = Start-Process -FilePath "python" -ArgumentList "-m uvicorn app.main:app --reload" -PassThru
    
    Write-ColorOutput Yellow "Server running at http://localhost:8000"
    Write-ColorOutput Yellow "Access Swagger UI at http://localhost:8000/docs"
    Write-Host "Press any key to stop the server..." -ForegroundColor Cyan
    
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    Stop-Process -Id $serverProcess.Id -Force
    Write-ColorOutput Green "Server stopped"
}

# Main script
do {
    Show-Menu
    $selection = Read-Host "Enter your choice"
    
    switch ($selection) {
        '1' {
            Run-AllTests
        }
        '2' {
            Select-TestModule
        }
        '3' {
            Run-TestsWithCoverage
        }
        '4' {
            Validate-CRUD
        }
        '5' {
            Run-Server
        }
        'q' {
            exit
        }
        default {
            Write-ColorOutput Red "Invalid selection!"
        }
    }
    
    Write-Host "`nPress any key to continue..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
} until ($selection -eq 'q')
