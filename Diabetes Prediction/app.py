import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Diabetes Risk Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the model and scaler
@st.cache_resource
def load_model():
    model = joblib.load('model.pkl')
    scaler = joblib.load('scaler.pkl')
    return model, scaler

model, scaler = load_model()

# Set clean, minimal custom CSS with dark theme
st.markdown("""
    <style>
    .stApp {
        background-color: #0F1116;
    }
    
    .stButton > button {
        background-color: #3B82F6;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        border: none;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: #2563EB;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem 1rem;
        color: #E5E7EB;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #3B82F6;
        color: white;
        border-radius: 0.5rem;
    }
    
    h1 {
        color: #E5E7EB;
        font-weight: 700;
    }
    
    h2, h3 {
        color: #E5E7EB;
        font-weight: 600;
    }
    
    .stMarkdown {
        color: #D1D5DB;
    }
    
    [data-testid="stMarkdownContainer"] {
        color: #D1D5DB;
    }
    
    [data-testid="stWidgetLabel"] {
        color: #E5E7EB;
    }
    
    /* Style number inputs and sliders */
    .stNumberInput > div > div > input {
        color: #E5E7EB;
        background-color: #1F2937;
        border-color: #374151;
    }
    
    .stSlider > div > div > div {
        background-color: #1F2937;
    }
    
    /* Style radio buttons */
    .stRadio > div {
        color: #E5E7EB;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #0083B8;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        margin-top: 2rem;
    }
    .prediction-box {
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Introduction
st.title("🏥 Diabetes Risk Predictor")

# Instructions and Information
st.markdown("""
### 📋 How to Use This Tool
1. Fill in your basic information like age, weight, and height
2. If you have recent medical test results (blood sugar, blood pressure), enter them
3. If you don't have some medical values, you can use the default values provided
4. Click the 'Predict Diabetes Risk' button to see your results

### ⚕️ Important Notes:
- This tool is for educational purposes only and should not replace professional medical advice
- All medical information you enter is processed locally and not stored anywhere
- Default values are provided but using your actual values will give more accurate results
""")

# Create tabs for different types of information
tab1, tab2 = st.tabs(["📊 Basic Information", "🔬 Medical Details (Optional)"])

with tab1:
    st.subheader("Basic Information")
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age (years)", min_value=20, max_value=90, value=40,
                            help="Enter your current age")
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0,
                               help="Enter your weight in kilograms")
    
    with col2:
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0,
                               help="Enter your height in centimeters")
        family_diabetes = st.radio("Do you have family members with diabetes?",
                                 ["No", "Yes, distant relatives", "Yes, parents or siblings"],
                                 help="Select based on your family history")    # Calculate BMI
    bmi = weight / ((height/100) ** 2)
    bmi_status = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
    
    if bmi < 18.5:
        st.warning(f"Your BMI is {bmi:.1f} - {bmi_status}")
    elif bmi < 25:
        st.success(f"Your BMI is {bmi:.1f} - {bmi_status}")
    elif bmi < 30:
        st.warning(f"Your BMI is {bmi:.1f} - {bmi_status}")
    else:
        st.error(f"Your BMI is {bmi:.1f} - {bmi_status}")

    # Map family history to diabetes pedigree function
    diabetes_pedigree = 0.1 if family_diabetes == "No" else 0.5 if family_diabetes == "Yes, distant relatives" else 1.0

with tab2:
    st.subheader("Medical Details (Optional)")
    st.info("💡 If you don't have these values from recent medical tests, you can leave them at default values")
    
    col3, col4 = st.columns(2)
    
    with col3:
        glucose = st.slider("Blood Sugar Level (mg/dL)", 70, 300, 100,
                          help="Fasting blood glucose level from your most recent test")
        blood_pressure = st.slider("Blood Pressure (systolic)", 60, 180, 120,
                                 help="The top number from your blood pressure reading (e.g., 120 in 120/80)")
    
    with col4:
        insulin = st.select_slider("Insulin Level",
                                 options=["Low", "Normal", "High", "Unknown"],
                                 value="Unknown",
                                 help="Based on your most recent blood test")
        pregnancies = st.number_input("Number of Pregnancies (for females)", 0, 15, 0,
                                    help="Enter 0 if male or if never pregnant")

    # Map insulin levels to numeric values
    insulin_map = {"Low": 50, "Normal": 150, "High": 250, "Unknown": 150}
    insulin_value = insulin_map[insulin]

    # Set a default value for skin thickness
    skin_thickness = 30  # Using a middle value as it's less critical for prediction

# Prediction button
if st.button("Predict Diabetes Risk"):    # Prepare input data
    input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, 
                           insulin_value, bmi, diabetes_pedigree, age]])
    
    # Scale the input data
    scaled_data = scaler.transform(input_data)
    
    # Make prediction
    prediction = model.predict(scaled_data)
    prediction_proba = model.predict_proba(scaled_data)
    risk_percentage = prediction_proba[0][1] * 100
      # Display results
    st.markdown("---")
    st.subheader("Your Results")
    
    # Create three columns for the results
    result_col1, result_col2, result_col3 = st.columns(3)
    
    with result_col1:        # Risk Level Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_percentage,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#2563eb"},
                'steps': [
                    {'range': [0, 33], 'color': "#bbf7d0"},  # Light green
                    {'range': [33, 66], 'color': "#fef08a"},  # Light yellow
                    {'range': [66, 100], 'color': "#fecaca"}  # Light red
                ]
            },
            title={'text': "Risk Score"}
        ))
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    with result_col2:
        risk_level = "Low" if risk_percentage < 33 else "Medium" if risk_percentage < 66 else "High"
        color = "green" if risk_level == "Low" else "orange" if risk_level == "Medium" else "red"
        st.markdown(f"""
            <div style='text-align: center;'>
                <h3>Risk Level</h3>
                <h2 style='color: {color};'>{risk_level}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with result_col3:
        st.markdown("""
            <div style='text-align: center;'>
                <h3>Recommendations</h3>
            </div>
        """, unsafe_allow_html=True)
        if risk_level == "Low":
            st.success("• Maintain your healthy lifestyle\n• Continue regular check-ups\n• Stay active and eat well")
        elif risk_level == "Medium":
            st.warning("• Consult with your healthcare provider\n• Monitor your blood sugar regularly\n• Consider lifestyle modifications")
        else:
            st.error("• Seek immediate medical consultation\n• Regular monitoring is essential\n• Strict lifestyle changes may be needed")

# Add information about the features at the bottom
with st.expander("ℹ️ About the Features"):
    st.markdown("""
    * **Age**: Age in years
    * **BMI**: Body Mass Index - weight in kg/(height in m)²
    * **Glucose Level**: Fasting blood glucose level in mg/dL
    * **Blood Pressure**: Systolic blood pressure in mm Hg
    * **Insulin**: 2-Hour serum insulin (mu U/ml)
    * **Skin Thickness**: Triceps skin fold thickness (mm)
    * **Pregnancies**: Number of times pregnant
    * **Diabetes Pedigree Function**: A function scoring likelihood of diabetes based on family history
    """)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Your Healthcare Team | © 2025")
