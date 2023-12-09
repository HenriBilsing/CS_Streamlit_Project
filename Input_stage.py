# input_stage.py
import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import requests

def get_location_from_address(street, city, postal_code):
    """Convert an address in Switzerland to latitude and longitude using Maps.co Geocoding API."""
    base_url = "https://geocode.maps.co/search"
    address = f"{street}, {city}, {postal_code}, Switzerland"
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
    st.write("## Select Your Location and Category")
    method = st.radio("Choose your method to input location:", ("Enter Coordinates", "Share Location", "Enter Address"))

    user_location = (None, None)
    radius_km = None

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

    elif method == "Enter Address":
        street = st.text_input("Street Name and Number")
        city = st.text_input("City")
        postal_code = st.text_input("Postal Code")

        # Check the length of postal code when it's entered
        if postal_code and len(postal_code) != 4:
            st.error("Postal code must be 4 digits.")
        else:
            user_location = get_location_from_address(street, city, postal_code)
            if user_location[0] is not None:
                st.write(f"Coordinates: {user_location}")

        # Show the country field when "Enter Address" is selected
        country = "Switzerland"
        st.text_input("Country", value=country, disabled=True)

    # Radius input
    radius_km = st.number_input('Radius in km', value=2)

    # Business category selection
    business_category = st.selectbox("Select Business Category", ["Restaurant", "Cafe", "Retail", "Other"])

    return user_location, business_category, radius_km