import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Concurrency levels to compare
concurrency_levels = [10, 20, 50]

# Load and tag all benchmark CSVs
all_data = []

# Load Knative
for level in concurrency_levels:
    filename = f"benchmark_output_{level}.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df["platform"] = "Knative"
        df["concurrency"] = level
        df.rename(columns={"ID": "request_id", "Time (ms)": "duration_ms", "Start": "start_type"}, inplace=True)
        df["start_type"] = df["start_type"].str.lower().fillna("unknown")
        all_data.append(df)

# Load Lambda
for level in concurrency_levels:
    filename = f"lambda_benchmark_results_{level}.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df["platform"] = "Lambda"
        df["concurrency"] = level
        df.rename(columns={"ID": "request_id", "Time (ms)": "duration_ms", "Start": "start_type"}, inplace=True)
        df["start_type"] = df["start_type"].str.lower().fillna("unknown")
        all_data.append(df)

# Combine all into a single DataFrame
df_all = pd.concat(all_data, ignore_index=True)

# Only include cold and warm start types
df_filtered = df_all[df_all["start_type"].isin(["cold", "warm"])]

# Group for summary
summary = df_filtered.groupby(["platform", "concurrency", "start_type"]).agg(
    avg_duration_ms=("duration_ms", "mean"),
    count=("request_id", "count")
).reset_index()

# Split into Knative and Lambda data
knative_data = summary[summary["platform"] == "Knative"]
lambda_data = summary[summary["platform"] == "Lambda"]

# Plot
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Knative subplot
sns.barplot(ax=axes[0], data=knative_data, x="concurrency", y="avg_duration_ms", hue="start_type", palette="Set2")
axes[0].set_title("Knative: Cold vs Warm Start")
axes[0].set_xlabel("Concurrency Level")
axes[0].set_ylabel("Average Duration (ms)")
axes[0].legend(title="Start Type")
axes[0].grid(True, axis='y', linestyle='--', alpha=0.4)

# Lambda subplot
sns.barplot(ax=axes[1], data=lambda_data, x="concurrency", y="avg_duration_ms", hue="start_type", palette="Set2")
axes[1].set_title("AWS Lambda: Cold vs Warm Start")
axes[1].set_xlabel("Concurrency Level")
axes[1].set_ylabel("")
axes[1].legend(title="Start Type")
axes[1].grid(True, axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig("knative_vs_lambda.png")
plt.show()
