import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from data_cleanner import DataCleanner
import matplotlib
matplotlib.use('TkAgg')  



# Initialisation et nettoyage des données
cleaner = DataCleanner("data/immoweb-dataset.csv")
cleaner.send_output_file("data/data_cleanned.csv")

# Chargement du fichier nettoyé
#df = pd.read_csv("data/data_cleanned.csv")
df = cleaner.to_real_value()
print(df)
# Sélection des colonnes numériques uniquement
numeric_df = df.select_dtypes(include=["int64", "float64"])

# Vérification de la présence de la colonne 'price'
if 'price' not in numeric_df.columns:
    raise ValueError("❌ La colonne 'price' est absente du dataset.")

# Calcul de la matrice de corrélation
corr_matrix = numeric_df.corr()

# Extraction des corrélations avec 'price'
price_corr = corr_matrix["price"].drop("price").sort_values()

# Visualisation graphique
plt.figure(figsize=(10, 6))
sns.barplot(x=price_corr.values, y=price_corr.index, hue=price_corr.index, palette="coolwarm", dodge=False, legend=False)
plt.title("Corrélation avec la variable 'price'")
plt.xlabel("Coefficient de corrélation")
plt.tight_layout()
plt.show()