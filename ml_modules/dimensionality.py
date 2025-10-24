"""
Dimensionality Reduction Module
Implements PCA and SVD
"""
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.preprocessing import StandardScaler
from ml_modules.visualization import DataVisualizer

class DimensionalityReduction:
    """Handle dimensionality reduction tasks"""
    
    def __init__(self, X):
        self.X = X
        self.X_scaled = None
        self.model = None
        self.X_reduced = None
        self.scaler = StandardScaler()
        
    def scale_data(self):
        """Scale features"""
        self.X_scaled = self.scaler.fit_transform(self.X)
        return self.X_scaled
    
    def pca_analysis(self, n_components=None):
        """Perform PCA"""
        if self.X_scaled is None:
            self.scale_data()
        
        # If n_components not specified, use all components
        if n_components is None:
            n_components = min(self.X_scaled.shape)
        
        self.model = PCA(n_components=n_components, random_state=42)
        self.X_reduced = self.model.fit_transform(self.X_scaled)
        
        explained_variance = self.model.explained_variance_ratio_
        cumulative_variance = np.cumsum(explained_variance)
        
        # Find number of components for 95% variance
        n_components_95 = np.argmax(cumulative_variance >= 0.95) + 1
        
        results = {
            'algorithm': 'Principal Component Analysis (PCA)',
            'n_components': int(n_components),
            'n_components_95_variance': int(n_components_95),
            'explained_variance_ratio': explained_variance.tolist(),
            'cumulative_variance': cumulative_variance.tolist(),
            'total_variance_explained': round(float(cumulative_variance[-1]), 4),
            'original_dimensions': int(self.X.shape[1]),
            'reduced_dimensions': int(n_components)
        }
        
        # Variance plot
        results['variance_plot'] = DataVisualizer.plot_pca_variance(
            explained_variance, cumulative_variance
        )
        
        # Component loadings (contribution of each feature to components)
        if hasattr(self.model, 'components_'):
            loadings = pd.DataFrame(
                self.model.components_.T,
                columns=[f'PC{i+1}' for i in range(n_components)],
                index=self.X.columns
            )
            results['component_loadings'] = loadings.to_dict()
            
            # Top contributing features for first 3 PCs
            top_features = {}
            for i in range(min(3, n_components)):
                pc_name = f'PC{i+1}'
                abs_loadings = loadings[pc_name].abs().sort_values(ascending=False)
                top_features[pc_name] = abs_loadings.head(5).to_dict()
            results['top_features_per_component'] = top_features
        
        return results
    
    def svd_analysis(self, n_components=None):
        """Perform Truncated SVD"""
        if self.X_scaled is None:
            self.scale_data()
        
        # SVD requires n_components < min(n_samples, n_features)
        max_components = min(self.X_scaled.shape) - 1
        if n_components is None or n_components >= max_components:
            n_components = max_components
        
        self.model = TruncatedSVD(n_components=n_components, random_state=42)
        self.X_reduced = self.model.fit_transform(self.X_scaled)
        
        explained_variance = self.model.explained_variance_ratio_
        cumulative_variance = np.cumsum(explained_variance)
        
        # Find number of components for 95% variance
        n_components_95 = np.argmax(cumulative_variance >= 0.95) + 1 if any(cumulative_variance >= 0.95) else n_components
        
        results = {
            'algorithm': 'Singular Value Decomposition (SVD)',
            'n_components': int(n_components),
            'n_components_95_variance': int(n_components_95),
            'explained_variance_ratio': explained_variance.tolist(),
            'cumulative_variance': cumulative_variance.tolist(),
            'total_variance_explained': round(float(cumulative_variance[-1]), 4),
            'original_dimensions': int(self.X.shape[1]),
            'reduced_dimensions': int(n_components),
            'singular_values': self.model.singular_values_.tolist()
        }
        
        # Variance plot
        results['variance_plot'] = DataVisualizer.plot_pca_variance(
            explained_variance, cumulative_variance
        )
        
        # Component loadings
        if hasattr(self.model, 'components_'):
            loadings = pd.DataFrame(
                self.model.components_.T,
                columns=[f'SVD{i+1}' for i in range(n_components)],
                index=self.X.columns
            )
            results['component_loadings'] = loadings.to_dict()
            
            # Top contributing features
            top_features = {}
            for i in range(min(3, n_components)):
                svd_name = f'SVD{i+1}'
                abs_loadings = loadings[svd_name].abs().sort_values(ascending=False)
                top_features[svd_name] = abs_loadings.head(5).to_dict()
            results['top_features_per_component'] = top_features
        
        return results
    
    def get_reduced_data(self, n_components=2):
        """Get reduced dataset for visualization or further analysis"""
        if self.X_reduced is None:
            self.pca_analysis(n_components)
        
        # Create dataframe with reduced dimensions
        columns = [f'Component_{i+1}' for i in range(self.X_reduced.shape[1])]
        df_reduced = pd.DataFrame(self.X_reduced, columns=columns)
        
        return df_reduced
