import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.data_cleanner import DataCleanner



def plot_top_expensive(df_region, title_prefix):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(f"{title_prefix} - Most Expensive Municipalities -", fontsize=16)

    # --- Average Price ---
    top_avg = df_region.nlargest(10, "avg_price")
    sns.barplot(
        data=top_avg,
        y="locality", x="avg_price",
        palette="Blues", ax=axes[0]
    )
    axes[0].set_title("Average Price (€)")
    for i, row in top_avg.iterrows():
        axes[0].text(row["avg_price"], i, f"{int(row['avg_price']):,}€", va='center', ha='left', fontsize=9)

    # --- Median Price ---
    top_median = df_region.nlargest(10, "med_price")
    sns.barplot(
        data=top_median,
        y="locality", x="med_price",
        palette="Greens", ax=axes[1]
    )
    axes[1].set_title("Median Price (€)")
    for i, row in top_median.iterrows():
        axes[1].text(row["med_price"], i, f"{int(row['med_price']):,}€", va='center', ha='left', fontsize=9)

    # --- Price per m² ---
    top_m2 = df_region.nlargest(10, "price_m2")
    sns.barplot(
        data=top_m2,
        y="locality", x="price_m2",
        palette="Oranges", ax=axes[2]
    )
    axes[2].set_title("Price per m² (€)")
    for i, row in top_m2.iterrows():
        axes[2].text(row["price_m2"], i, f"{int(row['price_m2']):,}€/m²", va='center', ha='left', fontsize=9)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
