# SmartML Dashboard - Testing Guide

## 🧪 Testing Your Application

This guide will help you test all features of the SmartML Dashboard.

---

## 📋 Pre-Testing Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Flask app running (`python app.py`)
- [ ] Browser open at http://localhost:5000

---

## 🔍 Test Scenarios

### 1. Homepage & UI Test
**Expected Result**: Modern, responsive dashboard with hero section

- [ ] Page loads without errors
- [ ] Navigation bar displays correctly
- [ ] Hero section with gradient background visible
- [ ] "Get Started" button works
- [ ] All icons display properly
- [ ] Responsive design works on different screen sizes

---

### 2. File Upload Test

#### Test Case 2.1: Valid CSV Upload
**File**: `sample_datasets/house_prices.csv`

Steps:
1. Click "Browse Files" or drag & drop CSV
2. Select house_prices.csv
3. Wait for upload

Expected Results:
- [ ] Progress bar shows during upload
- [ ] Success message appears
- [ ] Dataset statistics display (200 rows, 5 columns)
- [ ] Data preview table shows first 10 rows
- [ ] Stat cards show correct numbers

#### Test Case 2.2: Invalid File Upload
**File**: Any .txt or .xlsx file

Expected Results:
- [ ] Error message: "Invalid file type"
- [ ] No data loaded
- [ ] Dashboard remains hidden

#### Test Case 2.3: Drag & Drop Upload
**File**: `sample_datasets/heart_disease.csv`

Steps:
1. Drag CSV file to upload area
2. Drop file

Expected Results:
- [ ] Upload area highlights on drag
- [ ] File uploads successfully
- [ ] Dashboard displays with 300 rows, 6 columns

---

### 3. Data Visualization Test

**Dataset**: house_prices.csv

Steps:
1. Upload dataset
2. Scroll to visualizations section
3. Click "Generate Visualizations"

Expected Results:
- [ ] Button shows loading spinner
- [ ] Correlation heatmap displays
- [ ] Distribution plots show for numeric columns
- [ ] Boxplots display properly
- [ ] All plots are clear and readable
- [ ] No errors in browser console

---

### 4. Regression Tests

**Dataset**: house_prices.csv

#### Test Case 4.1: Linear Regression
Steps:
1. Click "Run Regression" button
2. Select "Price" as target column
3. Click "Linear" algorithm button

Expected Results:
- [ ] Modal shows loading
- [ ] Results section appears
- [ ] Metrics displayed: MAE, MSE, RMSE, R² Score
- [ ] Regression plot shows (Actual vs Predicted)
- [ ] Residual plot displays
- [ ] Feature importance chart shows
- [ ] R² score is reasonable (>0.5 for this dataset)

#### Test Case 4.2: Polynomial Regression
Steps:
1. Run regression with "Polynomial" algorithm
2. Check degree parameter

Expected Results:
- [ ] Results show polynomial degree
- [ ] Metrics are calculated
- [ ] Plots display correctly

#### Test Case 4.3: Random Forest Regression
Steps:
1. Run Random Forest algorithm
2. Check with n_estimators=100

Expected Results:
- [ ] Processing completes
- [ ] Feature importance shows
- [ ] R² score typically higher than linear
- [ ] All metrics calculated correctly

---

### 5. Classification Tests

**Dataset**: heart_disease.csv

#### Test Case 5.1: Decision Tree
Steps:
1. Upload heart_disease.csv
2. Click "Run Classification"
3. Select "HeartDisease" as target
4. Click "Decision Tree" button

Expected Results:
- [ ] Accuracy, Precision, Recall, F1 Score displayed
- [ ] Confusion matrix visualization shows
- [ ] Metrics are reasonable (accuracy >0.6)
- [ ] Feature importance chart displays

#### Test Case 5.2: SVM Classification
Steps:
1. Select SVM algorithm
2. Use default kernel (rbf)

Expected Results:
- [ ] Classification runs successfully
- [ ] Confusion matrix displays
- [ ] Metrics calculated
- [ ] Results comparable to Decision Tree

#### Test Case 5.3: Random Forest Classification
Steps:
1. Run Random Forest classifier

Expected Results:
- [ ] Feature importance shows
- [ ] Typically better accuracy than single tree
- [ ] All metrics displayed

#### Test Case 5.4: Ensemble Methods
Steps:
1. Test AdaBoost
2. Test Gradient Boosting

Expected Results:
- [ ] Both algorithms run successfully
- [ ] Feature importance available
- [ ] Performance metrics reasonable

---

### 6. Clustering Tests

**Dataset**: customer_segmentation.csv

#### Test Case 6.1: K-Means Clustering
Steps:
1. Upload customer_segmentation.csv
2. Click "Run Clustering"
3. Set n_clusters = 3
4. Click "Run K-Means"

Expected Results:
- [ ] Silhouette score calculated
- [ ] Cluster visualization displays (2D plot)
- [ ] Cluster distribution shown
- [ ] 3 distinct clusters visible
- [ ] Centroids marked on plot

#### Test Case 6.2: Elbow Method
Steps:
1. Click "Elbow Method" button
2. Use default max_k = 10

Expected Results:
- [ ] Elbow curve displays
- [ ] Recommended K value shown
- [ ] Inertia values decrease as K increases
- [ ] Clear elbow point visible (typically K=3-4)

#### Test Case 6.3: DBSCAN
Steps:
1. Set eps = 0.5, min_samples = 5
2. Click "Run DBSCAN"

Expected Results:
- [ ] Number of clusters detected
- [ ] Noise points counted
- [ ] Cluster visualization shows
- [ ] Cluster distribution displayed

---

### 7. Dimensionality Reduction Tests

**Dataset**: house_prices.csv or heart_disease.csv

