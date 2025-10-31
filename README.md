# E-Commerce Chatbot

![Accuracy](https://img.shields.io/badge/Accuracy-81.05%25-brightgreen)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Framework](https://img.shields.io/badge/Framework-Flask-black)
![ML](https://img.shields.io/badge/ML-LinearSVM-orange)

An intelligent e-commerce chatbot with **81.05% accuracy** using Linear SVM and 948 training patterns across 21 intents.

## 🎯 Features

- ✅ **81.05% Accuracy** - Linear SVM model with TF-IDF
- ✅ **21 Intents** - Greetings, products, orders, shipping, payments, returns, etc.
- ✅ **948 Training Patterns** - Comprehensive training dataset
- ✅ **Order Tracking** - Mock data for 5 sample orders (ORD100-ORD104)
- ✅ **No Database Required** - Simplified deployment
- ✅ **Production Ready** - Configured for Render/Heroku deployment
- ✅ **Fast Startup** - No database connection delays

## 🚀 Quick Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

**See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.**

Quick steps:
1. Push to GitHub
2. Connect to Render
3. Deploy automatically using `render.yaml`
4. Done! Your chatbot is live 🎉

## 💻 Local Development

### Prerequisites
- Python 3.12+ recommended
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ecommerce-chatbot.git
   cd ecommerce-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   - Navigate to http://127.0.0.1:5000
   - Start chatting!

## 🧪 Testing

**Test the model directly:**
```bash
python direct_test.py
```

**Test without MongoDB:**
```bash
python test_no_mongodb.py
```

**Run with different queries:**
```bash
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"hello"}'
```

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| **Accuracy** | 81.05% |
| **Algorithm** | Linear SVM |
| **Training Samples** | 948 |
| **Intents** | 21 |
| **Features** | TF-IDF (max 2000) |

**Perfect Performance (100% Recall):**
- Promotions
- Change Address
- Shipping Carrier
- Payments
- Contact Info
- Shipping Time

## 🛠️ Project Structure

```
ecommerce_chatbot/
├── app.py                      # Main Flask application
├── model/
│   ├── intents.json            # Training data (948 patterns)
│   ├── sklearn_pipeline.pkl    # Trained Linear SVM model
│   └── train_sklearn_model.py  # Model training script
├── templates/
│   └── index_bundle.html       # Chat UI (self-contained)
├── static/
│   ├── script.js               # Frontend JavaScript
│   └── style.css               # Styling
├── scripts/
│   ├── ultimate_train.py       # Advanced training with CV
│   └── maximize_accuracy.py    # Data expansion script
├── requirements.txt            # Python dependencies
├── Procfile                    # Deployment config
├── render.yaml                 # Render deployment config
├── build.sh                    # Build script
└── DEPLOYMENT.md               # Deployment guide
```

## 📝 Available Intents

1. **Customer Service**: greeting, goodbye, thanks, about_us, contact_info
2. **Products**: list_products, product_inquiry
3. **Orders**: order_status, change_address
4. **Payments**: payments, affirmative
5. **Shipping**: shipping, shipping_time, shipping_cost, international_shipping, express_shipping, shipping_carrier
6. **Support**: returns, technical_support, account_management
7. **Marketing**: promotions, chitchat

## 🎨 Customization

### Add New Intents

Edit `model/intents.json`:
```json
{
  "tag": "your_intent",
  "patterns": [
    "sample question 1",
    "sample question 2"
  ],
  "responses": [
    "response 1",
    "response 2"
  ]
}
```

### Retrain Model
```bash
python model/train_sklearn_model.py
```

### Update Mock Orders

Edit `app.py` - `mock_orders` dictionary:
```python
mock_orders = {
    "ORD100": {"status": "In transit", "eta": "2 days", ...},
    # Add more orders
}
```

## 📈 Performance Improvements

See [ACCURACY_IMPROVEMENT.md](ACCURACY_IMPROVEMENT.md) for details:
- Started: 10% accuracy (deep learning on small dataset)
- Final: **81.05% accuracy** (Linear SVM with optimized data)
- 8x improvement through algorithm change and data expansion

## 🔧 Configuration

### Environment Variables (Optional)

- `PORT` - Server port (default: 5000)
- `FLASK_RUN_HOST` - Host address (default: 127.0.0.1)
- `FLASK_DEBUG` - Debug mode (default: False)

### Production Deployment

Uses **Gunicorn** WSGI server (configured in `Procfile`):
```
web: gunicorn app:app
```

## 📚 Documentation

- [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed deployment guide
- [ACCURACY_IMPROVEMENT.md](ACCURACY_IMPROVEMENT.md) - Model improvement journey
- [MONGODB_REMOVAL.md](MONGODB_REMOVAL.md) - Database simplification

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🎉 Credits

Built with:
- Flask (Web framework)
- scikit-learn (Machine Learning)
- Linear SVM (Classification algorithm)
- TF-IDF (Feature extraction)

---

**Made with ❤️ for e-commerce customer service automation**

