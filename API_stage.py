# API_stage.py
import requests

def process_api_data(input_data):
    """
    Querrys the Yelp API based on the selected category and user location
    
    @return: Response from Yelp API with name, location and rating of business returned by the querry
    """
    # Step 1: Use Yelp API
    yelp_api_url = 'https://api.yelp.com/v3/businesses/search'
    api_key = 'Vsfhiaf8e7xi1tqb9f6os-CIQxN-Qo8Vg80Ir0yG9m61wLtcL8EdCWM8K9l9Y8Oaj3wI-nRMh7M1GzRaIGTDPkwXRdOLzYbxAkRlkyRk-PhyvEyU0sHsBIRpOBlrZXYx'

    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    params = {
        'term': input_data['category'],
        'location': input_data['address'] if 'address' in input_data else f'{input_data["coordinates"]["latitude"]},{input_data["coordinates"]["longitude"]}',
    }

    response = requests.get(yelp_api_url, headers=headers, params=params)

    # Step 2: Process API Response
    if response.status_code == 200:
        api_data = response.json()
        businesses = api_data.get('businesses', [])

        # Step 3: Format Output
        output_data = {
            'results': [
                {
                    'name': business.get('name', 'Unknown'),
                    'latitude': business['coordinates']['latitude'] if 'coordinates' in business and 'latitude' in business['coordinates'] else None,
                    'longitude': business['coordinates']['longitude'] if 'coordinates' in business and 'longitude' in business['coordinates'] else None,
                    'distance': business.get('distance'),
                    'rating': business.get('rating'),
                }
                for business in businesses
            ]
        }

        return output_data

    else:
        print(f'Error accessing Yelp API. Status code: {response.status_code}')

        # Optionally, handle specific error cases
        if response.status_code == 401:
            print('Unauthorized access. Check your API key.')
        elif response.status_code == 403:
            print('Forbidden. Check your API key permissions.')
        else:
            # Handle other error cases as needed
            print('Unhandled error. Check your request and try again.')

        return None