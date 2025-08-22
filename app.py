
import streamlit as st
import fitz  # PyMuPDF
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Load and parse PDFs
@st.cache_data
def load_pdf_text(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Split text into chunks
def split_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# Embed text chunks
@st.cache_resource
def embed_chunks(chunks, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(chunks, show_progress_bar=True)
    return model, embeddings

# Build FAISS index
def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index

# Search FAISS index
def search_index(query, model, index, chunks, top_k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    return [chunks[i] for i in indices[0]]

# Load documents
hm50_text = load_pdf_text("HM50Guidelines-6th_Edition-unlocked 1.pdf")
tankcleaning_text = load_pdf_text("Tankcleanig memos.pdf")
combined_text = hm50_text + "\n" + tankcleaning_text
# Sidebar filters
st.sidebar.header("Filters")
cargo_type = st.sidebar.text_input("Cargo Type")
cleaning_method = st.sidebar.text_input("Cleaning Method")
matrix_used = st.sidebar.text_input("Matrix Used")
inspection_result = st.sidebar.text_input("Inspection Result")

# Apply filters
filtered_text = combined_text
if cargo_type:
    filtered_text = "\n".join([line for line in filtered_text.split("\n") if cargo_type.lower() in line.lower()])
if cleaning_method:
    filtered_text = "\n".join([line for line in filtered_text.split("\n") if cleaning_method.lower() in line.lower()])
if matrix_used:
    filtered_text = "\n".join([line for line in filtered_text.split("\n") if matrix_used.lower() in line.lower()])
if inspection_result:
    filtered_text = "\n".join([line for line in filtered_text.split("\n") if inspection_result.lower() in line.lower()])

# Split and embed
chunks = split_text(filtered_text)
model, embeddings = embed_chunks(chunks)
index = build_faiss_index(np.array(embeddings))

# Main interface
st.title("Tank Cleaning Q&A App (Semantic Search)")
query = st.text_input("Ask a question about tank cleaning procedures:")

if query:
    results = search_index(query, model, index, chunks)
    st.subheader("Top Results")
    for res in results:
        st.write(res)