#### Test Case 7.1: PCA
Steps:
1. Upload dataset
2. Click "Run Analysis"
3. Leave n_components empty (auto)
4. Click "Run PCA"

Expected Results:
- [ ] Explained variance ratio displayed
- [ ] Cumulative variance plot shows
- [ ] Individual variance bar chart shows
- [ ] 95% variance threshold line visible
- [ ] Component loadings calculated
- [ ] Top features per component shown

#### Test Case 7.2: PCA with Fixed Components
Steps:
1. Set n_components = 2
2. Run PCA

Expected Results:
- [ ] Only 2 components analyzed
- [ ] Plots show 2 components
- [ ] Total variance explained shown

#### Test Case 7.3: SVD
Steps:
1. Run SVD algorithm

Expected Results:
- [ ] Similar results to PCA
- [ ] Singular values displayed
- [ ] Variance plots show
- [ ] Component loadings available

---

## 🎯 Performance Tests

### Response Time Tests
- [ ] File upload completes in <5 seconds (for 200-row dataset)
- [ ] Visualizations generate in <10 seconds
- [ ] ML algorithms complete in <15 seconds
- [ ] Page is responsive during processing

### Stress Tests
- [ ] Upload 1000-row dataset - should work
- [ ] Upload 10,000-row dataset - may be slow but should complete
- [ ] Run multiple algorithms consecutively
- [ ] Generate visualizations multiple times

---

## 🐛 Common Issues & Solutions

### Issue 1: Visualizations Not Showing
**Solution**: 
- Check browser console for JavaScript errors
- Verify Flask app is running
- Ensure dataset has numeric columns

### Issue 2: ML Algorithm Fails
**Solution**:
- Verify target column is selected
- Check if dataset has enough rows (minimum 10)
- Ensure no all-NaN columns
- Verify column types are appropriate

### Issue 3: Slow Performance
**Solution**:
- Use smaller datasets for testing
- Reduce n_estimators for ensemble methods
- Close other browser tabs
- Check system resources

### Issue 4: Upload Fails
**Solution**:
- Verify file is CSV format
- Check file size (<16MB)
- Ensure proper CSV encoding (UTF-8)
- Check for special characters in headers

---

## ✅ Feature Checklist

### Core Features
- [ ] File upload (drag & drop + browse)
- [ ] Data validation
- [ ] Data preview table
- [ ] Dataset statistics
- [ ] Correlation heatmap
- [ ] Distribution plots
- [ ] Boxplots

### Regression Algorithms
- [ ] Linear Regression
- [ ] Polynomial Regression
- [ ] Random Forest Regressor
- [ ] Gradient Boosting Regressor

### Classification Algorithms
- [ ] Decision Tree
- [ ] SVM
- [ ] Random Forest Classifier
- [ ] AdaBoost
- [ ] Gradient Boosting Classifier

### Clustering Algorithms
- [ ] K-Means
- [ ] Elbow Method
- [ ] DBSCAN

### Dimensionality Reduction
- [ ] PCA
- [ ] SVD

### UI/UX Features
- [ ] Responsive design
- [ ] Loading indicators
- [ ] Error notifications
- [ ] Success messages
- [ ] Smooth scrolling
- [ ] Interactive modals
- [ ] Hover effects
- [ ] Color-coded metrics

---

## 📊 Expected Results Summary

### house_prices.csv (Regression)
- **R² Score**: Should be >0.7 for Random Forest
- **RMSE**: Lower is better
- **Feature Importance**: Size should be most important

### heart_disease.csv (Classification)
- **Accuracy**: Should be >0.65
- **Confusion Matrix**: Should show reasonable balance
- **Feature Importance**: Age, Cholesterol should be important

### customer_segmentation.csv (Clustering)
- **Optimal K**: Should be around 3-4
- **Silhouette Score**: Should be >0.3
- **Clusters**: Should be visually distinct

---

## 🔬 Advanced Testing

### Browser Compatibility
Test on:
- [ ] Chrome (Recommended)
- [ ] Edge
- [ ] Firefox
- [ ] Safari

### Responsive Design
Test on:
- [ ] Desktop (1920x1080)
- [ ] Laptop (1366x768)
- [ ] Tablet (768px)
- [ ] Mobile (375px)

### Error Handling
Test with:
- [ ] Empty CSV file
- [ ] CSV with all NaN values
- [ ] CSV with single column
- [ ] Very large file (>16MB)
- [ ] Corrupted CSV

---

## 📝 Test Report Template

```
Test Date: _____________
Tester: ________________

Overall Status: [ ] Pass [ ] Fail [ ] Partial

Issues Found:
1. ___________________________
2. ___________________________

Suggestions:
1. ___________________________
2. ___________________________

Notes:
_________________________________
_________________________________
```

---

## 🎓 Learning Outcomes Verification

After testing, you should understand:
- [ ] How to upload and validate data
- [ ] How to generate exploratory visualizations
- [ ] How different ML algorithms work
- [ ] How to interpret regression metrics
- [ ] How to read confusion matrices
- [ ] How clustering algorithms group data
- [ ] How PCA reduces dimensions
- [ ] How to compare algorithm performance

---

## 🚀 Next Steps After Testing

1. **If all tests pass**: 
   - Try with your own datasets
   - Experiment with parameters
   - Compare algorithm performance
   - Take screenshots for documentation

2. **If issues found**:
   - Document the issue
   - Check console errors
   - Review relevant code section
   - Test with sample datasets first

3. **Enhancement ideas**:
   - Add more visualizations
   - Implement model comparison
   - Add export functionality
   - Create user authentication

---

**Happy Testing! 🧪✨**

For questions or issues, refer to:
- PROJECT_SUMMARY.md
- QUICKSTART.md
- README.md
