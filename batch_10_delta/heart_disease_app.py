# -*- coding: utf-8 -*-

import numpy as np
import pickle
from flask import Flask, request, render_template, redirect, url_for

# Load your ML model
model = pickle.load(open('model.pkl', 'rb'))

# Create application
app = Flask(__name__)

# Dummy user data for authentication
users = {'user@example.com': 'password123'}

# Bind login function to URL
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid Credentials. Please try again.")
    return render_template('login.html')

# Bind home function to URL (after login)
@app.route('/home')
def home():
    return render_template('Heart Disease Classifier.html')

# Bind predict function to URL
@app.route('/predict', methods=['POST'])
def predict():
    # Put all form entries values in a list 
    features = [float(i) for i in request.form.values()]
    # Convert features to array
    array_features = [np.array(features)]
    # Predict features
    prediction = model.predict(array_features)
    
    # Check the output values and return the result based on prediction
    if prediction == 1:
        result = 'The patient is not likely to have heart disease!'
    else:
        result = 'The patient is likely to have heart disease!'
    
    return render_template('Heart Disease Classifier.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
