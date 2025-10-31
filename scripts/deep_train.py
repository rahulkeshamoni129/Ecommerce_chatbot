"""
Deep training data expansion for maximum accuracy
Adding highly specific patterns to reduce confusion
"""
import json

# Load current intents
with open('model/intents.json', 'r') as f:
    data = json.load(f)

# Find intent by tag
def find_intent(tag):
    for intent in data['intents']:
        if intent['tag'] == tag:
            return intent
    return None

# Expand shipping_time with very specific patterns
shipping_time = find_intent('shipping_time')
if shipping_time:
    new_patterns = [
        "how long does it take to ship",
        "how long will shipping take",
        "how many days for shipping",
        "shipping takes how long",
        "time for delivery",
        "delivery duration",
        "how soon will it arrive",
        "when can i expect delivery",
        "how long before it arrives",
        "days for delivery",
        "how long is standard shipping",
        "standard shipping time",
        "normal delivery time",
        "typical delivery time"
    ]
    for p in new_patterns:
        if p not in shipping_time['patterns']:
            shipping_time['patterns'].append(p)

# Expand international_shipping
international = find_intent('international_shipping')
if international:
    new_patterns = [
        "do you ship internationally",
        "international shipping available",
        "can you ship abroad",
        "ship to canada",
        "ship to europe",
        "ship to asia",
        "overseas delivery",
        "foreign shipping",
        "outside usa shipping",
        "ship to my country",
        "worldwide shipping",
        "global delivery"
    ]
    for p in new_patterns:
        if p not in international['patterns']:
            international['patterns'].append(p)

# Expand shipping (cost) with more specific patterns
shipping_cost = find_intent('shipping')
if shipping_cost:
    new_patterns = [
        "what are the shipping costs",
        "shipping cost",
        "how much is delivery",
        "price of shipping",
        "shipping fees",
        "delivery charges",
        "cost to ship",
        "shipping rates",
        "how much for shipping",
        "is shipping free",
        "free delivery",
        "shipping price"
    ]
    for p in new_patterns:
        if p not in shipping_cost['patterns']:
            shipping_cost['patterns'].append(p)

# Expand payments with more variations
payments = find_intent('payments')
if payments:
    new_patterns = [
        "payment security",
        "is payment safe",
        "are payments secure",
        "is it safe to pay",
        "secure checkout",
        "payment protection",
        "safe payment",
        "secure transaction",
        "is my card safe",
        "payment encryption"
    ]
    for p in new_patterns:
        if p not in payments['patterns']:
            payments['patterns'].append(p)

# Expand returns with more variations  
returns = find_intent('returns')
if returns:
    new_patterns = [
        "return procedure",
        "return steps",
        "how to send back",
        "return instructions",
        "sending item back",
        "return my order",
        "return a product",
        "send back my purchase"
    ]
    for p in new_patterns:
        if p not in returns['patterns']:
            returns['patterns'].append(p)

# Expand product listing with category-specific patterns
list_products = find_intent('list_products')
if list_products:
    new_patterns = [
        "show products",
        "browse products",
        "view products",
        "see products",
        "product listings",
        "available items",
        "what do you sell",
        "items for sale",
        "your products",
        "product categories"
    ]
    for p in new_patterns:
        if p not in list_products['patterns']:
            list_products['patterns'].append(p)

# Save
with open('model/intents.json', 'w') as f:
    json.dump(data, f, indent=2)

# Print stats
print("="*70)
print("DEEP TRAINING DATA EXPANSION COMPLETE")
print("="*70)

for intent in data['intents']:
    print(f"{intent['tag']}: {len(intent['patterns'])} patterns")

total_patterns = sum(len(intent['patterns']) for intent in data['intents'])
print(f"\nTotal patterns: {total_patterns}")
print("="*70)
