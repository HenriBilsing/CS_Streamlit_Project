# input_stage.py
import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import requests

def get_location_from_address(address):
    """Convert an address to latitude and longitude using Maps.co Geocoding API."""
    base_url = "https://geocode.maps.co/search"
    params = {"q": address}
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            # Assuming the first result is the most relevant
            latitude = data[0]["lat"]
            longitude = data[0]["lon"]
            return latitude, longitude
    return None, None

def input_stage():
    

    # Location input methods
    st.write("## Select Your Location and Category")
    method = st.radio("Choose your method to input location:", ("Enter Coordinates", "Share Location", "Enter Address"))

    if method == "Enter Coordinates":
        lat = st.number_input("Enter Latitude", format="%.6f")
        lon = st.number_input("Enter Longitude", format="%.6f")
        user_location = (lat, lon)

    elif method == "Share Location":
        location = streamlit_geolocation()
        if location:
            lat = location['latitude']
            lon = location['longitude']
            user_location = (lat, lon)
            st.write(f"Coordinates: {user_location}")

        else:
            user_location = (None, None)

    elif method == "Enter Address":
        address = st.text_input("Enter your address")
        user_location = get_location_from_address(address)
        if user_location[0] is not None:
            st.write(f"Coordinates: {user_location}")

    # Business category selection
    business_category = st.selectbox("Select Business Category", ["Restaurant", "Cafe", "Retail", "Other"])

    return user_location, business_category
