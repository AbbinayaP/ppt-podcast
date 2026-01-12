import asyncio
import edge_tts

async def main():
    voices = await edge_tts.list_voices()
    for v in voices:
        print(f"{v['Name']} - {v['ShortName']}")

if __name__ == "__main__":
    asyncio.run(main())
