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

user_coordinates = (40.7128, -74.0060)  # Example user coordinates
radius_km = 5  # 5 km radius
business_type = 'Restaurant'  # User-selected business type


# Get businesses of a specific type within the radius
businesses = businesses_in_radius(user_coordinates, radius_km, business_type, data)
businesses



