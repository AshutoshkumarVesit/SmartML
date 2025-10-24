"""
Regression Algorithms Module
Implements various regression algorithms
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from ml_modules.visualization import DataVisualizer

class RegressionModel:
    """Handle regression tasks"""
    
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
            self.X, self.y, test_size=self.test_size, random_state=self.random_state
        )
        return {
            'train_size': len(self.X_train),
            'test_size': len(self.X_test),
            'feature_count': self.X_train.shape[1]
        }
    
    def linear_regression(self):
        """Train Linear Regression model"""
        if self.X_train is None:
            self.split_data()
        
        self.model = LinearRegression()
        self.model.fit(self.X_train, self.y_train)
        self.predictions = self.model.predict(self.X_test)
        
        results = self._calculate_metrics()
        
        # Get feature names safely
        if hasattr(self.X, 'columns'):
            feature_names = self.X.columns.tolist()
        else:
            feature_names = [f'Feature_{i}' for i in range(self.X.shape[1])]
        
        results['coefficients'] = dict(zip(feature_names, self.model.coef_))
        results['intercept'] = float(self.model.intercept_)
        results['algorithm'] = 'Linear Regression'
        
        # Build equation string
        equation_parts = [f"{self.model.intercept_:.4f}"]
        for feature, coef in zip(feature_names, self.model.coef_):
            sign = "+" if coef >= 0 else ""
            equation_parts.append(f"{sign}{coef:.4f}×{feature}")
        
        results['equation'] = " ".join(equation_parts)
        results['equation_formatted'] = f"y = {results['equation']}"
        
        # Actual vs Predicted + Residuals plot
        results['prediction_plot'] = DataVisualizer.plot_regression_results(
            self.y_test, self.predictions, 'Linear Regression'
        )
        
        # Feature importance based on absolute coefficients
        feature_importance = {col: abs(coef) for col, coef in results['coefficients'].items()}
        results['feature_importance_plot'] = DataVisualizer.plot_feature_importance(feature_importance)
        
        return results
    
    def polynomial_regression(self, degree=2):
        """Train Polynomial Regression model"""
        if self.X_train is None:
            self.split_data()
        
        # Get feature names safely
        if hasattr(self.X, 'columns'):
            feature_names = self.X.columns.tolist()
        else:
            feature_names = [f'Feature_{i}' for i in range(self.X.shape[1])]
        
        # Create polynomial features
        poly = PolynomialFeatures(degree=degree)
        X_train_poly = poly.fit_transform(self.X_train)
        X_test_poly = poly.transform(self.X_test)
        
        # Store the polynomial transformer for predictions
        self.poly_transformer = poly
        
        self.model = LinearRegression()
        self.model.fit(X_train_poly, self.y_train)
        self.predictions = self.model.predict(X_test_poly)
        
        results = self._calculate_metrics()
        results['degree'] = degree
        results['n_polynomial_features'] = X_train_poly.shape[1]
        results['algorithm'] = f'Polynomial Regression (degree={degree})'
        
        # Actual vs Predicted + Residuals plot
        results['prediction_plot'] = DataVisualizer.plot_regression_results(
            self.y_test, self.predictions, f'Polynomial Regression (degree={degree})'
        )
        
        return results
    
    def random_forest_regression(self, n_estimators=100, max_depth=None):
        """Train Random Forest Regression model"""
        if self.X_train is None:
            self.split_data()
        
        # Get feature names safely
        if hasattr(self.X, 'columns'):
            feature_names = self.X.columns.tolist()
        else:
            feature_names = [f'Feature_{i}' for i in range(self.X.shape[1])]
        
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=self.random_state
        )
        self.model.fit(self.X_train, self.y_train)
        self.predictions = self.model.predict(self.X_test)
        
        results = self._calculate_metrics()
        results['n_estimators'] = n_estimators
        results['algorithm'] = 'Random Forest Regression'
        
        # Actual vs Predicted + Residuals plot
        results['prediction_plot'] = DataVisualizer.plot_regression_results(
            self.y_test, self.predictions, 'Random Forest Regression'
        )
        
        # Feature importance
        feature_importance = dict(zip(feature_names, self.model.feature_importances_))
        results['feature_importance_plot'] = DataVisualizer.plot_feature_importance(feature_importance)
        results['feature_importance'] = feature_importance
        
        return results
    
    def gradient_boosting_regression(self, n_estimators=100, learning_rate=0.1):
        """Train Gradient Boosting Regression model"""
        if self.X_train is None:
            self.split_data()
        
        # Get feature names safely
        if hasattr(self.X, 'columns'):
            feature_names = self.X.columns.tolist()
        else:
            feature_names = [f'Feature_{i}' for i in range(self.X.shape[1])]
        
        self.model = GradientBoostingRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            random_state=self.random_state
        )
        self.model.fit(self.X_train, self.y_train)
        self.predictions = self.model.predict(self.X_test)
        
        results = self._calculate_metrics()
        results['n_estimators'] = n_estimators
        results['learning_rate'] = learning_rate
        results['algorithm'] = 'Gradient Boosting Regression'
        
        # Actual vs Predicted + Residuals plot
        results['prediction_plot'] = DataVisualizer.plot_regression_results(
            self.y_test, self.predictions, 'Gradient Boosting Regression'
        )
        
        # Feature importance
        feature_importance = dict(zip(feature_names, self.model.feature_importances_))
        results['feature_importance_plot'] = DataVisualizer.plot_feature_importance(feature_importance)
        results['feature_importance'] = feature_importance
        
        return results
    
    def _calculate_metrics(self):
        """Calculate regression metrics"""
        mae = mean_absolute_error(self.y_test, self.predictions)
        mse = mean_squared_error(self.y_test, self.predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(self.y_test, self.predictions)
        
        return {
            'metrics': {
                'mae': round(mae, 4),
                'mse': round(mse, 4),
                'rmse': round(rmse, 4),
                'r2': round(r2, 4),
                'test_samples': int(len(self.y_test)),
                'train_samples': int(len(self.y_train))
            }
        }
    
    def predict_single(self, input_values):
        """
        Predict target value for single input
        
        Args:
            input_values: dict or list/array of feature values
        
        Returns:
            dict with prediction and feature details
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Train a model first.")
        
        # Get feature names
        if hasattr(self.X, 'columns'):
            feature_names = self.X.columns.tolist()
        else:
            feature_names = [f'Feature_{i}' for i in range(self.X.shape[1])]
        
        # Convert input to proper format
        if isinstance(input_values, dict):
            # Ensure all features are present
            input_array = []
            for feature in feature_names:
                if feature not in input_values:
                    raise ValueError(f"Missing feature: {feature}")
                input_array.append(input_values[feature])
            input_array = np.array([input_array])
        else:
            input_array = np.array([input_values])
        
        # Check if we need polynomial transformation
        if hasattr(self, 'poly_transformer'):
            input_array = self.poly_transformer.transform(input_array)
        
        # Make prediction
        prediction = self.model.predict(input_array)[0]
        
        return {
            'prediction': round(float(prediction), 4),
            'input_features': dict(zip(feature_names, input_array[0])) if not hasattr(self, 'poly_transformer') else input_values
        }
