import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from data_cleanner import DataCleanner

matplotlib.use('TkAgg')

# Initialization and data cleaning
cleaner = DataCleanner("data/immoweb-dataset.csv")
cleaner.send_output_file("data/data_cleanned.csv")

# Loading the cleaned file
#df = pd.read_csv("data/data_cleanned.csv")
df = cleaner.to_real_value()
print(df)

# Selecting only numeric columns
numeric_df = df.select_dtypes(include=["int64", "float64"])

# Calculation of the correlation matrix
corr_matrix = numeric_df.corr()

# Extracting correlations with 'price'
price_corr = corr_matrix["price"].drop("price").sort_values()

# Graphical visualization
plt.figure(figsize=(10, 6))
sns.barplot(x=price_corr.values, y=price_corr.index, hue=price_corr.index, palette="coolwarm", dodge=False, legend=False)
plt.title("Correlation with the variable 'price'")
plt.xlabel("Correlation coefficient")
plt.ylabel("Features")
plt.tight_layout()
plt.show()