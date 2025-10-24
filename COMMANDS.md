# SmartML Dashboard - Commands Cheat Sheet

## 🎯 Quick Reference Guide

### 📦 Installation & Setup

```powershell
# Clone or navigate to project
cd c:\Users\vinay\OneDrive\Desktop\SmartML

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate virtual environment (Windows CMD)
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Upgrade pip first (recommended)
python -m pip install --upgrade pip
```

### 🚀 Running the Application

```powershell
# Standard run
python app.py

# Run on different port
python app.py --port 5001

# Run with specific host
python app.py --host 0.0.0.0
```

### 🔄 Development Commands

```powershell
# Check Python version
python --version

# List installed packages
pip list

# Check if Flask is installed
pip show Flask

# Update all packages
pip install --upgrade -r requirements.txt

# Freeze current environment
pip freeze > requirements_freeze.txt
```

### 🧹 Maintenance

```powershell
# Clear uploaded files
Remove-Item static\uploads\* -Exclude .gitkeep

# Clear Python cache
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Force -Recurse

# Deactivate virtual environment
deactivate
```

### 📊 Testing

```powershell
# Test with sample dataset
# Open browser to http://localhost:5000
# Upload: sample_datasets/house_prices.csv

# Check Flask routes
python -c "from app import app; print(app.url_map)"

# Test Python imports
python -c "import flask, pandas, sklearn; print('All imports OK')"
```

---

## 🌐 Browser Commands

### Open Dashboard
```
http://localhost:5000
```

### API Endpoints (for testing with tools like Postman)
```
POST http://localhost:5000/upload
POST http://localhost:5000/visualize
POST http://localhost:5000/ml/regression
POST http://localhost:5000/ml/classification
POST http://localhost:5000/ml/clustering
POST http://localhost:5000/ml/dimensionality
```

---

## 🐛 Debugging

### Check if port is in use
```powershell
netstat -ano | findstr :5000
```

### Kill process on port 5000
```powershell
# Find PID
netstat -ano | findstr :5000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### View Flask logs
```powershell
# Logs appear in terminal where you ran `python app.py`
# Set debug mode in config.py: DEBUG = True
```

### Python debugging
```python
# Add to code for debugging
import pdb; pdb.set_trace()

# Or use print statements
print(f"Variable value: {variable}")
```

---

## 📝 File Management

### View project structure
```powershell
tree /F
```

### Count lines of code
```powershell
# PowerShell
Get-ChildItem -Recurse -Include *.py, *.html, *.css, *.js | Get-Content | Measure-Object -Line

# Or use this simpler version
(Get-ChildItem -Recurse -Include *.py | Get-Content).Count
```

### Search for text in files
```powershell
# Find in Python files
Get-ChildItem -Recurse -Include *.py | Select-String "search_term"

# Find in all files
Get-ChildItem -Recurse | Select-String "search_term"
```

---

## 🔧 Git Commands (if using version control)

```powershell
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: SmartML Dashboard"

# Check status
git status

# View history
git log --oneline

# Create branch
git branch feature-name

# Switch branch
git checkout feature-name
```

---

## 📦 Package Management

### Install specific versions
```powershell
pip install Flask==3.0.0
pip install pandas==2.1.4
pip install scikit-learn==1.3.2
```

### Install from requirements file
```powershell
pip install -r requirements.txt
```

### Create requirements file
```powershell
pip freeze > requirements.txt
```

### Check for outdated packages
```powershell
pip list --outdated
```

### Update specific package
```powershell
pip install --upgrade package_name
```

---

## 🎨 Frontend Development

### Open browser console
```
F12 or Ctrl+Shift+I (Chrome/Edge)
Ctrl+Shift+K (Firefox)
```

### Check JavaScript errors
```javascript
// In browser console
console.log("Debug message");
console.error("Error message");
```

### Clear browser cache
```
Ctrl+Shift+Delete (Most browsers)
Or Hard refresh: Ctrl+F5
```

---

## 🔍 Common Troubleshooting Commands

### Check if Flask app is running
```powershell
curl http://localhost:5000
# Or
Invoke-WebRequest http://localhost:5000
```

### Test file upload
```powershell
# Using curl (if installed)
curl -F "file=@sample_datasets/house_prices.csv" http://localhost:5000/upload
```

### Check Python path
```powershell
python -c "import sys; print(sys.executable)"
```

### Check module installation location
```powershell
python -c "import flask; print(flask.__file__)"
```

### Verify scikit-learn
```powershell
python -c "from sklearn import __version__; print(__version__)"
```

---

## 📊 Data Commands

### View CSV in terminal
```powershell
# First few lines
Get-Content sample_datasets\house_prices.csv -Head 10

