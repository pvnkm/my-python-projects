import pandas as pd
from tensorflow.keras.models import load_model
import pickle
import tensorflow as tf
import numpy as np
import streamlit as st
import keras


### load the trained model, 
model = load_model('model.h5')

#load encoders and decoders
with open('label_encoder_gender.pkl','rb') as file:
    label_encoder_gender = pickle.load(file)

with open('onehot_encoder_geo.pkl','rb') as file:
    onehot_encoder_geo = pickle.load(file)

#load scaler
with open('scaler.pkl','rb') as file:
    scaler = pickle.load(file)

##Streamlit app

st.title("Customer Churn Prediction")

# user input
geography = st.selectbox('Geography',onehot_encoder_geo.categories_[0])
gender = st.selectbox('Gender',label_encoder_gender.classes_)
age = st.slider('Age',18,92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input("Estimated Salary")
tenure = st.slider('Tenure',0,10)
num_of_products = st.slider('Number of Products',1,4)
has_cr_card = st.selectbox('Has Credit Card',[0,1])
is_active_member = st.selectbox("Is Active Member",[1,0])

#Prepare input data
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [label_encoder_gender.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
})

#onehot encode geography
geo_encoded = onehot_encoder_geo.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded,columns=onehot_encoder_geo.get_feature_names_out(['Geography']))

## concat onehot encoder and input data
input_df = pd.concat([input_data.reset_index(drop=True),geo_encoded_df],axis=1)

#scale the input data
input_scaler = scaler.transform(input_df)

#predict churn

prediction = model.predict(input_scaler)
prediction_prob = prediction[0][0]

st.write(f"Churn Probability : {prediction_prob:.2f}")

if prediction_prob >0.5:
    st.write("The customer is likely to churn.")
else:
    st.write("The customer is not likely to churn.")