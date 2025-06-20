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

    def clean_empty_cells(self):
        # remove empty lines
        # remove empty columns
        # what to do with empty cells?
        pass