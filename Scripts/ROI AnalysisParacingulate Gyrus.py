import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ROI values
values = np.array([
    1.382849,
    0.251498,
    1.076516,
    -0.204187,
    -0.083569,
    0.211481,
    0.745574,
    0.717658,
    0.266753,
    0.032209,
    -0.272230,
    0.278538,
    -0.076362,
    -0.154583,
    -0.108827,
    -0.390160,
    0.219326,
    -0.927641,
    -0.624439,
    -0.148986,
    -0.009286,
    0.362603,
    1.010809,
    -0.373671,
    -0.552863,
    0.213336
])

subjects = np.arange(1, len(values) + 1)

# =========================
# Statistical Analysis
# =========================

t_stat, p_value = stats.ttest_1samp(values, 0)

mean_val = np.mean(values)
std_val = np.std(values)

print("\n===== ROI Statistical Analysis =====")
print(f"Mean Activation : {mean_val:.4f}")
print(f"Standard Deviation : {std_val:.4f}")
print(f"T-statistic : {t_stat:.4f}")
print(f"P-value : {p_value:.6f}")

if p_value < 0.05:
    print("Result: Significant activation detected (p < 0.05)")
else:
    print("Result: No significant activation detected")

# =========================
# Modern Visualization
# =========================

plt.style.use('default')

fig, ax = plt.subplots(figsize=(12, 6))

# Background
fig.patch.set_facecolor('#f8fafc')
ax.set_facecolor('#f8fafc')

# Scatter plot
scatter = ax.scatter(
    subjects,
    values,
    s=100,
    c=values,
    cmap='coolwarm',
    edgecolors='black',
    linewidths=0.8,
    alpha=0.9,
    zorder=3
)

# Mean line
ax.axhline(
    mean_val,
    color='#2563eb',
    linewidth=2.5,
    label=f'Mean = {mean_val:.2f}'
)

# Zero line
ax.axhline(
    0,
    color='#64748b',
    linestyle='--',
    linewidth=1.5
)

# Standard deviation band
ax.fill_between(
    [0, len(values)+1],
    mean_val - std_val,
    mean_val + std_val,
    color='#93c5fd',
    alpha=0.25,
    label='±1 SD'
)

# Labels
ax.set_title(
    'ROI Analysis — Paracingulate Gyrus',
    fontsize=20,
    fontweight='bold',
    pad=20
)

ax.set_xlabel('Subjects', fontsize=14)
ax.set_ylabel('Mean Z-stat Value', fontsize=14)

# Grid
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.3)

# Remove extra borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Legend
ax.legend(fontsize=11, frameon=True)

# Colorbar
cbar = plt.colorbar(scatter, ax=ax, pad=0.02)
cbar.set_label('Activation Strength', fontsize=12)

# Statistical annotation
ax.text(
    0.02,
    0.95,
    f't = {t_stat:.2f}\np = {p_value:.4f}',
    transform=ax.transAxes,
    fontsize=12,
    verticalalignment='top',
    bbox=dict(
        boxstyle='round,pad=0.4',
        facecolor='white',
        alpha=0.85,
        edgecolor='gray'
    )
)

plt.tight_layout()
plt.show()