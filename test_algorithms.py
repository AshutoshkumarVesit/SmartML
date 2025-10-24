"""
Quick Test Script for SmartML Algorithms
Run this to verify all components work
"""
import sys
import requests
import json
import os

BASE_URL = "http://localhost:5000"

def test_server():
    """Test if server is running"""
    try:
        response = requests.get(BASE_URL)
        print("✅ Server is running")
        return True
    except:
        print("❌ Server is NOT running")
        print("   Run: python app.py")
        return False

def test_upload():
    """Test file upload"""
    filepath = "sample_datasets/house_prices.csv"
    
    if not os.path.exists(filepath):
        print(f"❌ Test file not found: {filepath}")
        return None
    
    try:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ File upload successful")
            print(f"   Session ID: {data['session_id']}")
            print(f"   Rows: {data['info']['shape'][0]}")
            print(f"   Columns: {data['info']['shape'][1]}")
            return data['session_id']
        else:
            print(f"❌ Upload failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return None

def test_regression(session_id):
    """Test regression algorithm"""
    payload = {
        'session_id': session_id,
        'target_column': 'Price',
        'algorithm': 'linear'
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/ml/regression",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                results = data['results']
                print("✅ Linear Regression successful")
                print(f"   R² Score: {results['metrics']['r2']:.4f}")
                print(f"   RMSE: {results['metrics']['rmse']:.4f}")
                return True
            else:
                print(f"❌ Regression failed: {data.get('error')}")
                return False
        else:
            print(f"❌ API error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Regression error: {e}")
        return False

def test_classification(session_id):
    """Test classification algorithm"""
    # First upload classification dataset
    filepath = "sample_datasets/heart_disease.csv"
    
    if not os.path.exists(filepath):
        print(f"⚠️  Classification test skipped - file not found")
        return None
    
    try:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        data = response.json()
        session_id = data['session_id']
        
        payload = {
            'session_id': session_id,
            'target_column': 'HeartDisease',
            'algorithm': 'decision_tree'
        }
        
        response = requests.post(
            f"{BASE_URL}/ml/classification",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                results = data['results']
                print("✅ Decision Tree Classification successful")
                print(f"   Accuracy: {results['metrics']['accuracy']:.4f}")
                return True
            else:
                print(f"❌ Classification failed: {data.get('error')}")
                return False
        else:
            print(f"❌ API error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Classification error: {e}")
        return False

def test_clustering(session_id):
    """Test clustering algorithm"""
    filepath = "sample_datasets/customer_segmentation.csv"
    
    if not os.path.exists(filepath):
        print(f"⚠️  Clustering test skipped - file not found")
        return None
    
    try:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        data = response.json()
        session_id = data['session_id']
        
        payload = {
            'session_id': session_id,
            'algorithm': 'kmeans',
            'n_clusters': 3
        }
        
        response = requests.post(
            f"{BASE_URL}/ml/clustering",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                results = data['results']
                print("✅ K-Means Clustering successful")
                print(f"   Silhouette Score: {results['metrics']['silhouette_score']:.4f}")
                return True
            else:
                print(f"❌ Clustering failed: {data.get('error')}")
                return False
        else:
            print(f"❌ API error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Clustering error: {e}")
        return False

def test_dimensionality(session_id):
    """Test dimensionality reduction"""
    payload = {
        'session_id': session_id,
        'algorithm': 'pca'
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/ml/dimensionality",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                results = data['results']
                print("✅ PCA Dimensionality Reduction successful")
                print(f"   Components: {results['metrics']['n_components']}")
                return True
            else:
                print(f"❌ Dimensionality failed: {data.get('error')}")
                return False
        else:
            print(f"❌ API error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Dimensionality error: {e}")
        return False

def main():
    print("\n" + "="*50)
    print("SmartML Algorithm Test Suite")
    print("="*50 + "\n")
    
    # Test 1: Server
    print("Test 1: Server Status")
    if not test_server():
        print("\n⚠️  Please start the server first!")
        return
    print()
    
    # Test 2: Upload
    print("Test 2: File Upload")
    session_id = test_upload()
    if not session_id:
        print("\n⚠️  Upload failed - stopping tests")
        return
    print()
    
    # Test 3: Regression
    print("Test 3: Regression Algorithm")
    test_regression(session_id)
    print()
    
    # Test 4: Classification
    print("Test 4: Classification Algorithm")
    test_classification(session_id)
    print()
    
    # Test 5: Clustering
    print("Test 5: Clustering Algorithm")
    test_clustering(session_id)
    print()
    
    # Test 6: Dimensionality
    print("Test 6: Dimensionality Reduction")
    test_dimensionality(session_id)
    print()
    
    print("="*50)
    print("Test Suite Complete!")
    print("="*50)
    print("\n✅ If all tests passed, algorithms are working!")
    print("❌ If any test failed, check the error messages above")
    print("\n📝 Next: Open browser and test UI manually")
    print("   URL: http://localhost:5000")

if __name__ == "__main__":
    main()
