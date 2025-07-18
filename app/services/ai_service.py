from google import genai
from google.genai import types
import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")


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

import ollama

async def stream_gemma3n_e2b_response(prompt):
    try:
        stream = ollama.chat(
            model="gemma3n:e2b",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        
        for chunk in stream:
            sys.stdout.write(chunk['message']['content'])
            sys.stdout.flush()
            await asyncio.sleep(0.1)

        print()
    except Exception as e:
        print(f"Error in Gemma 3n:e2b chat: {str(e)}")
        sys.stdout.flush()

async def gemma3n_e2b_chat(prompt):
    try:
        await stream_gemma3n_e2b_response(prompt)
    except Exception as e:
        print(f"Error in Gemma 3n:e2b chat: {str(e)}")
        sys.stdout.flush()