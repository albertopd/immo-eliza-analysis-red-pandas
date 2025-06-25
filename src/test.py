# Import required libraries
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import pandas as pd
from data_cleanner import DataCleanner  # Custom data loading/cleaning class



# Load and clean the dataset using your custom cleaner
data = DataCleanner("data/data_cleanned.csv")
df = data.load_data_file()

# Filter out unrealistic price and surface entries
df = df[df["price"] > 10000]
df = df[df["habitableSurface"] > 10]  # Remove invalid or extremely small surfaces

# Compute price per square meter
df["price_per_m2"] = df["price"] / df["habitableSurface"]

####################################################################################
# Add a new column 'region' based on Belgian postcode ranges
####################################################################################

def map_postcode_to_region(postcode):
    try:
        pc = int(postcode)
        if 1000 <= pc <= 1299:
            return "Brussels"
        elif (1300 <= pc <= 1499) or (4000 <= pc <= 7999):
            return "Wallonia"
        elif 1500 <= pc <= 3999:
            return "Flanders"
        else:
            return "Unknown"
    except:
        return "Unknown"

# Apply postcode-to-region mapping
df["region"] = df["postCode"].apply(map_postcode_to_region)

# Prepare a summarized DataFrame with key geographic and pricing info
summary_df = df[["locality", "province", "region", "price", "price_per_m2"]].copy()

# Aggregate stats at locality level
agg_df = summary_df.groupby(["region", "province", "locality"]).agg(
    avg_price=("price", "mean"),
    med_price=("price", "median"),
    price_m2=("price_per_m2", "mean"),
    count=("price", "count")
).reset_index()




###########################################################################################################
#           Fonction :Price comparaison by median number of bedrooms                                      #
###########################################################################################################
# Function to plot price metrics by subtype, with avg bedroom as label
def plot_price_by_rooms(df,room):
    # Step 1: Clean and filter data
    df = df[
        (df["subtype"].notna()) &
        (df[room].notna()) & (df[room] >= 0) &
        (df["price"].notna()) & (df["price"] > 10000) & (df["price"] < 1_000_000) &
        (df["habitableSurface"].notna()) & (df["habitableSurface"] > 10)
    ].copy()

    # Step 2: Compute price per square meter
    df["price_per_m2"] = df["price"] / df["habitableSurface"]

    # Step 3: Group by property subtype
    grouped = df.groupby("subtype", as_index=False).agg({
        "price": ["mean", "median"],
        "price_per_m2": "mean",
        room: "median"
    })

    # Step 4: Rename flattened column names
    grouped.columns = ["subtype", "avg_price", "med_price", "price_m2", "median_room"]

    # Step 5: Round results to 2 decimals
    grouped = grouped.round({
        "avg_price": 2,
        "med_price": 2,
        "price_m2": 2,
        "median_room": 1
    })

    # Step 6: Sort by average bedroom count
    grouped = grouped.sort_values("median_room", ascending=True)

    # Step 7: Plotting
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    fig.suptitle(f"Price Metrics by Property Subtype (Labels = Median {room} Count)", fontsize=16)

    # Price metrics and palettes
    metrics = ["avg_price", "med_price", "price_m2"]
    titles = ["Average Price (€)", "Median Price (€)", "Price per m² (€)"]
    palettes = ["Blues_r", "Greens_r", "Oranges_r"]

    for idx, (col, title, palette) in enumerate(zip(metrics, titles, palettes)):
        ax = axes[idx]
        plot = sns.barplot(
            data=grouped, x=col, y="subtype",
            palette=palette, ax=ax
        )
        ax.set_title(title)
        ax.xaxis.set_major_formatter(mtick.StrMethodFormatter("€{x:,.0f}"))
        ax.tick_params(axis='x', rotation=45)

        # Add bedroom labels in front of each bar
        for container, label in zip(plot.containers, grouped["median_room"]):
            for bar in container:
                if bar.get_height() > 0:
                    ax.text(
                        bar.get_x() + bar.get_width(), bar.get_y() + bar.get_height() / 2,
                        f"{label:.1f} br", va="center", ha="left", fontsize=9, color="black"
                    )

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

plot_price_by_rooms(df,'bedroomCount')

plot_price_by_rooms(df,'bathroomCount')
