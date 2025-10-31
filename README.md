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

=
## 💻 Local Development

### Prerequisites
- Python 3.12+ recommended
- pip (Python package manager)

### Installation

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

### Retrain Model
```bash
python model/train_sklearn_model.py
```



## 📈 Performance Improvements

See [ACCURACY_IMPROVEMENT.md](ACCURACY_IMPROVEMENT.md) for details:
- Started: 10% accuracy (deep learning on small dataset)
- Final: **81.05% accuracy** (Linear SVM with optimized data)
- 8x improvement through algorithm change and data expansion




Built with:
- Flask (Web framework)
- scikit-learn (Machine Learning)
- Linear SVM (Classification algorithm)
- TF-IDF (Feature extraction)


