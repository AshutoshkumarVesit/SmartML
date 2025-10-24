"""
SmartML Dashboard - Main Flask Application
"""
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import json
from config import Config
from utils.helpers import (allowed_file, save_uploaded_file, get_dataset_info, 
                          get_summary_statistics, detect_problem_type, get_feature_target_split)
from ml_modules.preprocessing import DataPreprocessor
from ml_modules.visualization import DataVisualizer
from ml_modules.regression import RegressionModel
from ml_modules.classification import ClassificationModel
from ml_modules.clustering import ClusteringModel
from ml_modules.dimensionality import DimensionalityReduction

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)
CORS(app)

# Store data in session (in production, use Redis or database)
datasets = {}
trained_models = {}  # Store trained models for predictions

@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only CSV files allowed'}), 400
        
        # Save file
        filepath = save_uploaded_file(file)
        if not filepath:
            return jsonify({'error': 'Error saving file'}), 500
        
        # Load dataset
        df = pd.read_csv(filepath)
        
        # Store dataset with session ID
        session_id = str(hash(file.filename))
        datasets[session_id] = df
        
        # Get dataset info
        info = get_dataset_info(df)
        stats = get_summary_statistics(df)
        
        # Validate data
        preprocessor = DataPreprocessor(df)
        validation = preprocessor.validate_data()
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'filename': file.filename,
            'info': info,
            'stats': stats,
            'validation': validation,
            'preview': df.head(10).to_dict('records')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/visualize', methods=['POST'])
