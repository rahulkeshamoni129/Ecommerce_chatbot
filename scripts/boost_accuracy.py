"""
Boost low-performing intents with more specific patterns
"""
import json

with open('model/intents.json', 'r') as f:
    data = json.load(f)

def find_intent(tag):
    for intent in data['intents']:
        if intent['tag'] == tag:
            return intent
    return None

# Boost change_address (0% recall)
change_address = find_intent('change_address')
if change_address:
    change_address['patterns'].extend([
        "i need to change my address",
        "update my address",
        "modify my shipping address",
        "change delivery address",
        "wrong shipping address",
        "update delivery address",
        "change where to ship",
        "different address",
        "new shipping address",
        "edit shipping address"
    ])

# Boost shipping_carrier (0% recall)
shipping_carrier = find_intent('shipping_carrier')
if shipping_carrier:
    shipping_carrier['patterns'].extend([
        "what carrier ships my order",
        "which company delivers",
        "shipping service",
        "delivery service",
        "who will deliver",
        "what shipping service",
        "carrier information",
        "shipping provider"
    ])

# Boost international_shipping (40% recall)
international = find_intent('international_shipping')
if international:
    international['patterns'].extend([
        "ship outside country",
        "deliver internationally",
        "send to another country",
        "ship abroad",
        "international delivery available",
        "do you deliver internationally",
        "ship to other countries",
        "foreign countries shipping",
        "overseas orders"
    ])

# Boost shipping_time (improve from 80%)
shipping_time = find_intent('shipping_time')
if shipping_time:
    shipping_time['patterns'].extend([
        "delivery timeline",
        "shipping timeline",
        "how long for my order",
        "when does it ship",
        "how quick is shipping",
        "speed of delivery",
        "time until delivery",
        "days to deliver"
    ])

# Boost chitchat (29% recall)
chitchat = find_intent('chitchat')
if chitchat:
    chitchat['patterns'].extend([
        "tell a joke",
        "make me laugh",
        "say something funny",
        "joke time",
        "any jokes",
        "you funny",
        "entertain me please"
    ])

# Boost contact_info (20% recall)
contact_info = find_intent('contact_info')
if contact_info:
    contact_info['patterns'].extend([
        "contact number",
        "phone number",
        "email address",
        "how to reach you",
        "customer service contact",
        "support contact",
        "call you",
        "email you"
    ])

with open('model/intents.json', 'w') as f:
    json.dump(data, f, indent=2)

print("="*70)
print("BOOSTED LOW-PERFORMING INTENTS")
print("="*70)
for intent in data['intents']:
    print(f"{intent['tag']}: {len(intent['patterns'])} patterns")
total = sum(len(i['patterns']) for i in data['intents'])
print(f"\nTotal: {total} patterns")
print("="*70)
