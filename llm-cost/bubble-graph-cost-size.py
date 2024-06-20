import pandas as pd
import matplotlib.pyplot as plt

# Add a legend for the sources
from matplotlib.patches import Patch

# Load the Excel file
file_path = "LLM_Pricing.xlsx"
pricing_models_df = pd.read_excel(file_path, sheet_name="Pricing + Models")

# Convert 'Context size' column to numeric by removing 'k' and converting to int
pricing_models_df["Context size"] = (
    pricing_models_df["Context size"].str.replace("k", "").astype(int) * 1000
)

# Add a column to distinguish between open and closed source
open_source_companies = ["Meta", "Mistral", "Cohere"]
pricing_models_df["Source"] = pricing_models_df["Developer"].apply(
    lambda x: "Open Source" if x in open_source_companies else "Closed Source"
)

# Visualization 1: Bubble chart comparing cost of input vs output, with bubble size as context size and color by developer
fig, ax = plt.subplots(figsize=(12, 8))
scatter = ax.scatter(
    pricing_models_df["Input $/1M"],
    pricing_models_df["Output $/1M"],
    s=pricing_models_df["Context size"] / 100,  # Scale up the bubble size
    c=pd.factorize(pricing_models_df["Developer"])[0],
    cmap="viridis",
    alpha=0.6,
)

# Add labels and title
ax.set_xlabel("Input Cost per 1M Tokens ($)")
ax.set_ylabel("Output Cost per 1M Tokens ($)")
ax.set_title("Cost of Input vs Output with Context Size and Developer")

# Add a legend for the developers
legend1 = ax.legend(
    *scatter.legend_elements(),
    title="Developers",
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
)
ax.add_artist(legend1)

plt.show()

# Visualization 2: Bar chart of cost per token, ordered by context window size and distinguished by source
pricing_models_df["Cost per Token"] = pricing_models_df["Avg. $/1M"] / 1_000_000
sorted_df = pricing_models_df.sort_values(by="Context size", ascending=False)

fig, ax = plt.subplots(figsize=(14, 8))
bars = ax.bar(
    sorted_df["Model"],
    sorted_df["Cost per Token"],
    color=sorted_df["Source"].map({"Open Source": "green", "Closed Source": "blue"}),
)

# Add labels and title
ax.set_xlabel("Model")
ax.set_ylabel("Cost per Token ($)")
ax.set_title("Cost per Token Ordered by Context Window Size")
ax.set_xticks(range(len(sorted_df)))
ax.set_xticklabels(sorted_df["Model"], rotation=90)

legend_labels = [
    Patch(color="green", label="Open Source"),
    Patch(color="blue", label="Closed Source"),
]
ax.legend(
    handles=legend_labels, title="Source", bbox_to_anchor=(1.05, 1), loc="upper left"
)

plt.show()
