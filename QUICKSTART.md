# SmartML Dashboard - Quick Start Guide

## 🚀 Getting Started

### Installation

1. **Create Virtual Environment**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```powershell
   python app.py
   ```

4. **Open Browser**
   Navigate to: `http://localhost:5000`

## 📊 Sample Datasets

The project includes three sample datasets in the `sample_datasets/` folder:

1. **house_prices.csv** - For regression analysis
   - Features: Size, Bedrooms, Age, Location_Score
   - Target: Price

2. **heart_disease.csv** - For classification
   - Features: Age, Cholesterol, BloodPressure, MaxHeartRate, ExerciseHours
   - Target: HeartDisease (0/1)

3. **customer_segmentation.csv** - For clustering
   - Features: Annual_Income, Spending_Score, Age, Purchase_Frequency

## 🎯 How to Use

### 1. Upload Dataset
- Click "Get Started" or scroll to Upload section
- Drag & drop your CSV file or browse to select
- Wait for upload and validation

### 2. Explore Data
- View dataset statistics (rows, columns, types)
- Check data preview table
- Click "Generate Visualizations" to see:
  - Correlation heatmap
  - Distribution plots
  - Boxplots

### 3. Run ML Algorithms

#### Regression
- Click "Run Regression"
- Select target column (numeric)
- Choose algorithm:
  - Linear Regression
  - Polynomial Regression
  - Random Forest
  - Gradient Boosting
- View results with metrics and plots

#### Classification
- Click "Run Classification"
- Select target column (categorical/binary)
- Choose algorithm:
  - Decision Tree
  - SVM
  - Random Forest
  - AdaBoost
  - Gradient Boosting
- View confusion matrix and metrics

#### Clustering
- Click "Run Clustering"
- K-Means: Set number of clusters
- Elbow Method: Find optimal K
- DBSCAN: Set epsilon and min_samples
- View cluster visualization

#### Dimensionality Reduction
- Click "Run Analysis"
- PCA or SVD
- Set number of components (optional)
- View explained variance

### 4. Interpret Results
- Metrics displayed in colorful cards
- Visualizations for each algorithm
- Feature importance (where applicable)
- Download or save results

## 🔧 Troubleshooting

### Port Already in Use
```powershell
python app.py
# If port 5000 is busy, modify app.py:
# app.run(debug=True, host='0.0.0.0', port=5001)
```

### Module Import Errors
```powershell
pip install -r requirements.txt --upgrade
```

### File Upload Errors
- Ensure CSV file is properly formatted
- Check file size (max 16MB)
- Verify no special characters in column names

## 📝 Example Workflow

1. Upload `house_prices.csv`
2. Generate visualizations to explore data
3. Run Linear Regression with 'Price' as target
4. View R² score and regression plot
5. Try Random Forest for comparison
6. Check feature importance

## 🎓 Educational Features

- **Data Preprocessing**: Automatic handling of missing values
- **Visualization**: Interactive plots for EDA
- **Multiple Algorithms**: Compare performance
- **Metrics**: Comprehensive evaluation
- **Feature Importance**: Understand model decisions
- **MLOps Concepts**: End-to-end workflow

## 💡 Tips

- Start with visualization before ML
- Use smaller datasets for faster results
- Compare multiple algorithms
- Check feature importance for insights
- Use elbow method before K-Means clustering

## 📚 Learning Resources

- Each algorithm shows relevant metrics
- Visualizations help interpret results
- Compare different approaches
- Understand preprocessing impact

## 🐛 Known Issues

- Large datasets (>10MB) may take time to process
- Complex visualizations may be slow
- Browser compatibility: Chrome/Edge recommended

## 🔄 Updates

Check README.md for latest features and updates.

---

**Happy Learning with SmartML! 🚀**
