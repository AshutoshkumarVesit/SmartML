"""
Test Decision Tree Visualization
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_decision_tree_with_visualization():
    """Test Decision Tree with tree visualization"""
    print("\n" + "="*60)
    print("TESTING DECISION TREE WITH TREE VISUALIZATION")
    print("="*60)
    
    # Step 1: Upload dataset
    print("\n1. Uploading heart_disease.csv...")
    files = {'file': open('sample_datasets/heart_disease.csv', 'rb')}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    
    if response.status_code != 200:
        print(f"❌ Upload failed: {response.text}")
        return
    
    data = response.json()
    if not data.get('success'):
        print(f"❌ Upload failed: {data.get('error')}")
        return
    
    session_id = data['session_id']
    print(f"✅ Upload successful! Session ID: {session_id}")
    
    # Step 2: Run Decision Tree
    print("\n2. Running Decision Tree Classification...")
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
    
    if response.status_code != 200:
        print(f"❌ Classification failed: {response.text}")
        return
    
    result = response.json()
    
    if result.get('success'):
        print("✅ Decision Tree Classification Successful!")
        
        results = result['results']
        
        # Display metrics
        print("\n📊 METRICS:")
        metrics = results.get('metrics', {})
        for key, value in metrics.items():
            if isinstance(value, float):
                print(f"  - {key.upper()}: {value:.4f}")
            else:
                print(f"  - {key.upper()}: {value}")
        
        # Check for tree visualization
        print("\n🌳 TREE VISUALIZATION:")
        if 'tree_plot' in results:
            print(f"  ✅ Tree plot generated (base64 length: {len(results['tree_plot'])} chars)")
            print(f"  - Tree Depth: {results.get('tree_depth', 'N/A')}")
            print(f"  - Number of Leaves: {results.get('n_leaves', 'N/A')}")
        else:
            print("  ❌ Tree plot NOT found in results!")
        
        # Check other plots
        print("\n📈 OTHER VISUALIZATIONS:")
        if 'confusion_matrix_plot' in results:
            print(f"  ✅ Confusion matrix generated")
        if 'feature_importance_plot' in results:
            print(f"  ✅ Feature importance plot generated")
        
        # Display all available keys
        print("\n🔑 ALL RESULT KEYS:")
        for key in results.keys():
            if '_plot' in key or key == 'tree_plot':
                print(f"  - {key}: ✅ (visualization)")
            else:
                print(f"  - {key}")
        
    else:
        print(f"❌ Classification failed: {result.get('error')}")

if __name__ == "__main__":
    try:
        test_decision_tree_with_visualization()
        print("\n" + "="*60)
        print("TEST COMPLETED")
        print("="*60)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
