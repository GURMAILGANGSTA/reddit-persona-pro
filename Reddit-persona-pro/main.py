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

MAX_CHUNKS = 300  # Limit total chunks to reduce processing time
MAX_ITEMS = 100   # Limit number of posts/comments to process

async def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Reddit User Persona Generator")
    parser.add_argument("--url", required=True, help="Reddit user profile URL (e.g. https://www.reddit.com/user/spez)")
    parser.add_argument("--output", default="sample_user_persona.md", help="Output markdown file name")
    args = parser.parse_args()

    if "/user/" not in args.url:
        print("❌ Invalid URL. Please provide a full Reddit user profile URL, e.g. https://reddit.com/user/spez")
        return

    username = args.url.strip('/').split('/')[-1]

    try:
        print(f"🔍 Fetching Reddit data for user: u/{username}")
        fetcher = RedditFetcher(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT', 'PersonaBot/1.0')
        )

        posts, comments = await fetcher.fetch_user_content(username)
        if not posts and not comments:
            print("⚠️ No public posts or comments found for this user.")
            return

        preprocessor = ContentPreprocessor()
        cleaned_posts, cleaned_comments = preprocessor.clean_and_chunk(posts, comments, max_items=MAX_ITEMS)

        print("🧠 Running NLP analysis...")
        analyzer = NLPAnalyzer()
        all_chunks = [chunk for p in cleaned_posts for chunk in p['chunks']] + \
                     [chunk for c in cleaned_comments for chunk in c['chunks']]
        all_chunks = all_chunks[:MAX_CHUNKS]

        sentiments = analyzer.analyze_sentiments_batch(all_chunks)
        topics_nested = analyzer.extract_topics_batch(all_chunks)
        entities_nested = [analyzer.extract_entities(text) for text in all_chunks]

        metadata = {
            'entities': sum(entities_nested, []),
            'sentiments': sentiments,
            'topics': sum(topics_nested, []),
            'posts': cleaned_posts,
            'comments': cleaned_comments,
            'texts': all_chunks
        }

        print("🧬 Generating structured persona...")
        engine = PersonaEngine()
        structured = engine.generate_persona(metadata)
        cited = engine.add_citations(structured, cleaned_posts + cleaned_comments)
        summary = engine.generate_natural_summary(structured)

        print("💾 Saving output...")
        writer = OutputWriter()
        markdown_file = writer.save_to_markdown(username, writer.format_persona(cited, summary))
        writer.convert_markdown_to_pdf(markdown_file)

        print(f"✅ Persona for u/{username} saved to: output/{markdown_file.replace('.md', '.pdf')}")

    except Exception as e:
        print(f"❌ Error generating persona for u/{username}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
