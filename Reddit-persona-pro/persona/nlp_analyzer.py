# reddit-persona-pro/persona/nlp_analyzer.py

from transformers import pipeline
import torch
from typing import List, Dict, Any


class NLPAnalyzer:
    def __init__(self):
        """
        Initializes NLP pipelines using HuggingFace transformers.
        Automatically selects GPU if available.
        """
        device = 0 if torch.cuda.is_available() else -1
        self.ner_pipeline = pipeline("ner", device=device)
        self.sentiment_pipeline = pipeline("sentiment-analysis", device=device)
        self.topic_pipeline = pipeline("zero-shot-classification", device=device)

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract named entities from a single piece of text.

        Args:
            text: Input text.

        Returns:
            A list of dictionaries containing entities.
        """
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

    def analyze_sentiments_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze sentiment for a batch of text chunks.

        Args:
            texts: List of input text strings.

        Returns:
            List of sentiment results for each text.
        """
        try:
            return self.sentiment_pipeline(texts)
        except Exception as e:
            print(f"Error in batch sentiment: {e}")
            return [{'label': 'NEUTRAL', 'score': 0.5} for _ in texts]

    def extract_topics_batch(self, texts: List[str]) -> List[List[Dict[str, Any]]]:
        """
        Extract topics using zero-shot classification for a batch of text inputs.

        Args:
            texts: List of text chunks.

        Returns:
            List of topic lists per input text.
        """
        try:
            candidate_topics = [
                "technology", "gaming", "sports", "politics",
                "entertainment", "science", "education", "business",
                "travel", "food", "health", "relationships"
            ]
            results = self.topic_pipeline(texts, candidate_topics, multi_label=True)

            # Ensure uniform handling
            if isinstance(results, dict):
                results = [results]

            return [[
                {'topic': label, 'score': score}
                for label, score in zip(r['labels'], r['scores'])
            ] for r in results]

        except Exception as e:
            print(f"Error in topic batch: {e}")
            return [[] for _ in texts]
