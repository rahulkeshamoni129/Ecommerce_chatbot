"""
Test script to verify chatbot accuracy improvements
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# Test cases covering various intents
test_cases = [
    # Greetings
    {"input": "Hello", "expected_keywords": ["hello", "hi", "help", "assist"]},
    {"input": "Hi there", "expected_keywords": ["hello", "hi", "help"]},
    
    # Thanks
    {"input": "Thank you", "expected_keywords": ["happy", "help", "welcome", "pleasure"]},
    
    # Goodbye
    {"input": "Bye", "expected_keywords": ["goodbye", "bye", "see", "talk"]},
    
    # Product inquiry
    {"input": "Show me laptops", "expected_keywords": ["laptop", "product", "category"]},
    {"input": "What electronics do you have?", "expected_keywords": ["electronic", "product"]},
    
    # Order status
    {"input": "Where is my order?", "expected_keywords": ["order", "id", "provide"]},
    
    # Payments
    {"input": "What payment methods do you accept?", "expected_keywords": ["payment", "accept", "credit", "paypal"]},
    
    # Shipping
    {"input": "How long does shipping take?", "expected_keywords": ["shipping", "deliver", "day", "week"]},
]

def test_chatbot():
    print("=" * 60)
    print("CHATBOT ACCURACY TEST")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        user_input = test["input"]
        expected_keywords = test["expected_keywords"]
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"message": user_input},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                bot_reply = response.json().get("reply", "").lower()
                
                # Check if any expected keyword is in the response
                keyword_found = any(keyword in bot_reply for keyword in expected_keywords)
                
                status = "✅ PASS" if keyword_found else "❌ FAIL"
                if keyword_found:
                    passed += 1
                else:
                    failed += 1
                
                print(f"\nTest {i}: {status}")
                print(f"  Input: {user_input}")
                print(f"  Response: {bot_reply}")
                print(f"  Expected keywords: {expected_keywords}")
            else:
                print(f"\nTest {i}: ❌ ERROR (Status {response.status_code})")
                failed += 1
                
        except Exception as e:
            print(f"\nTest {i}: ❌ ERROR - {str(e)}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print(f"Accuracy: {(passed / len(test_cases) * 100):.1f}%")
    print("=" * 60)

if __name__ == "__main__":
    test_chatbot()
