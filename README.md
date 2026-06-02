# 🌾 AI-Based Crop Health, Soil & Pest Risk Detection System

An end-to-end precision agriculture system using hyperspectral imaging, deep learning, and real-time IoT monitoring.

---

## 📌 Overview

This system analyzes hyperspectral imaging data (112 spectral bands, 400–2500nm) to monitor crop health, predict soil properties, and detect pesticide distribution patterns across agricultural fields in real-time.

---

## 🎯 Key Features

- Crop health classification across 5 conditions with >85% accuracy
- Soil property estimation with R² > 0.80
- Pesticide distribution zone analysis
- Real-time IoT monitoring dashboard
- Automated WARNING and CRITICAL alert system

---

## 🧠 Models

| Module | Model | Performance |
|---|---|---|
| Crop Health | ViT + EfficientNet-1D + SRAN + XGBoost | >85% Accuracy |
| Soil Properties | Gradient Boosting Regressor | R² > 0.80 |
| Pesticide Detection | Spectral Index Analysis | Zone Classification |

---

## 📊 Crop Health Classes

| Class | Description |
|---|---|
| Healthy | Normal vegetation |
| Nutrient Deficiency | Reduced chlorophyll |
| Pest Infection | Damaged leaf tissue |
| Water Stress | Low water content |
| Disease | General plant disease |

---

## 📁 Project Structure
crop-monitoring-system/
│
├── main.py
├── requirements.txt
├── README.md
│
├── modules/
│   ├── __init__.py
│   ├── hyperspectral_loader.py
│   ├── ensemble_model.py
│   ├── soil_analyzer.py
│   ├── pesticide_analyzer.py
│   ├── iot_dashboard.py
│   └── visualization_engine.py
│
├── data/
│   ├── crop_data/
│   ├── soil_data/
│   └── field_maps/
│
├── outputs/
│   ├── plots/
│   ├── models/
│   └── reports/
│
└── notebooks/
    └── crop_monitoring.ipynb


    ---

## 🔧 Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.8+ | Core language |
| TensorFlow / Keras | Deep learning models |
| Scikit-learn | ML models & preprocessing |
| XGBoost | Meta-learner classification |
| NumPy / Pandas | Data manipulation |
| Matplotlib / Seaborn | Visualizations |
| SciPy | Signal filtering |

---

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/Charan-tec/crop-monitoring-system

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the system
python main.py
```

---

## 📈 Results

- Crop Health Classification: **>85% Accuracy**
- Soil Organic Matter R²: **>0.80**
- Soil Nitrogen R²: **>0.80**
- Soil pH R²: **>0.80**
- Soil Moisture R²: **>0.80**
- Pesticide Coverage: Missed / Under / Optimal / Over zone detection

---

## 💡 Future Improvements

- Integrate real satellite or drone datasets
- Deploy as Streamlit web application
- Add crop yield prediction module
- Extend with live weather API integration

---

## 👤 Author

**Charan Teja**
- LinkedIn: [charan-teja93](https://www.linkedin.com/in/charan-teja93)
- GitHub: [Charan-tec](https://github.com/Charan-tec)


