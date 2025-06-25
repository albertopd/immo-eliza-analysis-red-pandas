import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.data_cleanner import DataCleanner
from dash import Dash, dcc, html, Input, Output


data = DataCleanner("data/cleaned_properties.csv")
# Load the cleaned dataset
df = data.load_data_file()

# Ensure necessary fields are clean and usable
df = df[df["price"] > 10000]
df = df[df["habitableSurface"] > 10]  # remove abnormal entries to have valid surface data only
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
##########################################################################################
# Region Maps: Create region-level choropleth map using public GeoJSON of Belgium regions#                                                   #
##########################################################################################

region_avg = df.groupby("region").agg(avg_price=("price", "mean")).reset_index()
fig_region = px.choropleth(
    region_avg,
    geojson="https://raw.githubusercontent.com/napoleon03/be-geojson/main/belgium_regions.geojson",
    featureidkey="properties.name",  # GeoJSON property key to match with 'region'
    locations="region",
    color="avg_price",
    color_continuous_scale="Blues",
    title="💶 Average Property Price by Region"
)
fig_region.update_geos(fitbounds="locations", visible=False)
########################################################################################
#                         Call back on click with dash                                 #
########################################################################################


# Initialize Dash application
app = Dash(__name__)

# Layout with region map and a placeholder for bar chart by province
app.layout = html.Div([
    html.H2("Belgium Real Estate - Regional Price Explorer"),
    dcc.Graph(id="map", figure=fig_region),  # Region-level map
    dcc.Graph(id="province-bar")             # Dynamic bar chart of provinces
])

# Callback to update province bar chart when a region is clicked
@app.callback(
    Output("province-bar", "figure"),
    Input("map", "clickData")
)
def update_province_chart(clickData):
    # Default: empty chart
    if not clickData:
        return px.bar(title="Click on a region to view province prices")

    # Extract selected region from clicked map data
    region = clickData["points"][0]["location"]

    # Filter data for selected region and compute average price per province
    province_avg = df[df["region"] == region].groupby("province").agg(avg_price=("price", "mean")).reset_index()

    # Create bar chart
    fig = px.bar(
        province_avg,
        x="avg_price",
        y="province",
        orientation="h",
        title=f"Average Property Price by Province in {region}",
        color="avg_price",
        color_continuous_scale="Viridis"
    )
    return fig

# Run the Dash web server
if __name__ == "__main__":
    app.run_server(debug=True)
