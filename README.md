# Diabetes Risk Predictor

A modern, user-friendly web application that helps predict the risk of diabetes based on various health parameters. Built with Streamlit and scikit-learn, this tool provides instant risk assessment and personalized recommendations.

![Diabetes Risk Predictor](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database)

## 🌟 Features

- **User-Friendly Interface**: Clean, intuitive design with dark theme
- **Two-Step Input Process**:
  - Basic Information (age, weight, height, family history)
  - Optional Medical Details (blood sugar, blood pressure, insulin levels)
- **Instant BMI Calculation**: Automatic BMI calculation with status indicator
- **Smart Defaults**: Reasonable default values for medical parameters
- **Visual Risk Assessment**:
  - Interactive gauge chart
  - Color-coded risk levels
  - Personalized recommendations
- **Privacy-Focused**: All calculations performed locally

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Getting Started

1. **Clone the repository:**
   ```powershell
   git clone <repository-url>
   cd "Diabetes Prediction"
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```powershell
   streamlit run app.py
   ```

The application will open in your default web browser at `http://localhost:8501`

## 📊 How It Works

1. Enter your basic information:
   - Age
   - Weight
   - Height
   - Family history of diabetes

2. (Optional) Provide medical details:
   - Blood sugar level
   - Blood pressure
   - Insulin level
   - Number of pregnancies (if applicable)

3. Click "Predict Diabetes Risk" to get your results

## 🔬 Technical Details

- **Framework**: Streamlit
- **ML Model**: Scikit-learn
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly

## ⚠️ Disclaimer

This tool is for educational purposes only and should not replace professional medical advice. Always consult with healthcare providers for medical decisions.

## 📝 Files Structure

```
├── app.py              # Main application file
├── model.pkl           # Trained machine learning model
├── scaler.pkl         # Data scaler for preprocessing
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## 🔧 Model Information

The prediction model is trained on a dataset containing various health parameters and their correlation with diabetes. The model uses the following features:
- Age
- BMI
- Blood Sugar Level
- Blood Pressure
- Insulin Level
- Skin Thickness
- Number of Pregnancies
- Diabetes Pedigree Function

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Data source: Original Pima Indians Diabetes Database
- Healthcare professionals who provided domain expertise
- Streamlit team for the excellent framework
