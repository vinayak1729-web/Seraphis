# import asyncio
# import platform

# # Import the ai_service module (adjust the import path based on your structure)
# from app.services.ai_service import gemini_chat

# async def test_gemini_chat():
#     """Test the Gemini chat function with a sample prompt"""
#     print("Starting Gemini chat test...")
#     await gemini_chat(input("enter :"))
#     print("Test completed.")

# if platform.system() == "Emscripten":
#     asyncio.ensure_future(test_gemini_chat())
# else:
#     if __name__ == "__main__":
#         asyncio.run(test_gemini_chat())
 
import asyncio
import platform

# Import the chat module (adjust the import path based on your structure)
from app.services.ai_service import chat

async def test_gemma3n_chat():
    """Test the Gemma3n chat function with a sample prompt"""
    print("Starting Gemma3n chat test...")
    await chat(input("enter :"), model="gemma3n")
    print("Test completed.")

if platform.system() == "Emscripten":
    asyncio.ensure_future(test_gemma3n_chat())
else:
    if __name__ == "__main__":
        asyncio.run(test_gemma3n_chat())