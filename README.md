
# Immoweb — Belgian Real Estate Analysis

A data analysis project for **Immoweb**, a Belgian real estate company, aiming to understand and predict property prices using Python, Pandas, and visualization tools.

---

## 🔍 Project Overview

Analyze a dataset of Belgian property listings (scraped from Immoweb) to:

- Uncover key features influencing property prices (e.g., area, number of rooms, location)
- Clean and process data (handle missing values, remove, normalize categorical columns)
- Conduct exploratory data analysis using visualizations: distributions, correlations, maps, heatmaps
- Provide actionable insights reinforced by clear visual outputs

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

## 📊 Data Analysis Highlights

- **Dataset size & structure**: ~5,700 rows × 32 columns; many fields like `Garden_Area`, `LandSurface` had >50% missing values.
- **Feature removal**: Columns like `Open_fire`, `Swimming_pool`, `TypeSale` removed due to low variance or rarity (<5% occurrence).
- **Outlier treatment**: Reduced noise using IQR-based detection on price distributions.
- **Correlation insights**:
  - Moderate to strong positive relationships between `Price` & (`Bedrooms`, `Living_area`)
  - Strong inter-correlation between `Bedrooms` & `Living_area`
- **Spatial analysis**: Mapped average prices across Belgium, spotlighting priciest localities per region.

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

## 📝 Insights & Recommendations

- **Top influencers of price**: living area, bedroom count, property state, location.
- **Data-driven adjustments**: consider standardizing property types and refining missing-value imputation.
- **Business implications**: Target marketing efforts and valuation models towards variables with strongest price correlation; highlight high-value localities in Brussels and Flanders.

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