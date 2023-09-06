# Import necessary modules
import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Streamlit setup
st.title("Analyzing Public Schools in Seattle Neighborhoods")

# Fetch Data
@st.cache
def load_data():
    gdf = gpd.read_file('https://raw.githubusercontent.com/aaubs/ds-master/main/data/Neighborhood_Map_Atlas_Districts.geojson')
    gdf_ps = gpd.read_file('https://raw.githubusercontent.com/aaubs/ds-master/main/data/Public_Schools.geojson')
    return gdf, gdf_ps

gdf, gdf_ps = load_data()

# Convert GeoDataFrame to DataFrame for Streamlit map
gdf['lon'] = gdf.geometry.centroid.x
gdf['lat'] = gdf.geometry.centroid.y
st.write("Seattle Neighborhoods")
st.map(gdf[['lat', 'lon']])

# Display a map
st.write("Seattle Neighborhoods")
st.map(gdf)

# Question 1: Number of Schools in Each Neighborhood
st.write("## Number of Schools in Each Neighborhood")
school_count = []
for neighborhood in gdf['geometry']:
    schools = gdf_ps[gdf_ps.geometry.within(neighborhood)]
    school_count.append(len(schools))

gdf['school_count'] = school_count
st.table(gdf[['L_HOOD','school_count']])

# Question 2: Average Distance from Downtown
st.write("## Average Distance of Schools from Downtown")

# Get Downtown centroid
downtown = gdf[gdf['L_HOOD']=='Downtown']['geometry'].centroid.iloc[0]

avg_distance = []
for neighborhood in gdf['geometry']:
    schools = gdf_ps[gdf_ps.geometry.within(neighborhood)]
    if len(schools) == 0:
        avg_distance.append(None)
    else:
        distances = schools['geometry'].distance(downtown)
        avg_distance.append(distances.mean())

gdf['avg_dist_downtown'] = avg_distance
st.table(gdf[['L_HOOD', 'avg_dist_downtown']])

# Question 3: Neighborhood with Largest Area but Fewest Schools
st.write("## Neighborhood with Largest Area but Fewest Schools")

gdf['area'] = gdf.geometry.area
gdf_filtered = gdf[gdf['school_count'] > 0]
largest_area_fewest_schools = gdf_filtered.loc[gdf_filtered['area'].idxmax()]
st.write("The neighborhood with the largest area but the fewest schools is:", largest_area_fewest_schools['L_HOOD'])

# Show some plots
fig, ax = plt.subplots()
gdf.boundary.plot(ax=ax)
gdf_ps.plot(ax=ax, color='red', markersize=10)
st.write("## Map of Schools in Neighborhoods")
st.pyplot(fig)
