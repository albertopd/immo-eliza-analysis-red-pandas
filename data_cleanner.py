import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class DataCleanner:
    REGEX_REMOVE_NON_NUMERIC = re.compile(r'[^0-9]')

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
        print(self.properties.info())

        # Clean column 'zimmo code'
        self.properties["zimmo code"] = self.properties["zimmo code"].fillna("").str.strip()

        # Clean column 'type'
        self.properties["type"] = self.properties["type"].fillna("").str.strip()

        # Drop rows that don't have a 'price'
        self.properties.dropna(subset=["price"], inplace=True)

        # Clean column 'street'
        self.properties["street"] = self.properties["street"].fillna("").str.strip()

        # Clean column 'number'
        self.properties["number"] = self.properties["number"].fillna("").str.strip()

        # Clean column 'postalcode' and convert it to Int64 (to be able to handle the NaN)
        self.properties["postcode"] = self.properties["postcode"].str.extract(r"(\d+)").astype("Int64") 
        # Is it a mandatory variable? Should we drop the rows that don't contain a value?
        self.properties.dropna(subset=["postcode"], inplace=True)

        # Clean column 'city'
        self.properties["city"] = self.properties["city"].fillna("").str.strip()

        # Convert column 'living area(m²)' to int
        self.properties["living area(m²)"] = self.properties["living area(m²)"].replace([np.nan, np.inf, -np.inf], 0).astype(int)
        # TODO: Is it a mandatory variable? Should we drop the rows that don't contain value?
        # self.properties = self.properties[self.properties["living area(m²)"] != 0]

        # Convert column 'ground area(m²)' to int
        self.properties["ground area(m²)"] = self.properties["ground area(m²)"].replace([np.nan, np.inf, -np.inf], 0).astype(int)

        # Convert column 'bedroom' to int
        self.properties["bedroom"] = self.properties["bedroom"].replace([np.nan, np.inf, -np.inf], 0).astype(int)
        # TODO: Is it a mandatory variable? Should we drop the rows that don't contain value?
        # self.properties = self.properties[self.properties["bedroom"] != 0]

        # Convert column 'bathroom' to int
        self.properties["bathroom"] = self.properties["bathroom"].replace([np.nan, np.inf, -np.inf], 0).astype(int)
        # TODO: Is it a mandatory variable? Should we drop the rows that don't contain value?
        # self.properties = self.properties[self.properties["bathroom"] != 0]

        # Convert column 'garage' to int (# of garages)
        # TODO: should we just convert to 1/0 (has garage or not?)
        self.properties["garage"] = self.properties["garage"].replace([np.nan, np.inf, -np.inf], 0).astype(int)

        # Convert column 'garden' to int (1=True, 0=False)
        self.properties["garden"] = self.properties["garden"].fillna(False).astype(int)

        # Convert column 'EPC(kWh/m²)' to int
        # Using a placeholder of -1 for NaN. Useful to signal "unknown" clearly, especially for ML models
        self.properties["EPC(kWh/m²)"] = self.properties["EPC(kWh/m²)"].replace([np.nan, np.inf, -np.inf], -1).astype(int)

        # Convert column 'renovation obligation' to int (1=True, 0=False)
        self.properties["renovation obligation"] = self.properties["renovation obligation"].fillna(0).astype(int)

        # Convert column 'year built' to int
        # Using a placeholder of -1 for NaN. Useful to signal "unknown" clearly, especially for ML models
        self.properties["year built"] = self.properties["year built"].replace([np.nan, np.inf, -np.inf], -1).astype(int)

        # Clean column 'mobiscore'
        # Using a placeholder of -1 for NaN. Useful to signal "unknown" clearly, especially for ML models
        self.properties["mobiscore"] = self.properties["mobiscore"].replace([np.nan, np.inf, -np.inf], -1)

        print(self.properties.info())

    def clean_empty_cells(self):
        # remove empty lines
        # remove empty columns
        # what to do with empty cells?
        pass

    def split_column_type(self):
        self.properties['property type'] = np.select(
            [self.properties['type'].str.contains('Huis', na=False), self.properties['type'].str.contains('Appartement', na=False)],
            ['Huis', 'Appartement'],
            default='Project'
        )
        self.properties['property subtype'] = self.properties['type'].str.replace(r' \((Huis|Appartement)\)', '', regex=True)

        # TODO: Should be drop the original column 'type'?
        # self.properties.drop(columns=['type'])

        # TODO: Should be drop the properties that have 'Project' as the 'type'?
        # self.properties = self.properties[~self.properties['property type'].str.contains('Project', na=False)]

        print(self.properties.value_counts("property type"))
        print(self.properties.value_counts("property subtype"))

    def export_data_to_csv(self, data_file_path: str):
        self.properties.to_csv(data_file_path, index=False)
