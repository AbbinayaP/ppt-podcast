import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

# ✅ Supported model
model = genai.GenerativeModel("gemini-flash-latest")


def generate_podcast_script(ppt_text: str) -> str:
    """
    Converts PPT text into a podcast-style narration script
    """

    prompt = f"""
You are a professional podcast narrator.

Convert the following PowerPoint content into a clear, engaging,
human-like podcast script. Do not mention slides. Use smooth transitions.

Content:
{ppt_text}
"""

    response = model.generate_content(prompt)

    return response.text.strip()
