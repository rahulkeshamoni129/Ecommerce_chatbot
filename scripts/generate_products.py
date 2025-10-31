import json
import random
import os

# Define the path to the products file
PRODUCTS_FILE = os.path.join(os.path.dirname(__file__), '..', 'model', 'products.json')

def generate_products():
    """
    Reads the existing product catalog, identifies categories, and generates
    placeholder products to ensure each category has at least 100 items.
    """
    try:
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            existing_products = data.get("products", [])
    except (FileNotFoundError, json.JSONDecodeError):
        existing_products = []

    # Organize existing products by category
    products_by_category = {}
    for product in existing_products:
        category = product.get("category", "Uncategorized")
        if category not in products_by_category:
            products_by_category[category] = []
        products_by_category[category].append(product)

    all_categories = list(products_by_category.keys())
    if not all_categories:
        print("No categories found. Please add some products first.")
        return

    new_product_list = []
    product_id_counter = len(existing_products) + 1

    # Process each category
    for category in all_categories:
        current_products = products_by_category.get(category, [])
        new_product_list.extend(current_products) # Add existing products
        
        num_to_generate = 100 - len(current_products)
        if num_to_generate <= 0:
            print(f"Category '{category}' already has {len(current_products)} products. No new products needed.")
            continue

        print(f"Generating {num_to_generate} new products for category '{category}'...")

        for i in range(num_to_generate):
            new_id = f"P{product_id_counter:03d}"
            product_number = len(current_products) + i + 1
            
            new_product = {
                "id": new_id,
                "name": f"{category} Product {product_number}",
                "category": category,
                "price": round(random.uniform(10.0, 2000.0), 2),
                "description": f"This is a generated description for {category} Product {product_number}. It offers great value and quality.",
                "in_stock": random.choice([True, False])
            }
            new_product_list.append(new_product)
            product_id_counter += 1

    # Write the new, expanded list back to the file
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump({"products": new_product_list}, f, indent=2)

    print(f"\nProduct generation complete. Total products: {len(new_product_list)}")

if __name__ == "__main__":
    generate_products()
