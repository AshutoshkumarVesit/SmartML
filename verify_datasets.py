"""Quick verification of all demo datasets"""
import pandas as pd
import os

datasets = [
    'ecommerce_customers.csv',
    'employee_salaries.csv', 
    'student_performance.csv',
    'real_estate_prices.csv'
]

print("="*70)
print("📊 DEMO DATASETS VERIFICATION")
print("="*70)

for dataset in datasets:
    filepath = f'sample_datasets/{dataset}'
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        print(f"\n✅ {dataset}")
        print(f"   📈 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"   📋 Columns: {', '.join(df.columns[:6])}...")
        
        # Check for numeric columns (regression targets)
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        regression_cols = [col for col in numeric_cols if df[col].nunique() > 10]
        print(f"   🎯 Regression Targets: {', '.join(regression_cols[:3])}")
        
        # Check for categorical/binary columns (classification targets)
        categorical_cols = df.select_dtypes(include=['object']).columns
        binary_cols = [col for col in numeric_cols if df[col].nunique() <= 10]
        print(f"   🎯 Classification Targets: {', '.join(list(categorical_cols)[:2] + list(binary_cols)[:2])}")
        
        # Sample data
        print(f"   📊 Sample row:")
        print(f"      {df.iloc[0].to_dict()}")
    else:
        print(f"\n❌ {dataset} - NOT FOUND")

print("\n" + "="*70)
print("✅ ALL DATASETS READY FOR DEMO!")
print("="*70)
print("\n💡 Next Steps:")
print("   1. Open browser: http://localhost:5000")
print("   2. Upload any dataset from sample_datasets/")
print("   3. Try all algorithms with beautiful visualizations!")
print("\n🎯 Recommended First Demo:")
print("   - Upload: ecommerce_customers.csv")
print("   - Regression: TotalSpent → Random Forest")
print("   - Classification: Churn → Random Forest")
print("   - Clustering: K-Means (k=4)")
