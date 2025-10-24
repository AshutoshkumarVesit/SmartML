# Algorithm Debugging Guide 🔧

## Problems Reported:
- "Algorithms are not fully functional"

## Let's Test Each Component:

### 1️⃣ File Upload Test
```javascript
// What should happen:
1. Click upload area
2. Select CSV file (e.g., house_prices.csv)
3. File uploads successfully
4. Dashboard appears with data preview
5. Modals are created
6. Column dropdowns populate
```

### 2️⃣ Regression Test
```javascript
Steps:
1. Upload house_prices.csv
2. Click "Regression" card
3. Modal opens
4. Select "Price" as target
5. Click any algorithm (Linear/Polynomial/RF/GB)
6. Loading overlay shows
7. Results display with metrics and plots
```

### 3️⃣ Classification Test
```javascript
Steps:
1. Upload heart_disease.csv
2. Click "Classification" card
3. Modal opens
4. Select "HeartDisease" as target
5. Click any algorithm
6. Results show accuracy, confusion matrix
```

### 4️⃣ Clustering Test
```javascript
Steps:
1. Upload customer_segmentation.csv
2. Click "Clustering" card
3. Modal opens
4. Set K=3 for K-Means
5. Click "Run K-Means"
6. Results show cluster plot
```

### 5️⃣ Dimensionality Test
```javascript
Steps:
1. Upload any dataset
2. Click "Dimensionality" card
3. Modal opens
4. Leave components empty (auto)
5. Click "Run PCA"
6. Results show variance plot
```

## Common Issues & Fixes:

### Issue 1: Modal doesn't open
**Symptom**: Clicking algorithm card does nothing
**Cause**: Modal not created or Bootstrap not loaded
**Fix**: Check console for errors, ensure createModals() runs

### Issue 2: Target dropdown empty
**Symptom**: No columns in dropdown
**Cause**: updateModalSelects() not called after upload
**Fix**: Already fixed in displayDatasetInfo()

### Issue 3: "Dataset not found" error
**Symptom**: API returns 404
**Cause**: session_id not passed or datasets dict empty
**Fix**: Check currentSessionId is set

### Issue 4: Loading overlay stuck
**Symptom**: Loading never completes
**Cause**: API error or network issue
**Fix**: Check browser Network tab, check Flask logs

### Issue 5: No results shown
**Symptom**: API succeeds but results don't appear
**Cause**: displayResults() function issue
**Fix**: Check console for JavaScript errors

## Testing Commands:

### Start Server (if not running):
```powershell
cd C:\Users\vinay\OneDrive\Desktop\SmartML
.\venv\Scripts\Activate.ps1
python app.py
```

### Check Sample Datasets:
```powershell
ls sample_datasets/
```

Should show:
- house_prices.csv (Regression)
- heart_disease.csv (Classification)
- customer_segmentation.csv (Clustering)

### Test API Directly:
```powershell
# Test upload
curl -X POST -F "file=@sample_datasets/house_prices.csv" http://localhost:5000/upload

# Test regression (after upload, use session_id from response)
curl -X POST http://localhost:5000/ml/regression `
  -H "Content-Type: application/json" `
  -d '{\"session_id\":\"SESSION_ID\",\"target_column\":\"Price\",\"algorithm\":\"linear\"}'
```

## Quick Fixes to Apply:

### Fix 1: Ensure modals work on click
Add this to index.html after algorithm cards:

```javascript
<script>
// Open modals when cards are clicked
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('[data-algo="regression"]').addEventListener('click', function() {
        new bootstrap.Modal(document.getElementById('regressionModal')).show();
    });
    // Similar for other cards
});
</script>
```

### Fix 2: Better error messages
Already implemented with notification system!

### Fix 3: Verify all imports in app.py
```python
# Check these are present:
from ml_modules.regression import RegressionModel
from ml_modules.classification import ClassificationModel
from ml_modules.clustering import ClusteringModel
from ml_modules.dimensionality import DimensionalityReduction
```

## Browser Console Checks:

### After page load:
```javascript
console.log(currentSessionId); // Should be null initially
console.log(currentDataset); // Should be null initially
```

### After file upload:
```javascript
console.log(currentSessionId); // Should be a UUID string
console.log(currentDataset); // Should be an object with data
console.log(document.getElementById('regressionTarget').options.length); // Should be > 1
```

### Check if modals exist:
```javascript
console.log(document.getElementById('regressionModal')); // Should not be null
console.log(document.getElementById('classificationModal')); // Should not be null
console.log(document.getElementById('clusteringModal')); // Should not be null
console.log(document.getElementById('dimensionalityModal')); // Should not be null
```

## Flask Server Logs to Watch:

### Successful upload:
```
POST /upload - 200 OK
Session created: <session_id>
Dataset loaded: <filename>
```

### Successful algorithm run:
```
POST /ml/regression - 200 OK
Algorithm: linear
Target: Price
Results generated
```

### Error (if any):
```
ERROR in run_regression: <error message>
500 Internal Server Error
```

## Testing Checklist:

- [ ] Server is running on http://localhost:5000
- [ ] Sample datasets exist in sample_datasets/
- [ ] Browser opens dashboard without errors
- [ ] Upload CSV file works
- [ ] Dashboard sections appear after upload
- [ ] Algorithm cards are visible
- [ ] Clicking algorithm card opens modal
- [ ] Target dropdown has columns
- [ ] Clicking algorithm button shows loading
- [ ] Results appear after processing
- [ ] Success notification shows
- [ ] Plots/charts are visible
- [ ] Metrics display correctly
- [ ] Can run multiple algorithms
- [ ] Error messages work properly

## Next Steps:

1. **Manual Test**: Upload file and try each algorithm
2. **Check Console**: Look for JavaScript errors
3. **Check Network**: Look for failed API calls
4. **Check Flask**: Look for Python errors
5. **Report Specific Issue**: "Which algorithm doesn't work?"

## Expected Behavior:

### ✅ Working System Should:
1. Upload file instantly
2. Show notification "Dataset uploaded successfully! 🎉"
3. Display data table with all rows
4. Show stat cards (rows, columns, etc.)
5. Algorithm cards clickable
6. Modals open smoothly
7. Dropdowns populated
8. Loading overlay during processing
9. Results slide up with animation
10. Success notification after completion
11. Plots clearly visible
12. Metrics easy to read

### ❌ If Something Fails:
- Check browser console (F12)
- Check Network tab for API errors
- Check Flask terminal for Python errors
- Read error notification message
- Try refreshing page (Ctrl+Shift+R)

---

**Status**: Ready for testing
**Server**: http://localhost:5000
**Test Data**: sample_datasets/
**Debug**: Check console + Flask logs
