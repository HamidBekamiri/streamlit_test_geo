import streamlit as st
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

@st.cache
def load_data():
    police = pd.read_csv('https://raw.githubusercontent.com/aaubs/ds-master/main/data/geopandas_data/SPD_Officer_Involved_Shooting__OIS__Data.csv')
    gdf_ps = gpd.read_file('https://raw.githubusercontent.com/aaubs/ds-master/main/data/Public_Schools.geojson')
    gdf = gpd.read_file('https://raw.githubusercontent.com/aaubs/ds-master/main/data/geopandas_data/Neighborhood_Map_Atlas_Districts.geojson')
    gdf_police = gpd.GeoDataFrame(police, geometry=gpd.points_from_xy(police['Longitude'], police['Latitude']))
    gdf_police.crs = "EPSG:4326"
    return police, gdf_ps, gdf, gdf_police

st.title("Analyzing Police-Involved Shootings and Schools in Seattle")

# Load the data
police, gdf_ps, gdf, gdf_police = load_data()

# Sidebar
st.sidebar.title("Options")
perform_analysis = st.sidebar.checkbox("Perform Analysis")

if perform_analysis:

    # 1. Common neighborhoods where most police-involved shootings happen
    st.subheader("Common Neighborhoods with Police-Involved Shootings")
    joined_police_gdf = gpd.sjoin(gdf_police, gdf, how="left", predicate="within")  # Updated predicate parameter
    most_common_neighborhoods = joined_police_gdf['L_HOOD'].value_counts()
    st.write(most_common_neighborhoods)

    # 2. Neighborhoods without any police-involved shootings
    st.subheader("Neighborhoods without Police-Involved Shootings")
    neighborhoods_no_incidents = gdf[~gdf['L_HOOD'].isin(joined_police_gdf['L_HOOD'].unique().tolist())]
    st.write(neighborhoods_no_incidents)

    # 3. Schools close to locations where police-involved shootings occurred
    st.subheader("Schools Close to Police-Involved Shootings")
    joined_police_ps = gpd.sjoin_nearest(gdf_police, gdf_ps, how='left', distance=0.09)
    schools_close_to_shootings = joined_police_ps['NAME'].value_counts()
    schools_close_to_shootings = joined_police_ps['NAME'].value_counts()
    st.write(schools_close_to_shootings)

    # 4. Types of schools most commonly close to police-involved shootings
    st.subheader("Types of Schools Close to Police-Involved Shootings")
    types_of_schools = joined_police_ps['TYPE'].value_counts()
    st.write(types_of_schools)

    # 5. Schools that have not had any police-involved shootings
    st.subheader("Schools without Police-Involved Shootings")
    schools_no_shootings = gdf_ps[~gdf_ps['NAME'].isin(joined_police_ps['NAME'].unique().tolist())]
    st.write(schools_no_shootings)

    # 6. School with the most police-involved shootings
    st.subheader("School with the Most Police-Involved Shootings")
    if not joined_police_ps['NAME'].empty:
        most_affected_school = joined_police_ps['NAME'].value_counts().idxmax()
        st.write(most_affected_school)
    else:
        st.write("No schools are close to locations where police-involved shootings have occurred.")
