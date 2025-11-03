# ========================================
# Notebook Environment Setup Script
# ========================================
# This script creates a virtual environment for Jupyter notebooks
# that shares the same dependencies as the backend agent.

param(
    [switch]$Force
)

Write-Host "Setting up Notebook Environment..." -ForegroundColor Cyan

# --- Configuration ---
$NotebooksDir = $PSScriptRoot
$ProjectRoot = Split-Path -Parent $NotebooksDir
$AgentDir = Join-Path $ProjectRoot "agent"
$VenvName = ".venv-notebooks"
$VenvPath = Join-Path $NotebooksDir $VenvName

# --- Step 1: Check if uv is installed ---
Write-Host "`nStep 1: Checking for uv installation..." -ForegroundColor Yellow
$uvCheck = Get-Command uv -ErrorAction SilentlyContinue
if ($null -eq $uvCheck) {
    Write-Host "[ERROR] uv not found." -ForegroundColor Red
    Write-Host "Please install uv first: pip install uv" -ForegroundColor Yellow
    exit 1
}
$uvVersion = uv --version 2>&1
Write-Host "[OK] uv found: $uvVersion" -ForegroundColor Green

# --- Step 2: Remove existing environment if -Force flag is used ---
if ($Force -and (Test-Path $VenvPath)) {
    Write-Host "`nStep 2: Removing existing environment..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $VenvPath
    Write-Host "[OK] Existing environment removed" -ForegroundColor Green
}

# --- Step 3: Create virtual environment ---
if (-not (Test-Path $VenvPath)) {
    Write-Host "`nStep 3: Creating virtual environment..." -ForegroundColor Yellow
    Set-Location $NotebooksDir
    uv venv $VenvName --python 3.11
    Write-Host "[OK] Virtual environment created at: $VenvPath" -ForegroundColor Green
} else {
    Write-Host "`nStep 3: Virtual environment already exists" -ForegroundColor Green
}

# --- Step 4: Activate environment and install dependencies ---
Write-Host "`nStep 4: Installing dependencies from agent pyproject.toml..." -ForegroundColor Yellow

$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"

if (Test-Path $ActivateScript) {
    Write-Host "Installing backend dependencies + dev extras..." -ForegroundColor Cyan
    
    # Upgrade pip first
    & "$VenvPath\Scripts\python.exe" -m pip install --upgrade pip
    
    # Install dependencies using uv pip
    uv pip install --python "$VenvPath\Scripts\python.exe" -e "$AgentDir[dev]"
    
    Write-Host "[OK] Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Activation script not found" -ForegroundColor Red
    exit 1
}

# --- Step 5: Verify Jupyter installation ---
Write-Host "`nStep 5: Verifying Jupyter installation..." -ForegroundColor Yellow
$JupyterCheck = Test-Path "$VenvPath\Scripts\jupyter.exe"
if ($JupyterCheck) {
    $JupyterVersion = & "$VenvPath\Scripts\jupyter.exe" --version 2>&1
    Write-Host "[OK] Jupyter installed successfully" -ForegroundColor Green
    Write-Host $JupyterVersion
} else {
    Write-Host "[ERROR] Jupyter installation verification failed" -ForegroundColor Red
    exit 1
}

# --- Step 6: Create IPython kernel ---
Write-Host "`nStep 6: Creating Jupyter kernel..." -ForegroundColor Yellow
& "$VenvPath\Scripts\python.exe" -m ipykernel install --user --name="podcast-agent-notebooks" --display-name="PodCast Agent (Python 3.11)"
Write-Host "[OK] Kernel 'podcast-agent-notebooks' created" -ForegroundColor Green

# --- Step 7: Create .env file for notebooks if it doesn't exist ---
$NotebooksEnvFile = Join-Path $NotebooksDir ".env"
$MainEnvFile = Join-Path $AgentDir ".env"

if (-not (Test-Path $NotebooksEnvFile)) {
    Write-Host "`nStep 7: Creating .env file for notebooks..." -ForegroundColor Yellow
    
    if (Test-Path $MainEnvFile) {
        Copy-Item $MainEnvFile $NotebooksEnvFile
        
        # Append notebook-specific settings
        $NotebookSettings = @"

# --- NOTEBOOK-SPECIFIC SETTINGS ---
JUPYTER_ENABLE_LAB=yes
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=podcast-agent-prototyping
"@
        Add-Content -Path $NotebooksEnvFile -Value $NotebookSettings
        
        Write-Host "[OK] .env file created from main .env with notebook settings" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] Main .env file not found at: $MainEnvFile" -ForegroundColor Yellow
        Write-Host "Please create notebooks/.env manually" -ForegroundColor Yellow
    }
} else {
    Write-Host "`nStep 7: .env file already exists" -ForegroundColor Green
}

# --- Success Message ---
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Notebook environment setup complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nTo activate the environment, run:" -ForegroundColor Cyan
Write-Host "  cd notebooks" -ForegroundColor White
Write-Host "  .\.venv-notebooks\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "`nTo start Jupyter Lab:" -ForegroundColor Cyan
Write-Host "  jupyter lab" -ForegroundColor White
Write-Host "`nThe kernel 'PodCast Agent (Python 3.11)' is now available in Jupyter" -ForegroundColor Cyan
