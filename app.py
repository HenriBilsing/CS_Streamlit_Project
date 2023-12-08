import streamlit as st
import Input_stage
import API_stage
import Output_stage
import pandas as pd
import pydeck as pdk

def main():
    st.title("Business Locator Application")

    # Calling the input stage function
    user_location, business_category, radius_km = Input_stage.input_stage()

    # Display the results from the input stage
    st.write(f"Location: {user_location}")
    st.write(f"Category: {business_category}")
    st.write(f"Radius: {radius_km}")

    # Call the relevant API-related function (if any) from API_stage
    api_data = API_stage.process_api_data({'coordinates': {'latitude': user_location[0], 'longitude': user_location[1]}, 'category': business_category})

    if api_data:
        yelp_businesses = [
            {
                'name': business['name'],
                'review': business.get('review', ''),
                'type': business_category,
                'latitude': business['coordinates']['latitude'],
                'longitude': business['coordinates']['longitude'],
            }
            for business in api_data
        ]

        # Get businesses of a specific type within the radius
        results = Output_stage.process_output_data(api_data)
        
        if results:
            # Prepare DataFrame for pydeck
            df = pd.DataFrame({
                'lat': [res['coordinates'][0] for res in results],
                'lon': [res['coordinates'][1] for res in results],
                'name': [res['name'] for res in results],
                'review': [res['review'] for res in results]  # Assuming 'review' is a field in your results
            })

             # Set the initial zoom level
            initial_zoom = 11

            # Adjust radius based on zoom level
            radius = 10 * 2**(13 - initial_zoom)

            # Create a pydeck Layer
            layer = pdk.Layer(
                'ScatterplotLayer',     # Use a ScatterplotLayer
                df,
                get_position=['lon', 'lat'],
                get_color=[255, 30, 0, 160],
                get_radius=radius,
                pickable=True
            )

            # Set the viewport location
            view_state = pdk.ViewState(
                latitude=df['lat'].mean(),
                longitude=df['lon'].mean(),
                zoom=initial_zoom,
                pitch=0
            )

            # Render the map with pydeck
            r = pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip={"html": "<b>Name:</b> {name}<br><b>Review:</b> {review}"}
            )
            st.pydeck_chart(r)

        else:
            st.write("No businesses found within the specified radius.")

if __name__ == "__main__":
    main()

