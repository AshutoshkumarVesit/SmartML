# SmartML Dashboard 🚀

A comprehensive web-based interactive machine learning and visualization platform for real-world data analysis and decision-making.

## 🎯 Features

- **Dataset Upload**: Easy CSV file upload with automatic validation
- **Data Visualization**: Interactive plots including heatmaps, scatterplots, histograms, and more
- **Machine Learning Algorithms**:
  - Linear Regression
  - Decision Tree Classifier
  - Support Vector Machine (SVM)
  - Ensemble Learning (Random Forest, AdaBoost, Gradient Boosting)
  - Multivariate Nonlinear Regression
  - Clustering (K-Means, DBSCAN)
  - Dimensionality Reduction (PCA, SVD)
- **Model Evaluation**: Comprehensive metrics and visualization
- **Insights Generation**: Automated feature importance and correlation analysis
- **Algorithm Comparison**: Side-by-side performance comparison

## 🛠️ Tech Stack

### Backend
- **Flask**: Lightweight Python web framework
- **pandas & numpy**: Data manipulation
- **scikit-learn**: Machine learning algorithms
- **matplotlib, seaborn, plotly**: Visualization

### Frontend
- **HTML5, CSS3, JavaScript**: Core web technologies
- **Bootstrap 5**: Responsive UI framework
- **Chart.js & Plotly.js**: Interactive charts

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager

## 🚀 Installation

1. Clone the repository:
```bash
cd SmartML
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Upload your CSV dataset and start exploring!

## 📁 Project Structure

```
SmartML/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── config.py                   # Configuration settings
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles
│   ├── js/
│   │   └── main.js            # Frontend JavaScript
│   └── uploads/               # Uploaded datasets
├── templates/
│   ├── index.html             # Homepage
│   ├── dashboard.html         # Main dashboard
│   └── results.html           # Results display
├── ml_modules/
│   ├── __init__.py
│   ├── preprocessing.py       # Data preprocessing
│   ├── visualization.py       # Visualization functions
│   ├── regression.py          # Regression algorithms
│   ├── classification.py      # Classification algorithms
│   ├── clustering.py          # Clustering algorithms
│   └── dimensionality.py      # PCA/SVD
├── utils/
│   ├── __init__.py
│   └── helpers.py             # Helper functions
└── sample_datasets/           # Example datasets
```

## 📊 Sample Datasets

The project includes sample datasets for testing:
- House Price Prediction (Regression)
- Heart Disease Prediction (Classification)
- Customer Segmentation (Clustering)
- Iris Dataset (PCA + Classification)

## 🎓 Educational Value

This project demonstrates:
- Complete ML pipeline implementation
- Data preprocessing and validation
- Model training and evaluation
- Interactive visualization techniques
- MLOps workflow understanding
- Real-world decision-making support

## 📝 License

MIT License

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Happy Machine Learning! 🎉**
