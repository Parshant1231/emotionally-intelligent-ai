# ml/test_setup.py
# Run this to verify your entire setup is working

import sys
print(f"✅ Python version: {sys.version}")

import torch
print(f"✅ PyTorch version: {torch.__version__}")

import transformers
print(f"✅ Transformers version: {transformers.__version__}")

import fastapi
print(f"✅ FastAPI version: {fastapi.__version__}")

import pandas
print(f"✅ Pandas version: {pandas.__version__}")

print("\n🎉 All packages working. Phase 1 complete!")
