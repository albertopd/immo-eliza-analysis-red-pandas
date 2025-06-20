from data_cleanner import DataCleanner

data_cleaner = DataCleanner("data/properties.csv")
data_cleaner.clean_duplicates()
data_cleaner.clean_errors()
data_cleaner.clean_empty_cells()
data_cleaner.split_column_type()

data_cleaner.export_data_to_csv("data/clean_data.csv")

