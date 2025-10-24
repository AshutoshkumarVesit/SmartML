"""
Quick SVM Test
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_svm():
    print("\n" + "="*60)
    print("QUICK SVM TEST")
    print("="*60)
    
    # Step 1: Upload dataset
    print("\n1. Uploading heart_disease.csv...")
    start = time.time()
    files = {'file': open('sample_datasets/heart_disease.csv', 'rb')}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    print(f"   Upload took: {time.time() - start:.2f}s")
    
    if response.status_code != 200:
        print(f"❌ Upload failed: {response.text}")
        return
    
    data = response.json()
    session_id = data['session_id']
    print(f"✅ Upload successful! Session: {session_id}")
    
    # Step 2: Run SVM
    print("\n2. Running SVM Classification...")
    start = time.time()
    payload = {
        'session_id': session_id,
        'target_column': 'HeartDisease',
        'algorithm': 'svm',
        'kernel': 'rbf'
    }
    
    response = requests.post(
        f"{BASE_URL}/ml/classification",
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    
    elapsed = time.time() - start
    print(f"   SVM took: {elapsed:.2f}s")
    
    if response.status_code != 200:
        print(f"❌ SVM failed with status {response.status_code}")
        print(f"Response: {response.text}")
        return
    
    result = response.json()
    
    if result.get('success'):
        print("✅ SVM Classification Successful!")
        
        results = result['results']
        
        # Display metrics
        print("\n📊 METRICS:")
        metrics = results.get('metrics', {})
        for key, value in metrics.items():
            if isinstance(value, float):
                print(f"  - {key.capitalize()}: {value:.4f}")
        
        # Check visualizations
        print("\n🎨 VISUALIZATIONS:")
        if 'decision_boundary_plot' in results and results['decision_boundary_plot']:
            print(f"  ✅ Decision boundary plot generated ({len(results['decision_boundary_plot'])} chars)")
        else:
            print(f"  ⚠️  Decision boundary plot: {results.get('decision_boundary_plot', 'Missing')}")
        
        if 'confusion_matrix_plot' in results:
            print(f"  ✅ Confusion matrix generated")
        
        print(f"\n  Support Vectors: {results.get('n_support_vectors', 'N/A')}")
        print(f"  Kernel: {results.get('kernel', 'N/A')}")
        
    else:
        print(f"❌ SVM failed: {result.get('error')}")
        if 'traceback' in result:
            print(f"\nTraceback:\n{result['traceback']}")

if __name__ == "__main__":
    try:
        test_svm()
        print("\n" + "="*60)
        print("TEST COMPLETED")
        print("="*60)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
