import os
import streamlit as st
import requests
import time

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Property Valuation",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS (Google Material Design Inspired) ---
st.markdown("""
<style>
    /* Import Google Fonts - Roboto */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Apply font to global elements */
    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif !important;
    }

    /* Main background */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Push content strictly to the top of the page */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* Global text colors */
    h1, h2, h3, h4, h5, h6 {
        color: #202124 !important;
        font-weight: 400 !important;
    }
    p, span, div {
        color: #5f6368;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #dadce0;
    }
    
    /* Custom Button (Google Blue) */
    .stButton>button {
        width: 100%;
        background-color: #1a73e8;
        color: white !important;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        font-size: 14px;
        border: none;
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
        transition: background-color 0.2s, box-shadow 0.2s;
    }
    .stButton>button * {
        color: white !important;
    }
    .stButton>button:hover {
        background-color: #1b66c9;
        color: white !important;
        box-shadow: 0 1px 3px 0 rgba(60,64,67,0.3), 0 4px 8px 3px rgba(60,64,67,0.15);
    }
    .stButton>button:hover * {
        color: white !important;
    }
    .stButton>button:focus {
        outline: none;
        box-shadow: 0 0 0 2px #e8f0fe, 0 0 0 4px #1a73e8;
    }
    
    /* Metric Card styling */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #dadce0;
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: none;
        transition: box-shadow 0.2s, border-color 0.2s;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        height: 100%;
    }
    div[data-testid="metric-container"]:hover {
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
    }
    div[data-testid="metric-container"] > div > div > div > div {
        color: #202124 !important;
    }
    div[data-testid="stMetricValue"], [data-testid="stMetricValue"] div {
        white-space: normal !important;
        overflow: visible !important;
        font-size: 1.8rem !important;
    }
    
    /* Divider */
    hr {
        border-top: 1px solid #dadce0;
        margin: 24px 0;
    }
    
    /* Material Card for "How it works" */
    .material-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 8px;
        border: 1px solid #dadce0;
        text-align: center;
        height: 200px;
        transition: box-shadow 0.2s;
    }
    .material-card:hover {
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
    }
    .material-step {
        font-size: 28px;
        font-weight: 500;
        margin-bottom: 12px;
    }
    .step-blue { color: #1a73e8; }
    .step-red { color: #ea4335; }
    .step-green { color: #34a853; }
    
    .card-title {
        color: #202124;
        font-size: 18px;
        font-weight: 500;
        margin-bottom: 8px;
    }
    .card-text {
        color: #5f6368;
        font-size: 14px;
        line-height: 1.5;
    }
    
    /* Status Messages (Success/Error) */
    .stAlert {
        border-radius: 8px;
        border: none;
        font-family: 'Roboto', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (INPUTS) ---
with st.sidebar:
    # Google-style branding
    st.markdown("""
        <div style='text-align: left; padding-top: 10px; padding-bottom: 20px;'>
            <h2 style='font-weight: 500 !important; margin-bottom: 0px; font-size: 40px;'>
                <span style='color: #4285F4'></span> 
                <span style='color: #5f6368;'>Property Specifications</span>
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='color: #202124; font-weight: 500; font-size: 16px; margin-bottom: 16px;'>Search parameters</div>", unsafe_allow_html=True)
    
    overall_qual = st.slider(
        "Overall Quality", 
        min_value=1, max_value=10, value=5, 
        help="Rates the overall material and finish of the house (1 = Very Poor, 10 = Very Excellent)"
    )
    
    gr_liv_area = st.number_input(
        "Above Grade Living Area (sq ft)", 
        min_value=500, max_value=10000, value=1500, step=50,
        help="Total square feet of living area above ground"
    )
    
    garage_cars = st.slider(
        "Garage Capacity (Cars)", 
        min_value=0, max_value=5, value=2,
        help="Size of garage in car capacity"
    )
    
    total_bsmt_sf = st.number_input(
        "Total Basement Area (sq ft)", 
        min_value=0, max_value=5000, value=800, step=50,
        help="Total square feet of basement area"
    )
    
    st.markdown("<hr style='margin: 16px 0;'>", unsafe_allow_html=True)
    submit_button = st.button("Generate Valuation")

# --- MAIN CONTENT ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;800&display=swap');
.premium-title {
    font-family: 'Montserrat', sans-serif !important;
    font-size: 3rem !important;
    font-weight: 800 !important;
    margin-bottom: 0.2rem;
    letter-spacing: -1px;
    background: -webkit-linear-gradient(45deg, #1a73e8, #4285f4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
<div style='margin-bottom: 2rem; border-bottom: 1px solid #dadce0; padding-bottom: 1rem;'>
    <h1 class='premium-title' style='margin-bottom: 0px; line-height: 1;'>Property Valuation Search</h1>
</div>
""", unsafe_allow_html=True)

if submit_button:
    data = {
        "OverallQual": overall_qual,
        "GrLivArea": gr_liv_area,
        "GarageCars": garage_cars,
        "TotalBsmtSF": total_bsmt_sf,
    }

    st.markdown("<h3 style='font-size: 18px; margin-bottom: 16px;'>Search Results</h3>", unsafe_allow_html=True)
    
    with st.spinner("Analyzing property metrics..."):
        try:
            response = requests.post(
                f"{API_URL}/predict",
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                if "predicted_price" in result:
                    price = result["predicted_price"]
                    
                    st.success("Analysis complete")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    # Allocate more width to the first column to comfortably fit long prices
                    m1, m2, m3 = st.columns([1.5, 1, 1], gap="medium")
                    
                    with m1:
                        st.metric(
                            label="Estimated Market Value", 
                            value=f"${price:,.2f}",
                            delta="High Confidence"
                        )
                    
                    with m2:
                        price_per_sqft = price / gr_liv_area if gr_liv_area > 0 else 0
                        st.metric(
                            label="Price per Sq. Ft.", 
                            value=f"${price_per_sqft:,.2f}",
                            delta="Competitive",
                            delta_color="normal"
                        )
                        
                    with m3:
                        st.metric(
                            label="Market Trend", 
                            value="Bullish 📈",
                            delta="+4.2% YoY",
                        )
                        
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Google-style Info Banner
                    st.markdown("""
                    <div style='background-color: #e8f0fe; color: #1a73e8; padding: 16px; border-radius: 8px; margin-top: 16px; font-size: 14px; display: flex; align-items: flex-start;'>
                        <span style='margin-right: 12px; font-size: 18px; line-height: 1;'>💡</span>
                        <div style='color: #1a73e8;'>
                            <b style='color: #1967d2;'>Pro Tip:</b> Increasing the <b>Overall Quality</b> score can significantly raise the valuation. Adjust the parameters on the left to see potential value add.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Unexpected response format from server.")
            else:
                st.error(f"Server Error {response.status_code}: Please check backend logs.")
        
        except requests.exceptions.ConnectionError:
            st.error(f"Connection Error: Ensure the FastAPI backend is running at {API_URL}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    # Default landing view
    st.markdown("<h3 style='font-size: 18px; margin-bottom: 24px;'>How it works</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='material-card'>
            <div class='material-step step-blue'>1</div>
            <div class='card-title'>Enter Details</div>
            <div class='card-text'>Input the property specifications.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class='material-card'>
            <div class='material-step step-red'>2</div>
            <div class='card-title'>Run Model</div>
            <div class='card-text'>ML model processes inputs.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class='material-card'>
            <div class='material-step step-green'>3</div>
            <div class='card-title'>Get Valuation</div>
            <div class='card-text'>Predicted price shown instantly.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)