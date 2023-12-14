# Define an array of big brand names active in Switzerland
big_brand_names = [
    "McDonald's", "Burger King", "KFC", "Subway", "Pizza Hut", "Domino's Pizza",
    "Starbucks", "Nespresso", "McCafé", "Costa Coffee", "Peet's Coffee",
    "Migros", "Coop", "Zara", "H&M", "IKEA", "Media Markt"
]

def process_output_data(output_data):
    # Process the data received from the API stage
    businesses = output_data.get('results', [])

    # Filter out businesses that match the big brand names
    filtered_businesses = [business for business in businesses if business['name'] not in big_brand_names]

    return filtered_businesses

# Haversine distance function was proposed by David Montani to calculate the distance to define the radius, the code he provided us is used below
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
    a = math.sin(dlat / 2)*2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)*2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance


# Function to select the Businesses in the defined radius--------------------------------------------------------------------------

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
                    'rating': entry.get('rating', '')
                })

    return nearby_businesses

def process_output_data(output_data):
    # Process the data received from the API stage
    businesses = output_data.get('results', [])

    # Filter out businesses that match the big brand names
    filtered_businesses = [business for business in businesses if business['name'] not in big_brand_names]

    return filtered_businesses

