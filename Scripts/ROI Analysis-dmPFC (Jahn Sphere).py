import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# =========================
# ROI values from fslmeants
# =========================
values = np.array([
    1.328597,
    0.747626,
    1.265742,
    0.513243,
    0.963755,
    1.420346,
    1.878770,
    1.968835,
    -0.084014,
    -0.179238,
    0.416731,
    1.368610,
    -0.378935,
    -0.218356,
    0.853670,
    0.429024,
    1.175458,
    0.153742,
    -0.740903,
    0.493883,
    0.637472,
    0.911115,
    1.552971,
    0.327688,
    -0.811581,
    0.991190
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
# Visualization
# =========================
plt.style.use('default')

fig, ax = plt.subplots(figsize=(12, 6))

fig.patch.set_facecolor('#f8fafc')
ax.set_facecolor('#f8fafc')

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

ax.axhline(mean_val, color='#2563eb', linewidth=2.5, label=f'Mean = {mean_val:.2f}')
ax.axhline(0, color='#64748b', linestyle='--', linewidth=1.5)

ax.fill_between(
    [0, len(values)+1],
    mean_val - std_val,
    mean_val + std_val,
    color='#93c5fd',
    alpha=0.25,
    label='±1 SD'
)

ax.set_title('ROI Analysis — dmPFC (Jahn Sphere)', fontsize=20, fontweight='bold', pad=20)
ax.set_xlabel('Volumes', fontsize=14)
ax.set_ylabel('Mean Z-stat Value', fontsize=14)

ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.legend(fontsize=11, frameon=True)

cbar = plt.colorbar(scatter, ax=ax, pad=0.02)
cbar.set_label('Activation Strength', fontsize=12)

ax.text(
    0.02, 0.95,
    f't = {t_stat:.2f}\np = {p_value:.4f}',
    transform=ax.transAxes,
    fontsize=12,
    verticalalignment='top',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.85, edgecolor='gray')
)

plt.tight_layout()
plt.show()