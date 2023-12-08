import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import requests
import pandas as pd
import math

def haversine_distance(coord1, coord2):
    # Radius of the Earth in kilometers
    R = 6371.0

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Difference in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance


# Function--------------------------------------------------------------------------

def businesses_in_radius(user_coord, radius, business_type, dataset):
    nearby_businesses = []

    for entry in dataset:
        if entry['type'] == business_type:
            business_coord = (entry['latitude'], entry['longitude'])
            distance = haversine_distance(user_coord, business_coord)
            
            if distance <= radius:
                nearby_businesses.append({
                    'name': entry['name'],
                    'coordinates': business_coord,
                    'review': entry['review']
                })

    return nearby_businesses
# Example usage
data = [
    {'name': 'Restaurant A', 'review': 'Excellent', 'type': 'Restaurant', 'latitude': 40.7128, 'longitude': -74.0060},
    {'name': 'Cafe B', 'review': 'Very Good', 'type': 'Cafe', 'latitude': 40.7328, 'longitude': -74.0160},
    {'name': 'Retail C', 'review': 'Good', 'type': 'Retail', 'latitude': 40.7528, 'longitude': -74.0260}
]

# Example usage
user_coordinates = (40.7128, -74.0060)  # Example user coordinates
radius_km = 5  # 5 km radius
business_type = 'Restaurant'  # User-selected business type

# Call Yelp API to get businesses
api_data = process_api_data({'coordinates': {'latitude': user_coordinates[0], 'longitude': user_coordinates[1]}, 'category': business_type})

if api_data:
    # Extract relevant information from Yelp API response
    yelp_businesses = [
        {
            'name': business['name'],
            'review': business.get('review', ''),
            'type': business_type,
            'latitude': business['coordinates']['latitude'],
            'longitude': business['coordinates']['longitude'],
        }
        for business in api_data
    ]

    # Get businesses of a specific type within the radius
    businesses = businesses_in_radius(user_coordinates, radius_km, business_type, yelp_businesses)
    businesses
else:
    print('Yelp API data retrieval failed. Check your API key and request.')



# Streamlit app
def main():
    st.title('Business Locator')

    # User inputs
    lat = st.number_input('Latitude', value=40.7128)  # Default values as an example
    lon = st.number_input('Longitude', value=-74.0060)
    radius_km = st.number_input('Radius in km', value=5)
    business_type = st.selectbox('Business Type', ['Restaurant', 'Cafe', 'Retail'])

    # Button to perform action
    if st.button('Find Businesses'):
        user_coordinates = (lat, lon)
        # Assuming 'data' is your dataset
        results = businesses_in_radius(user_coordinates, radius_km, business_type, data)
        
        if results:
            # Prepare DataFrame for st.map
            df = pd.DataFrame({
                'lat': [res['coordinates'][0] for res in results],
                'lon': [res['coordinates'][1] for res in results]
            })
            st.map(df)
            # Optionally display details in a table
            st.write(results)
        else:
            st.write("No businesses found within the specified radius.")

if __name__ == "__main__":
    main()



