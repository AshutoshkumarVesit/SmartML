# SmartML Dashboard - System Architecture

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE (Browser)                     │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Upload     │  │ Visualize    │  │  Run ML      │              │
│  │   Dataset    │  │    Data      │  │ Algorithms   │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                  │                  │                       │
└─────────┼──────────────────┼──────────────────┼───────────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FRONTEND (HTML/CSS/JavaScript)                    │
│                                                                       │
│  ├─ index.html          : Main dashboard page                       │
│  ├─ style.css           : Custom styling & animations               │
│  └─ main.js             : AJAX calls, DOM manipulation              │
│                                                                       │
│  Technologies: Bootstrap 5, Chart.js, Plotly.js                     │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ HTTP Requests (JSON)
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       BACKEND (Flask API)                            │
│                                                                       │
│  app.py - Main Application Server                                   │
│  ├─ Route: /upload           → Handle file uploads                  │
│  ├─ Route: /visualize        → Generate visualizations              │
│  ├─ Route: /preprocess       → Data preprocessing                   │
│  ├─ Route: /ml/regression    → Run regression models                │
│  ├─ Route: /ml/classification → Run classification models           │
│  ├─ Route: /ml/clustering    → Run clustering models                │
│  └─ Route: /ml/dimensionality → Run PCA/SVD                         │
│                                                                       │
│  config.py - Configuration Settings                                 │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                  ┌───────────────┼───────────────┐
                  ▼               ▼               ▼
┌──────────────────────┐ ┌──────────────────┐ ┌─────────────────────┐
│   UTILS MODULE       │ │  ML MODULES      │ │  DATA STORAGE       │
│                      │ │                  │ │                     │
│  helpers.py          │ │ preprocessing.py │ │ static/uploads/     │
│  ├─ File validation  │ │ ├─ Data cleaning │ │ ├─ CSV files        │
│  ├─ Dataset info     │ │ ├─ Missing values│ │ └─ User datasets    │
│  ├─ Feature/target   │ │ ├─ Encoding      │ │                     │
│  └─ Type detection   │ │ └─ Scaling       │ │ sample_datasets/    │
│                      │ │                  │ │ ├─ house_prices.csv │
│                      │ │ visualization.py │ │ ├─ heart_disease.csv│
│                      │ │ ├─ Heatmaps      │ │ └─ customer_seg.csv │
│                      │ │ ├─ Distributions │ │                     │
│                      │ │ ├─ Boxplots      │ └─────────────────────┘
│                      │ │ └─ Result plots  │
│                      │ │                  │
│                      │ │ regression.py    │
│                      │ │ ├─ Linear        │
│                      │ │ ├─ Polynomial    │
│                      │ │ ├─ Random Forest │
│                      │ │ └─ Gradient Boost│
│                      │ │                  │
│                      │ │ classification.py│
│                      │ │ ├─ Decision Tree │
│                      │ │ ├─ SVM           │
│                      │ │ ├─ Random Forest │
│                      │ │ ├─ AdaBoost      │
│                      │ │ └─ Gradient Boost│
│                      │ │                  │
│                      │ │ clustering.py    │
│                      │ │ ├─ K-Means       │
│                      │ │ ├─ Elbow Method  │
│                      │ │ └─ DBSCAN        │
│                      │ │                  │
│                      │ │ dimensionality.py│
│                      │ │ ├─ PCA           │
│                      │ │ └─ SVD           │
└──────────────────────┘ └──────────────────┘
```

---

## 🔄 Data Flow Diagram

```
┌─────────┐
│  User   │
└────┬────┘
     │ 1. Upload CSV
     ▼
┌─────────────────┐
│  File Upload    │
│  Handler        │
└────┬────────────┘
     │ 2. Validate & Save
     ▼
┌─────────────────┐
│  pandas         │◄──── Load CSV
│  DataFrame      │
└────┬────────────┘
     │ 3. Process
     ▼
┌─────────────────────────────┐
│  Preprocessing Module       │
│  ├─ Handle missing values   │
│  ├─ Remove duplicates       │
│  ├─ Encode categories       │
│  └─ Scale features          │
└────┬────────────────────────┘
     │ 4. Cleaned Data
     ├────────────┬────────────────┬─────────────┐
     ▼            ▼                ▼             ▼
┌──────────┐ ┌──────────┐ ┌──────────────┐ ┌────────────┐
│Visualize │ │Regression│ │Classification│ │ Clustering │
│          │ │          │ │              │ │            │
│• Heatmap │ │• Linear  │ │• Dec. Tree   │ │• K-Means   │
│• Distrib.│ │• Poly.   │ │• SVM         │ │• DBSCAN    │
│• Boxplots│ │• RF      │ │• RF          │ │• Elbow     │
└────┬─────┘ └────┬─────┘ └──────┬───────┘ └─────┬──────┘
     │            │                │               │
     │ 5. Generate Results         │               │
     └────────────┴────────────────┴───────────────┘
                  │
                  ▼
     ┌─────────────────────────┐
     │  Results Package        │
     │  ├─ Metrics             │
     │  ├─ Plots (base64)      │
     │  ├─ Feature importance  │
     │  └─ Insights            │
     └────────┬────────────────┘
              │ 6. JSON Response
              ▼
     ┌─────────────────┐
     │  JavaScript     │
     │  Display Results│
     └────────┬────────┘
              │ 7. Render
              ▼
     ┌─────────────────┐
     │  User sees      │
     │  Results on     │
     │  Dashboard      │
     └─────────────────┘
