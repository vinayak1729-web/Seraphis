from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.services.user_service import save_user_data, get_user_data, save_questionnaire_responses, get_questionnaire_responses, save_meditation_log, get_meditation_stats, save_mood, get_moods
from app.services.ai_service import gemini_chat
from app.utils.decorators import login_required
# from Create_modules.close_end_questionaire import get_random_close_questions
# from Create_modules.open_end_questions import get_random_open_questions
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if 'email' not in session:
        return redirect('/login')

    if request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        occupation_type = request.form.get('occupation_type')
        occupation_detail = request.form.get('occupation_detail')
        occupation = occupation_detail if occupation_type == 'Other' else occupation_type

        user_data = {
            'age': age,
            'gender': gender,
            'occupation': occupation
        }
        save_user_data(session['email'], user_data)
        return redirect('/login')

    return render_template('questionnaire.html')

@user_bp.route('/home')
def home():
    return render_template('home.html')

@user_bp.route('/meditation')
@login_required
def meditation():
    return render_template('meditation.html')

@user_bp.route('/log_meditation', methods=['POST'])
@login_required
def log_meditation():
    username = session.get('username')
    meditation_data = request.json
    save_meditation_log(username, meditation_data)
    stats = get_meditation_stats(username)
    return jsonify({
        'status': 'success',
        'message': 'Meditation session logged successfully',
        'total_sessions': stats['total_sessions']
    })

@user_bp.route('/get_meditation_stats')
@login_required
def get_meditation_stats_route():
    username = session.get('username')
    stats = get_meditation_stats(username)
    return jsonify(stats)

@user_bp.route('/personal_info')
@login_required
def personal_info():
    username = session.get('username')
    user_data = get_user_data(username) or {
        "age": "",
        "gender": "",
        "occupation": "",
        "timestamp": datetime.now().isoformat()
    }
    return render_template('personal_info.html', user_data=user_data)

@user_bp.route('/update_personal_info', methods=['POST'])
@login_required
def update_personal_info():
    username = session.get('username')
    updated_data = {
        "age": request.form.get('age'),
        "gender": request.form.get('gender'),
        "occupation": request.form.get('occupation')
    }
    save_user_data(session['email'], updated_data)
    return redirect(url_for('user.personal_info'))

@user_bp.route('/closed_ended')
def close_ended():
    random_questions = get_random_close_questions()
    return render_template('closed_ended.html', questions=random_questions)

@user_bp.route('/submit_close_end', methods=['POST'])
def submit_close_ended():
    if request.method == 'POST':
        responses = [{"question": question, "answer": request.form[question]} for question in request.form]
        save_questionnaire_responses(session['username'], "closed_ended", responses)
        return redirect(url_for('user.submit_opended'))

@user_bp.route('/open_ended', methods=['GET', 'POST'])
def submit_opended():
    if request.method == 'POST':
        responses = [{"question": key, "answer": value} for key, value in request.form.items()]
        save_questionnaire_responses(session['username'], "open_ended", responses)
        return redirect(url_for('user.thank_you'))
    else:
        random_questions = get_random_open_questions()
        return render_template('open_ended.html', questions=random_questions)

@user_bp.route('/thank_you')
def thank_you():
    username = session.get('username', "Guest")
    responses = get_questionnaire_responses(username)
    close_ended_str = ""
    open_ended_str = ""
    for response in responses:
        if response['type'] == "closed_ended":
            close_ended_str = " ".join([f"{r['question']}: {r['answer']}" for r in response['responses']])
        elif response['type'] == "open_ended":
            open_ended_str = " ".join([f"{r['question']}: {r['answer']}" for r in response['responses']])

    judge_gemini = gemini_chat(f"This is my assessment of close-ended questions and open-ended questions. Please provide feedback on me in friendly tone in summary like a professional psychiatrist. in english {close_ended_str} {open_ended_str}")
    return render_template('thank_you.html', judge_gemini=judge_gemini, user_name=username, completejudege=judge_gemini)

@user_bp.route('/feedback')
def feedback():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    username = session.get('username')
    user_data = get_user_data(username) or {}
    if 'wellness_report' not in user_data:
        responses = get_questionnaire_responses(username)
        close_ended_str = ""
        open_ended_str = ""
        for response in responses:
            if response['type'] == "closed_ended":
                close_ended_str = " ".join([f"{r['question']}: {r['answer']}" for r in response['responses']])
            elif response['type'] == "open_ended":
                open_ended_str = " ".join([f"{r['question']}: {r['answer']}" for r in response['responses']])

        default = "This is my assessment of close-ended questions and open-ended questions. Please provide feedback on me in friendly tone in summary like a professional psychiatrist."
        judge_gemini = gemini_chat(default + " " + close_ended_str + " " + open_ended_str)
        user_data['wellness_report'] = judge_gemini
        save_user_data(session['email'], user_data)
    else:
        judge_gemini = user_data['wellness_report']

    return render_template('thank_you.html', judge_gemini=judge_gemini, user_name=username, completejudege=judge_gemini)

@user_bp.route('/mood_tracker')
@login_required
def mood_tracker():
    return render_template('mood_tracker.html')

@user_bp.route('/log_mood', methods=['POST'])
@login_required
def log_mood():
    data = request.json
    username = session.get('username')
    save_mood(username, data)
    return jsonify({'status': 'success'})

@user_bp.route('/get_moods')
@login_required
def get_moods_route():
    username = session.get('username')
    moods = get_moods(username)
    return jsonify({'moods': moods})