
import os
from cognitab_automation.config import Config

def build_templates(template_folder) -> dict[str, str]:
    """Build a dictionary of template names to their file paths."""
    templates = dict()
    
    for filename in os.listdir(template_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            template_name = os.path.splitext(filename)[0]
            templates[template_name] = os.path.join(template_folder, filename)
    
    return templates