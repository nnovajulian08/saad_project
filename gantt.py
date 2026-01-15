import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", font_scale=1.1)

# LOAD FILE
instance = "ft06"
method = "CP"

filename = f"{instance}_schedule_{method}.csv"
df = pd.read_csv(f"results/{filename}")


# Clean column names 
df.columns = [c.strip() for c in df.columns]

# Ensure numeric
for col in ["Job", "Operation", "Machine", "Start", "End"]:
    df[col] = pd.to_numeric(df[col])

# Sort for nicer plotting
df = df.sort_values(["Machine", "Start"]).reset_index(drop=True)

# COLOR MAP (one color per job)
jobs = sorted(df["Job"].unique())
cmap = plt.get_cmap("tab10")  # makes it good for up to 10 jobs
job_to_color = {job: cmap(i % 10) for i, job in enumerate(jobs)}

# Palatte change
palette = sns.color_palette("Set3", n_colors=len(jobs))
job_to_color = dict(zip(jobs, palette))


# PLOT SECTION
machines = sorted(df["Machine"].unique())
machine_to_y = {m: i for i, m in enumerate(machines)}

fig, ax = plt.subplots(figsize=(16, 9))

bar_height = 0.8

for _, r in df.iterrows():
    job = int(r["Job"])
    op = int(r["Operation"])
    m = int(r["Machine"])
    start = float(r["Start"])
    end = float(r["End"])
    dur = end - start

    y = machine_to_y[m]

    ax.barh(
        y=y,
        width=dur,
        left=start,
        height=bar_height,
        color=job_to_color[job],
        edgecolor="black",
        linewidth=0.6
    )

    ax.text(
        start + dur / 2,
        y,
        f"J{job}-O{op}",
        ha="center",
        va="center",
        fontsize=9,
        color="black"
    )

# Y axis formatting
ax.set_yticks([machine_to_y[m] for m in machines])
ax.set_yticklabels([f"M{m}" for m in machines])

ax.set_xlabel("Time")
ax.set_ylabel("Machine")
ax.set_title(f"Job Shop Schedule (MIP) — Gantt Chart ({instance})")

ax.grid(axis="x", linestyle="--", alpha=0.4)

# Legend 
handles = [
    plt.Line2D([0], [0], color=job_to_color[j], lw=8, label=f"Job {j}")
    for j in jobs
]

ax.legend(
    handles=handles,
    title="Jobs",
    loc="upper center",
    bbox_to_anchor=(0.5, -0.12),
    ncol=len(jobs),
    frameon=False
)

plt.savefig(f"results/figures/gantt_{instance}_{method}.png", dpi=200, bbox_inches="tight")
plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.show()

