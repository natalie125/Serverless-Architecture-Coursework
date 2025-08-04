import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load and combine all CSVs
dataframes = []
for level in [10, 20, 50]:
    filename = f"benchmark_output_{level}.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df["concurrency"] = level
        dataframes.append(df)
    else:
        print(f" File not found: {filename}")

# Merge into one DataFrame
df_all = pd.concat(dataframes, ignore_index=True)

df_all["Start"] = df_all["Start"].str.lower().fillna("unknown")

# Group and calculate average duration for cold/warm
summary = df_all[df_all["Start"].isin(["cold", "warm"])].groupby(
    ["concurrency", "Start"]
).agg(
    avg_duration_ms=("Time (ms)", "mean"),
    count=("ID", "count")
).reset_index()

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(data=summary, x="concurrency", y="avg_duration_ms", hue="Start")

plt.title("Knative Performance: Cold vs Warm Starts at Varying Concurrency")
plt.xlabel("Concurrency Level")
plt.ylabel("Average Duration (ms)")
plt.legend(title="Start Type")
plt.tight_layout()

# Save the graph to a file
plt.savefig("benchmark_comparison.png")

# Show the graph
plt.show()
