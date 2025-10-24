"""
Clustering Algorithms Module
Implements K-Means and DBSCAN clustering
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from ml_modules.visualization import DataVisualizer

class ClusteringModel:
    """Handle clustering tasks"""
    
    def __init__(self, X):
        self.X = X
        self.X_scaled = None
        self.model = None
        self.labels = None
        self.scaler = StandardScaler()
        
    def scale_data(self):
        """Scale features for clustering"""
        self.X_scaled = self.scaler.fit_transform(self.X)
        return self.X_scaled
    
    def kmeans(self, n_clusters=3, init='k-means++', n_init=10):
        """Perform K-Means clustering"""
        if self.X_scaled is None:
            self.scale_data()
        
        # Limit n_init for faster computation
        self.model = KMeans(
            n_clusters=n_clusters,
            init=init,
            n_init=min(n_init, 5),  # Reduce iterations for speed
            max_iter=300,
            random_state=42
        )
        self.labels = self.model.fit_predict(self.X_scaled)
        
        results = self._calculate_metrics()
        results['n_clusters'] = n_clusters
        results['algorithm'] = 'K-Means Clustering'
        results['cluster_centers'] = self.model.cluster_centers_.tolist()
        results['inertia'] = float(self.model.inertia_)
        
        # Enhanced 3D visualization (with timeout protection)
        try:
            results['cluster_plot'] = DataVisualizer.plot_cluster_results_3d(
                self.X_scaled, 
                self.labels,
                centers=self.model.cluster_centers_,
                title=f'K-Means Clustering (K={n_clusters})'
            )
        except Exception as e:
            print(f"Warning: Could not generate 3D cluster plot: {str(e)}")
            results['cluster_plot'] = None
        
        # Cluster distribution
        unique, counts = np.unique(self.labels, return_counts=True)
        results['cluster_distribution'] = {f'Cluster {int(k)}': int(v) for k, v in zip(unique, counts)}
        
        return results
    
    def kmeans_elbow(self, k_range=range(2, 11)):
        """Find optimal K using elbow method"""
        if self.X_scaled is None:
            self.scale_data()
        
        inertias = []
        silhouette_scores = []
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
            kmeans.fit(self.X_scaled)
            inertias.append(kmeans.inertia_)
            
            labels = kmeans.labels_
            if len(np.unique(labels)) > 1:
                silhouette_scores.append(silhouette_score(self.X_scaled, labels))
            else:
                silhouette_scores.append(0)
        
        elbow_plot = DataVisualizer.plot_elbow_curve(inertias, list(k_range))
        
        return {
            'k_range': list(k_range),
            'inertias': inertias,
            'silhouette_scores': silhouette_scores,
            'elbow_plot': elbow_plot,
            'recommended_k': list(k_range)[np.argmax(silhouette_scores)]
        }
    
    def dbscan(self, eps=0.5, min_samples=5):
        """Perform DBSCAN clustering"""
        if self.X_scaled is None:
            self.scale_data()
        
        self.model = DBSCAN(eps=eps, min_samples=min_samples)
        self.labels = self.model.fit_predict(self.X_scaled)
        
        n_clusters = len(set(self.labels)) - (1 if -1 in self.labels else 0)
        n_noise = list(self.labels).count(-1)
        
        results = {
            'algorithm': 'DBSCAN Clustering',
            'eps': eps,
            'min_samples': min_samples,
            'n_clusters': n_clusters,
            'n_noise_points': n_noise,
            'total_samples': len(self.labels)
        }
        
        # Only calculate metrics if we have valid clusters
        if n_clusters > 1:
            # Filter out noise points for metric calculation
            mask = self.labels != -1
            if np.sum(mask) > 0:
                try:
                    results['silhouette_score'] = round(
                        silhouette_score(self.X_scaled[mask], self.labels[mask]), 4
                    )
                except:
                    results['silhouette_score'] = None
        
        # Enhanced 3D visualization
        results['cluster_plot'] = DataVisualizer.plot_cluster_results_3d(
            self.X_scaled,
            self.labels,
            centers=None,
            title=f'DBSCAN Clustering (eps={eps}, min_samples={min_samples})'
        )
        
        # Cluster distribution
        unique, counts = np.unique(self.labels, return_counts=True)
        cluster_dist = {}
        for label, count in zip(unique, counts):
            key = 'Noise' if int(label) == -1 else f'Cluster {int(label)}'
            cluster_dist[key] = int(count)
        results['cluster_distribution'] = cluster_dist
        
        return results
    
    def _calculate_metrics(self):
        """Calculate clustering metrics"""
        metrics = {}
        
        # Silhouette Score
        if len(np.unique(self.labels)) > 1:
            metrics['silhouette_score'] = round(
                silhouette_score(self.X_scaled, self.labels), 4
            )
        
        # Davies-Bouldin Index (lower is better)
        if len(np.unique(self.labels)) > 1:
            metrics['davies_bouldin_score'] = round(
                davies_bouldin_score(self.X_scaled, self.labels), 4
            )
        
        # Calinski-Harabasz Index (higher is better)
        if len(np.unique(self.labels)) > 1:
            metrics['calinski_harabasz_score'] = round(
                calinski_harabasz_score(self.X_scaled, self.labels), 4
            )
        
        return metrics
    
    def _get_2d_projection(self):
        """Get 2D projection using PCA for visualization"""
        pca = PCA(n_components=2)
        return pca.fit_transform(self.X_scaled)
