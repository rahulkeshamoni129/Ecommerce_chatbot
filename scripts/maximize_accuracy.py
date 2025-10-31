"""
MAXIMIZE ACCURACY - Target low-performing intents identified in classification report
Focus areas:
- express_shipping: 0% recall (CRITICAL)
- technical_support: 40% recall 
- promotions: 50% recall
- chitchat: 56% recall
- returns: 57% recall
- about_us: 60% recall
- affirmative: 60% recall
- greeting: 62% recall
"""

import json
import random

# Load current intents
with open('model/intents.json', 'r') as f:
    data = json.load(f)

intents = data['intents']

# Expansion patterns for each weak intent
expansions = {
    'express_shipping': [
        "i need express shipping",
        "fastest shipping option",
        "rush delivery available",
        "expedited shipping cost",
        "overnight delivery",
        "can you ship this quickly",
        "urgent delivery needed",
        "how fast can you ship",
        "next day delivery",
        "priority shipping",
        "speed up my delivery",
        "express delivery options",
        "quick shipping methods",
        "fast track my order",
        "accelerated shipping",
        "premium shipping speed",
        "rapid delivery service",
        "swift shipping available",
        "hurry my order",
        "emergency shipping"
    ],
    'technical_support': [
        "website not loading properly",
        "page keeps crashing",
        "checkout button broken",
        "cart not updating",
        "images not showing",
        "search function not working",
        "login keeps failing",
        "can't upload profile picture",
        "payment page freezing",
        "mobile app crashing",
        "site running very slow",
        "error 404 on product page",
        "video not playing",
        "filter options broken",
        "wishlist disappeared",
        "reviews not loading",
        "coupon code won't apply",
        "account settings not saving",
        "notification settings broken",
        "browser compatibility issue"
    ],
    'promotions': [
        "what deals do you have",
        "current sales available",
        "discount codes today",
        "special offers this week",
        "bargains available",
        "clearance items",
        "flash sale happening",
        "promo codes active",
        "savings opportunities",
        "limited time offers",
        "seasonal discounts",
        "member exclusive deals",
        "bundle offers available",
        "buy one get one deals",
        "percent off sales",
        "coupon available now",
        "hot deals today",
        "best price guarantees",
        "holiday specials",
        "weekly promotions"
    ],
    'chitchat': [
        "that's interesting",
        "sounds good to me",
        "i see what you mean",
        "makes sense",
        "got it thanks",
        "understood",
        "fair enough",
        "that works",
        "no problem",
        "all good",
        "perfect",
        "excellent",
        "wonderful",
        "great to hear",
        "appreciate it",
        "noted",
        "will do",
        "sure thing",
        "absolutely",
        "of course"
    ],
    'returns': [
        "refund policy details",
        "send this back",
        "return shipping cost",
        "exchange for different size",
        "defective item return",
        "wrong item received",
        "didn't fit properly",
        "not what i expected",
        "change my mind return",
        "unopened package return",
        "return time limit",
        "restocking fee amount",
        "return label needed",
        "where to ship returns",
        "refund processing time",
        "store credit instead",
        "damaged in shipping return",
        "return without receipt",
        "warranty return process",
        "money back guarantee"
    ],
    'about_us': [
        "your company background",
        "business history",
        "founding year",
        "company mission statement",
        "corporate values",
        "who owns this company",
        "headquarters location",
        "how long in business",
        "company culture",
        "team size",
        "company achievements",
        "awards won",
        "sustainability practices",
        "community involvement",
        "charitable work",
        "company vision",
        "why shop with you",
        "what makes you different",
        "competitive advantages",
        "company story"
    ],
    'affirmative': [
        "yeah that's right",
        "exactly what i want",
        "that's correct",
        "you got it",
        "affirmative",
        "yup",
        "yep for sure",
        "absolutely yes",
        "definitely yes",
        "sure thing",
        "right on",
        "spot on",
        "precisely",
        "indeed",
        "confirmed",
        "correct",
        "that's the one",
        "perfect match",
        "sounds right",
        "agreed"
    ],
    'greeting': [
        "good morning",
        "good afternoon",
        "good evening",
        "hey there",
        "hi how are you",
        "hello friend",
        "greetings",
        "what's up",
        "howdy",
        "yo",
        "hiya",
        "good day",
        "nice to meet you",
        "pleasure to talk",
        "happy to be here",
        "hello again",
        "back again",
        "it's me again",
        "hey chatbot",
        "hi bot"
    ]
}

# Apply expansions
total_added = 0
for intent in intents:
    tag = intent['tag']
    if tag in expansions:
        original_count = len(intent['patterns'])
        new_patterns = [p for p in expansions[tag] if p.lower() not in [existing.lower() for existing in intent['patterns']]]
        intent['patterns'].extend(new_patterns)
        added = len(new_patterns)
        total_added += added
        print(f"✓ {tag}: {original_count} → {len(intent['patterns'])} patterns (+{added})")

# Save updated intents
with open('model/intents.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✅ Total patterns added: {total_added}")
print(f"📊 New total training samples: {sum(len(i['patterns']) for i in intents)}")
