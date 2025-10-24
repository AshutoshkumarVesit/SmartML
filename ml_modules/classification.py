"""
Classification Algorithms Module
Implements various classification algorithms
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, confusion_matrix, classification_report)
from ml_modules.visualization import DataVisualizer

class ClassificationModel:
    """Handle classification tasks"""
    
    def __init__(self, X, y, test_size=0.2, random_state=42):
        self.X = X
        self.y = y
        self.test_size = test_size
        self.random_state = random_state
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        self.model = None
        self.predictions = None
        
    def split_data(self):
        """Split data into train and test sets"""
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=self.test_size, random_state=self.random_state, stratify=self.y
        )
        return {
            'train_size': len(self.X_train),
            'test_size': len(self.X_test),
            'feature_count': self.X_train.shape[1],
            'classes': np.unique(self.y).tolist()
        }
    
    def decision_tree(self, max_depth=None, min_samples_split=2):
        """Train Decision Tree Classifier"""
        if self.X_train is None:
            self.split_data()
        
        self.model = DecisionTreeClassifier(
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            random_state=self.random_state
        )
        self.model.fit(self.X_train, self.y_train)
        self.predictions = self.model.predict(self.X_test)
        
        results = self._calculate_metrics()
        results['max_depth'] = max_depth
        results['algorithm'] = 'Decision Tree Classifier'
        
        # Feature importance
        feature_importance = dict(zip(self.X.columns, self.model.feature_importances_))
        results['feature_importance_plot'] = DataVisualizer.plot_feature_importance(feature_importance)
        results['feature_importance'] = feature_importance
        
        # Decision Tree Visualization
        class_names = np.unique(self.y).astype(str).tolist()
        results['tree_plot'] = DataVisualizer.plot_decision_tree(
            self.model, 
            feature_names=self.X.columns.tolist(),
            class_names=class_names,
            max_depth=3  # Show top 3 levels for clarity
        )
        results['tree_depth'] = int(self.model.get_depth())
        results['n_leaves'] = int(self.model.get_n_leaves())
        
        return results
    
    def support_vector_machine(self, kernel='rbf', C=1.0):
        """Train SVM Classifier"""
        if self.X_train is None:
            self.split_data()
        
        # Use probability=True and class_weight='balanced' for better performance
        self.model = SVC(
            kernel=kernel, 
            C=C, 
            random_state=self.random_state, 
            probability=True, 
            max_iter=1000,
            class_weight='balanced',  # Handle imbalanced classes
            gamma='scale'  # Better default for RBF kernel
        )
        self.model.fit(self.X_train, self.y_train)
        self.predictions = self.model.predict(self.X_test)
        
        results = self._calculate_metrics()
        results['kernel'] = kernel
        results['C'] = C
        results['algorithm'] = f'Support Vector Machine (kernel={kernel})'
        
        # Skip decision boundary for large datasets
        if len(self.X_train) > 500:
            print("Info: Skipping SVM decision boundary plot for large dataset")
            results['decision_boundary_plot'] = None
        else:
            # Decision boundary visualization (with error handling)
            try:
                results['decision_boundary_plot'] = DataVisualizer.plot_svm_decision_boundary(
                    self.X_train,
                    self.y_train,
                    self.model,
                    self.X.columns.tolist()
                )
            except Exception as e:
                print(f"Warning: Could not generate SVM decision boundary plot: {str(e)}")
                results['decision_boundary_plot'] = None
        
        results['n_support_vectors'] = int(len(self.model.support_))
        
        return results
    
    def random_forest(self, n_estimators=100, max_depth=None):
        """Train Random Forest Classifier"""
        if self.X_train is None:
            self.split_data()
        
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=self.random_state
        )
        self.model.fit(self.X_train, self.y_train)
        self.predictions = self.model.predict(self.X_test)
        
        results = self._calculate_metrics()
        results['n_estimators'] = n_estimators
        results['algorithm'] = 'Random Forest Classifier'
        
        # Feature importance with enhanced visualization
        feature_importance = dict(zip(self.X.columns, self.model.feature_importances_))
        results['feature_importance_plot'] = DataVisualizer.plot_feature_importance_detailed(
            feature_importance, 
            title='Random Forest - Feature Importance'
        )
        results['feature_importance'] = feature_importance
        
        # Sample trees visualization
        class_names = np.unique(self.y).astype(str).tolist()
        results['forest_trees_plot'] = DataVisualizer.plot_random_forest_trees(
            self.model,
            feature_names=self.X.columns.tolist(),
            class_names=class_names,
            n_trees_to_show=3
        )
        results['n_trees'] = int(n_estimators)
        
        return results
        results['feature_importance_plot'] = DataVisualizer.plot_feature_importance(feature_importance)
        results['feature_importance'] = feature_importance
        
        return results
    
    def adaboost(self, n_estimators=50, learning_rate=1.0):
        """Train AdaBoost Classifier"""
        if self.X_train is None:
            self.split_data()
        
        self.model = AdaBoostClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            random_state=self.random_state
        )
        self.model.fit(self.X_train, self.y_train)
        self.predictions = self.model.predict(self.X_test)
        
        results = self._calculate_metrics()
        results['n_estimators'] = n_estimators
        results['learning_rate'] = learning_rate
        results['algorithm'] = 'AdaBoost Classifier'
        
        # Feature importance
        feature_importance = dict(zip(self.X.columns, self.model.feature_importances_))
        results['feature_importance_plot'] = DataVisualizer.plot_feature_importance(feature_importance)
        results['feature_importance'] = feature_importance
        
        return results
    
    def gradient_boosting(self, n_estimators=100, learning_rate=0.1):
        """Train Gradient Boosting Classifier"""
        if self.X_train is None:
            self.split_data()
        
        self.model = GradientBoostingClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            random_state=self.random_state
        )
        self.model.fit(self.X_train, self.y_train)
        self.predictions = self.model.predict(self.X_test)
        
        results = self._calculate_metrics()
        results['n_estimators'] = n_estimators
        results['learning_rate'] = learning_rate
        results['algorithm'] = 'Gradient Boosting Classifier'
        
        # Feature importance
        feature_importance = dict(zip(self.X.columns, self.model.feature_importances_))
        results['feature_importance_plot'] = DataVisualizer.plot_feature_importance(feature_importance)
        results['feature_importance'] = feature_importance
        
        return results
    
    def _calculate_metrics(self):
        """Calculate classification metrics"""
        accuracy = accuracy_score(self.y_test, self.predictions)
        
        # Handle multi-class vs binary
        average = 'binary' if len(np.unique(self.y)) == 2 else 'weighted'
        
        precision = precision_score(self.y_test, self.predictions, average=average, zero_division=0)
        recall = recall_score(self.y_test, self.predictions, average=average, zero_division=0)
        f1 = f1_score(self.y_test, self.predictions, average=average, zero_division=0)
        
        # Confusion matrix
        cm = confusion_matrix(self.y_test, self.predictions)
        labels = np.unique(self.y).tolist()
        cm_plot = DataVisualizer.plot_confusion_matrix(cm, labels)
        
        # Classification report
        report = classification_report(self.y_test, self.predictions, output_dict=True)
        
        return {
            'metrics': {
                'accuracy': round(accuracy, 4),
                'precision': round(precision, 4),
                'recall': round(recall, 4),
                'f1_score': round(f1, 4),
                'test_samples': int(len(self.y_test)),
                'train_samples': int(len(self.y_train))
            },
            'confusion_matrix': cm.tolist(),
            'confusion_matrix_plot': cm_plot,
            'classification_report': report,
            'classes': labels
        }
