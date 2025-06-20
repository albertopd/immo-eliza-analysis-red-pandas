from data_cleanner import DataCleanner

data_cleaner = DataCleanner("data/properties.csv")
#data_cleaner.clean_duplicates()
#data_cleaner.clean_errors()
#data_cleaner.clean_empty_cells()

if __name__ == "__main__":
    data_cleaner.send_output_file("data/cleaned_properties.csv")