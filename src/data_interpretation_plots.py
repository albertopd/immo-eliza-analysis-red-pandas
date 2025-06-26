import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import matplotlib.patches as mpatches

matplotlib.use('TkAgg')



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
        plt.title("Distribution of the number of properties according to the surface area")
        plt.xlabel("habitableSurface (m²)")
        plt.ylabel("Number of properties ")
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


def plot_top_localities(stats: pd.DataFrame, title: str, plot_file_path: str, show_plot: bool):
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

    if show_plot:
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
        plt.title(f"Price distribution for properties with surface area > {min_surface} m²")
        plt.ylabel("Price (€)")
        plt.tight_layout()

        # Enregistrement du graphique
        if plot_file_path:
            plt.savefig(plot_file_path, dpi=300)

        if show_plot:
            plt.show()

    except Exception as e:
        print(f"[ERRO] Failed to plot big surface boxplot => {e}")

def data_interpretation_plots(df: pd.DataFrame, show_plot: bool):
    plot_surface_histogram(df, "plots/05_histogram_surface.png", show_plot)

    # Appliquer le mapping des régions
    df = assign_region(df)

    # Belgique
    top_be = get_top_localities(df)
    plot_top_localities(top_be, "Top 10 Most Expensive Localities in Belgium", "plots/06_top_expensive_belgium.png", show_plot)

    # Wallonie
    top_wal = get_top_localities(df, region_filter="Wallonie")
    plot_top_localities(top_wal, "Top 10 Most Expensive Localities in Wallonia", "plots/07_top_expensive_wallonia.png", show_plot)

    # Flandre
    top_vla = get_top_localities(df, region_filter="Flandre")
    plot_top_localities(top_vla, "Top 10 Most Expensive Localities in Flanders", "plots/08_top_expensive_flander.png", show_plot)

    # Bruxelles
    top_bru = get_top_localities(df, region_filter="Bruxelles")
    plot_top_localities(top_bru, "Top 10 Most Expensive Localities in Brussels", "plots/09_top_expensive_bruxelles.png", show_plot)

    # big value for surface
    plot_big_surface_boxplot(df, min_surface=1000, plot_file_path="plots/10_big_surface_boxplot.png", show_plot=show_plot)

df = pd.read_csv("data/data_cleanned.csv")
data_interpretation_plots(df, show_plot=True)