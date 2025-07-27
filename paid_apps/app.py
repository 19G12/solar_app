import streamlit as st

st.title("Paid Version – Solar Analytics")
st.markdown("Welcome, premium user ☀️")

slider_val = st.slider("Solar Panel Efficiency (%)", 50, 100, 75)

if st.button("Submit"):
    st.write(f"Predicted savings with {slider_val}% efficiency...")
