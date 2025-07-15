# reddit-persona-pro/main.py

import argparse
import asyncio
import os
from dotenv import load_dotenv
from persona.reddit_fetcher import RedditFetcher
from persona.content_preprocessor import ContentPreprocessor
from persona.nlp_analyzer import NLPAnalyzer
from persona.persona_engine import PersonaEngine
from persona.output_writer import OutputWriter

async def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Reddit User Persona Generator")
    parser.add_argument("--url", required=True, help="Reddit user profile URL")
    parser.add_argument("--output", default="sample_user_persona.md", help="Output file name")
    args = parser.parse_args()

    username = args.url.strip('/').split('/')[-1]

    try:
        print(f"🔍 Fetching Reddit data for user: {username}")
        fetcher = RedditFetcher(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT', 'PersonaBot/1.0')
        )
        posts, comments = await fetcher.fetch_user_content(username)

        preprocessor = ContentPreprocessor()
        cleaned_posts, cleaned_comments = preprocessor.clean_and_chunk(posts, comments)

        print("🧠 Running NLP analysis...")
        analyzer = NLPAnalyzer()

        all_texts = [chunk for p in cleaned_posts for chunk in p['chunks']] + \
                    [chunk for c in cleaned_comments for chunk in c['chunks']]

        metadata = {
            'entities': sum([analyzer.extract_entities(t) for t in all_texts], []),
            'sentiments': [analyzer.analyze_sentiment(t) for t in all_texts],
            'topics': sum([analyzer.extract_topics(t) for t in all_texts], []),
            'posts': cleaned_posts,
            'comments': cleaned_comments,
            'texts': all_texts
        }

        print("🧬 Generating structured persona...")
        engine = PersonaEngine()
        structured = engine.generate_persona(metadata)
        cited = engine.add_citations(structured, cleaned_posts + cleaned_comments)
        summary = engine.generate_natural_summary(structured)

        print("💾 Saving output...")
        writer = OutputWriter()
        writer.save_markdown(cited, summary, filename=args.output)

        print(f"✅ Persona for u/{username} saved to '{args.output}'")

    except Exception as e:
        print(f"❌ Error generating persona for '{username}': {e}")

if __name__ == "__main__":
    asyncio.run(main())
