import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Sample Q&A dataset
qa_data = [
    {"question": "How to clean a tank after diesel?", "answer": "Use a degreaser and rinse thoroughly with water."},
    {"question": "How to clean a tank after ethanol?", "answer": "Flush with water and use a neutralizing agent."},
    {"question": "How to clean a tank after gasoline?", "answer": "Ventilate the tank, use a solvent cleaner, and rinse with water."},
    {"question": "What safety measures are needed during tank cleaning?", "answer": "Wear protective gear and ensure proper ventilation."},
    {"question": "How to dispose of tank cleaning waste?", "answer": "Follow local hazardous waste disposal regulations."}
]

# Extract questions for vectorization
questions = [item["question"] for item in qa_data]

# Initialize TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(questions)

# Streamlit UI
st.title("Tank Cleaning Q&A App")
query = st.text_input("Enter your question:")

if query:
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    best_match_idx = np.argmax(similarities)
    best_score = similarities[best_match_idx]

    if best_score > 0.3:
        st.subheader("Answer:")
        st.write(qa_data[best_match_idx]["answer"])
    else:
        st.warning("No matching results found. Please try a different keyword.")
