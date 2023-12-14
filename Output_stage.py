# Define an array of big brand names active in Switzerland
big_brand_names = [
    "McDonald's", "Burger King", "KFC", "Subway", "Pizza Hut", "Domino's Pizza",
    "Starbucks", "Nespresso", "McCafé", "Costa Coffee", "Peet's Coffee",
    "Migros", "Coop", "Zara", "H&M", "IKEA", "Media Markt"
]

def process_output_data(output_data):
    """
    Takes results from the Yelp API and filters them to exclude entries marked as 'big businesses'
    
    @return: Filtered businesses
    """
    # Process the data received from the API stage
    businesses = output_data.get('results', [])

    # Filter out businesses that match the big brand names
    filtered_businesses = [business for business in businesses if not any(brand in business['name'] for brand in big_brand_names)]

    return filtered_businesses