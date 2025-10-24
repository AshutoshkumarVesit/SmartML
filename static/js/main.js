// SmartML Dashboard - Main JavaScript

let currentSessionId = null;
let currentDataset = null;

// Notification System
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification-toast ${type}`;
    notification.innerHTML = `
        <i class="bi bi-${type === 'success' ? 'check-circle-fill' : 'exclamation-triangle-fill'}"></i> 
        ${message}
    `;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}

// Loading Overlay
function showLoading(message = 'Processing...') {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.id = 'loadingOverlay';
    overlay.innerHTML = `
        <div class="loading-content">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <h4>${message}</h4>
        </div>
    `;
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.opacity = '0';
        setTimeout(() => overlay.remove(), 300);
    }
}

// Initialize when document is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupFileUpload();
    setupVisualizationButton();
    createModals();
}

// File Upload Functionality
function setupFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.querySelector('.upload-area');
    
    // Click to upload
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#0d6efd';
        uploadArea.style.backgroundColor = '#e7f1ff';
    });
    
    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#dee2e6';
        uploadArea.style.backgroundColor = '#f8f9fa';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#dee2e6';
        uploadArea.style.backgroundColor = '#f8f9fa';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect({ target: { files: files } });
        }
    });
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    
    if (!file) return;
    
    if (!file.name.endsWith('.csv')) {
        showNotification('Please upload a CSV file', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    // Show loading
    showLoading('Uploading and analyzing dataset...');
    document.getElementById('uploadProgress').style.display = 'block';
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        document.getElementById('uploadProgress').style.display = 'none';
        
        if (data.success) {
            currentSessionId = data.session_id;
            currentDataset = data;
            
            // Show file info
            document.getElementById('fileName').textContent = data.filename;
            document.getElementById('fileInfo').style.display = 'block';
            
            // Display dataset info
            displayDatasetInfo(data);
            
            showNotification('Dataset uploaded successfully! 🎉', 'success');
            
            // Show dashboard
            setTimeout(() => {
                document.getElementById('dashboard').style.display = 'block';
                document.getElementById('dashboard').scrollIntoView({ behavior: 'smooth' });
            }, 500);
        } else {
            showNotification(data.error || 'Error uploading file', 'error');
        }
    })
    .catch(error => {
        hideLoading();
        document.getElementById('uploadProgress').style.display = 'none';
        showNotification('Error uploading file: ' + error.message, 'error');
    });
}

function displayDatasetInfo(data) {
    // Update stats
    document.getElementById('totalRows').textContent = data.info.shape[0];
    document.getElementById('totalColumns').textContent = data.info.shape[1];
    document.getElementById('numericColumns').textContent = data.info.numeric_columns.length;
    document.getElementById('categoricalColumns').textContent = data.info.categorical_columns.length;
    
    // Display data preview
    displayDataPreview(data.preview, data.info.columns);
    
    // Create and populate modals with dataset info
    createModals();
    updateModalSelects();
}

function displayDataPreview(data, columns) {
    const table = document.getElementById('dataPreview');
    const thead = table.querySelector('thead');
    const tbody = table.querySelector('tbody');
    
    // Clear existing content
    thead.innerHTML = '';
    tbody.innerHTML = '';
    
    // Create header
    const headerRow = document.createElement('tr');
    columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    
    // Create rows
    data.forEach(row => {
        const tr = document.createElement('tr');
        columns.forEach(col => {
            const td = document.createElement('td');
            td.textContent = row[col] !== null ? row[col] : 'N/A';
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}

// Visualizations
function setupVisualizationButton() {
    const btn = document.getElementById('generateVisualizationsBtn');
    btn.addEventListener('click', generateVisualizations);
}

function generateVisualizations() {
    if (!currentSessionId) {
        showAlert('warning', 'Please upload a dataset first');
        return;
    }
    
    const btn = document.getElementById('generateVisualizationsBtn');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Generating...';
    
    fetch('/visualize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            session_id: currentSessionId
        })
    })
    .then(response => response.json())
    .then(data => {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-graph-up"></i> Generate Visualizations';
        
        if (data.success) {
            displayVisualizations(data.visualizations);
        } else {
            showAlert('danger', data.error || 'Error generating visualizations');
        }
    })
    .catch(error => {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-graph-up"></i> Generate Visualizations';
        showAlert('danger', 'Error: ' + error.message);
    });
}

function displayVisualizations(visualizations) {
    const container = document.getElementById('visualizationsContainer');
    
    if (visualizations.correlation_heatmap) {
        document.getElementById('correlationHeatmap').src = visualizations.correlation_heatmap;
    }
    
    if (visualizations.distribution_plots) {
        document.getElementById('distributionPlots').src = visualizations.distribution_plots;
    }
    
    if (visualizations.boxplots) {
        document.getElementById('boxplots').src = visualizations.boxplots;
    }
    
    container.style.display = 'block';
    container.scrollIntoView({ behavior: 'smooth' });
}

// Machine Learning Functions
function runRegression(algorithm) {
    const targetColumn = document.getElementById('regressionTarget').value;
    const featureSelect = document.getElementById('regressionFeatures');
    const selectedFeatures = Array.from(featureSelect.selectedOptions).map(opt => opt.value);
    
    if (!targetColumn) {
        showNotification('Please select a target column', 'error');
        return;
    }
    
    if (selectedFeatures.length === 0) {
        showNotification('Please select at least 1 feature column', 'error');
        return;
    }
    
    const params = {
        session_id: currentSessionId,
        target_column: targetColumn,
        feature_columns: selectedFeatures,
        algorithm: algorithm
    };
    
    closeModal('regressionModal');
    showLoading(`Running linear regression...`);
    
    fetch('/ml/regression', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.success) {
            displayResults(data.results, 'Regression');
            showNotification('Regression analysis completed! ✨', 'success');
        } else {
            showNotification(data.error || 'Error running regression', 'error');
        }
    })
    .catch(error => {
        hideLoading();
        showNotification('Error: ' + error.message, 'error');
    });
}

function runClassification(algorithm) {
    console.log('🔍 runClassification called with algorithm:', algorithm);
    
    const targetColumn = document.getElementById('classificationTarget').value;
    console.log('🎯 Selected target column:', targetColumn);
    
    if (!targetColumn) {
        console.log('❌ No target column selected');
        showNotification('Please select a target column', 'error');
        return;
    }
    
    const params = {
        session_id: currentSessionId,
        target_column: targetColumn,
        algorithm: algorithm
    };
    
    console.log('📦 Request params:', params);
    
    if (algorithm === 'decision_tree') {
        params.max_depth = parseInt(document.getElementById('maxDepth').value) || null;
    } else if (algorithm === 'svm') {
        params.kernel = document.getElementById('svmKernel').value || 'rbf';
    }
    
    closeModal('classificationModal');
    showLoading(`Running ${algorithm.replace('_', ' ')} classification...`);
    
    fetch('/ml/classification', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.success) {
            displayResults(data.results, 'Classification');
            showNotification('Classification completed! 🎯', 'success');
        } else {
            showNotification(data.error || 'Error running classification', 'error');
        }
    })
    .catch(error => {
        hideLoading();
        showNotification('Error: ' + error.message, 'error');
    });
}

function runClustering(algorithm) {
    const params = {
        session_id: currentSessionId,
        algorithm: algorithm
    };
    
    if (algorithm === 'kmeans') {
        params.n_clusters = parseInt(document.getElementById('nClusters').value) || 3;
    } else if (algorithm === 'dbscan') {
        params.eps = parseFloat(document.getElementById('eps').value) || 0.5;
        params.min_samples = parseInt(document.getElementById('minSamples').value) || 5;
    } else if (algorithm === 'kmeans_elbow') {
        params.max_k = parseInt(document.getElementById('maxK').value) || 10;
    }
    
    closeModal('clusteringModal');
    showLoading(`Running ${algorithm.replace('_', ' ')} clustering...`);
    
    fetch('/ml/clustering', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.success) {
            displayResults(data.results, 'Clustering');
            showNotification('Clustering analysis completed! 📊', 'success');
        } else {
            showNotification(data.error || 'Error running clustering', 'error');
        }
    })
    .catch(error => {
        hideLoading();
        showNotification('Error: ' + error.message, 'error');
    });
}

function runDimensionality(algorithm) {
    const params = {
        session_id: currentSessionId,
        algorithm: algorithm
    };
    
    const nComponents = parseInt(document.getElementById('nComponents').value);
    if (nComponents) {
        params.n_components = nComponents;
    }
    
    closeModal('dimensionalityModal');
    showLoading(`Running ${algorithm.toUpperCase()} dimensionality reduction...`);
    
    fetch('/ml/dimensionality', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.success) {
            displayResults(data.results, 'Dimensionality Reduction');
            showNotification('Dimensionality reduction completed! 🔍', 'success');
        } else {
            showNotification(data.error || 'Error running dimensionality reduction', 'error');
        }
    })
    .catch(error => {
        hideLoading();
        showNotification('Error: ' + error.message, 'error');
    });
}

// Display Results
function displayResults(results, category, additionalData = {}) {
    const container = document.getElementById('resultsContainer');
    const section = document.getElementById('resultsSection');
    
    let html = `
        <div class="card shadow-lg border-0 mb-4 fade-in">
            <div class="card-header bg-success text-white">
                <h4 class="mb-0"><i class="bi bi-trophy-fill"></i> ${results.algorithm || category}</h4>
            </div>
            <div class="card-body">
    `;
    
    // Display metrics - Handle both old and new format
    html += '<div class="row mb-4">';
    
    // Check if metrics are in a 'metrics' object
    const metrics = results.metrics || results;
    
    const metricMappings = {
        'accuracy': 'Accuracy',
        'precision': 'Precision',
        'recall': 'Recall',
        'f1_score': 'F1 Score',
        'mae': 'MAE',
        'mse': 'MSE',
        'rmse': 'RMSE',
        'r2': 'R² Score',
        'silhouette_score': 'Silhouette Score',
        'n_clusters': 'Number of Clusters',
        'total_variance_explained': 'Variance Explained',
        'n_components': 'Components',
        'n_components_95_variance': '95% Variance Components'
    };
    
    for (const [key, label] of Object.entries(metricMappings)) {
        if (metrics[key] !== undefined) {
            const value = typeof metrics[key] === 'number' ? metrics[key].toFixed(4) : metrics[key];
            
            html += `
                <div class="col-md-3 mb-3">
                    <div class="metric-card">
                        <div class="metric-label">${label}</div>
                        <div class="metric-value">${value}</div>
                    </div>
                </div>
            `;
        }
    }
    
    html += '</div>';
    
    // Display Decision Tree visualization
    if (results.tree_plot) {
        html += `
            <div class="mb-4">
                <h5><i class="bi bi-diagram-3"></i> Decision Tree Structure</h5>
                <div class="alert alert-info">
                    <i class="bi bi-info-circle"></i> Tree Depth: <strong>${results.tree_depth || 'N/A'}</strong> | 
                    Number of Leaves: <strong>${results.n_leaves || 'N/A'}</strong>
                </div>
                <div class="tree-plot-container" style="overflow-x: auto; max-width: 100%;">
                    <img src="${results.tree_plot}" class="img-fluid rounded shadow-sm" alt="Decision Tree" style="max-width: none; width: auto;">
                </div>
            </div>
        `;
    }
    
    // Random Forest Trees
    if (results.forest_trees_plot) {
        html += `
            <div class="mb-4">
                <h5><i class="bi bi-trees"></i> Random Forest - Sample Trees</h5>
                <div class="alert alert-info">
                    <i class="bi bi-info-circle"></i> Showing 3 sample trees from ${results.n_trees || 'N/A'} total trees
                </div>
                <div class="tree-plot-container" style="overflow-x: auto; max-width: 100%;">
                    <img src="${results.forest_trees_plot}" class="img-fluid rounded shadow-sm" alt="Random Forest Trees" style="max-width: none; width: auto;">
                </div>
            </div>
        `;
    }
    
    // SVM Decision Boundary
    if (results.decision_boundary_plot) {
        html += `
            <div class="mb-4">
                <h5><i class="bi bi-bounding-box"></i> SVM Decision Boundary</h5>
                <div class="alert alert-info">
                    <i class="bi bi-info-circle"></i> Support Vectors: <strong>${results.n_support_vectors || 'N/A'}</strong> | 
                    Kernel: <strong>${results.kernel || 'RBF'}</strong>
                </div>
                <img src="${results.decision_boundary_plot}" class="img-fluid rounded shadow-sm" alt="SVM Decision Boundary">
            </div>
        `;
    }
    
    // Linear Regression Equation
    if (results.equation_formatted) {
        html += `
            <div class="mb-4">
                <h5><i class="bi bi-calculator"></i> Regression Equation</h5>
                <div class="alert alert-success">
                    <h6 class="mb-2">Model Formula:</h6>
                    <code style="font-size: 1.1em; display: block; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                        ${results.equation_formatted}
                    </code>
                    <small class="text-muted mt-2 d-block">
                        <i class="bi bi-info-circle"></i> Use this equation to predict values manually
                    </small>
                </div>
            </div>
        `;
    }
    
    // Regression: Actual vs Predicted
    if (results.prediction_plot) {
        html += `
            <div class="mb-4">
                <h5><i class="bi bi-graph-up"></i> Prediction Analysis</h5>
                <img src="${results.prediction_plot}" class="img-fluid rounded shadow-sm" alt="Prediction Analysis">
            </div>
        `;
    }
    
    // Clustering 3D Plot
    if (results.cluster_plot) {
        html += `
            <div class="mb-4">
                <h5><i class="bi bi-diagram-3-fill"></i> Cluster Visualization</h5>
                <img src="${results.cluster_plot}" class="img-fluid rounded shadow-sm" alt="Cluster Visualization">
            </div>
        `;
    }
    
    // Display plots (old format for backward compatibility)
    if (results.plot && !results.prediction_plot && !results.cluster_plot) {
        html += `
            <div class="mb-4">
                <h5><i class="bi bi-graph-up"></i> Visualization</h5>
                <img src="${results.plot}" class="img-fluid rounded shadow-sm" alt="Plot">
            </div>
        `;
    }
    
    if (results.confusion_matrix_plot) {
        html += `
            <div class="mb-4">
                <h5><i class="bi bi-grid-3x3"></i> Confusion Matrix</h5>
                <img src="${results.confusion_matrix_plot}" class="img-fluid rounded shadow-sm" alt="Confusion Matrix">
            </div>
        `;
    }
    
    if (results.feature_importance_plot) {
        html += `
            <div class="mb-4">
                <h5><i class="bi bi-bar-chart"></i> Feature Importance</h5>
                <img src="${results.feature_importance_plot}" class="img-fluid rounded shadow-sm" alt="Feature Importance">
            </div>
        `;
    }
    
    if (results.elbow_plot) {
        html += `
            <div class="mb-4">
                <h5><i class="bi bi-graph-down"></i> Elbow Curve</h5>
                <img src="${results.elbow_plot}" class="img-fluid rounded shadow-sm" alt="Elbow Curve">
                <p class="mt-2"><strong>Recommended K:</strong> ${results.recommended_k}</p>
            </div>
        `;
    }
    
    if (results.variance_plot) {
        html += `
            <div class="mb-4">
                <h5><i class="bi bi-pie-chart"></i> Explained Variance</h5>
                <img src="${results.variance_plot}" class="img-fluid rounded shadow-sm" alt="Variance Plot">
            </div>
        `;
    }
    
    // Additional info
    if (results.cluster_distribution) {
        html += '<div class="mb-3"><h5>Cluster Distribution</h5><ul>';
        for (const [key, value] of Object.entries(results.cluster_distribution)) {
            html += `<li>${key}: ${value} samples</li>`;
        }
        html += '</ul></div>';
    }
    
    html += '</div></div>';
    
    container.innerHTML = html;
    section.style.display = 'block';
    section.scrollIntoView({ behavior: 'smooth' });
    
    // Generate prediction inputs after HTML is rendered (for regression only)
    if (results.algorithm && results.algorithm.includes('Regression')) {
        // Get feature_names from backend response (already processed correctly)
        // Backend has already excluded target, outcomes, and handled categorical encoding
        let featureNames = [];
        
        // Priority 1: Get from additionalData (sent from backend)
        if (additionalData && additionalData.feature_names) {
            featureNames = additionalData.feature_names;
            console.log('✅ Using feature names from backend:', featureNames);
        }
        // Priority 2: Get from results
        else if (results.feature_names) {
            featureNames = results.feature_names;
            console.log('✅ Using feature names from results:', featureNames);
        }
        // Priority 3: Try to extract from coefficients/importance
        else if (results.coefficients) {
            featureNames = Object.keys(results.coefficients);
            console.log('⚠️ Extracted from coefficients:', featureNames);
        } else if (results.feature_importance) {
            featureNames = Object.keys(results.feature_importance);
            console.log('⚠️ Extracted from feature_importance:', featureNames);
        }
        
        // No prediction inputs needed anymore - removed feature
    }
}

// Utility Functions
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function showLoadingInModal(modalId) {
    const modal = document.getElementById(modalId);
    const body = modal.querySelector('.modal-body');
    body.innerHTML = `
        <div class="spinner-container">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        <p class="text-center mt-3">Processing... Please wait</p>
    `;
}

function closeModal(modalId) {
    const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
    if (modal) {
        modal.hide();
    }
}

// Create Modals
function createModals() {
    const modalsHTML = `
        <!-- Regression Modal -->
        <div class="modal fade" id="regressionModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title"><i class="bi bi-graph-up"></i> Regression Analysis</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="alert alert-info">
                            <i class="bi bi-info-circle"></i> <strong>Tip:</strong> Select the <strong>numeric column</strong> you want to predict (e.g., Price, Salary, Temperature). All other columns will be used as features.
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Feature Columns (Input Variables)</label>
                            <select id="regressionFeatures" class="form-select form-select-lg" multiple size="5">
                                <option value="">Select feature columns...</option>
                            </select>
                            <small class="text-muted">Hold Ctrl/Cmd to select multiple features. At least 1 required.</small>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Target Column (What to Predict)</label>
                            <select id="regressionTarget" class="form-select form-select-lg">
                                <option value="">Select numeric target column...</option>
                            </select>
                            <small class="text-muted">The numeric column you want to predict</small>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Algorithm</label>
                            <div class="row g-2">
                                <div class="col-12">
                                    <button type="button" class="btn btn-primary btn-lg w-100" onclick="runRegression('linear')">
                                        <i class="bi bi-graph-up"></i> Run Linear Regression
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Classification Modal -->
        <div class="modal fade" id="classificationModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-success text-white">
                        <h5 class="modal-title"><i class="bi bi-diagram-3"></i> Classification Analysis</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="alert alert-info">
                            <i class="bi bi-info-circle"></i> <strong>Tip:</strong> Select the column you want to <strong>predict</strong> (e.g., HeartDisease, Outcome, Status). All other columns will be used as features automatically.
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Target Column (What to Predict)</label>
                            <select id="classificationTarget" class="form-select form-select-lg">
                                <option value="">Select target column to predict...</option>
                            </select>
                            <small class="text-muted">The column containing categories/classes you want to predict</small>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Algorithm</label>
                            <div class="btn-group-vertical w-100" role="group">
                                <button type="button" class="btn btn-outline-success mb-1" onclick="runClassification('decision_tree')">
                                    <i class="bi bi-diagram-2"></i> Decision Tree
                                </button>
                                <button type="button" class="btn btn-outline-success mb-1" onclick="runClassification('svm')">
                                    <i class="bi bi-bounding-box"></i> Support Vector Machine (SVM)
                                </button>
                                <button type="button" class="btn btn-outline-success mb-1" onclick="runClassification('random_forest')">
                                    <i class="bi bi-trees"></i> Random Forest
                                </button>
                                <button type="button" class="btn btn-outline-success mb-1" onclick="runClassification('adaboost')">
                                    <i class="bi bi-rocket-takeoff"></i> AdaBoost
                                </button>
                                <button type="button" class="btn btn-outline-success" onclick="runClassification('gradient_boosting')">
                                    <i class="bi bi-speedometer2"></i> Gradient Boosting
                                </button>
                            </div>
                        </div>
                        
                        <!-- Hidden fields for algorithm parameters -->
                        <input type="hidden" id="maxDepth" value="">
                        <input type="hidden" id="svmKernel" value="rbf">
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Clustering Modal -->
        <div class="modal fade" id="clusteringModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-info text-white">
                        <h5 class="modal-title"><i class="bi bi-diagram-3-fill"></i> Clustering Analysis</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="alert alert-info">
                            <i class="bi bi-info-circle"></i> <strong>Note:</strong> Clustering uses <strong>all numeric columns</strong> automatically. No need to select features!
                        </div>
                        
                        <h6 class="fw-bold mb-3"><i class="bi bi-grid-3x3"></i> K-Means Clustering</h6>
                        <div class="mb-3">
                            <label class="form-label">Number of Clusters (K)</label>
                            <input type="number" id="nClusters" class="form-control form-control-lg" value="3" min="2" max="10">
                            <small class="text-muted">How many groups to create (2-10)</small>
                        </div>
                        <div class="row g-2 mb-4">
                            <div class="col-6">
                                <button type="button" class="btn btn-info w-100" onclick="runClustering('kmeans')">
                                    <i class="bi bi-play-fill"></i> Run K-Means
                                </button>
                            </div>
                            <div class="col-6">
                                <button type="button" class="btn btn-outline-info w-100" onclick="runClustering('kmeans_elbow')">
                                    <i class="bi bi-graph-down"></i> Elbow Method
                                </button>
                            </div>
                        </div>
                        
                        <hr>
                        
                        <h6 class="fw-bold mb-3"><i class="bi bi-circle"></i> DBSCAN Clustering</h6>
                        <div class="mb-3">
                            <label class="form-label">Epsilon (ε)</label>
                            <input type="number" id="eps" class="form-control" placeholder="Maximum distance" value="0.5" step="0.1" min="0.1">
                            <small class="text-muted">Maximum distance between points in a cluster</small>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Min Samples</label>
                            <input type="number" id="minSamples" class="form-control" placeholder="Minimum points" value="5" min="2">
                            <small class="text-muted">Minimum points to form a cluster</small>
                        </div>
                        <button type="button" class="btn btn-info w-100" onclick="runClustering('dbscan')">
                            <i class="bi bi-play-fill"></i> Run DBSCAN
                        </button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Dimensionality Modal -->
        <div class="modal fade" id="dimensionalityModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-warning text-dark">
                        <h5 class="modal-title"><i class="bi bi-arrow-down-up"></i> Dimensionality Reduction</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="alert alert-warning">
                            <i class="bi bi-info-circle"></i> <strong>Purpose:</strong> Reduce high-dimensional data to fewer dimensions while preserving important information. Uses <strong>all numeric columns</strong> automatically.
                        </div>
                        
                        <div class="mb-4">
                            <label class="form-label fw-bold">Number of Components (Optional)</label>
                            <input type="number" id="nComponents" class="form-control form-control-lg" placeholder="Leave empty for automatic selection" min="2">
                            <small class="text-muted">How many dimensions to reduce to (leave empty for automatic)</small>
                        </div>
                        
                        <div class="row g-2">
                            <div class="col-6">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <h6 class="card-title">PCA</h6>
                                        <p class="card-text small">Principal Component Analysis</p>
                                        <button type="button" class="btn btn-warning w-100" onclick="runDimensionality('pca')">
                                            <i class="bi bi-play-fill"></i> Run PCA
                                        </button>
                                    </div>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <h6 class="card-title">SVD</h6>
                                        <p class="card-text small">Singular Value Decomposition</p>
                                        <button type="button" class="btn btn-outline-warning w-100" onclick="runDimensionality('svd')">
                                            <i class="bi bi-play-fill"></i> Run SVD
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('modalsContainer').innerHTML = modalsHTML;
}

