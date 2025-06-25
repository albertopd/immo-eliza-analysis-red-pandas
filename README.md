
# Immoweb — Belgian Real Estate Analysis

A data analysis project for **Immoweb**, a Belgian real estate company, aiming to understand and predict property prices using Python, Pandas, and visualization tools.

---

## 🔍 Project Overview

Analyze a real estate dataset from Immoweb to:
- Clean and preprocess raw data (remove duplicates, handle missing values, standardize formats).
- Explore data quality, feature distributions, and relationships.
- Visualize insights: missing data, correlations, outliers, surface distributions.
- Identify the most and least expensive municipalities across Belgium, Wallonia, Flanders, and Brussels.
- Build a foundation for predictive modeling and strategic insights.

---

## 🛠️ Setup Instructions

1. **Clone the repo**  
   ```bash
   git clone https://github.com/albertopd/immo-eliza-analysis-red-pandas.git
   cd immo-eliza-analysis-red-pandas
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

### 1. Run the entire analysis from scratch:
```bash
python main.py
```
- Executes data cleaning and genearte charts.

---

## 📈 Data Analysis Highlights

### 🧼 Data Quality & Distributions

- Missing Data: Features like gardenSurface and epcScore show high missing ratios → informed filling/removal.
- Feature–Price Correlations: Surface area and room counts strongly correlate with price.
- Count-Feature Interrelations: Rooms, bathrooms, and facades intercorrelate — watch for multicollinearity in models.
- Outlier Detection: Boxplots highlight features with extreme values needing capping or removal.

### 📐 Surface Insights

- Surface Distribution: Most properties are small to mid-size with a long tail of large homes.
- Large-Surface Price: Properties > 1,000 m² command high prices, with visible variability across listings.

---

## 📈 Outputs

### 🧼 Data Quality & Distribution
- **01_missing_values_percentage.png**  
  Visualizes the percentage of missing values per feature.

- **02_correlation_with_variable_price.png**  
  Shows correlation coefficients between each numeric feature and the target variable `price`.

- **03_count_features_correlations.png**  
  Heatmap of correlations among count-based features like rooms, bathrooms, and parking spots.

- **04_outliers.png**  
  Boxplot visualization of outliers in numeric features, with annotations indicating counts.

### 📐 Surface Area Analysis
- **05_histogram_surface.png**  
  Histogram displaying the distribution of property surface areas.

- **06_big_surface_boxplot.png** / **10_big_surface_boxplot.png**  
  Boxplot showing price distribution for properties with very large surfaces (above 1000 m²).

### 💰 Most Expensive Municipalities
- **06_top_expensive_belgium.png** / **07_top_expensive_belgium.png**  
  Most expensive municipalities across Belgium based on average, median, and €/m².

- **07_top_expensive_wallonia.png** / **08_top_expensive_wallonia.png**  
  Most expensive municipalities in Wallonia.

- **08_top_expensive_flander.png** / **09_top_expensive_flander.png**  
  Most expensive municipalities in Flanders.

- **09_top_expensive_bruxelles.png** / **10_top_expensive_bruxelles.png**  
  Most expensive municipalities in Brussels.

### 💸 Least Expensive Municipalities
- **11_least_expensive_belgium.png**  
  Least expensive municipalities across Belgium.

- **12_least_expensive_wallonia.png**  
  Least expensive municipalities in Wallonia.

- **13_least_expensive_flander.png**  
  Least expensive municipalities in Flanders.

- **14_least_expensive_bruxelles.png**  
  Least expensive municipalities in Brussels.

---

## ⏳ Project Timeline

� Duration: ~3 days  
- Day 1: Data cleaning
- Day 2: Data analysis  
- Day 3: Data interpretation

---


## 🧰 Requirements

- **Python ≥ 3.8**
- Libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`, `dash`

See [requirements.txt](requirements.txt) for the full list.

---

## 👥 Contributors

- [Hajer Smiai](https://github.com/hajersmiai)
- [Charly Hornaert](https://github.com/CharlyHo)
- [Alberto Pérez Dávila](https://github.com/albertopd)