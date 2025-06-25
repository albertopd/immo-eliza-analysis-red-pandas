import matplotlib
from src.data_cleanner import DataCleanner
from src.data_analysis_plots import data_analysis_plots
from src.data_interpretation_plots import data_interpretation_plots

matplotlib.use('TkAgg')

# Initialization and data cleaning
cleaner = DataCleanner("data/immoweb-dataset.csv")
cleaner.send_output_file("data/data_cleanned.csv")

# Convert -1 values to NaN so they are not included in the correlation
df = cleaner.to_real_values() 

data_analysis_plots(df, True)

data_interpretation_plots(df, True)