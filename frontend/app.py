import streamlit as st
import requests
from io import BytesIO
import time
import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")

st.set_page_config(
    page_title="RAG Research Assistant",
    page_icon="RAG",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #374151;
        margin-top: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #D1FAE5;
        border-radius: 0.5rem;
        border-left: 4px solid #10B981;
    }
    .info-box {
        padding: 1rem;
        background-color: #DBEAFE;
        border-radius: 0.5rem;
        border-left: 4px solid #3B82F6;
    }
    .stButton > button {
        width: 100%;
    }
    .api-url-display {
        font-family: monospace;
        background-color: #F3F4F6;
        padding: 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.9rem;
        word-break: break-all;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">RAG Research Assistant</h1>', unsafe_allow_html=True)

# Sidebar for navigation and configuration
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Upload Documents", "Query Assistant", "View Document Chunks"]
)

# Configuration in sidebar
st.sidebar.markdown("---")
st.sidebar.title("Configuration")

# API URL configuration using session state
if 'api_base_url' not in st.session_state:
    st.session_state.api_base_url = DEFAULT_API_URL

with st.sidebar.expander("⚙️ API Settings", expanded=False):
    api_url = st.text_input(
        "Backend API URL",
        value=st.session_state.api_base_url,
        help="URL of your FastAPI backend (e.g., http://localhost:8000/api/v1)"
    )
    
    if st.button("Update API URL"):
        st.session_state.api_base_url = api_url
        st.success(f"API URL updated to: {api_url}")
        st.rerun()
    
    st.markdown(f"""
    **Current API URL:**
    <div class="api-url-display">{st.session_state.api_base_url}</div>
    """, unsafe_allow_html=True)

