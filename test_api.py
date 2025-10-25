"""
Test script for Oasis API endpoints
"""
import requests
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_root_endpoint():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint status: {response.status_code}")
        print(f"Root endpoint response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing root endpoint: {e}")
        return False

def test_predict_endpoint():
    """Test the predict endpoint"""
    print("\nTesting predict endpoint...")
    try:
        payload = {
            "symbol": "TSLA",
            "type": "stock",
            "period": "1y",
            "epochs": 10
        }
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        print(f"Predict endpoint status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Predicted price: ${data['predicted_price']:.2f}")
            print(f"Current price: ${data['current_price']:.2f}")
            print(f"Change: {data['change_percent']:.2f}%")
            return True
        else:
            print(f"Error response: {response.text}")
            return False
    except Exception as e:
        print(f"Error testing predict endpoint: {e}")
        return False

def test_historical_endpoint():
    """Test the historical endpoint"""
    print("\nTesting historical endpoint...")
    try:
        params = {
            "symbol": "TSLA",
            "range": "1mo"
        }
        response = requests.get(f"{BASE_URL}/historical", params=params)
        print(f"Historical endpoint status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Retrieved {len(data['data'])} historical records")
            return True
        else:
            print(f"Error response: {response.text}")
            return False
    except Exception as e:
        print(f"Error testing historical endpoint: {e}")
        return False

def test_update_model_endpoint():
    """Test the update_model endpoint"""
    print("\nTesting update_model endpoint...")
    try:
        params = {
            "symbol": "TSLA",
            "period": "1y",
            "epochs": 10
        }
        response = requests.post(f"{BASE_URL}/update_model", params=params)
        print(f"Update model endpoint status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Update message: {data['message']}")
            return True
        else:
            print(f"Error response: {response.text}")
            return False
    except Exception as e:
        print(f"Error testing update_model endpoint: {e}")
        return False

def main():
    """Main test function"""
    print("Oasis API Testing")
    print("=" * 50)
    
    # Test all endpoints
    tests = [
        test_root_endpoint,
        test_historical_endpoint,
        test_predict_endpoint,
        test_update_model_endpoint
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            # Add a small delay between tests
            time.sleep(1)
        except Exception as e:
            print(f"Error running test {test.__name__}: {e}")
            results.append(False)
    
    # Print summary
    print("\n" + "=" * 50)
    print("Test Summary:")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("All tests passed! ✅")
    else:
        print("Some tests failed! ❌")

if __name__ == "__main__":
    main()