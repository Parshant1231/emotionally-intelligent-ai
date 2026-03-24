.DEFAULT_GOAL := help

SECTIONS := backend frontend ml research

.PHONY: help section-cmds run backend-dev frontend-dev frontend-build frontend-lint ml-test-setup ml-test-chatbots ml-test-detector research-download

help:
	@echo "Emotionally Intelligent AI - Root Commands"
	@echo ""
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@echo "Common targets:"
	@echo "  make section-cmds      # Show section-wise commands"
	@echo "  make run SECTION=<name> CMD=\"<command>\""
	@echo ""
	@echo "Examples:"
	@echo "  make run SECTION=frontend CMD=\"npm run dev\""
	@echo "  make run SECTION=backend CMD=\"uvicorn app.main:app --reload\""
	@echo ""
	@echo "Dev shortcuts:"
	@echo "  make backend-dev"
	@echo "  make frontend-dev"
	@echo "  make frontend-build"
	@echo "  make frontend-lint"
	@echo "  make ml-test-setup"
	@echo "  make ml-test-chatbots"
	@echo "  make ml-test-detector"
	@echo "  make research-download"

section-cmds:
	@echo "Section command map"
	@echo ""
	@echo "[backend]"
	@echo "  uvicorn app.main:app --reload"
	@echo ""
	@echo "[frontend]"
	@echo "  npm install"
	@echo "  npm run dev"
	@echo "  npm run build"
	@echo "  npm run lint"
	@echo ""
	@echo "[ml]"
	@echo "  python test_setup.py"
	@echo "  python test_chatbots.py"
	@echo "  python emotion_detector/test_detector.py"
	@echo ""
	@echo "[research]"
	@echo "  python research/download_dataset.py"

run:
	@if [ -z "$(SECTION)" ] || [ -z "$(CMD)" ]; then \
		echo "Usage: make run SECTION=<backend|frontend|ml|research> CMD=\"<command>\""; \
		exit 1; \
	fi
	@if ! echo "$(SECTIONS)" | grep -qw "$(SECTION)"; then \
		echo "Invalid SECTION='$(SECTION)'. Allowed: $(SECTIONS)"; \
		exit 1; \
	fi
	@echo "Running in $(SECTION): $(CMD)"
	@cd $(SECTION) && sh -c '$(CMD)'

backend-dev:
	@cd backend && uvicorn app.main:app --reload --port 8000

frontend-dev:
	@cd frontend && npm run dev

frontend-build:
	@cd frontend && npm run build

frontend-lint:
	@cd frontend && npm run lint

ml-test-setup:
	@cd ml && python test_setup.py

ml-test-chatbots:
	@cd ml && python test_chatbots.py

ml-test-detector:
	@cd ml && python emotion_detector/test_detector.py

research-download:
	@python research/download_dataset.py
