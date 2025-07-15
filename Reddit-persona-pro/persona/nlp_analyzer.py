# reddit-persona-pro/persona/nlp_analyzer.py

from transformers import pipeline
import torch

class NLPAnalyzer:
    def __init__(self):
        device = 0 if torch.cuda.is_available() else -1
        self.ner_pipeline = pipeline("ner", device=device)
        self.sentiment_pipeline = pipeline("sentiment-analysis", device=device)
        self.topic_pipeline = pipeline("zero-shot-classification", device=device)

    def extract_entities(self, text: str) -> list:
        """Extract named entities from text"""
        try:
            entities = self.ner_pipeline(text)
            return [{
                'entity': e['entity'],
                'word': e['word'],
                'score': e['score']
            } for e in entities]
        except Exception as e:
            print(f"Error in entity extraction: {e}")
            return []

    def analyze_sentiment(self, text: str) -> dict:
        """Analyze sentiment of text"""
        try:
            result = self.sentiment_pipeline(text)[0]
            return {
                'label': result['label'],
                'score': result['score']
            }
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return {'label': 'NEUTRAL', 'score': 0.5}

    def extract_topics(self, text: str) -> list:
        """Extract main topics from text using zero-shot classification"""
        try:
            candidate_topics = [
                "technology", "gaming", "sports", "politics", 
                "entertainment", "science", "education", "business",
                "travel", "food", "health", "relationships"
            ]
            result = self.topic_pipeline(
                text,
                candidate_topics,
                multi_label=True
            )
            return [{
                'topic': label,
                'score': score
            } for label, score in zip(result['labels'], result['scores'])]
        except Exception as e:
            print(f"Error in topic extraction: {e}")
            return []
