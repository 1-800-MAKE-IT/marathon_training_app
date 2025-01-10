import streamlit as st
import logging

st.set_page_config(page_title="Performance Entry", page_icon="📝")

# Load custom CSS for styling
with open("styles/styles.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# Performance Entry Page
st.title("Performance Entry")
st.write("Log your recent training performance.")

user = st.text_input("Username:")
distance = st.text_input("Distance (e.g., 10km):")
time = st.text_input("Time (e.g., 55:00):")
condition = st.text_input("Condition (e.g., Sunny):")
injuries = st.text_input("Injuries (if any):")
notes = st.text_area("Notes:")

if st.button("Save Data"):
    logging.info(f"Attempting to save data for user: {user}")
    try:
        # TODO: Connect to backend data storage logic
        st.success("Data saved successfully!")
        logging.info(f"Data saved successfully for user: {user}")
    except Exception as e:
        st.error("Failed to save data.")
        logging.error(f"Error saving data for user: {user}: {e}")