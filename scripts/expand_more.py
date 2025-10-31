"""
Add even MORE training data with common variations and typos
"""
import json

# Load
with open('model/intents.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# More comprehensive additions
massive_additions = {
    "greeting": [
        "hey there", "hi again", "hello again", "sup", "howdy partner",
        "good to meet you", "nice to meet you", "pleased to meet you",
        "how can you help", "i need help", "can you help me",
        "hello bot", "hey chatbot", "hi bot", "start"
    ],
    "goodbye": ["bye bye", "see ya", "gtg", "take it easy", "peace", "ciao", "adieu", "cheerio", "later gator"],
    "thanks": ["thanks a ton", "many thanks", "thanks again", "tysm", "thx a lot", "appreciated", "ta", "kudos"],
    "order_status": [
        "wheres my stuff", "where is my package", "package location",
        "find my order", "locate my order", "search order", "order number",
        "i ordered something", "my shipment", "track shipment",
        "delivery status", "package status", "my delivery"
    ],
    "payments": [
        "can i use my card", "credit card payment", "debit payment",
        "how to checkout", "checkout options", "paying method",
        "transaction security", "is this secure", "safe to pay",
        "payment gateway", "pay now", "make payment"
    ],
    "shipping": [
        "delivery fees", "shipping cost", "how much to ship",
        "shipping options", "fast delivery", "quick shipping",
        "overnight shipping", "same day delivery", "next day delivery",
        "where do you ship", "shipping locations", "delivery areas"
    ],
    "returns": [
        "refund policy", "money back", "get refund", "item refund",
        "wrong item", "defective product", "broken item", "not as described",
        "changed my mind", "dont want this", "return window"
    ],
    "product_inquiry": [
        "whats this", "what is this item", "item details", "product info",
        "more about this", "specifications", "features", "price",
        "cost", "how much", "whats the price", "stock status",
        "available", "in stock"
    ],
    "list_products": [
        "show catalog", "full catalog", "all items", "everything you have",
        "whats for sale", "browse catalog", "see products", "view items",
        "shop", "shopping", "buy", "purchase", "category", "categories"
    ],
    "affirmative": [
        "yes please", "yes indeed", "yup sure", "yea", "uh huh",
        "roger that", "affirmative", "indeed", "confirmed", "thats right",
        "you bet", "for sure", "absolutely yes"
    ],
    "account_management": [
        "my profile", "user settings", "edit profile", "account info",
        "change details", "update info", "my details", "account help",
        "forgot password", "cant login", "login issues"
    ],
    "promotions": [
        "any offers", "whats on sale", "sale items", "discounted items",
        "special deals", "limited offers", "todays deals", "clearance",
        "voucher codes", "referral code", "first time discount"
    ],
    "technical_support": [
        "bug report", "error message", "not loading", "cant access",
        "website down", "page not found", "broken link", "tech help needed",
        "system error", "glitch", "malfunction"
    ],
    "about_us": [
        "who runs this", "company background", "your story", "company mission",
        "business details", "what do you do", "about this store",
        "when did you start", "how long in business"
    ],
    "contact_info": [
        "support contact", "help desk", "customer care", "call center",
        "support line", "help line", "email support", "chat support",
        "contact us", "reach out", "get help"
    ],
    "chitchat": [
        "tell joke", "funny", "humor", "entertain", "something cool",
        "whats up", "hows it going", "whats good", "how you doing",
        "nice chatting", "youre helpful", "good bot", "smart bot"
    ]
}

# Add them
for intent in data['intents']:
    tag = intent['tag']
    if tag in massive_additions:
        before = len(intent['patterns'])
        intent['patterns'].extend(massive_additions[tag])
        after = len(intent['patterns'])
        print(f"{tag}: {before} → {after} (+{after-before})")

# Save
with open('model/intents.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

total = sum(len(i['patterns']) for i in data['intents'])
print(f"\n✅ TOTAL PATTERNS: {total}")
