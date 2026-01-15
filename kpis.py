import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Setting seaborn style
sns.set_theme(
    style="whitegrid",
    context="paper",
    font_scale=1.2
)


# KPI data
data = {
    "Method": ["CP", "MIP"],
    "Cmax": [61, 61],
    "Solve Time (s)": [0.07, 0.23],
    "Variables": [43, 127],
    "Constraints": [45, 246],
    "Binaries": [0, 90],
}

df = pd.DataFrame(data)

# Plotting makespan comparision

plt.figure(figsize=(6, 4))
ax = sns.barplot(
    data=df,
    x="Method",
    y="Cmax",
    palette="muted"
)
ax.set_title("FT06 — Makespan (Cmax)")
ax.set_ylabel("Cmax")
ax.set_xlabel("")

for i, v in enumerate(df["Cmax"]):
    ax.text(i, v, f"{v}", ha="center", va="bottom")

plt.tight_layout()
plt.savefig("results/figures/kpi_ft06_makespan.png", dpi=300)
plt.close()

# Plotting solve time comparison

plt.figure(figsize=(6, 4))
ax = sns.barplot(
    data=df,
    x="Method",
    y="Solve Time (s)",
    palette="muted"
)
ax.set_title("FT06 — Total Solve Time")
ax.set_ylabel("Time (seconds)")
ax.set_xlabel("")

for i, v in enumerate(df["Solve Time (s)"]):
    ax.text(i, v, f"{v:.2f}", ha="center", va="bottom")

plt.tight_layout()
plt.savefig("results/figures/kpi_ft06_solve_time.png", dpi=300)
plt.close()

# Plot model size comparision

df_size = df.melt(
    id_vars="Method",
    value_vars=["Variables", "Constraints", "Binaries"],
    var_name="Metric",
    value_name="Count"
)

plt.figure(figsize=(8, 4))
ax = sns.barplot(
    data=df_size,
    x="Method",
    y="Count",
    hue="Metric",
    palette="Set2"
)

ax.set_title("FT06 — Model Size Comparison")
ax.set_ylabel("Count")
ax.set_xlabel("")
ax.legend(title="Metric")

for container in ax.containers:
    ax.bar_label(container, padding=2)

plt.tight_layout()
plt.savefig("results/figures/kpi_ft06_model_size.png", dpi=300)
plt.close()


