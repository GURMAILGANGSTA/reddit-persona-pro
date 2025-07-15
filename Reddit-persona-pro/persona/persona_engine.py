# reddit-persona-pro/persona/persona_engine.py

import openai
import os
from typing import Dict, List
from collections import Counter

class PersonaEngine:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def generate_persona(self, analyzed_data: Dict) -> Dict:
        """Generate persona based on analyzed data"""
        entities = analyzed_data.get('entities', [])
        sentiments = analyzed_data.get('sentiments', [])
        topics = analyzed_data.get('topics', [])

        locations = [e['word'] for e in entities if e['entity'].endswith('LOC')]
        interests = [t['topic'] for t in topics if t['score'] > 0.7]

        sentiment_scores = [s['score'] for s in sentiments]
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.5

        return {
            'location': Counter(locations).most_common(1)[0][0] if locations else 'Unknown',
            'interests': list(set(interests)),
            'personality': self._derive_personality(avg_sentiment, topics),
            'activity_level': self._calculate_activity_level(analyzed_data),
            'writing_style': self._analyze_writing_style(analyzed_data)
        }

    def add_citations(self, persona: Dict, source_data: List) -> Dict:
        """Add citations to generated persona"""
        cited_persona = {}
        for key, value in persona.items():
            citations = self._find_supporting_content(key, value, source_data)
            cited_persona[key] = {
                'value': value,
                'citations': citations
            }
        return cited_persona

    def _derive_personality(self, sentiment_score: float, topics: List) -> str:
        traits = []
        if sentiment_score > 0.7:
            traits.append('optimistic')
        elif sentiment_score < 0.3:
            traits.append('critical')

        topic_scores = {t['topic']: t['score'] for t in topics}
        if topic_scores.get('technology', 0) > 0.8:
            traits.append('tech-savvy')
        if topic_scores.get('gaming', 0) > 0.8:
            traits.append('gamer')

        return ', '.join(traits) if traits else 'balanced'

    def _calculate_activity_level(self, data: Dict) -> str:
        post_count = len(data.get('posts', []))
        comment_count = len(data.get('comments', []))
        total = post_count + comment_count

        if total > 1000:
            return 'very active'
        elif total > 500:
            return 'active'
        elif total > 100:
            return 'moderately active'
        else:
            return 'casual'

    def _analyze_writing_style(self, data: Dict) -> str:
        styles = []
        all_text = ' '.join(data.get('texts', []))

        if len(all_text.split()) / max(len(all_text.split('.')), 1) > 20:
            styles.append('detailed')
        if '!' in all_text:
            styles.append('enthusiastic')
        if '?' in all_text:
            styles.append('inquisitive')

        return ', '.join(styles) if styles else 'straightforward'

    def _find_supporting_content(self, key: str, value: any, source_data: List) -> List[Dict]:
        citations = []
        for item in source_data:
            if isinstance(value, str) and value.lower() in item['text'].lower():
                citations.append({
                    'text': item['text'][:100] + '...',
                    'type': item['type'],
                    'subreddit': item['subreddit'],
                    'link': f"https://reddit.com/{item['id']}"
                })
            if len(citations) >= 3:
                break
        return citations

    def generate_natural_summary(self, structured_persona: Dict) -> str:
        prompt = f"""
You are a UX researcher. Based on the following user persona traits, write a natural-language paragraph summarizing the user:

{structured_persona}

Make it sound like a real, human-centric description (as if shown in an HR document or marketing slide). Keep it concise and insightful.
"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating summary: {e}"
