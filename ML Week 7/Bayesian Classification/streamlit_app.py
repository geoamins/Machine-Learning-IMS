import os
import streamlit as st
import pandas as pd
from sklearn.naive_bayes import CategoricalNB
from sklearn.preprocessing import LabelEncoder


def load_data():
    # Prefer the provided CSV in the same folder as this app
    path = os.path.join(os.path.dirname(__file__), 'Book1.csv')
    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        # fallback sample dataset (matches the commented example in the notebook)
        df = pd.DataFrame({
            'Outlook': ['sunny', 'sunny', 'overcast', 'rain', 'rain', 'rain', 'overcast', 'sunny', 'sunny', 'rain', 'sunny', 'overcast', 'overcast', 'rain'],
            'Temperature': ['hot', 'hot', 'hot', 'mild', 'cool', 'cool', 'cool', 'mild', 'cool', 'mild', 'mild', 'mild', 'hot', 'mild'],
            'Humidity': ['high', 'high', 'high', 'high', 'normal', 'normal', 'normal', 'high', 'normal', 'normal', 'normal', 'high', 'normal', 'high'],
            'Windy': ['false', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'true'],
            'Class': ['N', 'N', 'P', 'P', 'P', 'N', 'P', 'N', 'P', 'P', 'P', 'P', 'P', 'N']
        })
    return df


def prepare_and_train(df):
    # Keep a copy of raw values for the UI
    df_raw = df.copy()

    # We'll use a LabelEncoder per column to preserve mappings
    encoders = {}
    df_enc = df.copy()
    for col in df.columns:
        le = LabelEncoder()
        try:
            df_enc[col] = le.fit_transform(df[col].astype(str))
        except Exception:
            # fallback: convert to string then encode
            df_enc[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    X = df_enc.drop('Class', axis=1)
    y = df_enc['Class']

    model = CategoricalNB()
    model.fit(X, y)
    return model, encoders, df_raw


def main():
    st.title('Simple Naive Bayes (Categorical)')
    st.write('Train a CategoricalNB on `Book1.csv` and make predictions from the UI.')

    df = load_data()

    if st.checkbox('Show raw data'):
        st.dataframe(df)

    model, encoders, df_raw = prepare_and_train(df)

    st.header('Make a prediction')
    features = [c for c in df.columns if c != 'Class']

    user_input = {}
    for col in features:
        # Use raw unique values for the selectbox
        opts = list(df_raw[col].astype(str).unique())
        user_input[col] = st.selectbox(col, opts)

    if st.button('Predict'):
        # encode user input
        sample = []
        for col in features:
            le = encoders[col]
            val = str(user_input[col])
            encoded = le.transform([val])[0]
            sample.append(encoded)

        pred = model.predict([sample])[0]
        proba = None
        try:
            proba = model.predict_proba([sample])[0]
        except Exception:
            proba = None

        # decode prediction
        class_le = encoders['Class']
        pred_label = class_le.inverse_transform([pred])[0]

        st.success(f'Predicted class: {pred_label}')
        if proba is not None:
            # supply readable probabilities mapping
            labels = class_le.inverse_transform(list(range(len(proba))))
            prob_map = {labels[i]: float(proba[i]) for i in range(len(proba))}
            st.write('Class probabilities:')
            st.json(prob_map)


if __name__ == '__main__':
    main()
