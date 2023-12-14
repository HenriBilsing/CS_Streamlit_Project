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