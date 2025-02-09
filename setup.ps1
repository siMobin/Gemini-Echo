<#
.SYNOPSIS
    Setup script for the Gemini Echo application.

.DESCRIPTION
    This script is designed to initialize and configure the necessary environment settings for the Gemini Echo system.
    It may perform tasks such as environment variable configuration, installation of required modules, and any preparatory 
    steps to ensure that dependencies and system settings are correctly established prior to running the main application.
    
.PARAMETERS
    None currently defined. Modify the script to accept and process parameters if dynamic configuration is required.

.NOTES
    File Path: ./setup.ps1
    This script automates the setup of your Gemini Echo development environment by checking for required software,
    creating a virtual environment, and installing dependencies. Tailor these instructions further to suit additional project needs.

.EXAMPLE
    To execute this setup script, open a PowerShell prompt and run:
        PS> .\setup.ps1
        
    Ensure that you have the necessary permissions and that your execution policy is set appropriately to allow script execution.
    You may need to run the following command to allow script execution:
        PS> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

.version
    1.0
    9 February 2025
#>


# Function to format output
function Write-Styled {
    param (
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}


# Check for Python and Pip
Write-Styled "🔄 Checking Python installation..." Cyan
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python (\d+)\.(\d+)\.(\d+)") {
    $major = [int]$matches[1]
    $minor = [int]$matches[2]
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 12)) {
        Write-Styled "❌ Python 3.12 or later is required. Please update your Python version." Red
        exit 1
    }
    Write-Styled "✅ $pythonVersion" Green
}
else {
    Write-Styled "❌ Python is not installed or not found in PATH." Red
    exit 1
}

Write-Styled "🔄 Checking Pip..." Cyan
$pipVersion = pip --version 2>&1
if ($pipVersion -match "pip (\d+\.\d+)") {
    Write-Styled "✅ $pipVersion" Green
}
else {
    Write-Styled "❌ Pip is not installed or not found in PATH." Red
    exit 1
}
Write-Host "`n"


# Installing virtualenv
Write-Styled "🔄 Installing virtualenv..." Cyan
pip install virtualenv | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Styled "❌ Failed to install virtualenv." Red
    exit 1
}
Write-Styled "✅ Virtualenv installed successfully." Green
Write-Host ""

Write-Styled "🔄 Checking virtual environment..." Cyan
if (Test-Path "Gemini Echo/Scripts/Activate.ps1") {
    Write-Styled "✅ Virtual environment 'Gemini Echo' already exists." Green
}
else {
    Write-Styled "🔄 Creating virtual environment 'Gemini Echo'..." Cyan
    python -m virtualenv "Gemini Echo"
    if ($LASTEXITCODE -ne 0) {
        Write-Styled "❌ Failed to create virtual environment." Red
        exit 1
    }
    Write-Styled "✅ Virtual environment 'Gemini Echo' created." Green
}

Write-Styled "🔄 Activating virtual environment..." Cyan
$venvActivate = "./Gemini Echo/Scripts/Activate.ps1"
if (Test-Path $venvActivate) {
    & $venvActivate
    Write-Styled "✅ Virtual environment activated." Green
}
else {
    Write-Styled "❌ Failed to activate virtual environment." Red
    exit 1
}
Write-Host "`n"


# Install dependencies
Write-Styled "🔄 Installing dependencies from requirements.txt..." Cyan
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Styled "❌ Failed to install dependencies." Red
        exit 1
    }
    Write-Styled "✅ Dependencies installed successfully." Green
}
else {
    Write-Styled "⚠️  Warning: requirements.txt not found. Skipping package installation." Yellow
    $warningFound = $true
}
Write-Host ""


# Check for .env file
Write-Styled "🔄 Checking for .env file..." Cyan
if (-Not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Styled "⚠️  .env file was missing. Created one from .env.example. Please configure it." Magenta
        # $warningFound = $true
    }
    else {
        Write-Styled "📍 No .env or .env.example file found. You may need to create one manually." DarkRed
        $warningFound = $true
    }
}
Write-Host ""

# Check if any warnings were found
if ($warningFound) {
    Write-Styled "✨ Setup completed with warnings!" Yellow 
}
else {
    Write-Styled "🎉 Setup completed successfully! Happy coding! 🚀" Green
}
