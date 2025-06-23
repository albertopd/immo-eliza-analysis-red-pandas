import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

matplotlib.use('TkAgg')

def plot_correlations_to_price(df: pd.DataFrame) -> None:
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

    # Save correlations plot to file
    plt.savefig("plots/correlation_with_variable_price.png", dpi=300)

    # Show correlations plot
    plt.show()

def plot_outliers(df: pd.DataFrame) -> None:
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
    plt.savefig("plots/all_features_outliers.png", dpi=300)

    # Show correlations plot
    plt.show()