# Hemalatha Freelancing — Projects Portfolio

This repository contains a collection of Python demo projects and small automation tools prepared for a freelancing portfolio. Each project is self-contained under the `Projects/` directory and includes a `main.py`, `README.md`, `requirements.txt`, and `screenshots/` with demo GIFs and images.

Highlights
- Cloud & DevOps: AWS EC2/S3 automation, Docker manager, Kubernetes health checker
- Data & Automation: Excel automation, log analyzers, CI/CD report generator
- Real-time: WebSocket chat, log tailer Web UI, MQTT sensor simulator, file watcher, system metrics streamer

How to use
1. Clone this repo locally.
2. Create and activate a Python virtual environment.
3. Install requirements for a project (example):

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
\.venv\Scripts\activate    # Windows PowerShell
pip install -r Projects/Project14_CICD_Pipeline_Report_Generator/requirements.txt
```

Run demos with `--demo` where available, e.g.:

```bash
python Projects/RT01_WebSocket_Chat_Server/main.py --demo
```

If you plan to push to GitHub, make sure to exclude large files (like `Projects.zip`) from commits — this repo already contains a `.gitignore` for that.

