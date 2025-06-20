from data_cleanner import DataCleanner

data_cleaner = DataCleanner()

data_cleaner.load_data_from_csv("data/properties.csv")

data_cleaner.clean_data()

data_cleaner.export_data_to_csv("data/clean_data.csv")