# Count lines
(Get-Content sample_datasets\house_prices.csv).Count
```

### Quick pandas check
```python
python -c "import pandas as pd; df = pd.read_csv('sample_datasets/house_prices.csv'); print(df.head())"
```

---

## 🚀 Deployment Commands

### For Heroku (example)
```powershell
# Install Heroku CLI first
heroku login
heroku create smartml-dashboard
git push heroku main
heroku open
```

### For Docker (example)
```powershell
# Create Dockerfile first
docker build -t smartml-dashboard .
docker run -p 5000:5000 smartml-dashboard
```

---

## 💡 Useful Python One-Liners

### Check all imports
```powershell
python -c "import flask; import pandas; import sklearn; import matplotlib; import seaborn; import plotly; print('✓ All imports successful')"
```

### Test dataset loading
```powershell
python -c "import pandas as pd; df = pd.read_csv('sample_datasets/house_prices.csv'); print(f'Loaded {len(df)} rows, {len(df.columns)} columns')"
```

### Check sklearn algorithms
```powershell
python -c "from sklearn.linear_model import LinearRegression; from sklearn.tree import DecisionTreeClassifier; from sklearn.cluster import KMeans; print('✓ sklearn models OK')"
```

---

## 📈 Performance Monitoring

### Monitor Python process
```powershell
# Get process info
Get-Process python

# Monitor CPU/Memory
Get-Process python | Select-Object CPU, WS
```

### Check disk space
```powershell
Get-PSDrive C
```

---

## 🎓 Learning Commands

### Interactive Python shell
```powershell
python

# Then in Python shell:
>>> import pandas as pd
>>> df = pd.read_csv('sample_datasets/house_prices.csv')
>>> df.head()
>>> df.describe()
>>> exit()
```

### Test ML algorithms
```python
python -c "
from sklearn.linear_model import LinearRegression
import numpy as np
X = np.array([[1], [2], [3]])
y = np.array([2, 4, 6])
model = LinearRegression().fit(X, y)
print(f'Coefficient: {model.coef_[0]:.2f}')
"
```

---

## 🔐 Security Commands

### Check file permissions
```powershell
Get-Acl static\uploads
```

### Set file permissions (if needed)
```powershell
# Example: restrict access to uploads folder
icacls "static\uploads" /inheritance:r
```

---

## 📱 Shortcuts

### VS Code
```
Ctrl+P          : Quick file open
Ctrl+Shift+P    : Command palette
Ctrl+`          : Terminal
Ctrl+/          : Comment line
F5              : Run/Debug
```

### Browser
```
Ctrl+Shift+I    : Developer tools
Ctrl+Shift+R    : Hard refresh
F12             : Inspect element
Ctrl+F          : Find in page
```

---

## 🎯 Quick Fixes

### "Module not found" error
```powershell
pip install module_name
# Or reinstall all
pip install -r requirements.txt --force-reinstall
```

### "Port already in use" error
```powershell
# Change port in app.py or kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### "Permission denied" error
```powershell
# Run as administrator or check file permissions
# Or change upload directory in config.py
```

### Browser not loading
```powershell
# Clear cache: Ctrl+Shift+Delete
# Try different browser
# Check if Flask is running
# Check firewall settings
```

---

## 📚 Documentation Commands

### Generate HTML docs (if using Sphinx)
```powershell
# Install sphinx first
pip install sphinx
sphinx-quickstart docs
sphinx-build -b html docs docs/_build
```

### View help
```powershell
python app.py --help
python -m flask --help
```

---

## 🎉 Success Verification

After running these commands, you should see:
- ✅ Flask server running on http://localhost:5000
- ✅ No import errors
- ✅ Sample datasets accessible
- ✅ Dashboard loads in browser
- ✅ File upload works
- ✅ ML algorithms execute successfully

---

## 📞 Need Help?

1. Check terminal/console for errors
2. Review browser console (F12)
3. Verify all dependencies installed
4. Test with sample datasets first
5. Refer to TESTING_GUIDE.md

---

**Happy Coding! 💻✨**

*Last updated: 2025*
