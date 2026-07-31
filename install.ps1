param(
    [switch]$SkipModels,
    [switch]$CpuOnly
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "Python launcher (py) was not found. Install Python 3.11 first."
}

if (-not (Test-Path $VenvPython)) {
    Write-Host "Creating Python 3.11 virtual environment..."
    py -3.11 -m venv (Join-Path $ProjectRoot ".venv")
}

Write-Host "Installing Python dependencies..."
& $VenvPython -m pip install --upgrade pip

if ($CpuOnly) {
    & $VenvPython -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
}

& $VenvPython -m pip install -r (Join-Path $ProjectRoot "requirements.txt")

if (-not $SkipModels) {
    Write-Host "Downloading models. This can take several minutes..."
    & $VenvPython (Join-Path $ProjectRoot "scripts\download_models.py")
}

Write-Host "Running installation checks..."
& $VenvPython (Join-Path $ProjectRoot "scripts\doctor.py")

Write-Host "Installation finished. Start Jarvis with:"
Write-Host ".\.venv\Scripts\python.exe .\jarvis.py"
