import asyncio
import edge_tts
import os

async def main():
    text = "Hello, this is a test of the text to speech system."
    voice = "en-US-AriaNeural"
    output_file = "test_audio.mp3"
    
    print(f"Generating audio for text: '{text}'")
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"Success! Audio file created. Size: {size} bytes")
        else:
            print("Error: File was not created.")
            
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
