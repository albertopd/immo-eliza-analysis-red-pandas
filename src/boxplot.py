# Import required libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from data_cleanner import DataCleanner  # Custom data loading/cleaning class
import matplotlib.ticker as mtick


# Load and clean the dataset using your custom cleaner
data = DataCleanner("data/cleaned_properties.csv")
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

#####################################################################################################
# Visualize Habitable Surface by Property Subtype                                                   #
#####################################################################################################

# Keep only valid surface entries and main property types
df = df[df['habitableSurface'].notna()]
df = df[df['type'].isin(['APARTMENT', 'HOUSE'])]
df = df[df["subtype"].isin([
    'APARTMENT', 'HOUSE', 'FLAT_STUDIO', 'DUPLEX', 'PENTHOUSE', 'GROUND_FLOOR',
    'APARTMENT_BLOCK', 'MANSION', 'EXCEPTIONAL_PROPERTY', 'MIXED_USE_BUILDING',
    'TRIPLEX', 'LOFT', 'VILLA', 'TOWN_HOUSE', 'CHALET', 'MANOR_HOUSE',
    'SERVICE_FLAT', 'KOT', 'FARMHOUSE', 'BUNGALOW', 'COUNTRY_COTTAGE',
    'OTHER_PROPERTY', 'CASTLE', 'PAVILION'
])]

# Boxplot with stripplot overlay for habitable surface per subtype
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, y='subtype', x='habitableSurface', palette='Set2')
sns.stripplot(data=df, y='subtype', x='habitableSurface', color='gray', size=3, jitter=True, alpha=0.4)
plt.title('Habitable Surface Comparison by Property Subtype')
plt.xlabel('Habitable Surface (m²)')
plt.ylabel('Subtype')
plt.grid(True)
plt.tight_layout()
plt.show()

#####################################################################################################
# Define a modular function to compare prices by any categorical variable                          #
#####################################################################################################

def plot_price_comparaison(df_region, title, var):
    # If aggregates not computed yet, calculate them on the fly
    if "avg_price" not in df_region.columns:
        if "price_per_m2" not in df_region.columns and "habitableSurface" in df_region.columns:
            df_region["price_per_m2"] = df_region["price"] / df_region["habitableSurface"]
        df_region = (
            df_region
            .groupby(var, as_index=False)
            .agg(
                avg_price=('price', 'mean'),
                med_price=('price', 'median'),
                price_m2=('price_per_m2', 'mean')
            )
        )

    # Create 3 side-by-side plots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(f"Price Comparison by {title}", fontsize=16)

    # Formatter for 2 decimals
    formatter = mtick.FormatStrFormatter('%.2f')
    # Average price barplot
    avg_bar = sns.barplot(
        data=df_region.nsmallest(15, "avg_price"),
        x="avg_price", y=var,
        palette="Blues_r", ax=axes[0],legend=False
    )
    axes[0].set_title("Average Price (€)")
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].xaxis.set_major_formatter(formatter)  # Format x-axis to 2 decimals
    axes[0].bar_label(avg_bar.containers[0], fmt="€ %.2f", padding=3)
      # --- Barplot: Median Price ---
    med_bar = sns.barplot(
        data=df_region.nsmallest(15, "med_price"),
        x="med_price", y=var,
        palette="Greens_r", ax=axes[1],legend=False
    )
    axes[1].set_title("Median Price (€)")
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].xaxis.set_major_formatter(formatter)
    axes[1].bar_label(med_bar.containers[0], fmt="€ %.2f", padding=3)

    # --- Barplot: Price per m² ---
    m2_bar = sns.barplot(
        data=df_region.nsmallest(15, "price_m2"),
        x="price_m2", y=var,
        palette="Oranges_r", ax=axes[2],legend=False
    )
    axes[2].set_title("Price per m² (€)")
    axes[2].tick_params(axis='x', rotation=45)
    axes[2].bar_label(m2_bar.containers[0], fmt="€ %.2f", padding=3)
    axes[2].xaxis.set_major_formatter(formatter)
    # Final layout adjustments
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

###########################################################################################################
#                       Price comparison by Property Subtype                                             #
###########################################################################################################

# Ensure price is available
df = df[df['price'].notna()]
# Plot price metrics per property subtype
plot_price_comparaison(df, "Property Subtype", "subtype")

###########################################################################################################
#                       Price comparison by Building Condition                                            #
###########################################################################################################

# Filter valid building conditions
df = df[df['buildingCondition'].notna()]
# Plot price metrics per building condition
plot_price_comparaison(df, "Building Condition", "buildingCondition")
###########################################################################################################
#                       Price comparison by Kitchen Type                                                  #
###########################################################################################################

# Filter valid kitchen Type
##TO REDO : fusionner les types de Kitchen et les trier
df = df[df['kitchenType'].notna()]
# Plot price metrics per building condition
plot_price_comparaison(df, "Kitchen Type", "kitchenType")
###########################################################################################################
#                       Price comparison by Heating Type                                                  #
###########################################################################################################

# Filter valid Heating Type
df = df[df['heatingType'].notna()]
# Plot price metrics per building condition
plot_price_comparaison(df, "Heating Type", "heatingType")
###########################################################################################################
#                       Price comparison by Flood Zone Type                                                 #
###########################################################################################################

# Filter valid Heating Type
df = df[df['floodZoneType'].notna()]
# Plot price metrics per building condition
plot_price_comparaison(df, "Flood Zone Type", "floodZoneType")


###########################################################################################################
#                       Price comparison by Bedroom Count (per Subtype)                                  #
###########################################################################################################
####TOO REDO
# Filter only valid entries where bedroomCount is not null
df = df[(df['bedroomCount'].notna()) & (df['bedroomCount'] >= 0)]
df["habitableSurface"] =df[(df["habitableSurface"]< 25000) and(df["habitableSurface"]>10)]
df["price_per_m2"] = df["price"] / df["habitableSurface"]
# Group by subtype to get bedroom stats and price indicators
bedroom_agg = (
    df
    .groupby("subtype", as_index=False)
    .agg(
        avg_price=("price", "mean"),
        med_price=("price", "median"),
        price_m2=("price_per_m2", "mean"),
        median_bedroom=("bedroomCount", "median"),
        count=("bedroomCount", "count")
    )
)

# Sort by average number of bedrooms
bedroom_agg = bedroom_agg.sort_values(by="median_bedroom")

# Plot using existing modular function
plot_price_comparaison(bedroom_agg, "Average Bedroom Count", "median_bedroom")

