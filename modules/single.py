import streamlit as st
import logging
from utils import RequestHandler
from utils import SentimentCategorizer as sc
import pandas as pd
import altair as alt


logger = logging.getLogger("frontend")

def sentiment_text(polarity: str, subjectivity: str, confidence: str):
    """Display the sentiment analysis results in a formatted way.
    
    Args:
        polarity (str): The sentiment polarity.
        subjectivity (str): The sentiment subjectivity.
        confidence (str): The confidence level of the analysis."""
    st.write(f"The sentiment is {polarity}.")
    st.write(f"It is formulated {subjectivity}")
    st.write(f"The sentient machine is {confidence} in this analysis.\n\n")

def build_graph(full_text_result, per_sentence_result):
    """Builds a bar chart to visualize the sentiment analysis results.

    Args:
        full_text_result (dict): _full text analysis results including polarity, subjectivity, and confidence.
        per_sentence_result (dict): _per sentence analysis results including average polarity, average subjectivity, and confidence.
    """
    polarity, subjectivity, confidence = 0, 0, 0
    if per_sentence_result or full_text_result:
        if full_text_result:
            confidence = full_text_result["confidence_nr"]
            polarity = full_text_result["polarity_nr"]
            subjectivity = full_text_result["subjectivity_nr"]
        elif per_sentence_result:
            confidence = per_sentence_result["confidence_nr"]
            polarity = per_sentence_result["average_polarity"]
            subjectivity = per_sentence_result["average_subjectivity"]

        chart_data = pd.DataFrame({
                "Metric": ["Polarity", "Subjectivity", "Confidence"],
                "Value": [polarity, subjectivity, confidence]
            })

        color_map = { 
                "Polarity": "#1f77b4" if polarity >= 0.0 else "#d62728", 
                "Subjectivity": "#2ca02c",
                "Confidence": "#ff7f0e"
            }

        chart = alt.Chart(chart_data).mark_bar().encode(
                x=alt.X("Metric", sort=None),
                y=alt.Y("Value", scale=alt.Scale(domain=[-1, 1])),
                color=alt.Color("Metric", scale=alt.Scale(domain=list(color_map.keys()), range=list(color_map.values())), legend=None)
            ).properties(height=300)
        
        st.altair_chart(chart, use_container_width=True)

def display_sentiment_analysis_results(full_text_result, per_sentence_result, col3):
    """Display the results of the sentiment analysis."""
    if full_text_result:
        try:
            with col3:
                sentiment_text(full_text_result["polarity"], full_text_result["subjectivity"], full_text_result["confidence"])
        except Exception as e:
            logger.error(f"An error occured: {e}")
            st.error("An error occurred while processing the full text analysis results.")
    if per_sentence_result:
        try:
            with col3:
                sentiment_text(per_sentence_result["polarity"], per_sentence_result["subjectivity"], per_sentence_result["confidence"]) 
            st.markdown("""### Per Sentence Analysis Results""" )

            st.markdown(f"""
                        | | value | 
                |--- | ---|
                |Average Polarity | {per_sentence_result['average_polarity']}|
                |Sum of Polarities | {per_sentence_result['sum_of_polarities']}|
                |Average Subjectivity | {per_sentence_result['average_subjectivity']}|
                |Sum of Subjectivities | {per_sentence_result['sum_of_subjectivities']}|
                |Total Sentences | {per_sentence_result['total_sentences']}|
                |Confidence | {per_sentence_result["confidence_nr"]}|
            """)
        except Exception as e:
            logger.error(f"An error occured: {e}")
            st.error("An error occurred while processing the per sentence analysis results.")

def analyze_per_sentence_button(request_handler, text, per_sentence_result=None):
    """Handles the per sentence analysis button click.

    Args:
        request_handler (RequestHandler): The request handler to make API calls.
        text (str): text to be analyzed.
        per_sentence_result (_type_, optional): Placeholder for the return value. Defaults to None.

    Returns:
        dict: per sentence analysis results including polarity, subjectivity, confidence, average polarity, sum of polarities, average subjectivity, sum of subjectivities, total sentences, and confidence number.
    """
    if text:
        result = request_handler.analyse_text_per_sentence(text)
        average_polarity = result["result"]["average_polarity"]
        sum_of_polarities = result["result"]["sum_of_polarities"]
        average_subjectivity = result["result"]["average_subjectivity"]
        sum_of_subjectivities = result["result"]["sum_of_subjectivities"]
        total_sentences = result["result"]["total_sentences"]
        confidence_nr = result["confidence"]

        polarity = sc.categorize_polarity(average_polarity)
        subjectivity = sc.categorize_subjectivity(average_subjectivity)
        confidence = sc.categorize_confidence(result["confidence"])
            
        per_sentence_result = { "polarity": polarity,
                                    "subjectivity": subjectivity,
                                    "confidence": confidence,
                                    "average_polarity": average_polarity,
                                    "sum_of_polarities": sum_of_polarities,
                                    "average_subjectivity": average_subjectivity,
                                    "sum_of_subjectivities": sum_of_subjectivities,
                                    "total_sentences": total_sentences,
                                    "confidence_nr": confidence_nr }
    else:
        st.error("Please enter some text to analyze.")
    return per_sentence_result

def analyze_full_text_button(request_handler, text, full_text_result=None):
    """Handles the full text analysis button click.

    Args:
        request_handler (RequestHandler): handler to make API calls.
        text (str): text to be analyzed.
        full_text_result (dict, optional): Placeholder . Defaults to None.

    Returns:
        dict: full text analysis results including polarity, subjectivity, confidence, and their numerical values.
    """
    if text:
        result = request_handler.analyse_full_text(text)

        polarity = sc.categorize_polarity(result["result"]["polarity"])
        subjectivity = sc.categorize_subjectivity(result["result"]["subjectivity"])
        confidence = sc.categorize_confidence(result["confidence"])
        polarity_nr = result["result"]["polarity"]
        subjectivity_nr = result["result"]["subjectivity"]
        confidence_nr = result["confidence"]

        full_text_result = { "polarity": polarity,
                                     "subjectivity": subjectivity,
                                     "confidence": confidence,
                                     "polarity_nr": polarity_nr,
                                     "subjectivity_nr": subjectivity_nr,
                                     "confidence_nr": confidence_nr }
                
        
    else:
        st.error("Please enter some text to analyze.")
    return full_text_result

def single_text_analysis_builder(URL: str):
    """Builds the single text analysis page.
    Args:
        URL (str): The API URL to send requests to.
    """
    request_handler = RequestHandler(url=URL)
    full_text_result = None
    per_sentence_result = None

    col1, col2, col3 = st.columns(3, vertical_alignment="center")

    with col1:
        text = st.text_area("", placeholder="Enter text to analyze", height=300, label_visibility="collapsed")

    st.sidebar.title("Single Text Analysis")

    if st.sidebar.button("Analyze Full Text"):
        full_text_result = analyze_full_text_button(request_handler, text)
    
    if st.sidebar.button("Analyze Per Sentence"):
        per_sentence_result = analyze_per_sentence_button(request_handler, text)

    display_sentiment_analysis_results(full_text_result, per_sentence_result, col3)
    
    with col2:
        build_graph(full_text_result, per_sentence_result)
