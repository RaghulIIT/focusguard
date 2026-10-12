# FOCUSGUARD — Focus Management Prototype

A student-project prototype for **FOCUSGUARD**, a digital wellbeing website that helps users plan focus sessions and build healthier screen-time habits.

## Features
- Focus timer with start, pause, and reset
- Pomodoro-style session length setting
- Daily focus goal and progress
- Personal distraction/block list (prototype simulation)
- Focus session history and streak-style progress
- Browser-local saving with `localStorage`
- Optional FastAPI + SQLite backend for saving completed sessions

> **Important prototype limitation:** A normal website cannot block other websites or reliably measure browsing activity across tabs. This demo manages focus sessions and simulates a block list. Real website blocking requires a browser extension and explicit user permissions.

## Run the frontend
Open `frontend/index.html` in a browser. No build step is required.

## Run the backend (optional)
Requires Python 3.10+.

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

API docs: http://127.0.0.1:8000/docs

## API endpoints
- `GET /` — health check
- `GET /sessions` — list completed sessions
- `POST /sessions` — save a completed focus session
- `GET /stats` — total focus minutes and session count

## Upload to GitHub
1. Extract this ZIP.
2. Create a new repository on https://github.com/new (suggested name: `focusguard`).
3. Upload the extracted files, or use Git:
   ```bash
   git init
   git add .
   git commit -m "Add FocusGuard prototype"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/focusguard.git
   git push -u origin main
   ```
4. Replace `YOUR-USERNAME` with your GitHub username.

## Suggested next steps
- Add a browser extension for actual website blocking.
- Connect the frontend to the FastAPI API.
- Add user authentication only if needed; do not store sensitive data without a clear privacy design.
