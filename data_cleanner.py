import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

class DataCleanner:

    def __init__(self, data_file_path: str) -> None:
        """Initialize the DataCleaner with the path to the CSV file."""
        self.data_file_path = data_file_path

    def clean_duplicates(self):
        """
        Removes duplicates based on physical property attributes.
        Merges multiple listings of the same property into one, enriching data.
        """
        # Step 1: Load the data file
        if os.path.exists(self.data_file_path) and os.path.getsize(self.data_file_path) > 0:
            try:
                df = pd.read_csv(self.data_file_path)
                if df.empty:
                    print(f"[WARNING] File exists but is empty: {self.data_file_path}")
                    return pd.DataFrame()
                print(f"[INFO] Loaded {self.data_file_path} ({len(df)} rows)")
            except Exception as e:
                print(f"[ERROR] Failed to read {self.data_file_path}: {e}")
                return pd.DataFrame()
        else:
            print(f"[WARNING] File is missing or empty: {self.data_file_path}")
            return pd.DataFrame()

        # Step 2: Define location identifier for merging
        if all(col in df.columns for col in ["street", "number", "postcode", "city"]):
            df["location"] = (
                                df["street"].fillna("").astype(str).str.strip() +
                                df["number"].fillna("").astype(str).str.strip() +
                                df["postcode"].fillna("").astype(str).str.strip() +
                                df["city"].fillna("").astype(str).str.strip()
                            )
        else:
            print("[ERROR] Required columns are missing (street, postcode, number,city)")
            return pd.DataFrame()

        
       
          # Step 3: Group by physical identifiers and merge rows
        group_cols=["type","price","location","bedroom"]
        merged_rows = []
        grouped = df.groupby(group_cols)

        for _, group in grouped:
            # Base record is the one with highest price (or most complete)
            selected = group.sort_values("price", ascending=False).iloc[0].to_dict()

            for col in df.columns:
                if pd.isna(selected.get(col)):
                    for val in group[col]:
                        if pd.notna(val):
                            selected[col] = val
                            break

            selected["Previous URLs"] = "; ".join(group["url"].dropna().unique())
            selected["Merged_from_n_entries"] = len(group)
            merged_rows.append(selected)

        return pd.DataFrame(merged_rows)

    def clean_errors(self):
        # clean data value
        # clean data types
        # changing False/True to 0/1
        # clean extra spaces/tabulations inside values
        pass

    def clean_empty_cells(self):
        # remove empty lines
        # remove empty columns
        # what to do with empty cells?https://github.com/albertopd/immo-eliza-analysis-red-pandas
        pass
    
    def send_output_file(self, output_file: str):
            """
            Exports the cleaned and deduplicated DataFrame to a new CSV file.
            """
            cleaned_df = self.clean_duplicates()
            if not cleaned_df.empty:
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                cleaned_df.to_csv(output_file, index=False)
                print(f"[SUCCESS] Exported {len(cleaned_df)} merged records → {output_file}")
            else:
                print("[WARNING] No data exported due to empty or invalid input.")