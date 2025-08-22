
import streamlit as st
import fitz  # PyMuPDF
from rapidfuzz import fuzz

# Load and parse PDFs
@st.cache_data
def load_pdf_text(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Fuzzy search function
def fuzzy_search(text, query, threshold=80):
    lines = text.split("\n")
    return [line for line in lines if fuzz.partial_ratio(query.lower(), line.lower()) > threshold]

# Optional: Highlight query in results
def highlight_query(text, query):
    return text.replace(query, f"**{query}**")

# Load documents
hm50_text = load_pdf_text("HM50Guidelines-6th_Edition-unlocked 1.pdf")
tankcleaning_text = load_pdf_text("Tankcleanig memos.pdf")

# Sidebar filters
st.sidebar.header("Filters")
cargo_type = st.sidebar.text_input("Cargo Type")
cleaning_method = st.sidebar.text_input("Cleaning Method")
matrix_used = st.sidebar.text_input("Matrix Used")
inspection_result = st.sidebar.text_input("Inspection Result")

# Main interface
st.title("Tank Cleaning Q&A App")
query = st.text_input("Ask a question about tank cleaning procedures:")

if query:
    combined_text = hm50_text + "\n" + tankcleaning_text

    # Apply filters
    if cargo_type:
        combined_text = "\n".join([line for line in combined_text.split("\n") if cargo_type.lower() in line.lower()])
    if cleaning_method:
        combined_text = "\n".join([line for line in combined_text.split("\n") if cleaning_method.lower() in line.lower()])
    if matrix_used:
        combined_text = "\n".join([line for line in combined_text.split("\n") if matrix_used.lower() in line.lower()])
    if inspection_result:
        combined_text = "\n".join([line for line in combined_text.split("\n") if inspection_result.lower() in line.lower()])

    # Fuzzy search
    results = fuzzy_search(combined_text, query)

    # Display results
    st.subheader("Results")
    if results:
        for res in results:
            st.markdown(highlight_query(res, query))
    else:
        st.write("No matching results found.")