def visualize_data():
    """Generate visualizations"""
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if session_id not in datasets:
            return jsonify({'error': 'Dataset not found'}), 404
        
        df = datasets[session_id]
        visualizer = DataVisualizer(df)
        
        visualizations = {
            'correlation_heatmap': visualizer.correlation_heatmap(),
            'distribution_plots': visualizer.distribution_plots(),
            'boxplots': visualizer.boxplots()
        }
        
        return jsonify({
            'success': True,
            'visualizations': visualizations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/preprocess', methods=['POST'])
def preprocess_data():
    """Preprocess dataset"""
    try:
        data = request.json
        session_id = data.get('session_id')
        strategy = data.get('strategy', 'mean')
        
        if session_id not in datasets:
            return jsonify({'error': 'Dataset not found'}), 404
        
        df = datasets[session_id]
        preprocessor = DataPreprocessor(df)
        
        # Apply preprocessing
        preprocessor.handle_missing_values(strategy=strategy)
        preprocessor.remove_duplicates()
        
        # Update dataset
        datasets[session_id] = preprocessor.df
        
        summary = preprocessor.get_preprocessing_summary()
        
        return jsonify({
            'success': True,
            'summary': summary,
            'info': get_dataset_info(preprocessor.df)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ml/regression', methods=['POST'])
def run_regression():
    """Run regression algorithms"""
    try:
        data = request.json
        session_id = data.get('session_id')
        target_column = data.get('target_column')
        feature_columns = data.get('feature_columns', [])  # Get selected features
        algorithm = data.get('algorithm', 'linear')
        
        if session_id not in datasets:
            return jsonify({'error': 'Dataset not found'}), 404
        
        df = datasets[session_id]
        
        # Validate target column is numeric
        if target_column not in df.columns:
            return jsonify({'error': f'Target column "{target_column}" not found'}), 400
        
        if not pd.api.types.is_numeric_dtype(df[target_column]):
            return jsonify({
                'error': f'Target column "{target_column}" must be numeric for regression. Current type: {df[target_column].dtype}. Please select a numeric column (e.g., Age, Price, Salary).'
            }), 400
        
        # Check if target has very few unique values (likely categorical)
        n_unique = df[target_column].nunique()
        if n_unique <= 10:
            return jsonify({
                'error': f'Target column "{target_column}" has only {n_unique} unique values. This looks like a classification problem. Please use Classification instead, or select a continuous numeric column.'
            }), 400
        
        # If features specified, use only those columns + target
        if feature_columns:
            selected_cols = feature_columns + [target_column]
            df_subset = df[selected_cols]
            X, y = get_feature_target_split(df_subset, target_column)
        else:
            # Use all columns except target
            X, y = get_feature_target_split(df, target_column)
        
        # Check minimum samples
        if len(y) < 4:
            return jsonify({'error': f'Not enough data: Only {len(y)} samples. Need at least 4 samples for regression.'}), 400
        
        model = RegressionModel(X, y, test_size=0.2)
        
        # Only Linear Regression supported
        if algorithm == 'linear':
            results = model.linear_regression()
        else:
            return jsonify({'error': 'Invalid algorithm. Only linear regression is supported.'}), 400
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ml/classification', methods=['POST'])
def run_classification():
    """Run classification algorithms"""
    try:
        data = request.json
        session_id = data.get('session_id')
        target_column = data.get('target_column')
        algorithm = data.get('algorithm', 'decision_tree')
        
        if session_id not in datasets:
            return jsonify({'error': 'Dataset not found'}), 404
        
        df = datasets[session_id]
        X, y = get_feature_target_split(df, target_column)
        
        model = ClassificationModel(X, y)
        
        if algorithm == 'decision_tree':
            max_depth = data.get('max_depth')
            results = model.decision_tree(max_depth=max_depth)
        elif algorithm == 'svm':
            kernel = data.get('kernel', 'rbf')
            C = data.get('C', 1.0)
            results = model.support_vector_machine(kernel=kernel, C=C)
        elif algorithm == 'random_forest':
            n_estimators = data.get('n_estimators', 100)
            results = model.random_forest(n_estimators=n_estimators)
        elif algorithm == 'adaboost':
            n_estimators = data.get('n_estimators', 50)
            learning_rate = data.get('learning_rate', 1.0)
            results = model.adaboost(n_estimators, learning_rate)
        elif algorithm == 'gradient_boosting':
            n_estimators = data.get('n_estimators', 100)
            learning_rate = data.get('learning_rate', 0.1)
            results = model.gradient_boosting(n_estimators, learning_rate)
        else:
            return jsonify({'error': 'Invalid algorithm'}), 400
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ml/clustering', methods=['POST'])
def run_clustering():
    """Run clustering algorithms"""
    try:
        data = request.json
        session_id = data.get('session_id')
        algorithm = data.get('algorithm', 'kmeans')
        columns = data.get('columns')
        
        if session_id not in datasets:
            return jsonify({'error': 'Dataset not found'}), 404
        
        df = datasets[session_id]
        
        # Select columns if specified
        if columns:
            X = df[columns]
        else:
            X = df.select_dtypes(include=['int64', 'float64'])
        
        model = ClusteringModel(X)
        
        if algorithm == 'kmeans':
            n_clusters = data.get('n_clusters', 3)
            results = model.kmeans(n_clusters=n_clusters)
        elif algorithm == 'kmeans_elbow':
            k_range = range(2, data.get('max_k', 11))
            results = model.kmeans_elbow(k_range=k_range)
        elif algorithm == 'dbscan':
            eps = data.get('eps', 0.5)
            min_samples = data.get('min_samples', 5)
            results = model.dbscan(eps=eps, min_samples=min_samples)
        else:
            return jsonify({'error': 'Invalid algorithm'}), 400
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ml/dimensionality', methods=['POST'])
def run_dimensionality_reduction():
    """Run dimensionality reduction"""
    try:
        data = request.json
        session_id = data.get('session_id')
        algorithm = data.get('algorithm', 'pca')
        n_components = data.get('n_components')
        columns = data.get('columns')
        
        if session_id not in datasets:
            return jsonify({'error': 'Dataset not found'}), 404
        
        df = datasets[session_id]
        
        # Select columns if specified
        if columns:
            X = df[columns]
        else:
            X = df.select_dtypes(include=['int64', 'float64'])
        
        model = DimensionalityReduction(X)
        
        if algorithm == 'pca':
            results = model.pca_analysis(n_components=n_components)
        elif algorithm == 'svd':
            results = model.svd_analysis(n_components=n_components)
        else:
            return jsonify({'error': 'Invalid algorithm'}), 400
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/detect_problem_type', methods=['POST'])
def detect_problem():
    """Detect if problem is regression or classification"""
    try:
        data = request.json
        session_id = data.get('session_id')
        target_column = data.get('target_column')
        
        if session_id not in datasets:
            return jsonify({'error': 'Dataset not found'}), 404
        
        df = datasets[session_id]
        problem_type = detect_problem_type(df, target_column)
        
        return jsonify({
            'success': True,
            'problem_type': problem_type
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Get port from environment variable (for Railway deployment)
    port = int(os.environ.get('PORT', 5000))
    
    app.run(debug=True, host='0.0.0.0', port=port)

