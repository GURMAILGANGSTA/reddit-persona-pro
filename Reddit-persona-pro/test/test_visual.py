# test_visual.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from persona.visual_renderer import PersonaVisualizer

# Dummy structured persona data (simulate output from persona_engine)
persona = {
    "name": {"value": "Lucas Mellor", "citations": []},
    "location": {"value": "London, UK", "citations": []},
    "interests": {"value": "technology, wellness, food", "citations": []},
    "personality": {"value": "optimistic, tech-savvy", "citations": []},
    "writing_style": {"value": "detailed, inquisitive", "citations": []},
    "activity_level": {"value": "active", "citations": []}
}

# GPT summary (simulate output from generate_natural_summary)
summary = (
    "Lucas Mellor is a tech-savvy and health-conscious Reddit user who enjoys exploring discussions "
    "around wellness, technology, and food. He writes in an inquisitive and detailed manner, and his "
    "engagement shows a consistent pattern of meaningful interaction. Based in London, he reflects the "
    "traits of a curious early adopter with an optimistic tone."
)

# Optional profile photo (or use a local fallback)
image_url = "https://i.imgur.com/7Q9G6Cd.png"  # Replace with a real Reddit avatar if scraping later

visualizer = PersonaVisualizer()
visualizer.render_to_pdf(
    persona=persona,
    summary=summary,
    image_url=image_url,
    output_filename="lucas_mellor.pdf"
)  # Saved in /output
