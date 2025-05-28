import folium
from streamlit_folium import st_folium

def render_map(lat, lon, units=[]):
    m = folium.Map(location=[lat, lon], zoom_start=16)
    folium.Marker([lat, lon], tooltip="Accident Location", icon=folium.Icon(color='red')).add_to(m)

    for unit in units:
        folium.Marker(
            [lat + 0.0005, lon + 0.0005],  # Dummy offset
            tooltip=f"{unit['type'].capitalize()} {unit['id']}",
            icon=folium.Icon(color='blue' if unit['type'] == 'ambulance' else 'green')
        ).add_to(m)

    return m