```

---

## 🧩 Component Interactions

### 1. Upload Workflow
```
User Action → FileInput → AJAX POST → Flask /upload endpoint
                                      ├─ Validate file
                                      ├─ Save to uploads/
                                      ├─ Load with pandas
                                      ├─ Generate statistics
                                      └─ Return JSON response
                                      
Response → JavaScript → Update DOM
                       ├─ Show statistics
                       ├─ Display data preview
                       └─ Enable ML buttons
```

### 2. Visualization Workflow
```
User Click → AJAX POST → Flask /visualize endpoint
                         ├─ Get stored dataset
                         ├─ DataVisualizer class
                         │  ├─ correlation_heatmap()
                         │  ├─ distribution_plots()
                         │  └─ boxplots()
                         ├─ Convert plots to base64
                         └─ Return JSON with images
                         
Response → JavaScript → Display images in <img> tags
```

### 3. ML Algorithm Workflow
```
User selects algorithm + parameters
         ↓
AJAX POST to /ml/{algorithm_type}
         ↓
Flask endpoint
├─ Retrieve dataset from session
├─ Split features/target
├─ Initialize model class
│  ├─ RegressionModel
│  ├─ ClassificationModel
│  ├─ ClusteringModel
│  └─ DimensionalityReduction
├─ Train model
├─ Generate predictions
├─ Calculate metrics
├─ Create visualizations
└─ Return results JSON
         ↓
JavaScript displays results
├─ Metrics cards
├─ Plots
└─ Insights
```

---

## 📦 Module Dependencies

```
app.py
├── flask (Framework)
├── config.py (Settings)
├── utils/helpers.py
│   ├── pandas
│   ├── numpy
│   └── werkzeug
├── ml_modules/preprocessing.py
│   ├── pandas
│   ├── numpy
│   ├── sklearn.preprocessing
│   └── sklearn.impute
├── ml_modules/visualization.py
│   ├── matplotlib
│   ├── seaborn
│   ├── plotly
│   └── base64
├── ml_modules/regression.py
│   ├── sklearn.linear_model
│   ├── sklearn.ensemble
│   ├── sklearn.preprocessing
│   └── sklearn.metrics
├── ml_modules/classification.py
│   ├── sklearn.tree
│   ├── sklearn.svm
│   ├── sklearn.ensemble
│   └── sklearn.metrics
├── ml_modules/clustering.py
│   ├── sklearn.cluster
│   ├── sklearn.decomposition
│   └── sklearn.metrics
└── ml_modules/dimensionality.py
    ├── sklearn.decomposition
    └── sklearn.preprocessing
```

---

## 🔐 Security Considerations

### File Upload Security
- ✅ File extension validation (.csv only)
- ✅ File size limit (16MB)
- ✅ Secure filename (werkzeug.secure_filename)
- ✅ Dedicated upload directory

### Data Handling
- ✅ Session-based data storage
- ✅ No permanent database (privacy)
- ✅ File validation before processing
- ✅ Error handling for malformed data

### API Security (Future Enhancement)
- ⚠️ Add CSRF protection
- ⚠️ Implement rate limiting
- ⚠️ Add user authentication
- ⚠️ Input sanitization

---

## 🚀 Performance Optimization

### Current Optimizations
- ✅ Non-blocking file upload
- ✅ Asynchronous AJAX calls
- ✅ Image compression (base64)
- ✅ Efficient pandas operations
- ✅ Matplotlib non-interactive backend

### Future Optimizations
- ⚠️ Redis for session storage
- ⚠️ Celery for background tasks
- ⚠️ Caching frequently used datasets
- ⚠️ Pagination for large results
- ⚠️ WebSocket for real-time updates

---

## 🔧 Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | HTML5 | Structure |
| | CSS3 | Styling |
| | JavaScript | Interactivity |
| | Bootstrap 5 | UI Framework |
| | Chart.js | Charts |
| | Plotly.js | Interactive Plots |
| **Backend** | Flask | Web Framework |
| | Python 3.8+ | Language |
| **Data Processing** | pandas | Data Manipulation |
| | NumPy | Numerical Computing |
| **ML Algorithms** | scikit-learn | ML Library |
| **Visualization** | matplotlib | Static Plots |
| | seaborn | Statistical Viz |
| | Plotly | Interactive Viz |
| **Utilities** | Werkzeug | File Handling |
| | Flask-CORS | Cross-Origin |

---

## 📈 Scalability Path

### Phase 1: Current (Prototype)
- Single user
- In-memory storage
- Development server
- Local deployment

### Phase 2: Production Ready
- Multiple users
- Database integration
- Production server (Gunicorn)
- Cloud deployment

### Phase 3: Enterprise
- User authentication
- Role-based access
- Load balancing
- Microservices architecture
- Container orchestration

---

## 🎯 Key Design Decisions

1. **Session-based Storage**: Quick prototyping, no database setup
2. **Base64 Images**: Simplifies image serving, no file system access
3. **Modular ML Code**: Easy to extend with new algorithms
4. **Bootstrap UI**: Rapid development, responsive design
5. **Flask over Django**: Lightweight, flexible, fast development
6. **pandas DataFrame**: Standard for ML data, scikit-learn compatible

---

This architecture provides a solid foundation for learning ML concepts while maintaining clean, extensible code structure! 🚀
