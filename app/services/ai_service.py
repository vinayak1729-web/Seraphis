import asyncio
import sys
import os
from dotenv import load_dotenv
import ollama
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Shared system prompt for both Gemini and Gemma3n
SYSTEM_PROMPT = """
You are Seraphis, an empathetic AI psychiatrist, providing mental health support using evidence-based coping strategies, behaving like a best friend, showing love, care, and secular Bhagavad Gita lessons (e.g., focus on the present, detachment from outcomes) tailored to users' emotional needs. Acknowledge feelings, assess concerns, suggest actionable techniques, and recommend professional help for severe symptoms. Use a warm, inclusive tone, avoid religious references, and encourage gradual progress.
"""
STRICT = "Just reply to the user's context in 97 to 280 characters, like a human, emotionally, helping Seraphis."


async def stream_gemini_response(prompt):
    """Generate streaming response from Gemini API"""
    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-pro"
    
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch()),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
        tools=tools,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text=SYSTEM_PROMPT + STRICT),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        sys.stdout.write(chunk.text)
        sys.stdout.flush()
        await asyncio.sleep(0.1)  # Simulate streaming with small delay

    print()  # New line after streaming completes

async def gemini_chat(prompt):
    """Handle Gemini chat with streaming output"""
    try:
        await stream_gemini_response(prompt)
    except Exception as e:
        print(f"Error in Gemini chat: {str(e)}")
        sys.stdout.flush()
async def stream_gemma3n_response(prompt, model_name="gemma3n:e2b"):
    """Generate streaming response from Gemma3n model"""
    try:
        stream = ollama.chat(
            model=model_name,
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT + STRICT},
                {'role': 'user', 'content': prompt}
            ],
            stream=True
        )
        for chunk in stream:
            sys.stdout.write(chunk['message']['content'])
            sys.stdout.flush()
            await asyncio.sleep(0.1)  # Simulate streaming with small delay

        print()  # New line after streaming completes
    except Exception as e:
        print(f"Error in Gemma3n chat: {str(e)}")
        sys.stdout.flush()

async def chat(prompt, model="both"):
    """Handle chat with streaming output for Gemini, Gemma3n, or both"""
    try:
        if model.lower() == "gemini":
            await stream_gemini_response(prompt)
        elif model.lower() == "gemma3n":
            await stream_gemma3n_response(prompt)
        else:  # Default to both
            print("Gemini response:")
            await stream_gemini_response(prompt)
            print("\nGemma3n response:")
            await stream_gemma3n_response(prompt)
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        sys.stdout.flush()
