import os
from pathlib import Path 
from logging.config import fileConfig 
import logging 
import streamlit as st
import json
from modules import single_text_analysis_builder, bulk_analysis_builder

os.chdir(Path(__file__).parent)
fileConfig("./logging.ini")

with open("config.json", "r") as f:
    config = json.load(f)

logger = logging.getLogger("frontend")

URL = config.get("api_url")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("",
        ("Single Text Analysis", "Bulk Analysis")
    )
    if page == "Single Text Analysis":
        single_text_analysis_builder(URL)
    elif page == "Bulk Analysis":
        bulk_analysis_builder(URL)

if __name__ == "__main__":
    main()
    