// Update modals when dataset is loaded
function updateModalSelects() {
    if (!currentDataset) return;
    
    const numericCols = currentDataset.info.numeric_columns;
    const regressionCols = currentDataset.info.regression_columns || numericCols; // Use regression_columns if available
    const allCols = currentDataset.info.columns;
    
    // Update regression features (all numeric columns)
    const regressionFeatures = document.getElementById('regressionFeatures');
    if (regressionFeatures) {
        regressionFeatures.innerHTML = '';
        if (numericCols.length === 0) {
            regressionFeatures.innerHTML += '<option value="" disabled>No numeric columns found</option>';
        } else {
            numericCols.forEach(col => {
                regressionFeatures.innerHTML += `<option value="${col}">${col}</option>`;
            });
        }
    }
    
    // Update regression target (only continuous numeric columns)
    const regressionTarget = document.getElementById('regressionTarget');
    if (regressionTarget) {
        regressionTarget.innerHTML = '<option value="">Select numeric target column...</option>';
        if (regressionCols.length === 0) {
            regressionTarget.innerHTML += '<option value="" disabled>No suitable columns found (need >10 unique values)</option>';
        } else {
            regressionCols.forEach(col => {
                regressionTarget.innerHTML += `<option value="${col}">${col}</option>`;
            });
        }
    }
    
    // Update classification target (all columns)
    const classificationTarget = document.getElementById('classificationTarget');
    if (classificationTarget) {
        classificationTarget.innerHTML = '<option value="">Select target column to predict...</option>';
        allCols.forEach(col => {
            classificationTarget.innerHTML += `<option value="${col}">${col}</option>`;
        });
    }
}

