import streamlit as st
import pandas as pd
import markdown

from df_parsing_connected_components import parse_df_connected_components

st.title("Compare CSV and Other Content")

# Create two columns
col1, col2 = st.columns(2)

# --- Left column: CSV viewer ---
with col1:
    st.header("CSV Viewer")
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.dataframe(df)  # scrollable spreadsheet

# --- Right column: Parsed Table Results ---
with col2:
    st.header("Parsed Table Results")

    # Button to execute function
    if st.button("Run Function"):
        sections = parse_df_connected_components(uploaded_file)

        # display the results in markdown
        # sections[0] --> assuming single sheet
        for section in sections[0]:
            title, section, idx, markdown_table = section
            st.subheader(f"{title} - {section}")
            st.markdown(markdown_table)