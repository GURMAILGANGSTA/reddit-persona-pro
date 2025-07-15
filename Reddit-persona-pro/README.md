# Reddit Persona Pro

A tool that analyzes Reddit users' post history to generate detailed personas with citations.

## Features
- Asynchronous Reddit data fetching
- Content preprocessing and chunking
- NLP analysis (entities, sentiment, topics)
- GPT-powered persona generation
- Automated citation generation

## Setup
1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your credentials
4. Run `python main.py`

## Usage
```python
from persona import RedditPersonaAnalyzer

analyzer = RedditPersonaAnalyzer()
result = analyzer.generate_persona('username')