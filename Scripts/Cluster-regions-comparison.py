import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
import numpy as np
import os

# -----------------------------
# STYLE
# -----------------------------
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.linewidth': 0.8,
})

# -----------------------------
# DATA
# -----------------------------
cluster_order = [6, 5, 4, 3, 2, 1]

data = {
    6: [98.81,31.11,73.11,26.10,93.34,98.94,148.84,93.51,50.48,51.19,20.80,15.38,31.05,-29.17,73.42,28.67,41.68,29.86,-3.57,12.19,66.74,78.90,110.88,57.81,9.08,-12.39],
    5: [74.52,13.93,63.02,110.18,62.21,39.56,46.78,57.18,17.36,22.32,36.52,55.78,55.59,-32.54,67.97,48.70,43.37,-3.58,23.13,30.25,101.71,13.98,95.10,12.47,19.90,39.96],
    4: [95.05,57.88,85.49,2.86,59.55,69.25,84.29,144.40,19.96,36.07,60.70,27.93,53.20,68.86,96.97,25.34,25.94,-41.56,29.48,-24.08,5.81,-56.34,109.93,14.10,-35.07,27.81],
    3: [140.80,52.49,123.11,60.49,63.95,21.56,85.44,34.53,3.93,11.70,26.88,127.24,25.00,11.05,94.97,37.05,33.67,2.18,-26.68,-4.80,77.94,28.00,69.04,33.81,15.24,19.66],
    2: [78.16,52.91,89.15,91.88,18.99,101.14,164.38,158.75,18.56,-48.56,66.13,90.48,8.56,-20.09,75.84,29.39,45.22,-0.61,-55.15,-15.59,38.72,55.33,139.77,22.31,-24.76,48.23],
    1: [89.69,34.61,126.01,45.80,88.75,-6.32,76.38,80.65,-1.13,3.41,31.95,77.59,25.71,-8.15,19.57,54.60,81.27,-44.33,-30.63,6.49,91.61,111.20,82.72,-5.00,3.15,10.14],
}

region_info = {
    6: {'short': 'Lateral Occipital (Sup)', 'color': '#0d3b66', 'mni': 'MNI: 24,-66,48'},
    5: {'short': 'Lateral Occipital (Inf)', 'color': '#1a5c96', 'mni': 'MNI: 42,-88,-6'},
    4: {'short': 'Occipital Cortex', 'color': '#1d6fa3', 'mni': 'MNI: 52,-68,-4'},
    3: {'short': 'Frontal / Motor', 'color': '#155e8a', 'mni': 'MNI: 44,4,22'},
    2: {'short': 'Cingulate', 'color': '#0e4d7a', 'mni': 'MNI: 4,16,46'},
    1: {'short': 'Insula / Orbital', 'color': '#1a6ea8', 'mni': 'MNI: 32,22,-6'},
}

# -----------------------------
# FIGURE
# -----------------------------
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

x = np.arange(26)

for idx, cnum in enumerate(cluster_order):

    ax = axes[idx]
    vals = np.array(data[cnum])
    info = region_info[cnum]

    mean = np.mean(vals)
    sem = np.std(vals, ddof=1) / np.sqrt(len(vals))
    sd = np.std(vals, ddof=1)

    # bars only
    colors = [info['color'] if v >= 0 else '#c0392b' for v in vals]

    ax.bar(x, vals, color=colors, alpha=0.8, width=0.7)

    # mean line
    ax.axhline(mean, color='black', linewidth=1.5)

    # SEM band
    ax.axhspan(mean - sem, mean + sem, color=info['color'], alpha=0.15)

    # zero line
    ax.axhline(0, color='gray', linewidth=0.8)

    # title
    ax.set_title(info['short'], fontsize=10, color=info['color'])

    # mni only (clean)
    ax.text(0.02, 0.95, info['mni'],
            transform=ax.transAxes,
            fontsize=8, va='top')

    # formatting
    ax.set_xlim(-0.5, 25.5)
    ax.set_xticks(x[::5])
    ax.set_xticklabels([f'V{i+1}' for i in x[::5]], fontsize=7)

    ax.yaxis.set_major_locator(ticker.MultipleLocator(50))
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# -----------------------------
# SAVE
# -----------------------------
output_dir = r"E:\FMRI python\outputs"
os.makedirs(output_dir, exist_ok=True)

save_path = os.path.join(output_dir, "clean_fmri_plot.png")

plt.tight_layout()
plt.savefig(save_path, dpi=400, bbox_inches='tight')

plt.close()

print("Saved successfully at:", save_path)