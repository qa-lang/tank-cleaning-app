
import streamlit as st
import fitz  # PyMuPDF

# Load and parse PDFs
@st.cache_data

def load_pdf_text(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

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

    if cargo_type:
        combined_text = "
".join([line for line in combined_text.split("
") if cargo_type.lower() in line.lower()])
    if cleaning_method:
        combined_text = "
".join([line for line in combined_text.split("
") if cleaning_method.lower() in line.lower()])
    if matrix_used:
        combined_text = "
".join([line for line in combined_text.split("
") if matrix_used.lower() in line.lower()])
    if inspection_result:
        combined_text = "
".join([line for line in combined_text.split("
") if inspection_result.lower() in line.lower()])

    results = [line for line in combined_text.split("
") if query.lower() in line.lower()]
    st.subheader("Results")
    for res in results:
        st.write(res)
