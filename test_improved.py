"""
Quick test of the improved model
"""
import requests
import time

BASE_URL = "http://127.0.0.1:5000"

# Wait for server
time.sleep(2)

# Test cases from your conversation
test_cases = [
    "hi",
    "i want to track my order",
    "payment methods",
    "what payments do you accept",
    "can i pay with credit card",
    "show me electronics",
    "contact customer support",
    "how long does shipping take",
    "return policy",
    "any discounts"
]

print("="*70)
print("TESTING IMPROVED CHATBOT")
print("="*70)

for query in test_cases:
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"message": query},
            timeout=10
        )
        
        if response.status_code == 200:
            reply = response.json().get("reply", "")
            print(f"\nYou: {query}")
            print(f"Bot: {reply}")
        else:
            print(f"\n❌ Error {response.status_code} for: {query}")
            
    except Exception as e:
        print(f"\n❌ Failed to test '{query}': {e}")
        
print("\n" + "="*70)
print("✅ Test complete! Check if responses are now accurate.")
print("="*70)
