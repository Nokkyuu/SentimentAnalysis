import streamlit as st
import logging
from utils import RequestHandler
from utils import SentimentCategorizer as sc
import pandas as pd

logger = logging.getLogger("frontend")

def bulk_analysis_builder(URL: str):
    request_handler = RequestHandler(url=URL)
    st.title("Bulk Analysis")
    st.sidebar.title("Bulk Analysis")


    uploaded_file = st.sidebar.file_uploader("Upload CSV(Format: 1 Column, no Header)", type=["csv"])
    result_df = None

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, header=None, delimiter=";")
        if df.shape[1] != 1:
            st.error("CSV must have exactly one column containing text.")
            return
        logger.debug(f"CSV uploaded with {len(df)} rows.")
        analyzed_df = request_handler.analyse_full_text_bulk(df)
        analyzed_df['polarity_category'] = analyzed_df['polarity'].apply(sc.categorize_polarity)
        analyzed_df['subjectivity_category'] = analyzed_df['subjectivity'].apply(sc.categorize_subjectivity)
        analyzed_df['confidence_category'] = analyzed_df['confidence'].apply(sc.categorize_confidence)
        st.dataframe(analyzed_df, hide_index=True)

        
        csv = analyzed_df.to_csv(index=False,).encode('utf-8')
        st.sidebar.download_button(
            label="Download Results as CSV",
            
            data=csv,
            file_name="sentiment_results.csv",
            mime="text/csv"
        )
    else:
        st.write("Please upload a CSV file in the sidebar to begin analysis.")