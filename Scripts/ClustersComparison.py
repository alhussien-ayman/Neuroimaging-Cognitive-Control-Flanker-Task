import matplotlib.pyplot as plt
import numpy as np

# لستة الملفات الـ 6
files = [f'Cluster{i}_values.txt' for i in [6, 5, 4, 3, 2, 1]]
titles = ['Cluster 6', 'Cluster 5', 'Cluster 4', 'Cluster 3', 'Cluster 2', 'Cluster 1']

fig, axes = plt.subplots(3, 2, figsize=(15, 12)) # 3 صفوف وعمودين
axes = axes.flatten()

for i, file in enumerate(files):
    data = np.loadtxt(file)
    subjects = np.arange(1, len(data) + 1)
    mean_val = np.mean(data)
    
    colors = ['steelblue' if v >= 0 else 'indianred' for v in data]
    axes[i].vlines(subjects, 0, data, colors=colors)
    axes[i].scatter(subjects, data, c=colors)
    axes[i].axhline(mean_val, color='steelblue', linestyle='--')
    axes[i].axhline(0, color='black', linewidth=0.8)
    axes[i].set_title(titles[i])

plt.tight_layout()
plt.savefig('All_Clusters_Report.png')
plt.show()