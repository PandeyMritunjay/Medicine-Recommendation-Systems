import streamlit as st
import pandas as pd
import pickle

# Load the data and similarity matrix
medicines_dict = pickle.load(open('medicine_dict.pkl', 'rb'))
medicines = pd.DataFrame(medicines_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to recommend medicines
def recommend(medicine):
    try:
        medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
        distances = similarity[medicine_index]
        medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended_medicines = [medicines.iloc[i[0]].Drug_Name for i in medicines_list]
        return recommended_medicines
    except IndexError:
        return ["Medicine not found. Please try another."]

# Add custom CSS for styling
def add_custom_css():
    st.markdown(
        """
        <style>
        /* Body styling with pink background */
        body {
            background-color: #ffc0cb; /* Light pink background */
            color: black;
            font-family: Arial, sans-serif;
        }

        /* Container styling */
        .container {
            background-color: rgba(255, 255, 255, 0.9);  /* White background with slight transparency */
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
            margin-top: 50px;
            text-align: center;
        }

        /* Heading Styling */
        h1 {
            font-size: 2.5rem;
            color: black; /* Black color for heading */
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2); /* Subtle shadow */
            margin-bottom: 20px;
        }

        /* Selectbox Styling */
        .stSelectbox > div {
            color: black;
        }

        /* Button Styling */
        .stButton button {
            background-color: #ff6f61;
            color: white;
            font-size: 1rem;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            transition: 0.3s;
        }

        .stButton button:hover {
            background-color: #e55039;
        }

        /* Results Styling */
        .results {
            margin-top: 20px;
        }

        .results ul {
            list-style: none;
            padding: 0;
        }

        .results li {
            background: rgba(255, 255, 255, 0.9);
            color: black;
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            text-align: left;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Add custom CSS
add_custom_css()

# Streamlit UI
st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown("<h1>💊 Medicine Recommendation System</h1>", unsafe_allow_html=True)

# Dropdown for user to select a medicine
medicine_options = medicines['Drug_Name'].tolist()
selected_medicine = st.selectbox("Select a Medicine:", options=medicine_options)

# Button to get recommendations
if st.button("Recommend"):
    st.markdown('<div class="results">', unsafe_allow_html=True)
    if selected_medicine:
        st.write("### Recommended Medicines:")
        recommendations = recommend(selected_medicine)
        st.markdown("<ul>", unsafe_allow_html=True)
        for med in recommendations:
            st.markdown(f"<li>{med}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)
    else:
        st.error("Please select a valid medicine.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
