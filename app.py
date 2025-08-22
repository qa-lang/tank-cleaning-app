import streamlit as st

qa_data = [
    {"question": "What is the recommended procedure for cleaning a fuel tank?", 
     "answer": "The recommended procedure includes draining the tank, removing sludge, washing with appropriate solvents, and drying thoroughly."},
    {"question": "Which chemicals are used for tank cleaning?", 
     "answer": "Common chemicals include caustic soda, detergents, and specialized tank cleaning agents depending on the tank contents."},
    {"question": "How often should a storage tank be cleaned?", 
     "answer": "It depends on the tank usage, but typically every 1 to 5 years or as per regulatory requirements."},
    {"question": "What safety precautions should be taken during tank cleaning?", 
     "answer": "Use personal protective equipment, ensure proper ventilation, and follow confined space entry protocols."},
    {"question": "Can tank cleaning be automated?", 
     "answer": "Yes, automated systems like rotary jet heads and CIP systems are commonly used for efficient cleaning."},
]

def search_qa(query):
    query_lower = query.lower()
    results = []
    for item in qa_data:
        if query_lower in item["question"].lower() or query_lower in item["answer"].lower():
            results.append(item)
    return results

st.title("Tank Cleaning Q&A App")
st.write("Search for answers related to tank cleaning procedures, chemicals, safety, and more.")

search_query = st.text_input("Enter your question or keyword:")

if search_query:
    matched_results = search_qa(search_query)
    if matched_results:
        st.subheader("Search Results:")
        for result in matched_results:
            st.markdown(f"**Q:** {result['question']}")
            st.markdown(f"**A:** {result['answer']}")
            st.markdown("---")
    else:
        st.warning("No matching results found. Please try a different keyword.")

if st.checkbox("Show all Q&A"):
    st.subheader("All Questions and Answers:")
    for item in qa_data:
        st.markdown(f"**Q:** {item['question']}")
        st.markdown(f"**A:** {item['answer']}")
        st.markdown("---")
