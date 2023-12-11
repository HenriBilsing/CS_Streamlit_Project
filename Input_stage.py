# input_stage.py
import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from streamlit.components.v1 import html
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

def is_location_in_switzerland(latitude, longitude):
    """Check if the given latitude and longitude are in Switzerland."""
    base_url = "https://geocode.maps.co/reverse"
    params = {"lat": latitude, "lon": longitude}
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data and 'address' in data and data['address'].get('country') == 'Switzerland':
            return True
    return False

def input_stage():
    # JavaScript to detect device type
    device_type_code = """
    <script>
    function isMobileDevice() {
        return (typeof window.orientation !== "undefined") || (navigator.userAgent.indexOf('IEMobile') !== -1);
    };
    let deviceType = isMobileDevice() ? "mobile" : "desktop";
    window.parent.postMessage({deviceType: deviceType}, "*");
    </script>
    """
    html(device_type_code, height=0)

    # Receive device type from JavaScript
    device_type = st.session_state.get('device_type', 'desktop')

    st.write("## Select Your Location and Category")
    method = st.radio("Choose your method to input location:", ("Enter Coordinates", "Share Location", "Enter Address"))

    user_location = (None, None)
    radius_km = None
    if st.session_state['device_type'] == 'desktop':
        # Exclude "Share Location" option
        method = st.radio("Choose your method to input location:", ("Enter Coordinates", "Enter Address"))
        if method == "Enter Coordinates":
            initial_lat = 47.4300025
            initial_lon = 9.37221840
            lat = st.number_input("Enter Latitude", value=initial_lat, format="%.6f")
            lon = st.number_input("Enter Longitude", value=initial_lon, format="%.6f")
            user_location = (lat, lon)
            if lat and lon:
                if not is_location_in_switzerland(lat, lon):
                    return None, None, None

        elif method == "Enter Address":
            street = st.text_input("Street Name and Number")
            city = st.text_input("City")
            postal_code = st.text_input("Postal Code")

            # Check the length of postal code when it's entered
            if postal_code and len(postal_code) != 4:
                st.error("Postal code must be 4 digits.")
            else:
                user_location = get_location_from_address(street, city, postal_code)
                if user_location[0] is not None and user_location[1] is not None:
                    if not is_location_in_switzerland(user_location[0], user_location[1]):
                        return None, None, None

            # Show the country field when "Enter Address" is selected
            country = "Switzerland"
            st.text_input("Country", value=country, disabled=True)
        else:
            method = st.radio("Choose your method to input location:", ("Enter Coordinates", "Enter Address"))
            if method == "Share Location":
                location = streamlit_geolocation()
                if location:
                    lat = location['latitude']
                    lon = location['longitude']
                    user_location = (lat, lon)
                    if lat and lon:
                        if not is_location_in_switzerland(lat, lon):
                            return None, None, None
                        
            elif method == "Enter Address":
                street = st.text_input("Street Name and Number")
                city = st.text_input("City")
                postal_code = st.text_input("Postal Code")

                # Check the length of postal code when it's entered
                if postal_code and len(postal_code) != 4:
                    st.error("Postal code must be 4 digits.")
                else:
                    user_location = get_location_from_address(street, city, postal_code)
                    if user_location[0] is not None and user_location[1] is not None:
                        if not is_location_in_switzerland(user_location[0], user_location[1]):
                            return None, None, None
            
            elif method == "Enter Coordinates":
                initial_lat = 47.4300025
                initial_lon = 9.37221840
                lat = st.number_input("Enter Latitude", value=initial_lat, format="%.6f")
                lon = st.number_input("Enter Longitude", value=initial_lon, format="%.6f")
                user_location = (lat, lon)
                if lat and lon:
                    if not is_location_in_switzerland(lat, lon):
                        return None, None, None

            # Show the country field when "Enter Address" is selected
            country = "Switzerland"
            st.text_input("Country", value=country, disabled=True)        

    # Radius input
    radius_km = st.number_input('Radius in km', value=2)

    # Business category selection
    business_category = st.selectbox("Select Business Category", ["Restaurant", "Cafe", "Retail", "Other"])

    return user_location, business_category, radius_km