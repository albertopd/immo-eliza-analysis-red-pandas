import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import matplotlib.patches as mpatches

matplotlib.use('TkAgg')

def generate_surface_charts(df: pd.DataFrame, show_plot: bool):
    plot_surface_histogram(df, "plots/05_histogram_surface.png", show_plot)

    # big value for surface
    plot_big_surface_boxplot(df, min_surface=1000, plot_file_path="plots/06_big_surface_boxplot.png", show_plot=show_plot)

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
        surface_data = surface_data[(surface_data > 0) & (surface_data <= 1000)]  # filtre max 2000 m²

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