# JarvisAI — Clone and Recovery Guide

This file contains everything needed to restore the project after a fresh clone.
Model weights are intentionally excluded from Git because GitHub rejects files larger than 100 MB.

## System requirements

- Windows 11
- Python 3.11 (64-bit)
- Ollama
- A working microphone and speaker
- NVIDIA GPU/CUDA is recommended; CPU mode is possible but slower
- Internet access is required during the first installation

## Fresh installation

Open PowerShell in the directory where you want the project, then run:

```powershell
git clone https://github.com/Ratchakrit20/Jarvis.git
cd Jarvis
Set-ExecutionPolicy -Scope Process Bypass
.\install.ps1
```

The installer will:

1. Create `.venv` with Python 3.11.
2. Install packages from `requirements.txt`.
3. Download the Thai Whisper model into `app/models/`.
4. Pull `qwen3:8b` through Ollama.
5. Run a lightweight installation check.

Model downloads can be skipped when restoring from a local backup:

```powershell
.\install.ps1 -SkipModels
```

For a machine without CUDA:

```powershell
.\install.ps1 -CpuOnly
```

## Start Jarvis

Make sure Ollama is running, then execute:

```powershell
.\.venv\Scripts\python.exe .\jarvis.py
```

Jarvis listens for speech and only processes a command after detecting the wake word
`จาร์วิส` or one of its configured aliases.

## Check an existing installation

```powershell
.\.venv\Scripts\python.exe .\scripts\doctor.py
```

## Download models separately

Download both Whisper and the Ollama model:

```powershell
.\.venv\Scripts\python.exe .\scripts\download_models.py
```

Download only Whisper:

```powershell
.\.venv\Scripts\python.exe .\scripts\download_models.py --skip-ollama
```

Pull only the Ollama model:

```powershell
.\.venv\Scripts\python.exe .\scripts\download_models.py --skip-whisper
```

## Files intentionally not stored in Git

- `.venv/` — rebuilt from `requirements.txt`
- `app/models/` and model weight files — rebuilt by `scripts/download_models.py`
- `.env` — machine-specific configuration; use `.env.example` as a template
- `logs/`, Python caches and generated audio files

Do not force-add these files. They are either large, generated, or machine-specific.

## Manual recovery checklist

If the automatic installer fails, perform these commands one at a time:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\scripts\download_models.py
.\.venv\Scripts\python.exe .\scripts\doctor.py
```

If `ollama pull qwen3:8b` fails, start Ollama and retry:

```powershell
ollama pull qwen3:8b
```

## Recommended backup policy

Keep source code, documentation, tests, `requirements.txt`, and recovery scripts in GitHub.
Keep irreplaceable data and future long-term memory databases in a separate encrypted backup.
Downloaded AI models do not need backup because they can be downloaded again.
