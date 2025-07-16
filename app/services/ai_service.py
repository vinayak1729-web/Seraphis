import google.generativeai as genai
import os
from dotenv import load_dotenv
from fer import FER
import cv2
import json

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 65536,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-thinking-exp-01-21",
    generation_config=generation_config,
)
chat_session = model.start_chat()

emotion_detector = FER(mtcnn=True)

def gemini_chat(user_input, history_file="dataset/intents.json"):
    try:
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                intents_data = json.load(f)
        else:
            intents_data = {"intents": []}

        response = chat_session.send_message(user_input)
        new_intent = {
            "patterns": [user_input],
            "responses": [response.text.strip()],
        }
        intents_data['intents'].insert(1, new_intent)

        with open(history_file, 'w') as f:
            json.dump(intents_data, f, indent=4)

        return response.text
    except Exception as e:
        print(f"Error during chat: {e}")
        return "An error occurred. Please try again."

def analyze_image(image_data):
    system_prompt = """
    <instructions>
    You are CHIKITSA, an AI combining the expertise of a compassionate digital psychiatrist and a skilled medical practitioner specializing in image analysis.
    [Full system prompt from your app.py]
    </instructions>
    """
    image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
    prompt_parts = [image_parts[0], system_prompt]
    response = model.generate_content(prompt_parts)
    return response.text

def detect_emotion_and_attention(frame, attention_status, dominant_emotion):
    display_frame = cv2.flip(frame.copy(), 1)
    results = emotion_detector.detect_emotions(frame)

    for result in results:
        bounding_box = result["box"]
        emotions_dict = result["emotions"]
        paying_attention, dominant_emotion = is_paying_attention(emotions_dict)
        attention_status = "Paying Attention" if paying_attention else "Not Paying Attention"

        x, y, w, h = bounding_box
        flipped_x = display_frame.shape[1] - (x + w)
        cv2.rectangle(display_frame, (flipped_x, y), (flipped_x + w, y + h), (255, 0, 0), 2)
        emotion_text = ", ".join([f"{emotion}: {prob:.2f}" for emotion, prob in emotions_dict.items()])
        cv2.putText(display_frame, f"{dominant_emotion} ({attention_status})", 
                    (flipped_x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(display_frame, emotion_text, 
                    (flipped_x, y + h + 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    return display_frame, attention_status, dominant_emotion

def is_paying_attention(emotions_dict, threshold=0.5):
    dominant_emotion = max(emotions_dict, key=emotions_dict.get)
    emotion_score = emotions_dict[dominant_emotion]
    return emotion_score > threshold, dominant_emotion