# Helper function for API calls
def call_api(endpoint, method="GET", data=None, files=None):
    """Generic API call helper"""
    url = f"{st.session_state.api_base_url}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, params=data)
        elif method == "POST":
            if files:
                response = requests.post(url, files=files)
            else:
                response = requests.post(url, json=data)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to backend API at: {url}")
        st.info("Please check if your FastAPI backend is running and the API URL is correct.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        if hasattr(e, 'response') and e.response:
            st.error(f"Response: {e.response.text}")
        return None

# Page 1: Upload Documents
if page == "Upload Documents":
    st.markdown('<h2 class="sub-header">Upload PDF Documents</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type="pdf",
            help="Upload PDF documents for processing"
        )
        
        if uploaded_file is not None:
            # Display file info
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size / 1024:.2f} KB",
                "File type": uploaded_file.type
            }
            
            st.write("**File Details:**")
            st.json(file_details)
            
            # Preview first page (optional)
            try:
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.getvalue()))
                num_pages = len(pdf_reader.pages)
                st.info(f"📄 Document has {num_pages} pages")
            except:
                pass
    
    with col2:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.write("**Upload Instructions:**")
        st.write("1. Select a PDF file")
        st.write("2. Click 'Upload & Process'")
        st.write("3. Wait for processing to complete")
        st.write("4. Get Document ID for future queries")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Upload button
    if uploaded_file is not None and st.button("Upload & Process", type="primary"):
        with st.spinner("Processing document..."):
            # Prepare file for upload
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            
            # Call FastAPI upload endpoint
            result = call_api("/upload", method="POST", files=files)
            
            if result:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("Document processed successfully!")
                st.write(f"**Document ID:** `{result.get('document_id')}`")
                st.write(f"**Number of chunks:** {result.get('chunks')}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Store document ID in session state for easy access
                if 'document_ids' not in st.session_state:
                    st.session_state.document_ids = []
                st.session_state.document_ids.append(result.get('document_id'))
                
                # Copy to clipboard button
                doc_id = result.get('document_id')
                if doc_id:
                    st.code(f"Document ID: {doc_id}", language="text")

# Page 2: Query Assistant
elif page == "Query Assistant":
    st.markdown('<h2 class="sub-header">Query Your Documents</h2>', unsafe_allow_html=True)
    
    # Document ID selection (with stored IDs if available)
    if 'document_ids' in st.session_state and st.session_state.document_ids:
        doc_options = ["All Documents"] + st.session_state.document_ids
        selected_doc = st.selectbox(
            "Select Document (Optional)",
            options=doc_options,
            help="Choose a specific document to query, or 'All Documents' to search all"
        )
        doc_id_input = selected_doc if selected_doc != "All Documents" else ""
    else:
        doc_id_input = st.text_input(
            "Document ID (Optional)",
            help="If you want to query a specific document, enter its ID. Leave empty to search all documents."
        )
    
    # Query input
    query = st.text_area(
        "Your Question",
        height=100,
        placeholder="Enter your question here...\nExample: What are the key findings in the document?",
        help="Ask any question based on your uploaded documents"
    )
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Advanced options
        with st.expander("Advanced Options"):
            top_k = st.slider("Number of relevant chunks", 1, 10, 4)

    
    with col2:
        # Query button
        if st.button("Get Answer", type="primary"):
            if not query.strip():
                st.warning("Please enter a question")
            else:
                with st.spinner("Searching documents and generating answer..."):
                    # Call FastAPI query endpoint
                    data = {"question": query}
                    result = call_api("/query", method="POST", data=data)
                    
                    if result:
                        answer = result.get("answer", "No answer generated")
                        
                        # Display answer
                        st.markdown("### Answer")
                        st.markdown(f'<div style="padding: 1rem; background-color: #F3F4F6; border-radius: 0.5rem;">{answer}</div>', unsafe_allow_html=True)
                        


# Page 3: View Document Chunks
elif page == "View Document Chunks":
    st.markdown('<h2 class="sub-header">View Document Chunks</h2>', unsafe_allow_html=True)
    
    # Document ID input with dropdown if available
    if 'document_ids' in st.session_state and st.session_state.document_ids:
        selected_doc = st.selectbox(
            "Select Document",
            options=st.session_state.document_ids,
            help="Choose a document to view its chunks"
        )
        doc_id = selected_doc
    else:
        doc_id = st.text_input(
            "Enter Document ID",
            placeholder="Paste your document ID here",
            help="Get the document ID from the upload page"
        )
    
    if doc_id:
        if st.button("Load Chunks"):
            with st.spinner("Loading document chunks..."):
                # Call FastAPI chunks endpoint
                result = call_api(f"/chunks/{doc_id}", method="GET")
                
                if result is not None:
                    if len(result) > 0:
                        st.success(f"Found {len(result)} chunks")
                        
                        # Display chunks in an expandable format
                        for i, chunk in enumerate(result):
                            with st.expander(f"Chunk {chunk.get('index', i) + 1}"):
                                st.text_area(
                                    f"Content {chunk.get('index', i) + 1}",
                                    chunk.get('text', ''),
                                    height=150,
                                    key=f"chunk_{doc_id}_{i}"
                                )
                        
                        # Statistics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Chunks", len(result))
                        with col2:
                            avg_length = sum(len(c.get('text', '').split()) for c in result) / len(result)
                            st.metric("Avg Words per Chunk", f"{avg_length:.1f}")
                        with col3:
                            total_words = sum(len(c.get('text', '').split()) for c in result)
                            st.metric("Total Words", total_words)
                    else:
                        st.warning("No chunks found for this document ID")

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
    <p>RAG Research Assistant v1.0 | Built with FastAPI & Streamlit</p>
    <p>API running at: <code>{st.session_state.api_base_url}</code></p>
    </div>
    """,
    unsafe_allow_html=True
)

# API status check in sidebar
if st.sidebar.checkbox("Check API Status"):
    try:
        response = requests.get(st.session_state.api_base_url.replace("/api/v1", "/docs"), timeout=3)
        if response.status_code == 200:
            st.sidebar.success("Backend API is running")
        else:
            st.sidebar.info(f"Backend responded with status: {response.status_code}")
    except requests.exceptions.RequestException:
        st.sidebar.error("Cannot connect to backend API")

# Clear session button
if st.sidebar.button("Clear Session"):
    st.session_state.clear()
    st.rerun()