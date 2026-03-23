# Create this file: research/download_dataset.py

from datasets import load_dataset
import pandas as pd
import os

print("📥 Downloading GoEmotions dataset from HuggingFace (free)...")

# Load from HuggingFace datasets — no account needed
dataset = load_dataset("go_emotions", "simplified")

# Convert to pandas for easy analysis
train_df = pd.DataFrame(dataset["train"])
test_df = pd.DataFrame(dataset["test"])
val_df = pd.DataFrame(dataset["validation"])

# Save locally
os.makedirs("research/datasets", exist_ok=True)
train_df.to_csv("research/datasets/go_emotions_train.csv", index=False)
test_df.to_csv("research/datasets/go_emotions_test.csv", index=False)
val_df.to_csv("research/datasets/go_emotions_val.csv", index=False)

print(f"✅ Train samples: {len(train_df)}")
print(f"✅ Test samples:  {len(test_df)}")
print(f"✅ Val samples:   {len(val_df)}")
print(f"\n📊 Columns: {list(train_df.columns)}")
print(f"\n🔍 Sample row:")
print(train_df.head(2).to_string())

print("\n✅ Dataset saved to research/datasets/")