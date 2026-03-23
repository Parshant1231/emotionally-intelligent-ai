# ml/notebooks/dataset_analysis.py
# Exploratory Data Analysis on GoEmotions dataset
# This generates stats you can put directly in your thesis

import pandas as pd
import json
from collections import Counter

print("📊 Loading GoEmotions dataset...")

train_df = pd.read_csv("../../research/datasets/go_emotions_train.csv")
test_df  = pd.read_csv("../../research/datasets/go_emotions_test.csv")
val_df   = pd.read_csv("../../research/datasets/go_emotions_val.csv")

total = len(train_df) + len(test_df) + len(val_df)

print("\n" + "="*50)
print("📌 DATASET OVERVIEW")
print("="*50)
print(f"  Training samples   : {len(train_df):,}")
print(f"  Test samples       : {len(test_df):,}")
print(f"  Validation samples : {len(val_df):,}")
print(f"  Total samples      : {total:,}")
print(f"\n  Columns: {list(train_df.columns)}")

print("\n📌 SAMPLE DATA (first 3 rows):")
print(train_df.head(3).to_string())

print("\n📌 LABEL DISTRIBUTION (Training set):")
# labels column contains lists — count each label
from ast import literal_eval
all_labels = []
for labels in train_df["labels"]:
    parsed = literal_eval(str(labels)) if isinstance(labels, str) else labels
    all_labels.extend(parsed if isinstance(parsed, list) else [parsed])

label_counts = Counter(all_labels)
print(f"  Unique label values: {sorted(set(all_labels))}")
print(f"  Most common: {label_counts.most_common(5)}")

print("\n✅ Dataset analysis complete!")
print("Use these stats in your thesis Chapter 3 (Methodology).")