import streamlit as st
import pandas as pd

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

user_coordinates = (40.7128, -74.0060)  # Example user coordinates
radius_km = 5  # 5 km radius
business_type = 'Restaurant'  # User-selected business type

# Get businesses of a specific type within the radius
businesses = businesses_in_radius(user_coordinates, radius_km, business_type, data)
businesses



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

