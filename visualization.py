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


def plot_surface_histogram(df: pd.DataFrame, plot_file_path: str, show_plot: bool) -> None:
    """
    Create a histogram of the number of properties according to their surface.

    Args:
        df (pd.DataFrame): The dataset containing property data.
        plot_file_path (str): If provided, saves the plot to this file path.
        show_plot (bool): Whether to display the plot on screen.
    """
    try:
        # Vérification de la présence de la colonne 'surface'
        if "habitableSurface" not in df.columns:
            raise ValueError("Column 'habitableSurface' not found in DataFrame.")

        # Suppression des valeurs manquantes ou aberrantes
        surface_data = df["habitableSurface"].dropna()
        surface_data = surface_data[(surface_data > 0) & (surface_data <= 2000)]  # filtre max 2000 m²

        # Création de l'histogramme
        plt.figure(figsize=(10, 6))
        sns.histplot(surface_data, bins=30, kde=False, color="skyblue", edgecolor="black")
        plt.title("Distribution du nombre de propriétés selon la surface")
        plt.xlabel("habitableSurface (m²)")
        plt.ylabel("Nombre de propriétés")
        plt.tight_layout()

        if plot_file_path:
            # Sauvegarde de l'histogramme
            plt.savefig(plot_file_path, dpi=300)

        if show_plot:
            # Affichage de l'histogramme
            plt.show()
            
    except Exception as e:
        print(f"[ERRO] Failed to plot surface histogram => {e}")


# Mapping des provinces vers régions
PROVINCE_TO_REGION = {
    "Antwerpen": "Flandre",
    "Limburg": "Flandre",
    "Oost-Vlaanderen": "Flandre",
    "West-Vlaanderen": "Flandre",
    "Vlaams-Brabant": "Flandre",
    "Hainaut": "Wallonie",
    "Liège": "Wallonie",
    "Luxembourg": "Wallonie",
    "Namur": "Wallonie",
    "Brabant wallon": "Wallonie",
    "Brussels": "Bruxelles"
}

def assign_region(df: pd.DataFrame) -> pd.DataFrame:
    df["region"] = df["province"].map(PROVINCE_TO_REGION)
    return df

def get_top_localities(df: pd.DataFrame, region_filter: str = None, top_n: int = 10) -> pd.DataFrame:
    # On filtre la région si demandée
    if region_filter:
        df = df[df["region"] == region_filter]

    # Nettoyage
    df = df.dropna(subset=["locality", "price", "habitableSurface"])
    df = df[df["habitableSurface"] > 0]

    # Calcul des stats
    grouped = df.groupby("locality").agg(
        average_price=("price", "mean"),
        median_price=("price", "median"),
        price_per_m2=("price", lambda x: x.sum() / df.loc[x.index, "habitableSurface"].sum())
    )
    return grouped.sort_values("average_price", ascending=False).head(top_n)


def plot_top_localities(stats: pd.DataFrame, title: str, plot_file_path: str = None):
    plt.figure(figsize=(12, 6))
    stats_sorted = stats.sort_values("average_price")
    
    ax = sns.barplot(x=stats_sorted["average_price"], y=stats_sorted.index, palette="crest")

    # Ajout d'annotations (mean, median, price/m²)
    for i, (idx, row) in enumerate(stats_sorted.iterrows()):
        label = (
            f"Mean: {row['average_price']:.0f} €\n"
            f"Median: {row['median_price']:.0f} €\n"
            f"{row['price_per_m2']:.0f} €/m²"
        )
        ax.text(row["average_price"], i, label, va="center", ha="left", fontsize=9, color="black")

    plt.xlabel("Average Price (€)")
    plt.title(title)
    plt.tight_layout()

    if plot_file_path:
        plt.savefig(plot_file_path, dpi=300)

    plt.show()


def plot_big_surface_boxplot(df: pd.DataFrame, surface_col="habitableSurface", price_col="price",
                             min_surface: int = 1000, plot_file_path: str = None, show_plot: bool = True) -> None:
    """
    Plot a boxplot of properties with very large surface area (default > 1000 m²), showing price distribution.
    """
    try:
        # Vérification des colonnes
        if surface_col not in df.columns or price_col not in df.columns:
            raise ValueError(f"Columns '{surface_col}' or '{price_col}' not found in DataFrame.")

        # Filtrage des données
        filtered_df = df[(df[surface_col] > min_surface) & (df[price_col].notna())]

        if filtered_df.empty:
            print(f"[INFO] No properties found with surface > {min_surface} m².")
            return

        # Création du boxplot
        plt.figure(figsize=(8, 6))
        sns.boxplot(y=filtered_df[price_col], color="tomato")
        plt.title(f"Distribution des prix pour les propriétés avec surface > {min_surface} m²")
        plt.ylabel("Prix (€)")
        plt.tight_layout()

        # Enregistrement du graphique
        if plot_file_path:
            plt.savefig(plot_file_path, dpi=300)

        if show_plot:
            plt.show()

    except Exception as e:
        print(f"[ERRO] Failed to plot big surface boxplot => {e}")