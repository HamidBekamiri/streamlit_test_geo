import streamlit as st
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# Load Data
@st.cache_data
def load_data():
    police = pd.read_csv('https://raw.githubusercontent.com/aaubs/ds-master/main/data/geopandas_data/SPD_Officer_Involved_Shooting__OIS__Data.csv')
    gdf_ps = gpd.read_file('https://raw.githubusercontent.com/aaubs/ds-master/main/data/Public_Schools.geojson')
    gdf = gpd.read_file('https://raw.githubusercontent.com/aaubs/ds-master/main/data/geopandas_data/Neighborhood_Map_Atlas_Districts.geojson')
    return police, gdf_ps, gdf

st.title("Analyzing Police-Involved Shootings and Schools in Seattle")

# Load the data
police, gdf_ps, gdf = load_data()

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

# Dummy data; replace with real analysis
# Assuming 'Neighborhood' is a column in your police DataFrame
most_common_neighborhoods = police['Neighborhood'].value_counts().index.tolist()

# Assuming 'Neighborhood' is also a column in your gdf DataFrame (the one for neighborhoods)
neighborhoods_in_gdf = gdf['Neighborhood'].unique().tolist()
neighborhoods_no_incidents = list(set(neighborhoods_in_gdf) - set(most_common_neighborhoods))

# Perform spatial join to find schools close to police-involved shootings
# Assuming 'geometry' column exists in both GeoDataFrames
joined_police_ps = gpd.sjoin(gdf_ps, police, how='left', op='within')  # Replace with your logic for "closeness"
schools_close_to_shootings = joined_police_ps['School_Name'].unique().tolist()

# Find types of those schools
types_of_schools = joined_police_ps['School_Type'].unique().tolist()

# Find schools with no shootings
all_schools = gdf_ps['School_Name'].unique().tolist()
schools_no_shootings = list(set(all_schools) - set(schools_close_to_shootings))

# Find the most affected school
most_affected_school = joined_police_ps['School_Name'].value_counts().idxmax()


if perform_analysis:

    if "What are the common neighborhoods where most police-involved shootings happen?" in selected_questions:
        st.subheader("1. Common Neighborhoods with Police-Involved Shootings")
        st.write(most_common_neighborhoods)

    if "Are there any neighborhoods without any police-involved shootings?" in selected_questions:
        st.subheader("2. Neighborhoods without Police-Involved Shootings")
        st.write(neighborhoods_no_incidents)

    if "Are there any schools close to locations where police-involved shootings have occurred?" in selected_questions:
        st.subheader("3. Schools Close to Police-Involved Shootings")
        st.write(schools_close_to_shootings)

    if "What types of schools (Elementary, High School, etc.) are most commonly close to police-involved shootings?" in selected_questions:
        st.subheader("4. Types of Schools Close to Police-Involved Shootings")
        st.write(types_of_schools)

    if "Are there any schools that have not had any police-involved shootings?" in selected_questions:
        st.subheader("5. Schools without Police-Involved Shootings")
        st.write(schools_no_shootings)

    if "Which school has had the most police-involved shootings?" in selected_questions:
        st.subheader("6. School with the Most Police-Involved Shootings")
        st.write(most_affected_school)
