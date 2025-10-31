"""
seed_db.py

Simple script to insert sample orders into the local MongoDB used by the app.
Run with PowerShell (adjust MONGODB_URI if needed):

$env:MONGODB_URI='mongodb://localhost:27017/'; C:/Users/hp/AppData/Local/Programs/Python/Python312/python.exe f:\ecommerce_chatbot\scripts\seed_db.py

"""
import os
from pymongo import MongoClient

MONGO_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
DB_NAME = os.environ.get('MONGODB_DB', 'chatbot_db')
ORDERS_COLLECTION = os.environ.get('MONGODB_ORDERS_COLLECTION', 'orders')

client = MongoClient(MONGO_URI)
db = client.get_database(DB_NAME)
orders = db.get_collection(ORDERS_COLLECTION)

sample_orders = [
    {
        'order_id': 'ORD100',
        'status': 'Processing',
        'eta': '3 days',
        'carrier': 'FastShip',
        'tracking': 'FS100ABC'
    },
    {
        'order_id': 'ORD101',
        'status': 'Shipped',
        'eta': '2 days',
        'carrier': 'QuickCarrier',
        'tracking': 'QC101XYZ'
    },
    {
        'order_id': 'ORD102',
        'status': 'Out for delivery',
        'eta': 'today',
        'carrier': 'FastShip',
        'tracking': 'FS102DEF'
    },
    {
        'order_id': 'ORD103',
        'status': 'Delivered',
        'eta': 'delivered yesterday',
        'carrier': 'ExpressPost',
        'tracking': 'EP103GHI'
    },
    {
        'order_id': 'ORD150',
        'status': 'In transit',
        'eta': '4 days',
        'carrier': 'GlobalShip',
        'tracking': 'GS150JKL'
    }
]

for o in sample_orders:
    existing = orders.find_one({'order_id': o['order_id']})
    if existing:
        print(f"Order {o['order_id']} already exists, skipping.")
    else:
        orders.insert_one(o)
        print(f"Inserted order {o['order_id']}")

print('Done')
