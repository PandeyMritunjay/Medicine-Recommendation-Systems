from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import nltk
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import os

app = Flask(__name__, template_folder="templates")


medicines_dict = pickle.load(open('Project/Medicine Recommendation/medicine_dict.pkl','rb'))
medicines = pd.DataFrame(medicines_dict)
similarity = pickle.load(open('Project\Medicine Recommendation\similarity.pkl','rb'))

# Function to recommend medicines based on input medicine
def recommend(medicine):
    medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
    distances = similarity[medicine_index]
    medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_medicines = [medicines.iloc[i[0]].Drug_Name for i in medicines_list]
    return recommended_medicines

@app.route('/')
def index():
    medicine_options = list(medicines['Drug_Name'])
    return render_template('index.html', medicines=medicine_options)


@app.route('/recommend', methods=['POST'])
def get_recommendations():
    # Get input medicine from the user
    user_input = request.json['input']
    # Get recommendations for the input medicine
    recommended_medicines = recommend(user_input)
    # Return recommendations as JSON response
    return jsonify({"recommendations": recommended_medicines})

if __name__ == '__main__':
    app.run(debug=True)
