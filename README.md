# 🌱 Explainable Multimodal Deep Learning for Crop Yield Prediction  
*Using satellite and climate data with SHAP explainability*

---

## 📌 Project Overview
This project develops an **explainable multimodal deep learning pipeline** for crop yield prediction.

It integrates:
- 🛰️ Satellite imagery  
- 🌦️ Climate data  
- 🌾 Historical yield records  

The model forecasts crop productivity while using **SHAP (SHapley Additive Explanations)** to interpret predictions.

### 🎯 Objective
Provide **transparent, reproducible insights** into how environmental variables influence crop yields, enabling better agricultural decision-making.

---

## 📂 Repository Structure
├── data/processed/ # Cleaned datasets
├── notebooks/ # Jupyter notebooks for analysis
├── results/ # CSVs, plots, interaction networks
├── src/ # Python scripts (modular pipeline)
├── requirements.txt # Dependencies
├── README.md # Project overview
└── .gitignore # Ignore unnecessary files


---

## ⚙️ Workflow

### 1. Data Preparation
- Satellite + climate data integration  
- Preprocessing and feature engineering  

### 2. Model Training
- XGBoost baseline  
- Multimodal deep learning models  

### 3. Explainability with SHAP
- Global feature importance  
- Per-crop analysis  
- Single prediction waterfall plots  
- Dependence & interaction plots  

### 4. Quantitative Reporting
- CSV exports (per crop, state, year)  
- Temporal trend visualizations  
- Correlation matrices  
- Ranked interaction strengths  
- Feature interaction networks  

---

## 📊 Key Outputs
- 📈 **Global importance plots** → Most influential features  
- 🌾 **Per-crop analysis** → Feature importance differences  
- ⏳ **Temporal trends** → Changes over time  
- 🔗 **Interaction networks** → Feature relationships  
- 📁 **CSV exports** → Actionable quantitative insights  

---

## 🔎 Insights
- Soybeans show strong sensitivity to **temperature variance**  
- Wheat yields are more influenced by **precipitation levels**  
- Climate variables form tightly connected clusters in SHAP interaction networks  

---

## 🚀 How to Reproduce

### 1. Clone the Repository
```bash
git clone https://github.com/arvina8/Explainable-Multimodal-Deep-Learning-for-Crop-Yield-Prediction-using-satellite-and-climate-data.git
cd Explainable-Multimodal-Deep-Learning-for-Crop-Yield-Prediction-using-satellite-and-climate-data

2. Create Environment & Install Dependencies
Recommended: Use Conda
# Create environment
conda create -n crop-yield python=3.12

# Activate environment
conda activate crop-yield

# Install dependencies
pip install -r requirements.txt

3. Run Notebooks
jupyter notebook
Run the notebooks in the following order:
01_data_preprocessing.ipynb
02_model_training.ipynb
03_shap_explainability.ipynb
04_reporting_and_visualizations.ipynb
📁 Outputs (plots, CSVs, interaction networks) will be saved automatically in the results/ folder.
