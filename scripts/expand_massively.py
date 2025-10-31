"""
Massive expansion of training data to fix chatbot accuracy issues
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

# PAYMENT PATTERNS - Add very specific patterns
payments_intent = find_intent('payments')
if payments_intent:
    new_payment_patterns = [
        "can i pay using credit card",
        "can i pay with credit card",
        "can i use credit card",
        "do you accept credit card",
        "credit card accepted",
        "can i pay by credit card",
        "payment by credit card",
        "use credit card to pay",
        "i want to pay with credit card",
        "how to pay with credit card",
        "credit card option",
        "paying with credit card",
        "credit or debit card",
        "card payment",
        "can i pay with my card",
        "can i use my credit card",
        "is credit card accepted",
        "credit card support",
        "pay via credit card",
        "payment through credit card",
        "credit card checkout",
        "checkout with credit card",
        "can i checkout with credit card",
        "what payment methods",
        "payment method",
        "how can i pay",
        "ways to pay",
        "payment option",
        "what are the payment options",
        "how do i make payment",
        "how to make payment",
        "payment process",
        "can i pay online",
        "online payment",
        "digital payment",
        "card accepted",
        "do you take cards",
        "which cards do you accept",
        "accepted cards",
        "payment types",
        "types of payment",
        "payment methods available",
        "available payment methods"
    ]
    
    for pattern in new_payment_patterns:
        if pattern not in payments_intent['patterns']:
            payments_intent['patterns'].append(pattern)

# LIST PRODUCTS / ELECTRONICS - Add very specific patterns
list_products_intent = find_intent('list_products')
if list_products_intent:
    new_product_patterns = [
        "show me electronics",
        "show electronics",
        "list electronics",
        "display electronics",
        "electronics products",
        "electronic items",
        "electronics category",
        "electronics section",
        "view electronics",
        "see electronics",
        "electronics available",
        "what electronics do you have",
        "what electronics are available",
        "electronics catalog",
        "browse electronics",
        "shop electronics",
        "i want electronics",
        "i need electronics",
        "looking for electronics",
        "show me electronic products",
        "show me electronic items",
        "show me gadgets",
        "list gadgets",
        "electronic gadgets",
        "tech products",
        "technology products",
        "show me tech",
        "show tech products",
        "show me fashion",
        "show fashion",
        "list fashion",
        "fashion items",
        "fashion products",
        "clothing",
        "clothes",
        "show me sports",
        "show sports",
        "list sports",
        "sports items",
        "sports products",
        "sports equipment",
        "show me home",
        "show home",
        "home products",
        "home items",
        "household items",
        "show me books",
        "show books",
        "list books",
        "book catalog",
        "i want to see electronics",
        "can i see electronics",
        "display all electronics",
        "all electronics",
        "electronics list",
        "full electronics catalog",
        "show all electronics"
    ]
    
    for pattern in new_product_patterns:
        if pattern not in list_products_intent['patterns']:
            list_products_intent['patterns'].append(pattern)

# ORDER STATUS - Add more specific patterns
order_status_intent = find_intent('order_status')
if order_status_intent:
    new_order_patterns = [
        "orderid is 12345",
        "order id is 12345",
        "my order id is 12345",
        "the order id is 12345",
        "order number is 12345",
        "my order number is 12345",
        "order # 12345",
        "order #12345",
        "check order 12345",
        "status of order 12345",
        "my orderid is 12345",
        "orderid 12345",
        "order id 12345",
        "the orderid is 12345",
        "here is my order id 12345",
        "here is order id 12345",
        "i want to check my order status",
        "i want to track my order",
        "track my order",
        "check my order",
        "order tracking",
        "where is my order",
        "order location",
        "when will my order arrive",
        "order delivery",
        "order shipment",
        "track order",
        "check order",
        "order update",
        "status update",
        "my package",
        "where is my package",
        "package location",
        "track package",
        "check package",
        "i need to track my order",
        "can i track my order",
        "how to track order",
        "tracking information",
        "order details",
        "shipment status",
        "delivery status",
        "when will it arrive",
        "delivery time",
        "estimated delivery",
        "order eta"
    ]
    
    for pattern in new_order_patterns:
        if pattern not in order_status_intent['patterns']:
            order_status_intent['patterns'].append(pattern)

# JOKES - Add joke request patterns
jokes_intent = find_intent('jokes')
if jokes_intent:
    new_joke_patterns = [
        "tell me a joke",
        "tell me another joke",
        "tell another joke",
        "one more joke",
        "give me another joke",
        "another joke please",
        "tell me one more joke",
        "more jokes",
        "any more jokes",
        "got any more jokes",
        "tell me more jokes",
        "i want another joke",
        "joke please",
        "more joke",
        "another one",
        "tell another",
        "one more",
        "do you know more jokes",
        "do you have more jokes",
        "can you tell another joke",
        "can you tell more jokes",
        "make me laugh again",
        "another funny joke",
        "tell a different joke",
        "different joke",
        "new joke",
        "fresh joke",
        "got another joke",
        "you got more jokes"
    ]
    
    for pattern in new_joke_patterns:
        if pattern not in jokes_intent['patterns']:
            jokes_intent['patterns'].append(pattern)

# PRODUCT INQUIRY - More specific product questions
product_inquiry_intent = find_intent('product_inquiry')
if product_inquiry_intent:
    new_inquiry_patterns = [
        "tell me about this product",
        "product information",
        "product details",
        "more info about product",
        "what is this product",
        "describe this product",
        "product description",
        "product specs",
        "product specifications",
        "features of this product",
        "what does this product do",
        "how does this product work",
        "is this product good",
        "product quality",
        "product review",
        "product ratings",
        "tell me more about product",
        "i want to know about product",
        "product info",
        "details about product",
        "about this product",
        "this product details",
        "product features",
        "what are the features",
        "product benefits"
    ]
    
    for pattern in new_inquiry_patterns:
        if pattern not in product_inquiry_intent['patterns']:
            product_inquiry_intent['patterns'].append(pattern)

# AFFIRMATIVE - Add more yes variations
affirmative_intent = find_intent('affirmative')
if affirmative_intent:
    new_affirmative_patterns = [
        "yes please",
        "yes i do",
        "yes i would",
        "yes please do",
        "absolutely",
        "definitely",
        "of course",
        "certainly",
        "correct",
        "that's right",
        "exactly",
        "yes that's what i want",
        "yes please show me",
        "yes i want that",
        "yes show me",
        "yes tell me",
        "affirmative",
        "roger that",
        "uh huh",
        "mhmm",
        "yes go ahead",
        "yes continue",
        "yes proceed"
    ]
    
    for pattern in new_affirmative_patterns:
        if pattern not in affirmative_intent['patterns']:
            affirmative_intent['patterns'].append(pattern)

# Save the expanded data
with open('model/intents.json', 'w') as f:
    json.dump(data, f, indent=2)

# Print statistics
print("="*70)
print("MASSIVE DATA EXPANSION COMPLETE")
print("="*70)

for intent in data['intents']:
    print(f"{intent['tag']}: {len(intent['patterns'])} patterns")

total_patterns = sum(len(intent['patterns']) for intent in data['intents'])
print(f"\nTotal patterns: {total_patterns}")
print("="*70)
