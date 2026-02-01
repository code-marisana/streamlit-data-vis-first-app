import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Metadata HTML and CSS
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">', unsafe_allow_html=True)

# Collect basic information
name = "Mr. Marisana A. Masha"
linkedin_url = "https://www.linkedin.com/in/marisanamasha"
linkedin_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0077b5" width="24px" height="24px">
    <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
</svg>
"""
orcid_url = "https://orcid.org/0000-0001-5121-2861"
orcid_svg = """
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" style="width:24px; vertical-align:middle;">
    <path fill="#A6CE39" d="M256,128c0,70.7-57.3,128-128,128S0,198.7,0,128S57.3,0,128,0S256,57.3,256,128z"/>
    <g fill="white">
        <path d="M86.3,186.2H70.9V79.1h15.4V186.2z"/>
        <path d="M108.9,79.1h41.6c39.6,0,57,28.3,57,53.6c0,27.5-21.5,53.6-56.8,53.6h-41.8V79.1z M124.3,172.4h24.5
        c34.1,0,44.8-26.5,44.8-40.6c0-11.8-4.5-39.2-44.5-39.2h-24.8V172.4z"/>
        <circle cx="78.6" cy="60.5" r="8.2"/>
    </g>
</svg>
"""
website_url = "https://marisananamasha.com"
website_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#555" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="24px" height="24px">
    <circle cx="12" cy="12" r="10"></circle>
    <line x1="2" y1="12" x2="22" y2="12"></line>
    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
</svg>
"""
field = "Chemical Engineering"
institution = "Cape Peninsula University of Technology"
st.title(f"Computational Fluid Dynamics Modeling of an Intensified Biomass Pyrolysis Reactor for Hydrogen Production: DATA VISUALISATION")
# Combine into a Flexbox Container
social_links_html = f"""
<div style="display: flex; justify-content: flex-start; align-items: center; gap: 20px;">
    <a href="{linkedin_url}" target="_blank" style="text-decoration: none; display: flex; align-items: center; gap: 8px;">
        {linkedin_svg}</a>
    <a href="{orcid_url}" target="_blank" style="text-decoration: none; display: flex; align-items: center; gap: 8px;">
        {orcid_svg}</a>
    <a href="{website_url}" target="_blank" style="text-decoration: none; display: flex; align-items: center; gap: 8px;">
        {website_svg}</a>
</div>
"""


st.divider()
st.header("Researcher Overview")
st.write(f"**Name:** {name}")
st.write(f"**Field of Research:** {field}")
st.write(f"**Institution:** {institution}")
st.markdown(social_links_html, unsafe_allow_html=True)
st.divider()

st.header("Related Publications")
st.write('publications that include the part of the data visualised here')

st.header("Results")

st.write("🔥 **Pyrolysis Process Interactive Explorer**")
st.markdown("""
Interactively adjust operating parameters to explore **qualitative trends**
in pyrolysis product distribution.
""")

# ---------------------------
# Sidebar controls
# ---------------------------
st.sidebar.header("Operating Parameters")

temperature = st.sidebar.slider(
    "Temperature (°C)", 300, 700, 500, step=10
)

heating_rate = st.sidebar.slider(
    "Heating Rate (°C/s)", 1, 100, 20
)

residence_time = st.sidebar.slider(
    "Vapour Residence Time (s)", 0.5, 10.0, 2.0, step=0.5
)

moisture = st.sidebar.slider(
    "Biomass Moisture Content (%)", 0, 30, 10
)

particle_size = st.sidebar.slider(
    "Particle Size (mm)", 0.1, 5.0, 1.0, step=0.1
)

# ---------------------------
# Simplified trend model
# ---------------------------
oil = (
    50
    + 0.08 * (temperature - 500)
    + 0.15 * heating_rate
    - 1.5 * residence_time
    - 0.4 * moisture
    - 1.2 * particle_size
)

char = (
    30
    - 0.05 * (temperature - 500)
    - 0.10 * heating_rate
    + 1.8 * residence_time
    + 0.3 * moisture
    + 0.8 * particle_size
)

gas = 100 - oil - char

# Keep values realistic
oil = np.clip(oil, 5, 75)
char = np.clip(char, 5, 60)
gas = np.clip(gas, 5, 60)

# Normalize to 100%
total = oil + char + gas
oil, char, gas = [x / total * 100 for x in (oil, char, gas)]

# ---------------------------
# Metrics
# ---------------------------
st.subheader("📊 Estimated Product Distribution")

c1, c2, c3 = st.columns(3)
c1.metric("Bio-oil (%)", f"{oil:.1f}")
c2.metric("Biochar (%)", f"{char:.1f}")
c3.metric("Syngas (%)", f"{gas:.1f}")

# ---------------------------
# Plotly bar chart
# ---------------------------
fig = go.Figure(
    data=[
        go.Bar(
            x=["Bio-oil", "Biochar", "Syngas"],
            y=[oil, char, gas],
            text=[f"{oil:.1f}%", f"{char:.1f}%", f"{gas:.1f}%"],
            textposition="auto"
        )
    ]
)

fig.update_layout(
    title="Pyrolysis Product Yield Distribution",
    yaxis_title="Yield (%)",
    yaxis=dict(range=[0, 100]),
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Interpretation helper
# ---------------------------
st.subheader("🧠 Interpretation Notes")
st.markdown("""
- **Higher temperature & heating rate** → increased **bio-oil and syngas**
- **Longer vapour residence time** → more **secondary cracking** → higher **syngas**
- **Higher moisture content** → reduced oil yield and quality
- **Larger particle size** → increased **char formation**
""")
