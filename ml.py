import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram

# Function to calculate Euclidean distance
def euclidean_distance(a, b):
    return np.linalg.norm(a - b)

# Generate data
n = 10
data = np.random.rand(n + 1, 2)

# Define linkage methods
linkage_methods = ['single', 'complete', 'average']

# Perform hierarchical clustering for each linkage method
for method in linkage_methods:
    # Calculate pairwise distance matrix
    distance_matrix = np.zeros((n + 1, n + 1))
    for i in range(n + 1):
        for j in range(n + 1):
            distance_matrix[i, j] = euclidean_distance(data[i], data[j])

    # Perform hierarchical clustering
    Z = linkage(distance_matrix, method)

    # Plot dendrogram
    plt.figure(figsize=(10, 5))
    dendrogram(Z)
    plt.title(f'{method.capitalize()} Linkage Dendrogram')
    plt.xlabel('Data Points')
    plt.ylabel('Euclidean Distance')
    plt.show()
