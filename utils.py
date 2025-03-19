from gtts import gTTS
import os

def generate_tts(text):
    """Generates a Text-to-Speech (TTS) file from the given text."""
    tts = gTTS(text=text, lang="en")
    
    # Ensure 'assets/' directory exists
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    tts_path = os.path.join(assets_dir, "news_summary.mp3")
    tts.save(tts_path)
    
    return tts_path
