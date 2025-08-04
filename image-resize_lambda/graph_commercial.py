import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load and combine all CSVs
dataframes = []
for level in [10, 20, 50]:
    filename = f"lambda_benchmark_results_{level}.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df["concurrency"] = level
        dataframes.append(df)
    else:
        print(f" File not found: {filename}")

# Merge into one DataFrame
df_all = pd.concat(dataframes, ignore_index=True)

df_all["start_type"] = df_all["start_type"].str.lower().fillna("unknown")

# Group and calculate average duration for cold/warm
summary = df_all[df_all["start_type"].isin(["cold", "warm"])].groupby(
    ["concurrency", "start_type"]
).agg(
    avg_duration_ms=("duration_ms", "mean"),
    count=("request_id", "count")
).reset_index()

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(data=summary, x="concurrency", y="avg_duration_ms", hue="start_type")

plt.title("AWS Lambda Performance: Cold vs Warm Starts at Varying Concurrency")
plt.xlabel("Concurrency Level")
plt.ylabel("Average Duration (ms)")
plt.legend(title="Start Type")
plt.tight_layout()


# Save plot
output_file = "lambda_cold_warm_comparison.png"
plt.savefig(output_file)
print(f" Graph saved as: {output_file}")

plt.show()