from flask import Blueprint, render_template, request, jsonify, Response, session, redirect
from app.services.ai_service import gemini_chat, analyze_image, detect_emotion_and_attention
from app.utils.decorators import login_required
import cv2
ai_bp = Blueprint('ai', __name__)

attention_status = "Not Paying Attention"
dominant_emotion = "neutral"

@ai_bp.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return render_template('chat.html')
    elif request.method == 'POST':
        try:
            data = request.get_json()
            user_input = data.get('message')
            response = gemini_chat(user_input)
            return jsonify({'response': response})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@ai_bp.route('/image_analysis', methods=['GET', 'POST'])
def image_analysis():
    analysis = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            return redirect(request.url)

        if uploaded_file:
            image_data = uploaded_file.read()
            analysis = analyze_image(image_data)
    return render_template('image_analysis.html', analysis=analysis)

@ai_bp.route('/talk_to_me', methods=['GET', 'POST'])
def talk_to_me():
    global attention_status, dominant_emotion

    if request.method == 'GET':
        return render_template('talk_to_me.html')

    elif request.method == 'POST':
        user_input = request.form.get('user_input', '')
        prompt = f"The user is in a {dominant_emotion} mood and is {'paying attention' if attention_status == 'Paying Attention' else 'not paying attention'}."
        bot_response = gemini_chat(user_input + " " + prompt)
        return jsonify({'response': bot_response})

    return "Unsupported request method", 405

# @ai_bp.route('/video_feed')
# def video_feed():
#     def generate_frames():
#         cap = cv2.VideoCapture(0)
#         global attention_status, dominant_emotion
#         while True:
#             success, frame = cap.read()
#             if not success:
#                 break
#             processed_frame, attention_status, dominant_emotion = detect_emotion_and_attention(frame, attention_status, dominant_emotion)
#             _, buffer = cv2.imencode('.jpg', processed_frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#         cap.release()
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')