import streamlit as st
from streamlit.components.v1 import html
import Input_stage
import API_stage
import Output_stage
import pandas as pd
import pydeck as pdk

def main():
    # Capture device type from JavaScript
    if "device_type" not in st.session_state:
        st.session_state['device_type'] = 'desktop'

    st.experimental_on_script_runner_execution(
        lambda: st.session_state.update({'device_type': st.experimental_get_query_params().get("deviceType", ["desktop"])[0]})
    )

    st.title("Business Locator Application")

    # Calling the input stage function
    user_location, business_category, radius_km = Input_stage.input_stage()

    if user_location and user_location[0] is not None:
        # Display the results from the input stage
        st.write(f"Location: {user_location}")
        st.write(f"Category: {business_category}")
        st.write(f"Radius: {radius_km}")

        # Button to perform action
        if st.button('Find Businesses'):
            # Call the relevant API-related function (if any) from API_stage
            api_data = API_stage.process_api_data({
                'coordinates': {
                    'latitude': user_location[0], 
                    'longitude': user_location[1]
                }, 
                'category': business_category
            })

            if api_data:
                # Get businesses of a specific type within the radius
                results = Output_stage.process_output_data(api_data)

                if results:
                    # Validate data and construct DataFrame
                    valid_results = [
                        res for res in results 
                        if 'latitude' in res and 'longitude' in res
                    ]

                    if valid_results:
                        df = pd.DataFrame({
                            'lat': [res['latitude'] for res in valid_results],
                            'lon': [res['longitude'] for res in valid_results],
                            'name': [res['name'] for res in valid_results],
                            'rating': [res['rating'] for res in valid_results]
                        })

                        # Rendering the map with pydeck
                        initial_zoom = 11
                        radius = 10 * 2**(13 - initial_zoom)
                        layer = pdk.Layer(
                            'ScatterplotLayer',
                            df,
                            get_position=['lon', 'lat'],
                            get_color=[255, 30, 0, 160],
                            get_radius=radius,
                            pickable=True
                        )
                        view_state = pdk.ViewState(
                            latitude=df['lat']. mean(),
                            longitude=df['lon'].mean(),
                            zoom=initial_zoom,
                            pitch=0
                        )
                        r = pdk.Deck(
                            layers=[layer],
                            initial_view_state=view_state,
                            tooltip={"html": "<b>Name:</b> {name}<br><b>Rating:</b> {rating}"}
                        )
                        st.pydeck_chart(r)
                    else:
                        st.write("No valid business data found.")
                else:
                    st.write("No businesses found within the specified radius.")
    else:
        st.error("Please enter a valid location within Switzerland.")     

if __name__ == "__main__":
    main()
