import os
import time
import streamlit as st
from streamlit_folium import st_folium

from agents.accident_agent import AccidentAgent
from agents.emergency_responder_agent import EmergencyResponderAgent
from utils.map_utils import render_map

# --- Streamlit setup ---
st.set_page_config(page_title="🚨 Accident Detection Dashboard", layout="wide")
st.title("🚨 Accident Detection and Emergency Response System")

# --- Initialize agents ---
agent = AccidentAgent()
responder = EmergencyResponderAgent()

# --- Session state initialization ---
default_state = {
    "summary": None,
    "dispatch_log": None,
    "location": None,
    "uploaded": False,
    "lat": None,
    "lon": None
}
for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- UI Controls ---
st.sidebar.header("📷 Input")
uploaded_image = st.sidebar.file_uploader("Upload accident scene image", type=["jpg", "png", "jpeg"])
camera_id = st.sidebar.selectbox("Select Camera Location", ["cam_entrance", "cam_parking", "cam_mainroad"])
notify_email = st.sidebar.text_input("WhatsApp Number", value="whatsapp:+918655287793")

# --- Trigger Detection ---
if uploaded_image and st.sidebar.button("🔍 Analyze for Accident"):
    with st.spinner("Analyzing uploaded image..."):
        temp_path = "temp_upload.jpg"
        with open(temp_path, "wb") as f:
            f.write(uploaded_image.read())

        # Accident detection + resource allocation
        summary, structured_resources = agent.handle_image(temp_path, camera_id, notify_email)

        # Clean up temp file
        os.remove(temp_path)

        # ✅ Early exit if no accident is detected
        if "no accident" in summary.lower():
            st.session_state["summary"] = summary
            st.session_state["uploaded"] = True
            st.warning("⚠️ No accident detected. No responders dispatched.")
            st.stop()

        # Get GPS location from camera
        loc = agent.loc_agent.get_location(camera_id)
        lat, lon = loc["lat"], loc["lon"]

        # Dispatch emergency responders
        dispatch_log = responder.dispatch(structured_resources, loc)

        # Store in session state
        st.session_state.update({
            "summary": summary,
            "dispatch_log": dispatch_log,
            "location": loc,
            "lat": lat,
            "lon": lon,
            "uploaded": True
        })

# --- Display Results After Detection ---
if st.session_state.uploaded and st.session_state.summary:
    st.success("✅ Accident Detected & Responders Notified")

    st.markdown("### 📋 Detection Summary")
    st.code(st.session_state.summary)

    st.markdown("### 🚨 Emergency Dispatch Log")
    for unit in st.session_state.dispatch_log["dispatched_units"]:
        st.markdown(f"""
        - **ID**: `{unit['id']}`
        - **Type**: {unit['type'].capitalize()}
        - **Status**: `{unit['status']}`
        - **Dispatched At**: {unit['dispatched_at']}
        - **ETA**: {unit['eta']}
        ---
        """)

    st.markdown("### 🗺️ Incident Location Map")
    m = render_map(st.session_state.lat, st.session_state.lon, st.session_state.dispatch_log["dispatched_units"])
    st_folium(m, width=700)

    with st.spinner("⏳ Waiting for responders (simulated)..."):
        time.sleep(6)

    st.markdown("### 🔄 Updated Unit Statuses")
    updated_units = responder.track_status()
    if updated_units:
        for unit in updated_units:
            st.success(f"✅ {unit['type'].capitalize()} {unit['id']} has arrived. | Status: {unit['status']}")
    else:
        st.info("ℹ️ No units have arrived yet. Try manual refresh below.")

# --- Manual Refresh ---
if st.button("🔄 Check for Updated Statuses"):
    updated_units = responder.track_status()
    st.markdown("### 🔄 Updated Unit Statuses")
    if updated_units:
        for unit in updated_units:
            st.success(f"✅ {unit['type'].capitalize()} {unit['id']} | Status: {unit['status']}")
    else:
        st.warning("⚠️ No units updated yet.")
