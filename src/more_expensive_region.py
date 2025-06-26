import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from data_cleanner import DataCleanner


data = DataCleanner("data/data_cleanned.csv")
# Load the cleaned dataset
df = data.load_data_file()

# Ensure necessary fields are clean and usable
df = df[
    (df["habitableSurface"].notna()) &
    (df["habitableSurface"] > 10) &
    (df["habitableSurface"] < 25000) &
    (df["price"] > 10000) &
    (df["price"] < 800000)
]  # remove abnormal entries to have valid surface data only
df["price_per_m2"] = df["price"] / df["habitableSurface"]

####################################################################################
# Official Region Mapping by Postcode (Belgium)                                    #
#| Region   | Postcode Range        |                                              #
#| -------- | --------------------- |                                              #
#| Brussels | 1000–1299             |                                              #
#| Flanders | 1500–3999             |                                              #
#| Wallonia | 1300–1499 & 4000–7999 |                                              #
#                                                                                  #
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

# Apply mapping
df["region"] = df["postCode"].apply(map_postcode_to_region)   

# Select relevant columns                                                          
summary_df = df[["locality", "province","region", "price", "price_per_m2"]].copy()   
# Compute stats per locality
agg_df = summary_df.groupby(["region", "province","locality"]).agg(
    avg_price=("price", "mean"),
    med_price=("price", "median"),
    price_m2=("price_per_m2", "mean"),
    count=("price", "count")
).reset_index()


# Function to plot by region
def plot_top_cheapest(df_region, title_prefix):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(f" {title_prefix} - Top 10 Most Expensive Municipalities -", fontsize=16)

    # Average Price
    sns.barplot(
        data=df_region.nlargest(10, "avg_price"), 
        x="avg_price", y="locality",
        palette="Blues_r", ax=axes[0]
    )
    axes[0].set_title("Average Price (€)")

    # Median Price
    sns.barplot(
        data=df_region.nlargest(10, "med_price"),
        x="med_price", y="locality",
        palette="Greens_r", ax=axes[1]
    )
    axes[1].set_title("Median Price (€)")

    # Price per m²
    sns.barplot(
        data=df_region.nlargest(10, "price_m2"),
        x="price_m2", y="locality",
        palette="Oranges_r", ax=axes[2]
    )
    axes[2].set_title("Price per m² (€)")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

# Filter per region
belgium_df = agg_df.copy()
brussels_df= agg_df[agg_df["region"] == "Brussels"]
wallonia_df = agg_df[agg_df["region"] == "Wallonia"]
flanders_df = agg_df[agg_df["region"] == "Flanders"]

# Plot each
plot_top_cheapest(belgium_df, "Belgium")
plot_top_cheapest(brussels_df, "Brussels")
plot_top_cheapest(wallonia_df, "Wallonia")
plot_top_cheapest(flanders_df, "Flanders")