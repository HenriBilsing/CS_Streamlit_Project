import streamlit as st
import pydeck as pdk
import Input_stage
import Output_stage
import pandas as pd
import math


def main():
    st.title("Business Locator Application")

    # Calling the input stage function
    user_location, business_category = Input_stage.input_stage()

    # User inputs
    radius_km = st.number_input('Radius in km', value=5)

      # Display the results from the input stage
    st.write(f"Location: {user_location}")
    st.write(f"Category: {business_category}")
    st.write(f"Radius: {radius_km}")

   # Example usage
    data = [
        {'name': 'Restaurant A', 'review': 'Excellent', 'type': 'Restaurant', 'latitude': 47.4331279, 'longitude': 9.3746559},
        {'name': 'Restaurant B', 'review': 'Good', 'type': 'Restaurant', 'latitude': 47.434, 'longitude': 9.377},
        {'name': 'Restaurant C', 'review': 'Bad', 'type': 'Restaurant', 'latitude': 47.435, 'longitude': 9.3743},
        {'name': 'Cafe B', 'review': 'Very Good', 'type': 'Cafe', 'latitude': 47.4331279, 'longitude': 9.3746559},
        {'name': 'Retail C', 'review': 'Good', 'type': 'Retail', 'latitude': 47.4331279, 'longitude': 9.3746559}
        ]
    
    # Button to perform action
    if st.button('Find Businesses'):
        # Use user_location as the coordinates
        results = Output_stage.businesses_in_radius(user_location, radius_km, business_category, data)
        
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
            radius = 20 * 1**(13 - initial_zoom)

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

