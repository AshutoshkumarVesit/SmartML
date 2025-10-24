"""
Helper utilities for SmartML Dashboard
"""
import os
import pandas as pd
from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    """Save uploaded file and return path"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        return filepath
    return None

def get_dataset_info(df):
    """Get comprehensive dataset information"""
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    # Filter numeric columns suitable for regression (exclude binary/low-cardinality columns)
    regression_cols = []
    for col in numeric_cols:
        n_unique = df[col].nunique()
        # Include only if has more than 10 unique values (continuous-like)
        if n_unique > 10:
            regression_cols.append(col)
    
    info = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.astype(str).to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'missing_percentage': (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
        'numeric_columns': numeric_cols,
        'regression_columns': regression_cols,  # New: columns suitable for regression
        'categorical_columns': df.select_dtypes(include=['object', 'category']).columns.tolist(),
        'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
    }
    return info

def get_summary_statistics(df):
    """Get summary statistics for dataset"""
    numeric_df = df.select_dtypes(include=['int64', 'float64'])
    if not numeric_df.empty:
        return numeric_df.describe().to_dict()
    return {}

def detect_problem_type(df, target_column):
    """Detect if problem is classification or regression"""
    if target_column not in df.columns:
        return None
    
    target = df[target_column]
    
    # Check if numeric
    if pd.api.types.is_numeric_dtype(target):
        # If unique values are less than 10 and all integers, likely classification
        unique_values = target.nunique()
        if unique_values <= 10 and target.dtype in ['int64', 'int32']:
            return 'classification'
        return 'regression'
    else:
        return 'classification'

def format_metric(value, decimals=4):
    """Format metric value for display"""
    if isinstance(value, (int, float)):
        return round(value, decimals)
    return value

def get_feature_target_split(df, target_column):
    """Split dataframe into features and target"""
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset")
    
    # List of common outcome/derived columns that should be excluded as features
    outcome_patterns = [
        'Grade', 'grade',
        'Pass', 'pass', 
        'AtRisk', 'atrisk', 'at_risk',
        'Churn', 'churn',
        'Promotion', 'promotion',
        'Attrition', 'attrition',
        'PriceCategory', 'price_category',
        'InvestmentPotential', 'investment_potential',
        'LoyaltyTier', 'loyalty_tier'
    ]
    
    # Columns to drop: target + outcome/derived columns
    cols_to_drop = [target_column]
    
    for col in df.columns:
        if col == target_column:
            continue
        # Check if column name matches outcome patterns
        col_lower = col.lower()
        for pattern in outcome_patterns:
            if pattern.lower() in col_lower:
                cols_to_drop.append(col)
                break
    
    X = df.drop(columns=cols_to_drop)
    y = df[target_column]
    
    # Handle categorical features
    X = pd.get_dummies(X, drop_first=True)
    
    return X, y
