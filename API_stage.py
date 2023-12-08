# Import necessary libraries
import requests
import json

# Function to process data in API stage
def process_api_data(input_data):
    # Step 2: Format and Validate Input
    # Assume input_data is a dictionary with keys 'coordinates', 'address', 'category'
    
    # Step 3: Use Yelp API
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

    # Step 4: Process API Response
   if response.status_code == 200:
        api_data = response.json()
        businesses = api_data.get('businesses', [])
        return businesses

    else:
        print(f'Error accessing Yelp API. Status code: {response.status_code}')
        return None

        # Step 5: Filter and Sort
        # Apply additional filtering and sorting if needed

        # Step 6: Format Output
        output_data = {
            'results': [
                {
                    'name': business['name'],
                    'distance': business.get('distance'),
                    'rating': business.get('rating'),
                }
                for business in businesses
            ]
        }

        # Convert output_data to JSON
        output_json = json.dumps(output_data)

        # Step 7: Send to Output Stage
        send_to_output_stage(output_json)

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
