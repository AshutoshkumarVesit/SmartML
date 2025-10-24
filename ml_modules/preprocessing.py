"""
Data Preprocessing Module
Handles data validation, cleaning, and preprocessing
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer

class DataPreprocessor:
    """Handle all data preprocessing tasks"""
    
    def __init__(self, df):
        self.df = df.copy()
        self.original_df = df.copy()
        self.preprocessing_steps = []
    
    def validate_data(self):
        """Validate the uploaded dataset"""
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check if dataframe is empty
        if self.df.empty:
            validation_results['is_valid'] = False
            validation_results['errors'].append("Dataset is empty")
            return validation_results
        
        # Check for minimum rows
        if len(self.df) < 10:
            validation_results['warnings'].append(f"Dataset has only {len(self.df)} rows. Minimum 10 rows recommended.")
        
        # Check for all NaN columns
        all_nan_cols = self.df.columns[self.df.isnull().all()].tolist()
        if all_nan_cols:
            validation_results['warnings'].append(f"Columns with all missing values: {all_nan_cols}")
        
        # Check for duplicate rows
        duplicate_count = self.df.duplicated().sum()
        if duplicate_count > 0:
            validation_results['warnings'].append(f"Found {duplicate_count} duplicate rows")
        
        return validation_results
    
    def handle_missing_values(self, strategy='mean', threshold=0.5):
        """
        Handle missing values in the dataset
        strategy: 'mean', 'median', 'mode', 'drop'
        threshold: columns with missing ratio > threshold will be dropped
        """
        missing_ratio = self.df.isnull().sum() / len(self.df)
        
        # Drop columns with too many missing values
        cols_to_drop = missing_ratio[missing_ratio > threshold].index.tolist()
        if cols_to_drop:
            self.df = self.df.drop(columns=cols_to_drop)
            self.preprocessing_steps.append(f"Dropped columns: {cols_to_drop} (>{threshold*100}% missing)")
        
        # Handle numeric columns
        numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            if strategy == 'drop':
                self.df = self.df.dropna(subset=numeric_cols)
                self.preprocessing_steps.append(f"Dropped rows with missing numeric values")
            else:
                imputer_strategy = strategy if strategy in ['mean', 'median'] else 'mean'
                imputer = SimpleImputer(strategy=imputer_strategy)
                self.df[numeric_cols] = imputer.fit_transform(self.df[numeric_cols])
                self.preprocessing_steps.append(f"Imputed numeric columns with {imputer_strategy}")
        
        # Handle categorical columns
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            imputer = SimpleImputer(strategy='most_frequent')
            self.df[categorical_cols] = imputer.fit_transform(self.df[categorical_cols])
            self.preprocessing_steps.append(f"Imputed categorical columns with mode")
        
        return self.df
    
    def remove_duplicates(self):
        """Remove duplicate rows"""
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates()
        removed = initial_rows - len(self.df)
        if removed > 0:
            self.preprocessing_steps.append(f"Removed {removed} duplicate rows")
        return self.df
    
    def encode_categorical(self, columns=None):
        """Encode categorical variables"""
        if columns is None:
            columns = self.df.select_dtypes(include=['object', 'category']).columns
        
        for col in columns:
            if col in self.df.columns:
                # Use one-hot encoding for columns with few categories
                unique_values = self.df[col].nunique()
                if unique_values <= 10:
                    # One-hot encoding
                    dummies = pd.get_dummies(self.df[col], prefix=col, drop_first=True)
                    self.df = pd.concat([self.df.drop(columns=[col]), dummies], axis=1)
                    self.preprocessing_steps.append(f"One-hot encoded: {col}")
                else:
                    # Label encoding
                    le = LabelEncoder()
                    self.df[col] = le.fit_transform(self.df[col].astype(str))
                    self.preprocessing_steps.append(f"Label encoded: {col}")
        
        return self.df
    
    def scale_features(self, columns=None, method='standard'):
        """Scale numeric features"""
        if columns is None:
            columns = self.df.select_dtypes(include=['int64', 'float64']).columns
        
        if len(columns) > 0:
            scaler = StandardScaler()
            self.df[columns] = scaler.fit_transform(self.df[columns])
            self.preprocessing_steps.append(f"Scaled {len(columns)} numeric columns using {method} scaling")
        
        return self.df
    
    def get_preprocessing_summary(self):
        """Get summary of preprocessing steps"""
        return {
            'original_shape': self.original_df.shape,
            'processed_shape': self.df.shape,
            'steps': self.preprocessing_steps,
            'missing_values_before': self.original_df.isnull().sum().sum(),
            'missing_values_after': self.df.isnull().sum().sum()
        }
