import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class DataCleanner:
    REGEX_REMOVE_NON_NUMERIC = re.compile(r'[^0-9]')

    def clean_duplicates(self):
        # remove duplicates, including multiple listings for the same property
        pass

    def clean_errors(self):
        print(self.properties.info())

        # Derop column 'zimmo code'
        self.properties.drop(columns=['zimmo code'], inplace=True)

        # Clean column 'type'
        self.properties['type'] = self.properties['type'].fillna("").str.strip()

        # Drop rows that don't have a 'price'
        self.properties.dropna(subset=['price'], inplace=True)

        # Drop column 'street'
        self.properties.drop(columns=['street'], inplace=True)

        # Drop column 'number'
        self.properties.drop(columns=['number'], inplace=True)

        # Clean column 'postalcode', convert it to Int64 and set value to -1 for undefined data
        self.properties['postcode'] = self.properties['postcode'].str.extract(r"(\d+)").astype("Int64").replace([np.nan, np.inf, -np.inf], -1)

        # TODO: Add column province from the postal codes

        # Clean column 'city'
        self.properties['city'] = self.properties['city'].fillna("").str.strip()

        # Drop rows that don't contain a 'living area(m²)'
        self.properties['living area(m²)'] = self.properties['living area(m²)'].replace([np.nan, np.inf, -np.inf], -1)
        self.properties = self.properties[self.properties['living area(m²)'] != -1]

        # Drop column 'ground area(m²)', not useful to us 
        self.properties.drop(columns=['ground area(m²)'], inplace=True)

        # Clean column 'bedroom' 
        # If there is not value for the bedroom, 
        #   we check 'living area'
        #       if living_area < 40 then assign 1 bedroom
        #       if living_area >= 40 then average(bedrooms)
        #       else: -1
        avg_bedrooms = round(self.properties['bedroom'].mean(skipna=True))
        self.properties['bedroom'] = self.properties.apply(
            lambda row: (
                1 if pd.isna(row['bedroom']) and pd.notna(row['living area(m²)']) and row['living area(m²)'] < 40 
                else avg_bedrooms if pd.isna(row['bedroom']) and pd.notna(row['living area(m²)']) and row['living area(m²)'] >= 40 
                else -1 if pd.isna(row['bedroom']) 
                else row['bedroom']
            ),
            axis=1
        ).astype(int)
        
        # Clean column 'bathroom'
        # If there is not value for the bathroom, 
        #   we check 'living area'
        #       if living_area < 100 then assign 1 bathroom
        #       if living_area >= 100 then average(bathtroom)
        #       else: -1
        avg_bathrooms = round(self.properties['bathroom'].mean(skipna=True))
        self.properties['bathroom'] = self.properties.apply(
            lambda row: (
                1 if pd.isna(row['bathroom']) and pd.notna(row['living area(m²)']) and row['living area(m²)'] < 100 
                else avg_bathrooms if pd.isna(row['bathroom']) and pd.notna(row['living area(m²)']) and row['living area(m²)'] >= 100 
                else -1 if pd.isna(row['bathroom']) 
                else row['bathroom']
            ),
            axis=1
        ).astype(int)

        # Convert column 'garage' and clean it up
        # If undefined then set -1
        # if garage > 0 then we assign 1
        # else assign 0
        self.properties['garage'] = self.properties['garage'].apply(
            lambda x: -1 if pd.isna(x) or x in [np.inf, -np.inf]
            else 1 if x > 0
            else 0
        ).astype(int)

        # Convert column 'garden' to int (1=True, 0=False)
        self.properties['garden'] = self.properties['garden'].fillna(False).astype(int)

        # Convert column 'EPC(kWh/m²)' to int
        # Using a placeholder of -1 for NaN. Useful to signal "unknown" clearly, especially for ML models
        self.properties['EPC(kWh/m²)'] = self.properties['EPC(kWh/m²)'].replace([np.nan, np.inf, -np.inf], -1).astype(int)

        # Convert column 'renovation obligation' to int (1=True, 0=False)
        self.properties['renovation obligation'] = self.properties['renovation obligation'].fillna(-1).astype(int)

        # Convert column 'year built' to int
        # Using a placeholder of -1 for NaN. Useful to signal "unknown" clearly, especially for ML models
        self.properties['year built'] = self.properties['year built'].replace([np.nan, np.inf, -np.inf], -1).astype(int)

        # Clean column 'mobiscore'
        # Using a placeholder of -1 for NaN. Useful to signal "unknown" clearly, especially for ML models
        self.properties['mobiscore'] = self.properties['mobiscore'].replace([np.nan, np.inf, -np.inf], -1)

        # Drop column url, not useful to us 
        self.properties.drop(columns=['url'], inplace=True)

        print(self.properties.info())

    def infer_bedrooms(self, row, avg_bedrooms):
        if pd.isna(row['bedroom']):
            if pd.notna(row['living_area']):
                if row['living_area'] < 40:
                    return 1
                elif row['living_area'] >= 40:
                    return round(avg_bedrooms)
            return -1
        return row['bedroom']

    def clean_empty_cells(self):
        # Drop fully empty rows
        self.properties.dropna(how='all', inplace=True)

        # Drop fully empty columns
        self.properties.dropna(axis=1, how='all', inplace=True)

    def split_column_type(self):
        # Find the position of the "type" column
        type_index = self.properties.columns.get_loc('type')

        # Insert "property type" and "property subtype" right after it
        self.properties.insert(type_index + 1, 'property type', 
            np.select(
                [self.properties['type'].str.contains('Huis', na=False),
                self.properties['type'].str.contains('Appartement', na=False)],
                ['Huis', 'Appartement'],
                default='Project'
            )
        )

        self.properties.insert(type_index + 2, 'property subtype', 
            self.properties['type'].str.replace(r' \((Huis|Appartement)\)', '', regex=True)
        )

        self.properties.drop(columns=['type'], inplace=True)

        # TODO: Should be drop the properties that have 'Project' as the 'type'?
        # self.properties = self.properties[~self.properties['property type'].str.contains('Project', na=False)]

        print(self.properties.value_counts("property type"))
        print(self.properties.value_counts("property subtype"))

    def load_data_from_csv(self, data_file_path: str):
        self.properties = pd.read_csv(data_file_path)

    def export_data_to_csv(self, data_file_path: str):
        self.properties.to_csv(data_file_path, index=False)

    def clean_data(self):
        self.clean_duplicates()
        self.clean_errors()
        self.clean_empty_cells()
        self.split_column_type()