// ==========================================
// PREDICTION FUNCTIONS
// ==========================================

// Store feature names globally
window.currentFeatureNames = [];

// Generate input fields for prediction
function generatePredictionInputs(featureNames) {
    window.currentFeatureNames = featureNames;
    const container = document.getElementById('predictionInputs');
    if (!container) return;
    
    let html = '<p class="mb-3"><i class="bi bi-info-circle-fill text-primary"></i> <strong>Enter values for all features below:</strong></p>';
    html += '<div class="row">';
    
    featureNames.forEach((feature, index) => {
        html += `
            <div class="col-md-6 col-lg-4 mb-3">
                <label for="feature_${index}" class="form-label">
                    <strong>${feature}</strong>
                    <span class="text-muted" style="font-size: 0.85em;"> (numeric)</span>
                </label>
                <input type="number" 
                       class="form-control" 
                       id="feature_${index}" 
                       placeholder="Enter ${feature}"
                       step="any"
                       required>
            </div>
        `;
    });
    
    html += '</div>';
    html += '<div class="alert alert-light border mt-2"><i class="bi bi-lightbulb"></i> <small>Tip: Fill all fields to get accurate prediction</small></div>';
    container.innerHTML = html;
}

// Make prediction using trained model
async function makePrediction() {
    const resultDiv = document.getElementById('predictionResult');
    
    if (!window.currentModelKey) {
        resultDiv.innerHTML = '<div class="alert alert-danger">No trained model found. Please run a regression analysis first.</div>';
        return;
    }
    
    // Collect input values
    const inputValues = {};
    let allFilled = true;
    
    window.currentFeatureNames.forEach((feature, index) => {
        const input = document.getElementById(`feature_${index}`);
        if (!input || input.value === '') {
            allFilled = false;
            return;
        }
        inputValues[feature] = parseFloat(input.value);
    });
    
    if (!allFilled) {
        resultDiv.innerHTML = '<div class="alert alert-warning">Please fill in all feature values</div>';
        return;
    }
    
    // Show loading
    resultDiv.innerHTML = '<div class="alert alert-info"><i class="bi bi-hourglass-split"></i> Predicting...</div>';
    
    try {
        const response = await fetch('/ml/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model_key: window.currentModelKey,
                input_values: inputValues
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            const prediction = data.prediction;
            resultDiv.innerHTML = `
                <div class="alert alert-success">
                    <h5><i class="bi bi-check-circle"></i> Prediction Result</h5>
                    <hr>
                    <div class="row">
                        <div class="col-md-6">
                            <h6>Input Features:</h6>
                            <ul class="list-unstyled">
                                ${Object.entries(inputValues).map(([key, val]) => 
                                    `<li><strong>${key}:</strong> ${val}</li>`
                                ).join('')}
                            </ul>
                        </div>
                        <div class="col-md-6">
                            <h6>Predicted ${prediction.target_column}:</h6>
                            <h3 class="text-success">${prediction.prediction.toFixed(4)}</h3>
                            <small class="text-muted">Algorithm: ${prediction.algorithm}</small>
                        </div>
                    </div>
                </div>
            `;
        } else {
            resultDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
    }
}
