# Streamlit Naive Bayes Demo

This small Streamlit app trains a categorical Naive Bayes (sklearn.CategoricalNB) on `Book1.csv` (if present) or a built-in example dataset and exposes a UI to make predictions.

How to run

1. Create a virtual environment and install dependencies:

   python -m venv .venv
   .venv\Scripts\Activate.ps1; pip install -r requirements.txt

2. Run the app:

   streamlit run streamlit_app.py

Notes

- The app uses `LabelEncoder` per column to encode categorical features. If your `Book1.csv` has different columns, you may need to adapt the app.
- This is a minimal demo intended for teaching and exploration.
