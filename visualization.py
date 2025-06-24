import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import matplotlib.patches as mpatches

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
            print(f"Correlation with the variable 'price' plot saved to file: {plot_file_path}")

        if show_plot:
            # Show correlations plot on screen
            print(f"Showing plot for correlation with the variable 'price'...")
            plt.show()

    except Exception as e:
        print(f"[ERRO] Failed to plot correlations with the the variable 'price' => {e}")

def plot_outliers(df: pd.DataFrame, plot_file_path: str, show_plot: bool) -> None:
    try:
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=["int64", "float64"])

        # Detect columns with outliers using the IQR method
        def outlier_count(series):
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            return ((series < lower) | (series > upper)).sum()

        # Create a dictionary with outlier counts
        outlier_counts = {col: outlier_count(numeric_df[col]) for col in numeric_df.columns}
        print(outlier_count)
        columns_with_outliers = {col: count for col, count in outlier_counts.items() if count > 0}
        print(columns_with_outliers)

        # Filter DataFrame
        filtered_df = numeric_df[list(columns_with_outliers.keys())]

        # Melt the dataframe into long format
        melted = filtered_df.melt(var_name="Feature", value_name="Value")

        # Sort features by number of outliers for better readability
        sorted_features = sorted(columns_with_outliers.items(), key=lambda x: x[1], reverse=True)
        feature_order = [feat for feat, _ in sorted_features]

        # Plot
        plt.figure(figsize=(16, 10))
        ax = sns.boxplot(
            x="Value",
            y="Feature",
            data=melted,
            order=feature_order,
            palette="coolwarm",
            showfliers=True
        )

        # Annotate outlier counts clearly to the right
        x_min, x_max = ax.get_xlim()
        x_range = x_max - x_min
        offset = x_range * 0.06  # 6% to the right

        for i, feature in enumerate(feature_order):
            count = columns_with_outliers[feature]
            x_pos = melted[melted["Feature"] == feature]["Value"].quantile(0.97)
            
            color = "lightcoral" if count > 1000 else "green"
            
            ax.text(
                x_pos + offset, i, f"{count}",
                va='center', ha='left', fontsize=9, fontweight='bold', color=color
            )

        # Titles and labels
        plt.title("Outliers in Numeric Features", fontsize=14, fontweight='bold')
        plt.xlabel("Feature Value (various units)", fontsize=12)
        plt.ylabel("Feature Name", fontsize=12)

        # Legend
        normal_patch = mpatches.Patch(color='green', label='Normal outlier count (<= 1000)')
        extreme_patch = mpatches.Patch(color='lightcoral', label='Extreme outlier count (> 1000)')
        plt.legend(handles=[normal_patch, extreme_patch], title='Legend', loc='lower right')
    
        plt.tight_layout()

        if plot_file_path:
            # Save outliers plot to file
            plt.savefig(plot_file_path, dpi=150)
            print(f"Outliers plot saved to file: {plot_file_path}")

        if show_plot:
            # Show outliers plot on screen
            print(f"Showing plot for outliers...")
            plt.show()

    except Exception as e:
        print(f"[ERRO] Failed to plot outliers => {e}")

def plot_count_features_correlations(df: pd.DataFrame, plot_file_path: str, show_plot: bool) -> None:
    try:
        # Define count-related columns
        count_columns = [
            "bathroomCount",
            "bedroomCount",
            "facedeCount",
            "floorCount",
            "parkingCountIndoor",
            "parkingCountOutdoor",
            "roomCount",
            "toiletCount"
        ]

        # Subset the DataFrame
        count_df = df[count_columns]

        # Compute the correlation matrix
        corr_matrix = count_df.corr()

        # Set up the plot
        plt.figure(figsize=(10, 8))
        heatmap = sns.heatmap(
            corr_matrix,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            square=True,
            cbar_kws={"label": "Pearson Correlation Coefficient"}
        )

        # Title and labels
        plt.title("Correlation Between Count-Based Features", fontsize=14, fontweight="bold", pad=12)
        plt.xlabel("Features (unit: count)", fontsize=12)
        plt.ylabel("Features (unit: count)", fontsize=12)

        # Improve layout and prevent text overlapping
        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)
        plt.tight_layout()

        if plot_file_path:
            # Save outliers plot to file
            plt.savefig(plot_file_path, dpi=300)
            print(f"Count Features Correlations plot saved to file: {plot_file_path}")

        if show_plot:
            # Show outliers plot on screen
            print(f"Showing plot for Count Features Correlations...")
            plt.show()

    except Exception as e:
        print(f"[ERRO] Failed to plot Count Features Correlations => {e}")

def plot_missing_values_percentage(df: pd.DataFrame, plot_file_path: str, show_plot: bool) -> None:
    try:
        # Calculate missing data information
        missing_data = df.isna().sum()
        missing_pct = (missing_data / len(df)) * 100

        # Filter to features with missing values
        missing_df = missing_pct[missing_pct > 0].sort_values(ascending=False)

        # Set up the plot
        plt.figure(figsize=(12, 8))
        bars = plt.barh(missing_df.index, missing_df.values, color=plt.cm.tab20.colors[:len(missing_df)])

        # Axis Labels and Title (with units)
        plt.xlabel("Missing Percentage (%)", fontsize=12)
        plt.ylabel("Feature", fontsize=12)
        plt.title("Missing Values Percentage per Feature", fontsize=14, fontweight="bold", pad=15)

        # Add text annotations to the end of each bar (no overlapping if sorted properly)
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 1,                    # small horizontal offset to the right
                    bar.get_y() + bar.get_height()/2,
                    f"{width:.1f}%", 
                    va='center', fontsize=10, fontweight="bold")

        # Invert y-axis so that features with highest missing % appear at the top
        plt.gca().invert_yaxis()

        plt.tight_layout()

        if plot_file_path:
            # Save outliers plot to file
            plt.savefig(plot_file_path, dpi=300)
            print(f"Missing Values Percentage plot saved to file: {plot_file_path}")

        if show_plot:
            # Show outliers plot on screen
            print(f"Showing plot for Missing Values Percentage...")
            plt.show()

    except Exception as e:
        print(f"[ERRO] Failed to plot Missing Values Percentage => {e}")


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