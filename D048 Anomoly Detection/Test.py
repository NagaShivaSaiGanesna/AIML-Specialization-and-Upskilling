from sklearn.datasets import make_circles
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import numpy as np

# Generate a non-linearly separable dataset (two concentric circles)
X, y = make_circles(n_samples=750, factor=0.5, noise=0.05)
# Note: y is not used — this is unsupervised

# Apply DBSCAN
db = DBSCAN(eps=0.10, min_samples=5)
labels = db.fit_predict(X)
# Labels: 0, 1, 2, ... for clusters; -1 for outliers/noise

# Identify outlier indices
outlier_indices = np.where(labels == -1)[0]

# Visualize
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', label='Clusters')
plt.scatter(X[outlier_indices, 0], X[outlier_indices, 1],
            edgecolors='red', facecolors='none', s=100, label='Outliers')
plt.legend()
plt.title('DBSCAN Anomaly Detection')
plt.show()