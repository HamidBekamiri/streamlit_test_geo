import streamlit as st
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# Load Data
@st.cache(allow_output_mutation=True)
def load_data():
    police = pd.read_csv('https://raw.githubusercontent.com/aaubs/ds-master/main/data/geopandas_data/SPD_Officer_Involved_Shooting__OIS__Data.csv')
    gdf_police = gpd.GeoDataFrame(police, geometry=gpd.points_from_xy(police['Longitude'], police['Latitude']))
    gdf_ps = gpd.read_file('https://raw.githubusercontent.com/aaubs/ds-master/main/data/Public_Schools.geojson')
    gdf = gpd.read_file('https://raw.githubusercontent.com/aaubs/ds-master/main/data/geopandas_data/Neighborhood_Map_Atlas_Districts.geojson')
    return gdf_police, gdf_ps, gdf

st.title("Analyzing Police-Involved Shootings and Schools in Seattle")

# Load the data
gdf_police, gdf_ps, gdf = load_data()

# Sidebar
st.sidebar.title("Options")
perform_analysis = st.sidebar.checkbox("Perform Analysis")

questions = [
    "What are the common neighborhoods where most police-involved shootings happen?",
    "Are there any neighborhoods without any police-involved shootings?",
    "Are there any schools close to locations where police-involved shootings have occurred?",
    "What types of schools (Elementary, High School, etc.) are most commonly close to police-involved shootings?",
    "Are there any schools that have not had any police-involved shootings?",
    "Which school has had the most police-involved shootings?"
]

selected_questions = st.sidebar.multiselect("Select Questions to Answer:", questions)

if perform_analysis:
    joined_police_gdf = gpd.sjoin(gdf_police, gdf, how="left", op="within")
    joined_police_ps = gdf_police.sjoin_nearest(gdf_ps, how='left')

    if "What are the common neighborhoods where most police-involved shootings happen?" in selected_questions:
        st.subheader("1. Common Neighborhoods with Police-Involved Shootings")
        most_common_neighborhoods = joined_police_gdf['L_HOOD'].value_counts()
        st.write(most_common_neighborhoods)

    if "Are there any neighborhoods without any police-involved shootings?" in selected_questions:
        st.subheader("2. Neighborhoods without Police-Involved Shootings")
        neighborhoods_no_incidents = gdf[~gdf.L_HOOD.isin(joined_police_gdf.L_HOOD.unique().tolist())]['L_HOOD']
        st.write(neighborhoods_no_incidents)

    if "Are there any schools close to locations where police-involved shootings have occurred?" in selected_questions:
        st.subheader("3. Schools Close to Police-Involved Shootings")
        schools_close_to_shootings = joined_police_ps['NAME'].value_counts()
        st.write(schools_close_to_shootings)

    if "What types of schools (Elementary, High School, etc.) are most commonly close to police-involved shootings?" in selected_questions:
        st.subheader("4. Types of Schools Close to Police-Involved Shootings")
        types_of_schools = joined_police_ps['TYPE'].value_counts()
        st.write(types_of_schools)

    if "Are there any schools that have not had any police-involved shootings?" in selected_questions:
        st.subheader("5. Schools without Police-Involved Shootings")
        schools_no_shootings = gdf_ps[~gdf_ps.NAME.isin(joined_police_ps.NAME.unique().tolist())]['NAME']
        st.write(schools_no_shootings)

    if "Which school has had the most police-involved shootings?" in selected_questions:
        st.subheader("6. School with the Most Police-Involved Shootings")
        most_affected_school = joined_police_ps['NAME'].value_counts().idxmax()
        st.write(most_affected_school)
