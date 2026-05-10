import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# 1. Setup Files and Anatomical Titles
# The list matches the order [6, 5, 4, 3, 2, 1]
files = [f'Cluster{i}_values.txt' for i in [6, 5, 4, 3, 2, 1]]

titles = [
    'Lateral Occipital (Sup)\nCluster 6',
    'Lateral Occipital (Inf)\nCluster 5',
    'Lateral Occipital (Inf)\nCluster 4',
    'Precentral / IFG\nCluster 3',
    'Paracingulate Gyrus\nCluster 2',
    'Insular / FOrb Cortex\nCluster 1'
]

means = []
conf_intervals = []
stars = []
p_values = []

# 2. Statistical Calculations
for file in files:
    data = np.loadtxt(file)
    means.append(np.mean(data))
    # Calculate 95% Confidence Interval
    conf_intervals.append(stats.sem(data) * stats.t.ppf((1 + 0.95) / 2, len(data) - 1))
    
    # Perform One-sample t-test
    _, p = stats.ttest_1samp(data, 0)
    p_values.append(p)

# 3. Apply Bonferroni Correction
num_comparisons = len(files)
for p in p_values:
    corrected_p = p * num_comparisons
    
    if corrected_p < 0.001:
        stars.append('***')
    elif corrected_p < 0.01:
        stars.append('**')
    elif corrected_p < 0.05:
        stars.append('*')
    else:
        stars.append('ns')

# 4. Plotting
plt.figure(figsize=(12, 7))
bars = plt.bar(titles, means, yerr=conf_intervals, capsize=7, color='#2c5985', edgecolor='black', alpha=0.8)

# Add Significance Stars
for i, bar in enumerate(bars):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + conf_intervals[i] + 2, 
             stars[i], ha='center', fontweight='bold', fontsize=12)

plt.title('Corrected Statistical Significance by Brain Region (Bonferroni)', fontsize=14, pad=20)
plt.ylabel('Mean BOLD Signal (Z-statistic)', fontsize=12)
plt.axhline(0, color='black', linewidth=0.8) # Baseline
plt.grid(axis='y', linestyle='--', alpha=0.3)

plt.tight_layout()
plt.savefig('Corrected_Regions_Report.png')
plt.show()