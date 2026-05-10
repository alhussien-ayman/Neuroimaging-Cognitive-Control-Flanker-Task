import numpy as np
import matplotlib.pyplot as plt
import os

BASE = "ROI_results_new"

main_blue_color = "#587898"

labels_ordered = ["Incongruent", "Congruent", "Inc - Con"]

region_names = {
    1: "Insula / OFC",
    2: "Paracingulate / ACC",
    3: "Precentral / IFG",
    4: "LOC Inf / MTG",
    5: "LOC Inf / Occipital Pole",
    6: "LOC Sup / Precuneus"
}

# =========================
# اختر الـ 4 clusters بنفسك هنا
# =========================
selected_clusters = [1, 5, 3, 4]

# =========================
# LOAD DATA
# =========================
data_list = []

for c in selected_clusters:

    con_file = os.path.join(BASE, f"ROI{c}_con_meanZ.txt")
    incon_file = os.path.join(BASE, f"ROI{c}_incon_meanZ.txt")

    if not os.path.exists(con_file) or not os.path.exists(incon_file):
        print(f"Missing ROI {c} → skipped")
        continue

    con = np.loadtxt(con_file)
    incon = np.loadtxt(incon_file)
    diff = incon - con

    data_list.append((c, con, incon, diff))

# =========================
# GLOBAL Y AXIS (FIXED MAX = 5)
# =========================
all_vals = []
for (_, con, incon, diff) in data_list:
    all_vals.extend(con)
    all_vals.extend(incon)
    all_vals.extend(diff)

y_min = min(0, np.min(all_vals))
y_max = 5

# =========================
# PLOT
# =========================
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes = axes.flatten()

for i, (c, con, incon, diff) in enumerate(data_list):

    means = [
        np.mean(incon),
        np.mean(con),
        np.mean(diff)
    ]

    stds = [
        np.std(incon),
        np.std(con),
        np.std(diff)
    ]

    ax = axes[i]

    ax.bar(labels_ordered, means, yerr=stds,
           color=main_blue_color,
           capsize=5,
           edgecolor='black')

    ax.set_title(f"Cluster {c}: {region_names.get(c, '')}",
                 fontsize=10, fontweight='bold')

    ax.set_ylim(y_min, y_max)

    ax.axhline(0, color='black', linewidth=1)
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # optional significance marker (simple)
    if abs(means[0] - means[1]) > 0.5:
        ax.text(0.5, 4.5, "**",
                ha='center',
                fontsize=14,
                color='darkorange',
                fontweight='bold')

    ax.tick_params(axis='x', rotation=15)

# remove extra plots if needed
for j in range(len(data_list), 4):
    fig.delaxes(axes[j])

plt.tight_layout()

out = os.path.join(BASE, "Selected4_Clusters_Fixed.png")
plt.savefig(out, dpi=300, bbox_inches="tight")

plt.show()

print("Saved selected clusters figure")