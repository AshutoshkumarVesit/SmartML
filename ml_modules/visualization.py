"""
Visualization Module
Generate various plots for data exploration and model results
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import base64
import json

# Set style
sns.set_style("whitegrid")
plt.style.use('seaborn-v0_8-darkgrid')

class DataVisualizer:
    """Handle all visualization tasks"""
    
    def __init__(self, df):
        self.df = df
    
    @staticmethod
    def fig_to_base64(fig):
        """Convert matplotlib figure to base64 string"""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return f"data:image/png;base64,{img_base64}"
    
    def correlation_heatmap(self):
        """Generate correlation heatmap"""
        numeric_df = self.df.select_dtypes(include=['int64', 'float64'])
        
        if numeric_df.shape[1] < 2:
            return None
        
        fig, ax = plt.subplots(figsize=(12, 10))
        correlation = numeric_df.corr()
        
        sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, square=True, ax=ax, cbar_kws={"shrink": 0.8})
        ax.set_title('Correlation Heatmap', fontsize=16, fontweight='bold', pad=20)
        
        return self.fig_to_base64(fig)
    
    def distribution_plots(self, max_cols=6):
        """Generate distribution plots for numeric columns"""
        numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns[:max_cols]
        
        if len(numeric_cols) == 0:
            return None
        
        n_cols = min(3, len(numeric_cols))
        n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        if n_rows == 1:
            axes = axes.reshape(1, -1) if len(numeric_cols) > 1 else np.array([[axes]])
        
        for idx, col in enumerate(numeric_cols):
            row = idx // n_cols
            col_idx = idx % n_cols
            ax = axes[row, col_idx] if n_rows > 1 or len(numeric_cols) > 1 else axes[0, 0]
            
            self.df[col].hist(bins=30, ax=ax, edgecolor='black', alpha=0.7)
            ax.set_title(f'Distribution of {col}', fontweight='bold')
            ax.set_xlabel(col)
            ax.set_ylabel('Frequency')
        
        # Hide empty subplots
        for idx in range(len(numeric_cols), n_rows * n_cols):
            row = idx // n_cols
            col_idx = idx % n_cols
            axes[row, col_idx].axis('off')
        
        plt.tight_layout()
        return self.fig_to_base64(fig)
    
    def boxplots(self, max_cols=6):
        """Generate boxplots for numeric columns"""
        numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns[:max_cols]
        
        if len(numeric_cols) == 0:
            return None
        
        n_cols = min(3, len(numeric_cols))
        n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        if n_rows == 1:
            axes = axes.reshape(1, -1) if len(numeric_cols) > 1 else np.array([[axes]])
        
        for idx, col in enumerate(numeric_cols):
            row = idx // n_cols
            col_idx = idx % n_cols
            ax = axes[row, col_idx] if n_rows > 1 or len(numeric_cols) > 1 else axes[0, 0]
            
            self.df.boxplot(column=col, ax=ax)
            ax.set_title(f'Boxplot of {col}', fontweight='bold')
            ax.set_ylabel(col)
        
        # Hide empty subplots
        for idx in range(len(numeric_cols), n_rows * n_cols):
            row = idx // n_cols
            col_idx = idx % n_cols
            axes[row, col_idx].axis('off')
        
        plt.tight_layout()
        return self.fig_to_base64(fig)
    
    def pairplot_plotly(self, max_cols=5):
        """Generate interactive pairplot using plotly"""
        numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns[:max_cols]
        
        if len(numeric_cols) < 2:
            return None
        
        fig = px.scatter_matrix(self.df[numeric_cols],
                               dimensions=numeric_cols,
                               title='Pairplot (Scatter Matrix)')
        
        fig.update_traces(diagonal_visible=False, showupperhalf=False)
        fig.update_layout(height=800, width=1000)
        
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    @staticmethod
    def plot_confusion_matrix(cm, labels=None):
        """Plot confusion matrix"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=labels, yticklabels=labels,
                   ax=ax, cbar_kws={"shrink": 0.8})
        
        ax.set_title('Confusion Matrix', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('True Label', fontsize=12)
        ax.set_xlabel('Predicted Label', fontsize=12)
        
        return DataVisualizer.fig_to_base64(fig)
    
    @staticmethod
    def plot_regression_results(y_true, y_pred):
        """Plot regression results"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Actual vs Predicted
        axes[0].scatter(y_true, y_pred, alpha=0.6, edgecolors='k')
        axes[0].plot([y_true.min(), y_true.max()], 
                    [y_true.min(), y_true.max()], 
                    'r--', lw=2, label='Perfect Prediction')
        axes[0].set_xlabel('Actual Values', fontsize=12)
        axes[0].set_ylabel('Predicted Values', fontsize=12)
        axes[0].set_title('Actual vs Predicted', fontsize=14, fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Residual Plot
        residuals = y_true - y_pred
        axes[1].scatter(y_pred, residuals, alpha=0.6, edgecolors='k')
        axes[1].axhline(y=0, color='r', linestyle='--', lw=2)
        axes[1].set_xlabel('Predicted Values', fontsize=12)
        axes[1].set_ylabel('Residuals', fontsize=12)
        axes[1].set_title('Residual Plot', fontsize=14, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return DataVisualizer.fig_to_base64(fig)
    
    @staticmethod
    def plot_feature_importance(importance_dict, top_n=10):
        """Plot feature importance"""
        # Sort by importance
        sorted_features = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)[:top_n]
        features, importances = zip(*sorted_features)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        y_pos = np.arange(len(features))
        ax.barh(y_pos, importances, color='skyblue', edgecolor='navy')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(features)
        ax.invert_yaxis()
        ax.set_xlabel('Importance', fontsize=12)
        ax.set_title(f'Top {len(features)} Feature Importances', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        return DataVisualizer.fig_to_base64(fig)
    
    @staticmethod
    def plot_cluster_results(X, labels, centers=None):
        """Plot clustering results (2D projection)"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        scatter = ax.scatter(X[:, 0], X[:, 1], c=labels, 
                           cmap='viridis', alpha=0.6, 
                           edgecolors='k', s=50)
        
        if centers is not None:
            ax.scatter(centers[:, 0], centers[:, 1], 
                      c='red', marker='X', s=200, 
                      edgecolors='black', linewidths=2,
                      label='Centroids')
        
        ax.set_title('Cluster Visualization', fontsize=14, fontweight='bold')
        ax.set_xlabel('Component 1', fontsize=12)
        ax.set_ylabel('Component 2', fontsize=12)
        plt.colorbar(scatter, ax=ax, label='Cluster')
        if centers is not None:
            ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return DataVisualizer.fig_to_base64(fig)
    
    @staticmethod
    def plot_elbow_curve(inertias, k_range):
        """Plot elbow curve for K-Means"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(k_range, inertias, 'bo-', linewidth=2, markersize=8)
        ax.set_xlabel('Number of Clusters (k)', fontsize=12)
        ax.set_ylabel('Inertia (Within-cluster sum of squares)', fontsize=12)
        ax.set_title('Elbow Method For Optimal k', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return DataVisualizer.fig_to_base64(fig)
    
    @staticmethod
    def plot_pca_variance(explained_variance_ratio, cumulative_variance):
        """Plot PCA explained variance"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Individual explained variance
        n_components = len(explained_variance_ratio)
        axes[0].bar(range(1, n_components + 1), explained_variance_ratio, 
                   alpha=0.7, color='skyblue', edgecolor='navy')
        axes[0].set_xlabel('Principal Component', fontsize=12)
        axes[0].set_ylabel('Explained Variance Ratio', fontsize=12)
        axes[0].set_title('Explained Variance by Component', fontsize=14, fontweight='bold')
        axes[0].grid(True, alpha=0.3, axis='y')
        
        # Cumulative explained variance
        axes[1].plot(range(1, n_components + 1), cumulative_variance, 
                    'ro-', linewidth=2, markersize=8)
        axes[1].axhline(y=0.95, color='g', linestyle='--', 
                       label='95% Explained Variance')
        axes[1].set_xlabel('Number of Components', fontsize=12)
        axes[1].set_ylabel('Cumulative Explained Variance', fontsize=12)
        axes[1].set_title('Cumulative Explained Variance', fontsize=14, fontweight='bold')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return DataVisualizer.fig_to_base64(fig)
    
    @staticmethod
    def plot_decision_tree(model, feature_names, class_names, max_depth=3):
        """Plot Decision Tree structure"""
        from sklearn.tree import plot_tree
        
        # Limit depth for readability
        actual_depth = min(model.get_depth(), max_depth)
        
        # Calculate figure size based on tree depth
        fig_width = max(20, actual_depth * 5)
        fig_height = max(12, actual_depth * 3)
        
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        
        plot_tree(
            model,
            feature_names=feature_names,
            class_names=[str(c) for c in class_names],
            filled=True,
            rounded=True,
            fontsize=10,
            max_depth=max_depth,
            ax=ax,
            impurity=True,
            proportion=True
        )
        
        ax.set_title(f'Decision Tree Visualization (showing top {max_depth} levels)', 
                    fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        return DataVisualizer.fig_to_base64(fig)
    
    @staticmethod
    def plot_random_forest_trees(model, feature_names, class_names, n_trees_to_show=3):
        """Plot sample trees from Random Forest"""
        from sklearn.tree import plot_tree
        
        n_trees = min(n_trees_to_show, len(model.estimators_))
        fig, axes = plt.subplots(1, n_trees, figsize=(25, 8))
        
        if n_trees == 1:
            axes = [axes]
        
        for idx in range(n_trees):
            plot_tree(
                model.estimators_[idx],
                feature_names=feature_names,
                class_names=[str(c) for c in class_names],
                filled=True,
                rounded=True,
                fontsize=8,
                max_depth=3,
                ax=axes[idx],
                impurity=False,
                proportion=True
            )
            axes[idx].set_title(f'Tree {idx + 1} of {len(model.estimators_)}', 
                               fontsize=14, fontweight='bold')
        
        plt.suptitle('Random Forest - Sample Trees', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        return DataVisualizer.fig_to_base64(fig)
    
    @staticmethod
    def plot_feature_importance_detailed(feature_importance_dict, title='Feature Importance'):
        """Enhanced feature importance plot with sorted bars and value labels"""
        features = list(feature_importance_dict.keys())
        importances = list(feature_importance_dict.values())
        
        # Sort by importance
        indices = np.argsort(importances)[::-1]
        features_sorted = [features[i] for i in indices]
        importances_sorted = [importances[i] for i in indices]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, max(6, len(features) * 0.3)))
        
        # Create horizontal bar chart
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(features_sorted)))
        bars = ax.barh(range(len(features_sorted)), importances_sorted, color=colors, edgecolor='navy', linewidth=1.5)
        
        # Customize
        ax.set_yticks(range(len(features_sorted)))
        ax.set_yticklabels(features_sorted, fontsize=10)
        ax.set_xlabel('Importance Score', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, importances_sorted)):
            ax.text(val + max(importances_sorted) * 0.01, i, f'{val:.4f}', 
                   va='center', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        return DataVisualizer.fig_to_base64(fig)
    
    @staticmethod
    def plot_svm_decision_boundary(X, y, model, feature_names):
        """Plot SVM decision boundary using first 2 principal components"""
        from sklearn.decomposition import PCA
        
        # Reduce to 2D using PCA if needed
        if X.shape[1] > 2:
            pca = PCA(n_components=2)
            X_2d = pca.fit_transform(X)
            x_label = f'PC1 ({pca.explained_variance_ratio_[0]:.1%} var)'
            y_label = f'PC2 ({pca.explained_variance_ratio_[1]:.1%} var)'
        else:
            X_2d = X.values if hasattr(X, 'values') else X
            x_label = feature_names[0] if len(feature_names) > 0 else 'Feature 1'
            y_label = feature_names[1] if len(feature_names) > 1 else 'Feature 2'
        
        # Create coarser mesh for faster rendering
        h = 0.1  # Increased from 0.02 for speed
        x_min, x_max = X_2d[:, 0].min() - 1, X_2d[:, 0].max() + 1
        y_min, y_max = X_2d[:, 1].min() - 1, X_2d[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        
        # Train a new model on 2D data for visualization
        from sklearn.svm import SVC
        model_2d = SVC(kernel=model.kernel, C=model.C if hasattr(model, 'C') else 1.0, gamma='auto')
        model_2d.fit(X_2d, y)
        
        # Predict on mesh
        Z = model_2d.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        
        # Plot
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Decision boundary
        ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdYlBu, levels=2)
        ax.contour(xx, yy, Z, colors='black', linewidths=1.5, alpha=0.8, levels=1)
        
        # Plot points
        scatter = ax.scatter(X_2d[:, 0], X_2d[:, 1], c=y, cmap=plt.cm.RdYlBu, 
                           edgecolors='black', s=100, alpha=0.8, linewidth=1.5)
        
        # Support vectors
        if hasattr(model_2d, 'support_vectors_'):
            ax.scatter(model_2d.support_vectors_[:, 0], model_2d.support_vectors_[:, 1],
                      s=250, linewidth=3, facecolors='none', edgecolors='lime', 
                      label=f'Support Vectors ({len(model_2d.support_vectors_)})', zorder=10)
        
        ax.set_xlabel(x_label, fontsize=12, fontweight='bold')
        ax.set_ylabel(y_label, fontsize=12, fontweight='bold')
        ax.set_title(f'SVM Decision Boundary (kernel={model.kernel})', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=11, framealpha=0.9)
        ax.grid(True, alpha=0.3)
        
        plt.colorbar(scatter, ax=ax, label='Class')
        plt.tight_layout()
        return DataVisualizer.fig_to_base64(fig)
    
    @staticmethod
    def plot_regression_results(y_true, y_pred, algorithm_name='Regression'):
        """Plot actual vs predicted and residuals for regression"""
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Plot 1: Actual vs Predicted
        axes[0].scatter(y_true, y_pred, alpha=0.6, s=80, edgecolors='navy', linewidth=1)
        
        # Perfect prediction line
        min_val = min(y_true.min(), y_pred.min())
        max_val = max(y_true.max(), y_pred.max())
        axes[0].plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')
        
        axes[0].set_xlabel('Actual Values', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Predicted Values', fontsize=12, fontweight='bold')
        axes[0].set_title(f'{algorithm_name} - Actual vs Predicted', fontsize=14, fontweight='bold')
        axes[0].legend(fontsize=10)
        axes[0].grid(True, alpha=0.3)
        
        # Plot 2: Residuals
        residuals = y_true - y_pred
        axes[1].scatter(y_pred, residuals, alpha=0.6, s=80, c=residuals, cmap='coolwarm', 
                       edgecolors='black', linewidth=1)
        axes[1].axhline(y=0, color='red', linestyle='--', linewidth=2, label='Zero Residual')
        
        axes[1].set_xlabel('Predicted Values', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Residuals (Actual - Predicted)', fontsize=12, fontweight='bold')
        axes[1].set_title(f'{algorithm_name} - Residual Plot', fontsize=14, fontweight='bold')
        axes[1].legend(fontsize=10)
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return DataVisualizer.fig_to_base64(fig)
    
    @staticmethod
    def plot_cluster_results_3d(X, labels, centers=None, title='Cluster Visualization'):
        """Enhanced 2D/3D cluster visualization"""
        from sklearn.decomposition import PCA
        
        # If X has more than 2 dimensions, reduce using PCA
        if X.shape[1] > 2:
            pca = PCA(n_components=min(3, X.shape[1]))
            X_proj = pca.fit_transform(X)
            var_explained = pca.explained_variance_ratio_
        else:
            X_proj = X
            var_explained = [1.0, 1.0]
        
        # Determine if 2D or 3D
        n_components = X_proj.shape[1]
        
        if n_components >= 3:
            # 3D plot
            fig = plt.figure(figsize=(14, 10))
            ax = fig.add_subplot(111, projection='3d')
            
            scatter = ax.scatter(X_proj[:, 0], X_proj[:, 1], X_proj[:, 2], 
                               c=labels, cmap='viridis', s=50, alpha=0.6, edgecolors='black')
            
            if centers is not None and len(centers) > 0:
                if centers.shape[1] != n_components:
                    centers_proj = pca.transform(centers)
                else:
                    centers_proj = centers
                ax.scatter(centers_proj[:, 0], centers_proj[:, 1], centers_proj[:, 2],
                          c='red', marker='X', s=300, edgecolors='black', linewidth=2, label='Centroids')
            
            ax.set_xlabel(f'PC1 ({var_explained[0]:.1%} var)', fontsize=10, fontweight='bold')
            ax.set_ylabel(f'PC2 ({var_explained[1]:.1%} var)', fontsize=10, fontweight='bold')
            ax.set_zlabel(f'PC3 ({var_explained[2]:.1%} var)', fontsize=10, fontweight='bold')
            
        else:
            # 2D plot
            fig, ax = plt.subplots(figsize=(12, 8))
            
            scatter = ax.scatter(X_proj[:, 0], X_proj[:, 1], 
                               c=labels, cmap='viridis', s=100, alpha=0.6, edgecolors='black', linewidth=1)
            
            if centers is not None and len(centers) > 0:
                if centers.shape[1] != n_components:
                    centers_proj = pca.transform(centers)
                else:
                    centers_proj = centers
                ax.scatter(centers_proj[:, 0], centers_proj[:, 1],
                          c='red', marker='X', s=300, edgecolors='black', linewidth=2, label='Centroids')
            
            ax.set_xlabel(f'PC1 ({var_explained[0]:.1%} var)', fontsize=12, fontweight='bold')
            ax.set_ylabel(f'PC2 ({var_explained[1]:.1%} var)', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend()
        
        plt.title(title, fontsize=14, fontweight='bold', pad=20)
        plt.colorbar(scatter, ax=ax if n_components == 2 else None, label='Cluster')
        plt.tight_layout()
        return DataVisualizer.fig_to_base64(fig)
