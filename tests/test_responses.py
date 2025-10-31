import importlib, sys
import os

# adjust path so repo root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
app = importlib.import_module('app')


def test_basic_intents():
    # Insert a sample order into the orders collection for the order-id lookup test
    try:
        app.orders_collection.insert_one({
            "order_id": "12345",
            "status": "Out for delivery",
            "eta": "today",
            "carrier": "FastShip",
            "tracking": "FS12345ABC"
        })
    except Exception:
        # If the DB isn't available, tests should still use the fallback behavior
        pass

    # Basic smoke tests using get_response directly (no server required)
    hi_resp = app.get_response('hi')
    # accept several polite greeting reply variants
    greet_ok = any(x in hi_resp.lower() for x in ['hello', 'hi', 'how can i', 'what can i'])
    assert greet_ok

    order_resp = app.get_response('where is my order')
    assert ('track' in order_resp.lower()) or ('order' in order_resp.lower())

    # order id lookup should respond with the order id we seeded above
    lookup_resp = app.get_response('order #12345')
    assert '12345' in lookup_resp

    refund_resp = app.get_response('when will i get my refund')
    assert ('refund' in refund_resp.lower()) or ('processed' in refund_resp.lower())


if __name__ == '__main__':
    test_basic_intents()
    print('All local response checks passed')
