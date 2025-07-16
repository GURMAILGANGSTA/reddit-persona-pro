from jinja2 import Environment, FileSystemLoader, TemplateError, TemplateNotFound
from weasyprint import HTML
from datetime import datetime
import os

class PersonaVisualizer:
    def __init__(self, template_dir="templates", output_dir="output"):
        abs_template_dir = os.path.abspath(template_dir)
        self.env = Environment(loader=FileSystemLoader(abs_template_dir))
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def render_to_pdf(self, persona: dict, summary: str, image_url: str, output_filename: str = None):
        flat_data = {key: val.get('value', '') for key, val in persona.items()}
        citations = {key: val.get('citations', []) for key, val in persona.items()}

        context = {
            "name": flat_data.get("name", "Anonymous"),
            "summary": summary or "No summary available.",
            "image_url": image_url or "https://www.redditstatic.com/avatars/defaults/v2/avatar_default_5.png",
            "persona": flat_data,
            "citations": citations,
            "generated_on": datetime.now().strftime("%B %d, %Y")
        }

        try:
            print("🔍 Looking for template in:", self.env.loader.searchpath)
            template = self.env.get_template("persona_template.html")
            html_out = template.render(context)

        except (TemplateNotFound, TemplateError) as te:
            print(f"⚠️ Template error: {te}")
            print("🛟 Using fallback template instead.")
            html_out = self.default_template().render(context)

        try:
            filename = output_filename or f"persona_{flat_data.get('name', 'user')}.pdf"
            output_path = os.path.join(self.output_dir, filename)
            HTML(string=html_out, base_url=".").write_pdf(output_path)
            print(f"✅ Visual persona saved to: {output_path}")
        except Exception as e:
            print(f"❌ PDF rendering error: {e}")
            raise e

    def default_template(self):
        # Internal fallback mini template
        from jinja2 import Template
        fallback_html = """
        <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ name }} - Reddit Persona Report</title>
  <link rel="stylesheet" href="../static/css/style.css">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
  <style>/* static/css/style.css */

body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  background: #f9fafb;
  color: #1f2937;
  line-height: 1.6;
}

.persona-wrapper {
  max-width: 960px;
  margin: auto;
  padding: 40px 20px;
  background: #ffffff;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.07);
  border-radius: 12px;
}

.hero {
  display: flex;
  gap: 30px;
  align-items: center;
  margin-bottom: 40px;
}

.hero-left {
  flex-shrink: 0;
}

.avatar {
  width: 180px;
  height: 180px;
  object-fit: cover;
  border-radius: 16px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.hero-right {
  flex-grow: 1;
}

.name {
  margin: 0;
  font-size: 2rem;
  font-weight: 800;
}

.summary {
  font-size: 1.1rem;
  margin-top: 10px;
  color: #374151;
}

.generated-on {
  font-size: 0.9rem;
  color: #6b7280;
  margin-top: 8px;
}

.traits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.trait-card {
  background: #f3f4f6;
  padding: 20px;
  border-radius: 10px;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);
}

.trait-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 10px;
  color: #111827;
}

.trait-value {
  font-size: 1rem;
  margin-bottom: 12px;
}

.citation-list {
  list-style: none;
  padding-left: 0;
  font-size: 0.9rem;
}

.citation-list blockquote {
  margin: 0 0 4px 0;
  padding-left: 12px;
  border-left: 3px solid #9ca3af;
  color: #374151;
  font-style: italic;
}

.subreddit {
  font-weight: bold;
  color: #2563eb;
  font-size: 0.85rem;
}

.footer {
  margin-top: 50px;
  text-align: center;
  font-size: 0.9rem;
  color: #9ca3af;
}
</style>
</head>
<body>
  <div class="persona-wrapper">
    <section class="hero">
      <div class="hero-left">
        <img class="avatar" src="{{ image_url }}" alt="{{ name }} Photo">
      </div>
      <div class="hero-right">
        <h1 class="name">{{ name }}</h1>
        <p class="summary">{{ summary }}</p>
        <p class="generated-on">📅 Generated on <strong>{{ generated_on }}</strong></p>
      </div>
    </section>

    <section class="traits-grid">
      {% for key, value in persona.items() %}
        <div class="trait-card">
          <h2 class="trait-title">{{ key.replace('_', ' ').title() }}</h2>
          <div class="trait-value">{{ value }}</div>
          {% if citations[key] %}
            <ul class="citation-list">
              {% for cite in citations[key] %}
                <li><blockquote>{{ cite.text }}</blockquote><span class="subreddit">r/{{ cite.subreddit }}</span> <a href="{{ cite.link }}" target="_blank">[view]</a></li>
              {% endfor %}
            </ul>
          {% endif %}
        </div>
      {% endfor %}
    </section>

    <footer class="footer">
      <p>Generated by <strong>Reddit Persona Pro</strong> — AI-powered User Insight Engine</p>
    </footer>
  </div>
</body>
</html>

        """
        return Template(fallback_html)
