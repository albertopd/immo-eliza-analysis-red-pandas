
# Immoweb — Belgian Real Estate Analysis

A data analysis project for **Immoweb**, a Belgian real estate company, aiming to understand and predict property prices using Python, Pandas, and visualization tools.

---

## 🔍 Project Overview

Analyze a dataset of Belgian property listings (scraped from Immoweb) to:

- Uncover key features influencing property prices (e.g., area, number of rooms, location)
- Clean and process data (handle missing values, remove outliers, structure dataset)
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
- Executes data cleaning, outlier removal, EDA, heatmap generation, and average-price maps.

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

## 📈 Visual Outputs

Found in results and plots:
- Correlation matrices (national and regional)
- Geospatial heatmaps of average prices (Belgium, Brussels, Wallonia, Flanders)
- Highlights on top & bottom localities

---

## 📝 Insights & Recommendations

- **Top influencers of price**: living area, bedroom count, property state, location.
- **Data-driven adjustments**: consider standardizing property types and refining missing-value imputation.
- **Business implications**: Target marketing efforts and valuation models towards variables with strongest price correlation; highlight high-value localities in Brussels and Flanders.

---

## ⏳ Project Timeline

� Duration: ~5 days  
- Day 1–2: Data cleaning & schema design  
- Day 3: Outlier detection & preliminary EDA  
- Day 4: Deep dive into correlation and visualisation  
- Day 5: Spatial mapping and final insight reporting

---


## 🧰 Requirements

- **Python ≥ 3.8**
- Libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`, `jupyter`

---

## 👥 Contributors

- [CharlyHo](https://github.com/CharlyHo)
- [hajersmiai](https://github.com/hajersmiai)
- [albertopd](https://github.com/albertopd)