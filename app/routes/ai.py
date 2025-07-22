from flask import Blueprint, render_template, request, jsonify, url_for, session, Response
import ollama
import json
import base64
from dotenv import load_dotenv
import os

load_dotenv()

ai_bp = Blueprint('ai', __name__)

# Route for Seraphis AI chat
@ai_bp.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        message = request.json.get('message')
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        # Placeholder for Seraphis AI logic
        response = "Seraphis response: " + message
        return jsonify({'response': response})
    return render_template('chat.html', chat_mode='seraphis', endpoint=url_for('ai.chat'))

@ai_bp.route('/chat/gemma3n', methods=['GET', 'POST'])
def gemma3n_chat():
    if request.method == 'POST':
        if "username" not in session:
            return Response("data: {'text': 'Please log in'}\n\n", content_type='text/event-stream')
        
        if 'message' not in request.form:
            return Response("data: {'text': 'Error: No message provided'}\n\n", content_type='text/event-stream')
        
        user_message = request.form['message']
        files = request.files.getlist('files')
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
        
        if files:
            images = [file.read() for file in files if file]
            messages[1]["images"] = images
        
        def generate():
            try:
                stream = ollama.chat(
                    model="gemma3n:e2b",
                    messages=messages,
                    stream=True
                )
                for chunk in stream:
                    content = chunk['message']['content']
                    yield f"data: {json.dumps({'text': content})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'text': f'Error: {str(e)}'})}\n\n"
            yield "data: [DONE]\n\n"
        
        return Response(generate(), content_type='text/event-stream')
    
    return render_template('consultant.html', chat_mode='gemma3n', endpoint=url_for('ai.gemma3n_chat'))
@ai_bp.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('testt.html')

@ai_bp.route('/talk_to_me', methods=['GET', 'POST'])
def talk_to_me():
    return render_template('talk_to_me.html')

@ai_bp.route('/image_analysis', methods=['GET', 'POST'])
def image_analysis():
    return render_template('image_analysis.html')