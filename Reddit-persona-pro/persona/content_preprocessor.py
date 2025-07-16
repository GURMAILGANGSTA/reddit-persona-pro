# reddit-persona-pro/persona/content_preprocessor.py

from typing import List, Dict, Tuple
import re
import uuid
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

class ContentPreprocessor:
    def __init__(self):
        self.chunk_size = 1000
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text: str) -> str:
        """Clean, normalize, and reduce text noise"""
        text = re.sub(r'http\S+|www\.\S+', '', text)  # remove URLs
        text = re.sub(r'\[.*?\]\(.*?\)', '', text)  # markdown links
        text = re.sub(r'[^\w\s.,!?-]', '', text)        # special characters
        text = re.sub(r'\s+', ' ', text).strip()        # whitespace cleanup
        return text

    def remove_stopwords(self, text: str) -> str:
        """Optional: Remove stopwords to focus on keywords"""
        words = word_tokenize(text)
        filtered = [word for word in words if word.lower() not in self.stop_words]
        return ' '.join(filtered)

    def chunk_content(self, content: str) -> List[str]:
        """Split content into token-length-safe chunks"""
        words = content.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            word_len = len(word) + 1
            if current_length + word_len > self.chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = word_len
            else:
                current_chunk.append(word)
                current_length += word_len

        if current_chunk:
            chunks.append(' '.join(current_chunk))
        return chunks

    def tag_content(self, content: Dict) -> Dict[str, str]:
        """Attach metadata and UUID tags to the content"""
        raw_text = content.get('body', content.get('selftext', ''))
        cleaned = self.clean_text(raw_text)
        tagged = {
            'id': str(uuid.uuid4()),
            'text': cleaned,
            'type': 'comment' if 'body' in content else 'post',
            'subreddit': content.get('subreddit', ''),
            'created_utc': content.get('created_utc', ''),
            'score': content.get('score', 0)
        }
        return tagged

    def clean_and_chunk(self, posts: List[Dict], comments: List[Dict], max_items: int = 100) -> Tuple[List[Dict], List[Dict]]:
        """Full pipeline for cleaning, tagging, and chunking posts/comments"""
        posts = sorted([p for p in posts if p.get('selftext')], key=lambda x: x.get('score', 0), reverse=True)[:max_items]
        comments = sorted([c for c in comments if c.get('body')], key=lambda x: x.get('score', 0), reverse=True)[:max_items]


        processed_posts = [self.tag_content(post) for post in posts if post.get('selftext')]
        processed_comments = [self.tag_content(comment) for comment in comments if comment.get('body')]

        for item in processed_posts + processed_comments:
            item['chunks'] = self.chunk_content(item['text'])

        return processed_posts, processed_comments
