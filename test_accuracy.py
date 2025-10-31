"""
Test the chatbot with the exact queries from user's conversation
"""
import requests
import time

BASE_URL = "http://127.0.0.1:5000"

# Wait for server to be ready
print("Waiting for server to be ready...")
time.sleep(1)

# Test cases from your conversation that were failing
test_cases = [
    ("hi", "Should greet back"),
    ("i want to check my order status", "Should ask for order ID"),
    ("can i pay using credit card", "Should explain credit card payment options"),
    ("order id is 12345", "Should show order status for 12345"),
    ("orderid is 12345", "Should show order status for 12345"),
    ("tell me a joke", "Should tell a joke"),
    ("tell me another joke", "Should tell another joke"),
    ("show me electronics", "Should list electronics products"),
]

print("="*80)
print("TESTING IMPROVED CHATBOT - USER'S EXACT QUERIES")
print("="*80)
print()

successful_tests = 0
failed_tests = 0

for query, expected_behavior in test_cases:
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"message": query},
            timeout=10
        )
        
        if response.status_code == 200:
            reply = response.json().get("reply", "")
            print(f"✓ Query: '{query}'")
            print(f"  Expected: {expected_behavior}")
            print(f"  Bot Reply: {reply}")
            print()
            successful_tests += 1
        else:
            print(f"✗ ERROR {response.status_code} for: '{query}'")
            print(f"  Expected: {expected_behavior}")
            print()
            failed_tests += 1
            
    except requests.exceptions.ConnectionError:
        print(f"✗ FAILED: Could not connect to server for '{query}'")
        print(f"  Make sure Flask app is running on {BASE_URL}")
        print()
        failed_tests += 1
        break
    except Exception as e:
        print(f"✗ FAILED: '{query}' - {e}")
        print()
        failed_tests += 1

print("="*80)
print(f"RESULTS: {successful_tests} successful, {failed_tests} failed")
print("="*80)

if successful_tests > 0:
    print("\n✅ The chatbot is now responding!")
    print("Check if the responses are accurate for each query type.")
else:
    print("\n❌ Could not test - server may not be running.")
