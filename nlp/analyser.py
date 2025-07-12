from textblob import TextBlob
import logging

logger = logging.getLogger("backend")

class SentimentAnalyser:
    def __init__(self):
        logger.info("SentimentAnalyser initialized.")

    def analyse_text_full(self, text: str) -> dict:
        """analysis full text sentiment with TextBlob

        Args:
            text (str): takes a string of a text to be analysed

        Returns:
            dict: returns a dictionary with the polarity and subjectivity of the text
        """
        try:
            blob = TextBlob(text)
            logger.info("Starting full text analysis.")
            full_text_analysis = {
                "polarity": blob.sentiment.polarity, #type:ignore
                "subjectivity": blob.sentiment.subjectivity, #type:ignore
            }
            logger.info("Full text analysis completed successfully.")
        except Exception as e:
            logger.warning(f"Warning, unable to analyze text: {e}")
            full_text_analysis = {
                "polarity": None,
                "subjectivity": None,
            }   
        return full_text_analysis
    
    def analyse_text_per_sentence(self, text: str) -> dict:
        """Analyses a test sentence by sentence using TextBlob.

        Args:
            text (str): string to be analysed

        Returns:
            dict: returns a dictionary with the average polarity and subjectivity of the text, as well as the sum of polarities and subjectivities, and the total number of sentences.
        """
        try:
            logger.info("Starting per sentence text analysis.")
            blob = TextBlob(text)
            polarities = 0.0
            subjectivities = 0.0

            for sentence in blob.sentences: #type: ignore
                polarities += sentence.sentiment.polarity
                subjectivities += sentence.sentiment.subjectivity
            
            average_polarity = polarities / len(blob.sentences) if len(blob.sentences) > 0 else 0 #type:ignore
            average_subjectivity = subjectivities / len(blob.sentences) if len(blob.sentences) > 0 else 0 #type:ignore

            per_sentence_analysis = {
                "average_polarity": average_polarity,
                "sum_of_polarities": polarities,
                "average_subjectivity": average_subjectivity,
                "sum_of_subjectivities": subjectivities,
                "total_sentences": len(blob.sentences) #type:ignore
            }
            logger.info("Per sentence text analysis completed successfully.")
        except Exception as e:
            logger.warning(f"Warning, unable to analyze text per sentence: {e}")
            per_sentence_analysis = {
                "average_polarity": None,
                "sum_of_polarities": None,
                "average_subjectivity": None,
                "sum_of_subjectivities": None,
                "total_sentences": 0
            }
        return per_sentence_analysis
    
    def sentiment_confidence_score(self, text):
        """Calculate the sentiment confidence score of the text.
        Score is calculated as the ratio of sentiment words to total words.

        Args:
            text (str): the text to analyze

        Returns:
            float: sentiment confidence score 0-1
        """
        blob = TextBlob(text)
        sentiment_words = [word for word in blob.words if TextBlob(word).sentiment.polarity != 0] #type: ignore
        return len(sentiment_words) / len(blob.words) if blob.words else 0 #type: ignore

if __name__ == "__main__":
    print("TextBlob sentiment analysis completed.")
