# Emotionally Intelligent AI — Research Project

## Setup
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Root Command Hub
You can run commands for any section directly from project root using the `Makefile`.

```bash
# Show all section-wise commands
make section-cmds

# Run any command inside a section
make run SECTION=frontend CMD="npm run dev"
make run SECTION=backend CMD="uvicorn app.main:app --reload"
make run SECTION=ml CMD="python test_chatbots.py"
```

Quick shortcuts:

```bash
make backend-dev
make frontend-dev
make frontend-build
make frontend-lint
make ml-test-setup
make ml-test-chatbots
make ml-test-detector
make research-download
```

## Structure
- `ml/` — All machine learning code
- `backend/` — FastAPI REST API
- `frontend/` — Next.js chat UI
- `research/` — Datasets and thesis notes





## ✅ Phase 1 Checklist
```
□ Python 3.11 installed
□ Git configured
□ Project folder + structure created
□ Virtual environment created & activated
□ All packages installed
□ requirements.txt saved
□ .gitignore set up
□ README written
□ Pushed to GitHub
□ VS Code extensions installed
□ test_setup.py passes ✅
□ GoEmotions dataset downloaded
```

## ✅ Phase 2 Checklist
```
□ detector.py created
□ test_detector.py passes ✅
□ Model downloads and caches (~300MB)
□ All 4 test cases pass
□ Dataset analysis script runs
□ Committed and pushed to GitHub
```
## ✅ Phase 3 Checklist
```
□ traditional_chatbot/bot.py created
□ ei_chatbot/bot.py created
□ test_chatbots.py runs successfully
□ Both bots respond to all 5 messages
□ Session log saved to research/sample_session_log.json
□ Committed and pushed to GitHub
```

## ✅ Phase 4 Checklist
```
□ Dependencies installed (sqlalchemy, aiosqlite)
□ .env file created
□ All backend files created
□ uvicorn starts without errors
□ /docs page loads in browser
□ /api/chat/start returns session_id
□ /api/chat/message returns bot response
□ /api/analytics/summary returns data
□ Committed and pushed
```