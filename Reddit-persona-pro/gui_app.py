# gui_app.py

import tkinter as tk
from tkinter import messagebox, PhotoImage
import asyncio
import os
from dotenv import load_dotenv
from persona.reddit_fetcher import RedditFetcher
from persona.content_preprocessor import ContentPreprocessor
from persona.nlp_analyzer import NLPAnalyzer
from persona.persona_engine import PersonaEngine
from persona.visual_renderer import PersonaVisualizer

load_dotenv()

async def generate_persona(username):
    try:
        fetcher = RedditFetcher(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        posts, comments = await fetcher.fetch_user_content(username)

        preprocessor = ContentPreprocessor()
        cleaned_posts, cleaned_comments = preprocessor.clean_and_chunk(posts, comments)

        analyzer = NLPAnalyzer()
        all_chunks = [chunk for p in cleaned_posts for chunk in p['chunks']] + \
                     [chunk for c in cleaned_comments for chunk in c['chunks']]

        metadata = {
            'entities': sum([analyzer.extract_entities(t) for t in all_chunks], []),
            'sentiments': [analyzer.analyze_sentiment(t) for t in all_chunks],
            'topics': sum([analyzer.extract_topics(t) for t in all_chunks], []),
            'posts': cleaned_posts,
            'comments': cleaned_comments,
            'texts': all_chunks
        }

        engine = PersonaEngine()
        persona = engine.generate_persona(metadata)
        cited = engine.add_citations(persona, cleaned_posts + cleaned_comments)
        summary = engine.generate_natural_summary(persona)

        avatar_url = await fetcher.fetch_user_avatar(username)
        image_url = avatar_url or "https://www.redditstatic.com/avatars/defaults/v2/avatar_default_5.png"

        visualizer = PersonaVisualizer()
        visualizer.render_to_pdf(
            persona=cited,
            summary=summary,
            image_url=image_url,
            output_filename=f"{username}_persona.pdf",
            metadata=metadata
        )

        os.startfile("output")  # Automatically open the output folder

        return True, f"✅ Persona saved to output/{username}_persona.pdf"

    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def start_gui():
    root = tk.Tk()
    root.title("Reddit Persona Pro — AI Insight Generator")
    root.geometry("620x360")
    root.configure(bg="#f8fafc")

    # Branding Banner
    banner = tk.Label(root, text="🔍 Reddit Persona Generator", font=("Inter", 20, "bold"), bg="#f8fafc", fg="#1e40af")
    banner.pack(pady=20)

    # Entry Area
    frame = tk.Frame(root, bg="#f1f5f9", padx=20, pady=15, bd=1, relief=tk.RIDGE)
    frame.pack(pady=10)

    tk.Label(frame, text="Paste Reddit Profile URL:", font=("Inter", 12), bg="#f1f5f9").pack(anchor="w")
    url_entry = tk.Entry(frame, width=60, font=("Inter", 11))
    url_entry.pack(pady=6)

    status_label = tk.Label(root, text="", fg="green", wraplength=580, justify="left", font=("Inter", 10), bg="#f8fafc")
    status_label.pack(pady=10)

    def on_submit():
        url = url_entry.get().strip()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a Reddit URL.")
            return

        username = url.rstrip('/').split('/')[-1]
        status_label.config(text="⏳ Generating persona, please wait...", fg="orange")

        async def run_async():
            success, message = await generate_persona(username)
            status_label.config(text=message, fg="green" if success else "red")

        asyncio.run(run_async())

    submit_btn = tk.Button(
        root, text="✨ Generate Persona", command=on_submit,
        bg="#2563eb", fg="white", font=("Inter", 12, "bold"), padx=16, pady=8, relief=tk.FLAT, cursor="hand2"
    )
    submit_btn.pack(pady=10)

    footer = tk.Label(root, text="Made with ❤️ using GPT-4, HuggingFace & Reddit API",
                      font=("Inter", 9), fg="#64748b", bg="#f8fafc")
    footer.pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
