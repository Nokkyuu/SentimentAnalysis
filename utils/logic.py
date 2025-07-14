import requests
import logging
import pandas as pd


logger = logging.getLogger("frontend")

class RequestHandler():
    """A class to handle requests to the sentiment analysis API."""
    def __init__(self, url: str = "http://localhost:8000"):
        """Initialize the RequestHandler with a base URL."""
        self.url = url
        logger.info(f"RequestHandler initialized with URL: {self.url}")

    def analyse_full_text(self, text: str) -> dict:
        """Send a request to analyze full text sentiment."""
        logger.info("Sending request to analyze full text.")
        params = {"type": "full"}
        json = {"text": text}
        response = requests.post(f"{self.url}/analyse", params=params, json=json)
        if response.status_code == 200:
            logger.info("Full text analysis completed successfully.")
            return response.json()
        else:
            logger.error(f"Error: {response.status_code} - {response.text}")
            return {"error": "Failed to analyze text."}

    def analyse_text_per_sentence(self, text: str) -> dict:
        """Send a request to analyze text sentiment per sentence."""
        logger.info("Sending request to analyze text per sentence.")
        params = {"type": "sentence"}
        json = {"text": text}
        response = requests.post(f"{self.url}/analyse", params=params, json=json)
        if response.status_code == 200:
            logger.info("Per sentence text analysis completed successfully.")
            return response.json()
        else:
            logger.error(f"Error: {response.status_code} - {response.text}")
            return {"error": "Failed to analyze text."}
    
    def analyse_full_text_bulk(self, df) -> pd.DataFrame:
        """Send a request to analyze full text sentiment for a DataFrame.

        Args:
            df (DataFrame): DataFrame containing a single column with text to be analyzed.

        Returns:
            DataFrame: a DataFrame with the results of the sentiment analysis.
        """
        logger.info("Sending request to analyze the whole DataFrame")
        texts = df.iloc[:, 0].tolist()
        logger.debug(f"Texts to analyze: {texts}")
        json = {"texts": texts}
        response = requests.post(f"{self.url}/analyse/bulk", json=json)
        if response.status_code == 200:
            logger.info("Full text analysis completed successfully. response: %s", response.json())
            analyzed_df = pd.DataFrame([
                {
                    "text": item["text"],
                    "polarity": item["result"]["polarity"],
                    "subjectivity": item["result"]["subjectivity"],
                    "confidence": item["confidence"]
                }
                for item in response.json()
            ])
            return analyzed_df
        else:
            logger.error(f"Error: {response.status_code} - {response.text}")
            logger.error("returning original DataFrame")
            return df

class SentimentCategorizer():
    """A class to categorize sentiment based on polarity."""
    
    @staticmethod
    def categorize_polarity(polarity: float,) -> str:
        """Categorize sentiment based on polarity and subjectivity.
        
        Args: 
            polarity (float): The polarity score of the text.   
            
        Returns:
            str: A string categorizing the sentiment."""
        logger.info("categoring polarity: %s", polarity)
        pol_categories = [
            (0.9, "overwhelmingly positive"),
            (0.5, "very positive"),
            (0.1, "positive"),
            (-0.1, "neutral"),
            (-0.5, "negative"),
            (-0.9, "very negative"),      
        ]
        for threshold, label in pol_categories:
            if polarity > threshold:
                return label
        logger.info("polarity successfully categorized.")
        return "overwhelmingly negative"
                 
    @staticmethod
    def categorize_subjectivity(subjectivity: float) -> str:
        """Categorize sentiment based on average polarity.
        
        Args:
            subjectivity (float): The subjectivity score of the text.
            
        Returns:
            str: A string categorizing the subjectivity."""
        logger.info("categorizing subjectivity: %s", subjectivity)
        sub_categories = [
            (0.9, "completely subjective"),
            (0.5, "mostly subjective"),
            (0.1, "slightly subjective"),
            (0.0, "objective")
        ]
        for threshold, label in sub_categories:
            if subjectivity > threshold:
                return label
        logger.info("subjectivity successfully categorized.")
        return "completely objective"
    
    @staticmethod
    def categorize_confidence(confidence: float,) -> str:
        """Categorize the confidence level of the sentiment analysis.
        
        Args: 
            confidence (float): The confidence score of the text.   
            
        Returns:
            str: A string categorizing the sentiment."""
        logger.info("categorizing confidence: %s", confidence)
        pol_categories = [
            #arbitary numbers, just a guess for now
            (0.9, "overwhelmingly confident"),
            (0.6, "very confident"),
            (0.3, "confident"),
            (0.2, "not very confident"),
            (0.1, "not confident")
        ]
        for threshold, label in pol_categories:
            if confidence > threshold:
                return label
        logger.info("confidence successfully categorized.")
        return "not confident at all"

if __name__ == "__main__":
    # testing the functions
    request_handler = RequestHandler(url="http://localhost:8000")
    text = "this is horrible. absolutely terrible. I love it. It's amazing!"
    full_analysis = request_handler.analyse_full_text(text)
    print("Full Analysis:", full_analysis)

    sentence_analysis = request_handler.analyse_text_per_sentence(text)
    print("Sentence Analysis:", sentence_analysis)
    
