# Import required libraries
import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium import Map
from streamlit_folium import folium_static
from shapely.geometry import Point

# Function to display map
def display_map(df):
    m = Map(location=[47.6062, -122.3321], zoom_start=10)
    for _, row in df.iterrows():
        folium.Marker(location=[row['Latitude'], row['Longitude']]).add_to(m)
    folium_static(m)

# Main app
st.title("Analyzing Police Officer-Involved Shootings and Schools in Seattle")

# Sidebar
st.sidebar.title("Data Filters")

# Load data
@st.cache
def load_data():
    police = pd.read_csv('https://raw.githubusercontent.com/aaubs/ds-master/main/data/geopandas_data/SPD_Officer_Involved_Shooting__OIS__Data.csv')
    gdf_ps = gpd.read_file('https://raw.githubusercontent.com/aaubs/ds-master/main/data/Public_Schools.geojson')
    gdf = gpd.read_file('https://raw.githubusercontent.com/aaubs/ds-master/main/data/geopandas_data/Neighborhood_Map_Atlas_Districts.geojson')
    return police, gdf_ps, gdf

police, gdf_ps, gdf = load_data()

# Convert the police DataFrame to GeoDataFrame
gdf_police = gpd.GeoDataFrame(police, geometry=gpd.points_from_xy(police['Longitude'], police['Latitude']))
gdf_police.crs = "EPSG:4326"

# Sidebar controls
show_police = st.sidebar.checkbox('Show Police Shootings', True)
show_schools = st.sidebar.checkbox('Show Schools', True)

# Displaying data on the map
if show_police:
    st.subheader("Locations of Police Shootings")
    display_map(police)
if show_schools:
    st.subheader("Locations of Schools")
    display_map(gdf_ps)

# More code to answer the questions can go here ...
