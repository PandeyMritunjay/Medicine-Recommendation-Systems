from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__, template_folder="templates", static_folder="static")

# Load the data and similarity matrix
medicines_dict = pickle.load(open('medicine_dict.pkl', 'rb'))
medicines = pd.DataFrame(medicines_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to recommend medicines based on input medicine
def recommend(medicine):
    try:
        # Get the index of the medicine in the dataset
        medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
        distances = similarity[medicine_index]
        # Sort medicines by similarity score and exclude the first one (itself)
        medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        # Extract medicine names for the recommendations
        recommended_medicines = [medicines.iloc[i[0]].Drug_Name for i in medicines_list]
        return recommended_medicines
    except IndexError:
        return ["Medicine not found. Please try another."]

@app.route('/')
def index():
    # Pass all medicine names for the dropdown in the UI
    medicine_options = list(medicines['Drug_Name'])
    return render_template('index.html', medicines=medicine_options)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    try:
        # Get input medicine from the user
        user_input = request.json.get('input', '').strip()
        if not user_input:
            return jsonify({"recommendations": ["Please provide a valid input."]})
        # Get recommendations for the input medicine
        recommended_medicines = recommend(user_input)
        return jsonify({"recommendations": recommended_medicines})
    except Exception as e:
        return jsonify({"recommendations": [f"Error occurred: {str(e)}"]})

if __name__ == '__main__':
    app.run(debug=True)
