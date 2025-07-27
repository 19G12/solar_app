import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.title("🔒 Paid Version – Solar Analytics")
st.markdown("Welcome, premium user ☀️")

# Create a form so everything runs only on submit
with st.form("efficiency_form"):
    efficiency = st.slider("Solar Panel Efficiency (%)", 50, 100, 75)
    submitted = st.form_submit_button("Submit")

# Only run the logic when the user clicks Submit
if submitted:
    st.success(f"Predicted savings for {efficiency}% efficiency:")

    # Data
    efficiencies = np.arange(50, 101)
    base_savings = 50000  # adjust this as needed
    predicted_savings = base_savings * (efficiencies / 100) ** 1.5

    # Plotly interactive line chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=efficiencies,
        y=predicted_savings,
        mode="lines",
        name="Savings Curve",
        line=dict(color="green")
    ))

    fig.add_trace(go.Scatter(
        x=[efficiency],
        y=[base_savings * (efficiency / 100) ** 1.5],
        mode="markers+text",
        name="Your Choice",
        marker=dict(color="red", size=10),
        text=[f"{efficiency}%"],
        textposition="top center"
    ))

    fig.update_layout(
        title="Predicted Savings vs Efficiency",
        xaxis_title="Efficiency (%)",
        yaxis_title="Predicted Savings",
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)
