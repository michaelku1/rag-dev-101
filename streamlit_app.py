import streamlit as st
import pandas as pd
import markdown
from parsers.parser_factory import ParserFactory

def process_file(file_path: str, file_type: str):
    pipeline = ParserFactory.get_pipeline(file_type)
    text = pipeline.run(file_path)
    # send text into embeddings/vector DB
    return text

def analyze_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return None
    
    # Get full file name
    file_name = uploaded_file.name  
    
    # Split into name + extension
    base_name, extension = os.path.splitext(file_name)

    file_info = {
        "file_name": file_name,
        "base_name": base_name,
        "file_type": extension.lower()
    }


    return uploaded_file, file_info

st.title("Compare CSV and Other Content")

# Create two columns
col1, col2 = st.columns(2)

uploaded_file_ = None

# --- Left column: CSV viewer ---
with col1:
    st.header("CSV Viewer")
    uploaded_file, file_info = analyze_uploaded_file(st.file_uploader("Upload an Excel file", type=["xlsx", "xls"]))
    # st.write("📂 File Info:")
    uploaded_file_ = uploaded_file
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.dataframe(df)  # scrollable spreadsheet

# --- Right column: Parsed Table Results ---
with col2:
    st.header("Parsed Table Results")

    # Button to execute function
    if st.button("Run Function"):
        sections = process_file(uploaded_file_, file_info['file_type'])

        # display the results in markdown
        # sections[0] --> assuming single sheet
        for section in sections[0]:
            title, section, idx, markdown_table = section
            st.subheader(f"{title} - {section}")
            st.markdown(markdown_table)