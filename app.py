import streamlit as st
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from streamlit_folium import folium_static
import folium

# Main Streamlit app
st.title("Analyzing Police Officer-Involved Shootings and Schools in Seattle")

# Sidebar Filters
st.sidebar.title("Data Filters")

# Load Data
@st.cache
def load_data():
    police = pd.read_csv('https://raw.githubusercontent.com/aaubs/ds-master/main/data/geopandas_data/SPD_Officer_Involved_Shooting__OIS__Data.csv')
    gdf_ps = gpd.read_file('https://raw.githubusercontent.com/aaubs/ds-master/main/data/Public_Schools.geojson')
    gdf = gpd.read_file('https://raw.githubusercontent.com/aaubs/ds-master/main/data/geopandas_data/Neighborhood_Map_Atlas_Districts.geojson')
    return police, gdf_ps, gdf

police, gdf_ps, gdf = load_data()

# Convert police DataFrame to GeoDataFrame
gdf_police = gpd.GeoDataFrame(police, geometry=gpd.points_from_xy(police['Longitude'], police['Latitude']))
gdf_police.crs = "EPSG:4326"

# Function to display Folium map
def display_folium_map(gdf, title):
    m = folium.Map(location=[47.6062, -122.3321], zoom_start=10)
    for _, row in gdf.iterrows():
        folium.Marker([row['geometry'].y, row['geometry'].x]).add_to(m)
    st.subheader(title)
    folium_static(m)

# Display Maps
show_police = st.sidebar.checkbox("Show Police Shootings", True)
show_schools = st.sidebar.checkbox("Show Schools", True)

if show_police:
    display_folium_map(gdf_police, "Locations of Police Shootings")

if show_schools:
    display_folium_map(gdf_ps, "Locations of Schools")

# Perform Spatial Analysis
perform_analysis = st.sidebar.button("Perform Spatial Analysis")

if perform_analysis:
    # Spatial join of police data with neighborhood data
    joined_police_gdf = gpd.sjoin(gdf_police, gdf, how="left", op="within")
    
    st.subheader("Common Neighborhoods with Police-Involved Shootings")
    st.write(joined_police_gdf.L_HOOD.value_counts())
    
    # Spatial join of police data with public school data
    joined_police_ps = gpd.sjoin(gdf_police, gdf_ps, how='left', op='within')
    
    st.subheader("Types of Schools Close to Police-Involved Shootings")
    st.write(joined_police_ps.TYPE.value_counts())
