import joblib
class PhishingURLDetector:
    def __init__(self, phishingDetectionModel, phishingVectorizer):
        # Load the trained model and the TF-IDF vectorizer
        try:
            self.model = joblib.load(phishingDetectionModel)
            self.vectorizer = joblib.load(phishingVectorizer)
        except:
            print("Error loading model and vectorizer")
           

    def is_phishing_url(self, url):
        url_tfidf = self.vectorizer.transform([url])  # Convert URL to TF-IDF features
        prediction = self.model.predict(url_tfidf)  # Predict using the trained model
        return prediction[0] == 1 # Return True if the prediction is phishing, False otherwise


