# Reddit Persona Pro 🧠

**Reddit Persona Pro** is an AI-powered desktop + CLI tool that extracts and visualizes detailed user personas based on public Reddit activity. It combines NLP, LLMs (like GPT-3.5), and stylish PDF rendering to generate user-centric insights with citations.

---

## 🚀 Features

- 🔍 **Fetch Reddit user posts & comments** using the Reddit API
- 🧹 **Preprocess and chunk content** for NLP efficiency
- 🧠 **Run NLP pipelines**:
  - Named Entity Recognition
  - Sentiment Analysis
  - Topic Classification (zero-shot)
- ✨ **Generate a structured persona**:
  - Interests
  - Location (if any)
  - Writing style
  - Activity level
  - Personality traits
- 🤖 **Summarize the persona** in natural language using OpenAI (GPT-3.5)
- 📎 **Cite real Reddit content** supporting each trait
- 📄 **Render beautiful PDFs** with Jinja2 + WeasyPrint
- 🖥️ **Cross-platform GUI** using Tkinter
- 💻 **Command-line support** for batch or scripted usage


---

## 🛠️ Installation

```bash
git clone https://github.com/yourusername/reddit-persona-pro.git
cd reddit-persona-pro

# Create environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

🔐 Setup Environment Variables
Create a .env file in the root:

REDDIT_CLIENT_ID=your_reddit_app_client_id
REDDIT_CLIENT_SECRET=your_reddit_app_secret
REDDIT_USER_AGENT=RedditPersonaProBot/1.0
OPENAI_API_KEY=your_openai_key

---

🖥️ Run GUI App

python gui_app.py

Optional (Windows only): rename to gui_app.pyw to launch without terminal window.

---
🧪 Run from CLI

python main.py --url https://www.reddit.com/user/spez --output spez_persona.md

Generates both .md and .pdf in the output/ folder.

---

📁 Project Structure

reddit-persona-pro/
├── persona/                 # Core logic
│   ├── reddit_fetcher.py    # Reddit API client
│   ├── content_preprocessor.py
│   ├── nlp_analyzer.py      # Transformers pipelines
│   ├── persona_engine.py    # Logic + OpenAI summary
│   ├── visual_renderer.py   # PDF generation (Jinja2 + WeasyPrint)
│   └── output_writer.py     # Markdown & PDF output
├── templates/               # HTML report template
│   └── persona_template.html
├── static/css/              # Optional report styling
├── gui_app.py               # Tkinter desktop interface
├── main.py                  # CLI interface
├── requirements.txt
└── .env                     # API keys


---

✅ Requirements
Python 3.8+

transformers, weasyprint, openai>=1.0.0, praw, jinja2, python-dotenv, tkinter

Install all with:
pip install -r requirements.txt

---

⚠️ Limitations
Only works for public Reddit profiles

Requires OpenAI API access for GPT summaries

Currently uses basic citation matching (exact string presence)

---

📜 License
MIT License © 2025 [GURMAIL_SINGH]

---

🤝 Contributing
PRs welcome! Please open an issue before submitting major changes.

---

💬 Questions?
Feel free to open an issue or contact me via GitHub 


---

Would you like me to also generate a `requirements.txt` to match this, or embed links and screenshots automatically?


---

THANKYOU

