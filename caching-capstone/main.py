import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.ensemble import GradientBoostingClassifier

URL = "https://raw.githubusercontent.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/refs/heads/master/18_caching_capstone/data/mushrooms.csv"
COLS = ['class', 'odor', 'gill-size', 'gill-color', 'stalk-surface-above-ring',
       'stalk-surface-below-ring', 'stalk-color-above-ring',
       'stalk-color-below-ring', 'ring-type', 'spore-print-color']

# Function to read the data
@st.cache_data
def get_df():
    df = pd.read_csv(URL)
    return df[COLS]

# Function to fit the LabelEncoder
@st.cache_resource
def get_le(df):
    le = LabelEncoder()
    le.fit(df['class'])
    return le

# Function to fit the OrdinalEncoder
@st.cache_resource
def get_oe(df):
    oe = OrdinalEncoder()
    X_cols = df.columns[1:]
    oe.fit(df[X_cols])
    return oe

# Function to encode data
@st.cache_data
def encode_data(df, _le, _oe):
    df['class'] = _le.transform(df['class'])

    X_cols = df.columns[1:]
    df[X_cols] = _oe.transform(df[X_cols])

    return df

# Function to train the model
@st.cache_resource
def train_model(df):
    X = df.drop(['class'], axis=1)
    y = df['class']
    gbc = GradientBoostingClassifier(max_depth=5, random_state=42)
    gbc.fit(X, y)
    return gbc

# Function to make a prediction
@st.cache_data
def predict(_model, _X_encoder, X_pred):
    features = [X[0] for X in X_pred]
    features = np.array(features).reshape(1, -1)

    encoded_features = _X_encoder.transform(features)

    pred = _model.predict(encoded_features)
    return pred[0]

if __name__ == "__main__":
    st.title("Mushroom classifier 🍄")
    
    # Read the data
    df = get_df()
    
    st.subheader("Step 1: Select the values for prediction")

    col1, col2, col3 = st.columns(3)

    with col1:
        odor = st.selectbox('Odor', ('a - almond', 'l - anisel', 'c - creosote', 'y - fishy', 'f - foul', 'm - musty', 'n - none', 'p - pungent', 's - spicy'))
        stalk_surface_above_ring = st.selectbox('Stalk surface above ring', ('f - fibrous', 'y - scaly', 'k - silky', 's - smooth'))
        stalk_color_below_ring = st.selectbox('Stalk color below ring', ('n - brown', 'b - buff', 'c - cinnamon', 'g - gray', 'o - orange', 'p - pink', 'e - red', 'w - white', 'y - yellow'))
    with col2:
        gill_size = st.selectbox('Gill size', ('b - broad', 'n - narrow'))
        stalk_surface_below_ring = st.selectbox('Stalk surface below ring', ('f - fibrous', 'y - scaly', 'k - silky', 's - smooth'))
        ring_type = st.selectbox('Ring type', ('e - evanescente', 'f - flaring', 'l - large', 'n - none', 'p - pendant', 's - sheathing', 'z - zone'))
    with col3:
        gill_color = st.selectbox('Gill color', ('k - black', 'n - brown', 'b - buff', 'h - chocolate', 'g - gray', 'r - green', 'o - orange', 'p - pink', 'u - purple', 'e - red', 'w - white', 'y - yellow'))
        stalk_color_above_ring = st.selectbox('Stalk color above ring', ('n - brown', 'b - buff', 'c - cinnamon', 'g - gray', 'o - orange', 'p - pink', 'e - red', 'w - white', 'y - yellow'))
        spore_print_color = st.selectbox('Spore print color', ('k - black', 'n - brown', 'b - buff', 'h - chocolate', 'r - green', 'o - orange', 'u - purple', 'w - white', 'y - yellow'))

    st.subheader("Step 2: Ask the model for a prediction")

    pred_btn = st.button("Predict", type="primary")

    # If the button is clicked:
    if pred_btn:
    # 1. Fit the LabelEncoder
        le = get_le(df)
    # 2. Fit the OrdinalEncoder
        oe = get_oe(df)
    # 3. Encode the data
        encoded_df = encode_data(df, le, oe)
    # 4. Train the model
        gbc = train_model(encoded_df)

        x_pred = [odor, 
                    gill_size, 
                    gill_color, 
                    stalk_surface_above_ring, 
                    stalk_surface_below_ring, 
                    stalk_color_above_ring, 
                    stalk_color_below_ring, 
                    ring_type, 
                    spore_print_color]
    
    # 5. Make a prediction
        pred = predict(gbc, oe, x_pred)
    # 6. Format the prediction to be a nice text
        if pred == 1:
            pred_text = 'The mushroom is poisonous'
        else:
            pred_text = 'The mushroom is edible'
    # 7. Output it to the screen
        st.write(pred_text)
    


