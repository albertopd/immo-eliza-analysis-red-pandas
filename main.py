import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from data_cleanner import DataCleanner
from visualization import plot_correlations_to_price, plot_outliers

matplotlib.use('TkAgg')

# Initialization and data cleaning
cleaner = DataCleanner("data/immoweb-dataset.csv")
cleaner.send_output_file("data/data_cleanned.csv")

# Plot correlations to price
df = cleaner.to_real_values() # Convert -1 values to NaN so they are not included in the correlation
plot_correlations_to_price(df, "plots/correlation_with_variable_price.png", True)

# Plot other correlations
# TODO: (Alberto) Create new plots for correlations between other variables

# Plot the outliers
plot_outliers(df, "plots/outliers.png", True)

# Other plots...
