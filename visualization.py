import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

matplotlib.use('TkAgg')

def plot_correlations_to_price(df: pd.DataFrame, plot_file_path: str, show_plot: bool) -> None:
    try:
        # Selecting only numeric columns
        numeric_df = df.select_dtypes(include=["int64", "float64"])

        # Calculation of the correlation matrix
        corr_matrix = numeric_df.corr()

        # Extracting correlations with 'price'
        price_corr = corr_matrix["price"].drop("price").sort_values()

        # Plotting the correlations
        plt.figure(figsize=(10, 6))
        sns.barplot(
            x=price_corr.values,
            y=price_corr.index,
            hue=price_corr.index,
            palette="coolwarm",
            dodge=False,
            legend=False
        )
        plt.title("Correlation with the variable 'price'")
        plt.xlabel("Correlation coefficient")
        plt.ylabel("Features")
        plt.tight_layout()

        if plot_file_path:
            # Save correlations plot to file
            plt.savefig(plot_file_path, dpi=300)

        if show_plot:
            # Show correlations plot on screen
            plt.show()      
    except Exception as e:
        print(f"[ERRO] Failed to plot correlations => {e}")

def plot_outliers(df: pd.DataFrame, plot_file_path: str, show_plot: bool) -> None:
    try:
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=["int64", "float64"])

        # Melt the dataframe into long format
        melted = numeric_df.melt(var_name="Feature", value_name="Value")

        # Plotting outliers
        plt.figure(figsize=(14, 8))
        sns.boxplot(x="Feature", y="Value", data=melted)
        plt.xticks(rotation=45)
        plt.title("Outliers in All Numeric Features")
        plt.tight_layout()

        # Save outliers plot to file
        if plot_file_path:
            plt.savefig(plot_file_path, dpi=300)

        if show_plot:
            # Show outliers plot on screen
            plt.show()
    except Exception as e:
        print(f"[ERRO] Failed to plot outliers => {e}")