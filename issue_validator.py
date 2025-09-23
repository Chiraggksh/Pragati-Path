"""
Civic Reporter Validation Module

This module provides validation utilities for the civic reporter application,
designed to work seamlessly with app.py's existing Flask structure.

Usage in app.py:

    from issue_validator import CivicValidator

    validator = CivicValidator()

    # In report_issue endpoint:
    img_valid, img_msg = validator.validate_image_file(image_file)
    caption = validator.get_florence_caption(image_path)
    score3 = validator.get_civic_score_strict3(caption, description)
"""

import os
import yaml
import re
from PIL import Image

class CivicValidator:
    """
    Lightweight validation utility for civic reporter Flask app.

    Provides image validation, captioning, and strict score string output.
    """

    def __init__(self, groq_api_key=None, config_path="config.yaml"):
        self.groq_api_key = groq_api_key or self._load_groq_key(config_path)
        self.ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        self.florence_client = self._init_florence_client()

    def _load_groq_key(self, config_path):
        try:
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    config = yaml.safe_load(f)
                    if config and "groq" in config:
                        return config["groq"].get("api_key")
            return os.environ.get("GROQ_API_KEY")
        except Exception as e:
            print(f"⚠️ Could not load Groq API key: {e}")
            return None

    def _init_florence_client(self):
        try:
            from gradio_client import Client
            client = Client("GF-John/Florence-2")
            print("✅ Florence-2 client initialized")
            return client
        except Exception as e:
            print(f"⚠️ Florence-2 not available: {e}")
            return None

    def allowed_file(self, filename):
        if not filename:
            return False
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def validate_image_file(self, file):
        try:
            if not file:
                return False, "No file provided"
            if not self.allowed_file(file.filename):
                return False, "Invalid file type."
            file.seek(0)
            img = Image.open(file)
            img.verify()
            file.seek(0)
            img = Image.open(file)
            width, height = img.size
            file.seek(0)
            if width < 100 or height < 100:
                return False, "Image too small."
            if width > 4000 or height > 4000:
                return False, "Image too large."
            return True, "Valid image"
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"

    def get_florence_caption(self, image_path):
        print(f"🔄 Generating caption for: {os.path.basename(image_path)}")
        if not self.florence_client:
            return "Caption generation unavailable"
        if not os.path.exists(image_path):
            return "Image file not found"
        try:
            from gradio_client import handle_file
            result = self.florence_client.predict(
                image=handle_file(image_path),
                task_prompt="Detailed Caption",
                text_input=None,
                model_id="microsoft/Florence-2-large",
                api_name="/process_image"
            )
            caption = self._extract_caption(result)
            return caption
        except Exception as e:
            return f"Caption generation failed: {str(e)}"

    def _extract_caption(self, result):
        try:
            if isinstance(result, (list, tuple)) and len(result) >= 1:
                caption = str(result[0]) if result[0] else "No caption generated"
            else:
                caption = str(result) if result else "No caption generated"
            if caption.startswith('{') and caption.endswith('}'):
                import ast
                try:
                    caption_dict = ast.literal_eval(caption)
                    if isinstance(caption_dict, dict):
                        caption = list(caption_dict.values())[0]
                except:
                    pass
            return caption
        except:
            return "Caption extraction failed"

    def get_civic_score_strict3(self, caption, description):
        """
        Returns ONLY a strict 3-digit string score as required (e.g., '087') for direct API app integration.
        """
        prompt_text = f"""You are a civic issue validator. 
Your task is to strictly rate the civic relevance of the report (0-100).
Evaluate BOTH the AI-generated image caption and the user-provided description. 
Check if they are consistent with each other and clearly describe a civic infrastructure or public issue.

IMAGE CAPTION: "{caption}"
USER DESCRIPTION: "{description}"

SCORING RULES:
- HIGH RELEVANCE (70-100): Directly related to civic/public issues such as 
road damage, potholes, waterlogging, sewage/drainage problems, street lighting, 
garbage/waste management, traffic signals, broken sidewalks, public transport, 
government facilities, electricity/power supply, or community infrastructure.
Both caption and description should clearly align on a civic issue.
- MEDIUM RELEVANCE (40-69): Vague or partially relevant civic issues. 
Example: Caption shows a road but description is unclear; description mentions 
"problem in colony" but not specific; mismatched caption/description but still 
possibly civic-related. Needs clarification.
- LOW RELEVANCE (0-39): Not related to civic/public issues. Includes:
personal complaints, private property, selfies, pets, family photos, 
festivals, shops/ads, or anything unrelated to infrastructure/public utilities.
Also applies when caption and description contradict each other 
(e.g., caption about nature but description about electricity).
STRICTNESS RULES:
- If description is too short, vague, or generic (e.g., "please fix this", "bad condition") → score low.
- If caption and description do not match → score low.
- Do NOT assume relevance if it's unclear. Prefer lowering score.

Respond EXACTLY in this format:
<number>

Where <number> is an integer from 0 to 100, zero-padded to 3 digits (e.g., 007, 085)."""
        # ---- Groq API Request ----
        import requests
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "openai/gpt-oss-20b",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text}
            ],
            "temperature": 0.1
        }
        url = "https://api.groq.com/openai/v1/chat/completions"
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                text = response.json()["choices"][0]["message"]["content"]
                return self._strict3score(text)
        except Exception as e:
            print(f"Validator: scoring error: {e}")
        return "000"  # fallback

    def _strict3score(self, text):
        """
        Extracts the integer score from text and outputs exactly a 3-digit string (zero-padded).
        """
        lines = text.strip().split('\n')
        for line in lines:
            if 'score' in line.lower():
                numbers = re.findall(r'\d+', line)
                if numbers:
                    val = max(0, min(100, int(numbers[0])))
                    return f"{val:03d}"
        # fallback for any lone number
        for line in lines:
            numbers = re.findall(r'\d+', line)
            if numbers:
                val = max(0, min(100, int(numbers[0])))
                return f"{val:03d}"
        return "000"

# -- Module-level quick usage help --

def create_validator(groq_api_key=None):
    """Create a CivicValidator instance."""
    return CivicValidator(groq_api_key=groq_api_key)

def validate_image(file):
    validator = CivicValidator()
    return validator.validate_image_file(file)

def generate_caption(image_path):
    validator = CivicValidator()
    return validator.get_florence_caption(image_path)

def score_strict3(caption, description, groq_api_key=None):
    validator = CivicValidator(groq_api_key=groq_api_key)
    return validator.get_civic_score_strict3(caption, description)
