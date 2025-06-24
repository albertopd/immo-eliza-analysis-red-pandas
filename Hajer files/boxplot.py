
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from data_cleanner import DataCleanner


data = DataCleanner("data/cleaned_properties.csv")
# Load the cleaned dataset
df = data.load_data_file()
#####################################################################################################
#               Habitable Surface Comparison by Property Type                                       #
#####################################################################################################

# Filter valid data
df = df[df['habitableSurface'].notna()]
df = df[df['type'].isin(['APARTMENT', 'HOUSE'])]
df = df[df["subtype"].isin([
    'APARTMENT', 'HOUSE', 'FLAT_STUDIO', 'DUPLEX', 'PENTHOUSE', 'GROUND_FLOOR',
    'APARTMENT_BLOCK', 'MANSION', 'EXCEPTIONAL_PROPERTY', 'MIXED_USE_BUILDING',
    'TRIPLEX', 'LOFT', 'VILLA', 'TOWN_HOUSE', 'CHALET', 'MANOR_HOUSE',
    'SERVICE_FLAT', 'KOT', 'FARMHOUSE', 'BUNGALOW', 'COUNTRY_COTTAGE',
    'OTHER_PROPERTY', 'CASTLE', 'PAVILION'
])]

# Plot
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, y='subtype', x='habitableSurface', palette='Set2')
sns.stripplot(data=df, y='subtype', x='habitableSurface', color='gray', size=3, jitter=True, alpha=0.4)

plt.title('Habitable Surface Comparison by Property Type')
plt.xlabel('Property Type')
plt.ylabel('Habitable Surface (m²)')
plt.grid(True)
plt.tight_layout()
plt.show()

###########################################################################################################
#                       Price comparison by Property Type                                                 #
###########################################################################################################

df = df[df['price'].notna()]
# Plot
plt.figure(figsize=(10, 6))
sns.barplot(data=df, y='subtype', x='price', palette='Set2')
sns.stripplot(data=df, y='subtype', x='price', color='gray', size=3, jitter=True, alpha=0.4)

plt.title('Price Comparison by Property Type')
plt.xlabel('Property Type')
plt.ylabel('Price')
plt.grid(True)
plt.tight_layout()
plt.show()
###########################################################################################################
#                       Price comparison by Building Condition                                               #
###########################################################################################################
df = df[df['buildingCondition'].notna()]
# Plot
plt.figure(figsize=(10, 6))
sns.barplot(data=df, y='buildingCondition', x='price', palette='Set2')
sns.stripplot(data=df, y='buildingCondition', x='price', color='gray', size=3, jitter=True, alpha=0.4)

plt.title('Price Comparison by Building Condition')
plt.ylabel('Building Condition')
plt.xlabel('Price')
plt.grid(True)
plt.tight_layout()
plt.show()