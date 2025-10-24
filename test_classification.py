"""
Test Decision Tree and SVM Specifically
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_decision_tree():
    """Test Decision Tree with heart disease dataset"""
    print("=" * 60)
    print("Testing Decision Tree Classification")
    print("=" * 60)
    
    # Upload heart disease dataset
    filepath = "sample_datasets/heart_disease.csv"
    
    try:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        if response.status_code != 200:
            print(f"❌ Upload failed: {response.text}")
            return
        
        data = response.json()
        session_id = data['session_id']
        print(f"✅ Dataset uploaded: {data['filename']}")
        print(f"   Rows: {data['info']['shape'][0]}, Columns: {data['info']['shape'][1]}")
        print(f"   Columns: {', '.join(data['info']['columns'])}")
        print()
        
        # Test Decision Tree
        print("Testing Decision Tree...")
        payload = {
            'session_id': session_id,
            'target_column': 'HeartDisease',
            'algorithm': 'decision_tree',
            'max_depth': None
        }
        
        response = requests.post(
            f"{BASE_URL}/ml/classification",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Decision Tree SUCCESS!")
                metrics = result['results']['metrics']
                print(f"   Accuracy: {metrics['accuracy']:.4f}")
                print(f"   Precision: {metrics['precision']:.4f}")
                print(f"   Recall: {metrics['recall']:.4f}")
                print(f"   F1 Score: {metrics['f1_score']:.4f}")
                
                if 'confusion_matrix' in result['results']:
                    print(f"   Confusion Matrix available: ✅")
                if 'feature_importance_plot' in result['results']:
                    print(f"   Feature Importance plot: ✅")
            else:
                print(f"❌ Decision Tree failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ API Error ({response.status_code}):")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('error', response.text)}")
            except:
                print(f"   Response: {response.text}")
        
        return session_id
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_svm(session_id=None):
    """Test SVM with heart disease dataset"""
    print("\n" + "=" * 60)
    print("Testing SVM Classification")
    print("=" * 60)
    
    # Upload heart disease dataset if no session
    if not session_id:
        filepath = "sample_datasets/heart_disease.csv"
        
        try:
            with open(filepath, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{BASE_URL}/upload", files=files)
            
            data = response.json()
            session_id = data['session_id']
            print(f"✅ Dataset uploaded: {data['filename']}")
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return
    
    # Test SVM
    try:
        print("\nTesting SVM with RBF kernel...")
        payload = {
            'session_id': session_id,
            'target_column': 'HeartDisease',
            'algorithm': 'svm',
            'kernel': 'rbf',
            'C': 1.0
        }
        
        response = requests.post(
            f"{BASE_URL}/ml/classification",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ SVM SUCCESS!")
                metrics = result['results']['metrics']
                print(f"   Accuracy: {metrics['accuracy']:.4f}")
                print(f"   Precision: {metrics['precision']:.4f}")
                print(f"   Recall: {metrics['recall']:.4f}")
                print(f"   F1 Score: {metrics['f1_score']:.4f}")
                print(f"   Kernel: {result['results'].get('kernel', 'N/A')}")
                
                if 'confusion_matrix' in result['results']:
                    print(f"   Confusion Matrix available: ✅")
            else:
                print(f"❌ SVM failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ API Error ({response.status_code}):")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('error', response.text)}")
            except:
                print(f"   Response: {response.text}")
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

def test_other_algorithms(session_id):
    """Test other classification algorithms"""
    print("\n" + "=" * 60)
    print("Testing Other Classification Algorithms")
    print("=" * 60)
    
    algorithms = ['random_forest', 'adaboost', 'gradient_boosting']
    
    for algo in algorithms:
        print(f"\nTesting {algo}...")
        try:
            payload = {
                'session_id': session_id,
                'target_column': 'HeartDisease',
                'algorithm': algo
            }
            
            response = requests.post(
                f"{BASE_URL}/ml/classification",
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    metrics = result['results']['metrics']
                    print(f"✅ {algo}: Accuracy = {metrics['accuracy']:.4f}")
                else:
                    print(f"❌ {algo} failed: {result.get('error')}")
            else:
                print(f"❌ {algo} API error: {response.status_code}")
        except Exception as e:
            print(f"❌ {algo} exception: {e}")

def main():
    print("\n" + "=" * 60)
    print("SmartML - Classification Algorithms Debug Test")
    print("=" * 60 + "\n")
    
    # Check server
    try:
        response = requests.get(BASE_URL)
        print("✅ Server is running\n")
    except:
        print("❌ Server is NOT running")
        print("   Please run: python app.py")
        return
    
    # Test Decision Tree
    session_id = test_decision_tree()
    
    if session_id:
        # Test SVM with same dataset
        test_svm(session_id)
        
        # Test other algorithms
        test_other_algorithms(session_id)
    else:
        print("\n⚠️  Decision Tree test failed, skipping other tests")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
