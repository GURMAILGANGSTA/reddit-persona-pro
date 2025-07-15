# reddit-persona-pro/persona/visual_renderer.py

import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime

class PersonaVisualizer:
    def __init__(self, template_dir="templates", output_dir="output"):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def render_to_pdf(self, persona: dict, summary: str, image_url: str, output_filename: str = None):
        template = self.env.get_template("persona_template.html")

        # Extract traits and flatten into key-value
        flat_data = {key: val['value'] for key, val in persona.items()}
        citations = {key: val['citations'] for key, val in persona.items()}

        context = {
            "name": flat_data.get("name", "Anonymous"),
            "summary": summary,
            "image_url": image_url,
            "persona": flat_data,
            "citations": citations,
            "generated_on": datetime.now().strftime("%B %d, %Y")
        }

        html_out = template.render(context)

        filename = output_filename or f"persona_{flat_data.get('name', 'user')}.pdf"
        output_path = os.path.join(self.output_dir, filename)
        HTML(string=html_out, base_url=".").write_pdf(output_path)

        print(f"✅ Visual persona saved to: {output_path}")
