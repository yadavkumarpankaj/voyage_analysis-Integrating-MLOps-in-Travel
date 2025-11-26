# Application Status Summary

## ✅ Travel Recommendation Model (Streamlit)

**Status**: ✅ **WORKING**

- **Location**: `Travel Recommendation Model/app.py`
- **Model File**: `cf_recommender.pkl` ✅ Present
- **Port**: 8501
- **URL**: http://localhost:8501

### Test Results:
- ✅ Model loads successfully
- ✅ Cities available: Barcelona, London, Paris
- ✅ 12 hotels in database
- ✅ Recommendations working

### To Run:
```bash
cd "Travel Recommendation Model"
streamlit run app.py
```

---

## ⚠️ Gender Classification Model (Flask)

**Status**: ⚠️ **MISSING MODEL FILES** (App updated with error handling)

- **Location**: `Gender Classification Model/app.py`
- **Port**: 8000
- **URL**: http://localhost:8000

### Missing Files:
- ❌ `scaler.pkl`
- ❌ `pca.pkl`
- ❌ `tuned_logistic_regression_model.pkl`

### Fixes Applied:
- ✅ Added error handling for missing model files
- ✅ Added input validation
- ✅ Better error messages
- ✅ Graceful degradation (app won't crash)

### To Generate Model Files:
1. Open `Gender_Classification_Model.ipynb`
2. Run the training cells
3. Save the model files in the same directory

### Dependencies Required:
```bash
pip install flask sentence-transformers scikit-learn pandas numpy joblib
```

### To Run (will show error until model files are added):
```bash
cd "Gender Classification Model"
python app.py
```

---

## ✅ Flight Price Prediction (Flask)

**Status**: ✅ **WORKING**

- **Location**: `Flight Price Prediction/app.py`
- **Model Files**: ✅ `rf_model.pkl`, `scaler.pkl` present
- **Port**: 5001
- **URL**: http://localhost:5001

### Fixes Applied:
- ✅ Feature name normalization fixed
- ✅ Matplotlib backend configured
- ✅ Error handling improved

---

## Summary

| App | Status | Model Files | Port | Notes |
|-----|--------|-------------|------|-------|
| Flight Price Prediction | ✅ Working | ✅ Present | 5001 | All fixed |
| Travel Recommendation | ✅ Working | ✅ Present | 8501 | Ready to use |
| Gender Classification | ⚠️ Needs Models | ❌ Missing | 8000 | Error handling added |

---

## Quick Commands

### Start Travel Recommendation (Streamlit):
```bash
cd "Travel Recommendation Model"
streamlit run app.py
# Access: http://localhost:8501
```

### Start Gender Classification (Flask):
```bash
cd "Gender Classification Model"
python app.py
# Access: http://localhost:8000
# Note: Will show error until model files are added
```

### Start Flight Price Prediction (Flask):
```bash
cd "Flight Price Prediction"
python app.py
# Access: http://localhost:5001
```

