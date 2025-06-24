import matplotlib
from data_cleanner import DataCleanner
from visualization import plot_correlations_to_price, plot_outliers
from visualization import (plot_surface_histogram, assign_region, get_top_localities, plot_top_localities, plot_big_surface_boxplot)
from visualization import plot_correlations_to_price
from visualization import plot_outliers
from visualization import plot_count_features_correlations
from visualization import plot_missing_values_percentage

matplotlib.use('TkAgg')

# Initialization and data cleaning
cleaner = DataCleanner("data/immoweb-dataset.csv")
cleaner.send_output_file("data/data_cleanned.csv")

# Plot correlations to price
df = cleaner.to_real_values() # Convert -1 values to NaN so they are not included in the correlation
plot_correlations_to_price(df, "plots/correlation_with_variable_price.png", True)

# Plot other correlations
# Correlation between count-based features (Pearson Correlation)
plot_count_features_correlations(df, "plots/count_features_correlations.png", True)

# Plot the outliers
plot_outliers(df, "plots/outliers.png", True)

# Plot missing values percentages
plot_missing_values_percentage(df, "plots/missing_values_percentage.png", True)

# Appliquer le mapping des régions
df = assign_region(df)

# Belgique
top_be = get_top_localities(df)
plot_top_localities(top_be, "Top 10 Most Expensive Localities in Belgium")

# Wallonie
top_wal = get_top_localities(df, region_filter="Wallonie")
plot_top_localities(top_wal, "Top 10 Most Expensive Localities in Wallonia")

# Flandre
top_vla = get_top_localities(df, region_filter="Flandre")
plot_top_localities(top_vla, "Top 10 Most Expensive Localities in Flanders")

# Bruxelles
top_bru = get_top_localities(df, region_filter="Bruxelles")
plot_top_localities(top_bru, "Top 10 Most Expensive Localities in Brussels")

# big value for surface
plot_big_surface_boxplot(df, min_surface=1000, plot_file_path="plots/big_surface_boxplot.png", show_plot=True)
