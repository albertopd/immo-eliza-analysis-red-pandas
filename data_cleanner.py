import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class DataCleanner:
    def __init__(self, data_file_path: str) -> None:
        self.properties = pd.read_csv(data_file_path)

    def clean_duplicates(self):
        # remove duplicates, including multiple listings for the same property
        pass

    def clean_errors(self):
        # clean data value
        # clean data types
        # changing False/True to 0/1
        # clean extra spaces/tabulations inside values
        pass

    def clean_empty_cells(self, properties):
        # Drop fully empty rows
        properties.dropna(how='all', inplace=True)

        # Drop fully empty columns
        properties.dropna(axis=1, how='all', inplace=True)

        # Replace remaining empty cells with a default value
        properties.fillna("No Info", inplace=True)

        # Save cleaned CSV
        properties.to_csv("cleaned_properties.csv", index=False)