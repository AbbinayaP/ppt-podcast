from gtts import gTTS

async def generate_audio(text: str, output_file: str, voice: str = "en") -> None:
    """
    Converts text to speech using Google Text-to-Speech (gTTS).
    Note: gTTS is synchronous, but we keep the async signature for compatibility.
    """
    try:
        tts = gTTS(text=text, lang=voice, slow=False)
        tts.save(output_file)
    except Exception as e:
        raise RuntimeError(f"gTTS generation failed: {str(e)}")
