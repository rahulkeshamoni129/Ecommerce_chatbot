"""
Script to expand training data with variations
This will make the chatbot MUCH more accurate
"""
import json
import random

# Load existing intents
with open('model/intents.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Expansions to add variety
greeting_additions = [
    "Hello there", "Good afternoon", "Hi how are you", "Wassup", "Hola", 
    "Hey what's up", "Good to see you", "Hi friend", "Greetings!", "Top of the morning"
]

goodbye_additions = [
    "I'm leaving now", "Gotta run", "Later", "Peace out", "Signing off",
    "I'm off", "See you soon", "Until next time", "Farewell", "Take care"
]

thanks_additions = [
    "Appreciate it", "Thanks a lot", "Cheers", "Thank you very much",
    "That helps", "Grateful", "Thanks so much", "Ty", "Thx", "Thanks!"
]

order_status_additions = [
    "Order tracking", "Where's my package", "Track my purchase",
    "Can you find my order", "What's happening with my order",
    "Is my order shipped", "Has my package left", "Order update please",
    "Tell me about my order", "I need order information"
]

payments_additions = [
    "Payment info", "How do I pay", "Can I pay online",
    "What cards do you take", "Do you accept debit cards",
    "Payment security", "Is payment safe", "Can I pay by card",
    "What are my payment options", "Do you take Visa"
]

shipping_additions = [
    "Delivery information", "How fast is shipping", "Delivery time",
    "When will it arrive", "Shipping time", "How long till delivery",
    "Do you deliver", "Can you ship to my location", "International delivery"
]

returns_additions = [
    "Can I send it back", "Return item", "Send back product",
    "I don't want this anymore", "Return process", "How to return",
    "Refund please", "I want my money back", "Cancel my order"
]

product_inquiry_additions = [
    "Tell me about this product", "Product details", "What's this item",
    "Info on product", "Describe this item", "Product specifications",
    "Is this in stock", "Product availability", "Item information",
    "Can you tell me more", "Product description"
]

list_products_additions = [
    "What do you sell", "Show products", "Browse items",
    "What's available", "Product catalog", "What items do you have",
    "Show me what you sell", "Product list", "Available products",
    "What can I buy"
]

affirmative_additions = [
    "Yeah", "Yep", "Sure", "OK", "Okay", "Alright", "Sounds good",
    "Absolutely", "Definitely", "Of course", "That's right", "Correct"
]

account_management_additions = [
    "My account", "Login help", "Change my password", "Update my email",
    "Edit my profile", "Account settings", "Manage account",
    "Reset password", "Update account info", "Profile settings"
]

promotions_additions = [
    "Any discounts", "Promo codes", "Sales happening", "Deals available",
    "Coupons", "Special offers", "Are there any sales", "Discount codes",
    "Current promotions", "Any deals"
]

technical_support_additions = [
    "Technical help", "Tech support", "IT support", "Website issues",
    "App not working", "Technical problem", "Site errors",
    "Help with technical issue", "Something's broken"
]

about_us_additions = [
    "About your company", "Company information", "Who are you",
    "Tell me about yourself", "Your company", "Business info",
    "What is your company", "Company history"
]

contact_info_additions = [
    "How do I reach you", "Contact details", "Phone number",
    "Customer service number", "Email address", "Support email",
    "How to contact", "Get in touch", "Reach customer service"
]

chitchat_additions = [
    "How's the weather", "What's new", "Any news", "How are things",
    "Nice day", "Great weather", "Beautiful day", "Make me laugh",
    "Something funny", "Entertain me", "Tell me something interesting"
]

# Apply additions
additions_map = {
    "greeting": greeting_additions,
    "goodbye": goodbye_additions,
    "thanks": thanks_additions,
    "order_status": order_status_additions,
    "payments": payments_additions,
    "shipping": shipping_additions,
    "returns": returns_additions,
    "product_inquiry": product_inquiry_additions,
    "list_products": list_products_additions,
    "affirmative": affirmative_additions,
    "account_management": account_management_additions,
    "promotions": promotions_additions,
    "technical_support": technical_support_additions,
    "about_us": about_us_additions,
    "contact_info": contact_info_additions,
    "chitchat": chitchat_additions,
}

# Expand the data
for intent in data['intents']:
    tag = intent['tag']
    if tag in additions_map:
        # Add new patterns
        intent['patterns'].extend(additions_map[tag])
        print(f"Expanded {tag}: added {len(additions_map[tag])} patterns")

# Save expanded data
with open('model/intents.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Count total
total = sum(len(intent['patterns']) for intent in data['intents'])
print(f"\n✅ Total training patterns now: {total}")
print(f"✅ Saved to model/intents.json")
