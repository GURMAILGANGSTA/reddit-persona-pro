# reddit-persona-pro/persona/output_writer.py

import os
from datetime import datetime
import markdown2
import pdfkit

class OutputWriter:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def format_persona(self, persona_data: dict, summary: str = "") -> str:
        """Format persona data into readable markdown text"""
        output = ["# Reddit User Persona Summary", ""]
        if summary:
            output.append(summary + "\n")
        output.append("---\n")

        for category, data in persona_data.items():
            output.append(f"## {category.replace('_', ' ').title()}")
            output.append(f"**Value:** {data['value']}\n")
            output.append("**Supporting Evidence:**")

            for citation in data['citations']:
                output.append(f"- {citation['text']} (_r/{citation['subreddit']}_) [Link]({citation['link']})")

            output.append("")

        return '\n'.join(output)

    def save_to_markdown(self, username: str, formatted_data: str) -> str:
        """Save formatted persona to a markdown file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{username}_persona_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(formatted_data)

        print(f"✅ Markdown saved to '{filepath}'")
        return filepath

    def convert_markdown_to_pdf(self, markdown_file: str, pdf_file: str = None):
        """Convert markdown file to PDF using pdfkit"""
        try:
            if not pdf_file:
                pdf_file = markdown_file.replace(".md", ".pdf")
            html = markdown2.markdown_path(markdown_file)
            pdfkit.from_string(html, pdf_file)
            print(f"📄 PDF saved to '{pdf_file}'")
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
