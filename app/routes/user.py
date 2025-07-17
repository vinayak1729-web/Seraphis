from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.services.user_service import save_user_data, get_user_data, save_questionnaire_responses, get_questionnaire_responses, save_meditation_log, get_meditation_stats, save_mood, get_moods
from app.services.ai_service import gemini_chat
from app.utils.decorators import login_required
from datetime import datetime
import numpy as np

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

# List of questions
questions = [
    "Have you been feeling depressed or sad lately?",
    "Do you often feel overwhelmed or anxious?",
    "Have you been experiencing difficulty sleeping or eating?",
    "Do you find yourself isolating yourself from others?",
    "Have you been having thoughts of harming yourself or others?",
    
    "Do you have any unhealthy coping mechanisms, such as substance abuse or excessive gambling?",
    "Do you engage in any self-harm behaviors?",
    "Have you tried talking to someone about your feelings?",
    "Do you practice any stress-relief techniques, such as meditation or exercise?",
    
    "Do you have a strong support system of friends and family?",
    "Do you feel comfortable talking to someone about your mental health concerns?",
    "Have you considered seeking professional help from a therapist or counselor?",
    
    "Do you often feel good about yourself?",
    "Do you believe you are capable of achieving your goals?",
    "Have you been experiencing feelings of inadequacy or worthlessness?",
    
    "Do you have healthy and supportive relationships?",
    "Are you able to express your feelings openly and honestly?",
    "Have you been experiencing conflict or difficulties in your relationships?",
    
    "Have you experienced any traumatic events in your life?",
    "Do you struggle with flashbacks or nightmares?",
    "Have you been feeling overwhelmed or stressed by recent events?",
    
    "Do you use any substances, such as alcohol or drugs?",
    "Have you noticed any negative consequences from your substance use?",
    "Have you considered seeking help for substance abuse?",
    "Have you noticed any changes in your mood over the last few days?"
"Have you noticed any changes in your sleep patterns?",
"Have you noticed any changes in your eating habits?",
"Do you feel more tired than usual?",
"How many close friends do you have?",
"Do you enjoy going to work/school/college?",
"Do you get distracted easily when working on something for a long time?",
"Do you often feel tired, worried, or stressed?",
"Are you aware of your emotions as you experience them?",
"Do you seek out activities that you enjoy?",
"Do you feel you have control over your emotions?",
"How many hobbies do you have?",
"How often do you engage in the activities that you like?",
"Do you often spend a lot of time thinking about things that happen to you?",
"Does your mood often go up and down?",
"Are you lively?",
"Do you often worry about things you should not have done or said?",
"Do you get irritated easily?",
"Are your feelings easily hurt?",
"Have you ever engaged in using alcohol or cigarettes after feeling hurt or sad?",
"How often do you feel ‘fed up’?",
"Are you always troubled about feelings of guilt?",
"How often do you feel nervous?",
"Do you worry that awful things might happen to you in the future?",
"Do you worry about your health?",
"Do you like mixing with people?",
"Do you feel life is dull or boring?",
"Do you think people are trying to avoid you?",
"Do you often feel lonely?",
"Do you experience difficulty in starting or completing daily tasks?",
"Have you withdrawn from social interactions or avoided people lately?",
"Do you find yourself feeling restless, fidgety, or unable to stay still?",
"Have you been feeling more irritable or easily frustrated than usual?",
"Do you often feel overwhelmed by your emotions or unable to control them?",
"Have you lost interest or pleasure in activities you used to enjoy?",
"Do you feel hopeless about the future?",
"Do you find yourself overthinking or worrying excessively about small things?",
"Have you had any thoughts of harming yourself or feeling that life is meaningless?",
"Do you ever feel like people are watching you or talking about you when they aren’t?",
"Have you experienced hearing voices or seeing things others don’t?",
"Do you feel disconnected from reality or like you are in a dream-like state sometimes?",
"Have you been struggling with memory, such as forgetting appointments or important details?",
"Do you have difficulty focusing on tasks or conversations?",
"Have you been making impulsive decisions that you later regret?",
"Do you feel mentally exhausted even after getting enough rest?",
"Do you feel like your thoughts are slower or harder to organize than before?",
"Have you been neglecting your personal hygiene or self-care lately?",
"Do you find it difficult to maintain eye contact during conversations?",
"Have others commented that you seem less expressive or emotionally distant?",
"Do you feel like your movements have become noticeably slower?",
"Have you been avoiding certain places or activities due to fear or discomfort?",
"Do you frequently experience sudden mood swings without a clear reason?",
"Have you felt emotionally numb or disconnected from your surroundings?",
"Do you feel like your emotions don’t match what’s happening around you? (e.g., laughing in serious situations)",
"Do you feel anxious when there’s no clear reason to be?",
"Have your thoughts been racing so fast that they’re hard to keep up with?",
"Do you often feel like you’re repeating the same thoughts over and over?",
"Have you been experiencing unusual or irrational fears that interfere with your daily life?",
"Do you sometimes feel like your thoughts are being controlled by an external force?",
"Have you been struggling to find the right words while speaking?",
"Do you frequently misplace things or forget where you have kept them?",
"Have you had trouble making even simple decisions lately?",
"Have you felt like time is moving either too fast or too slow lately?",
"Have you noticed any recent changes in your speech, such as speaking too fast or too slow?",
"Have you experienced difficulty understanding or processing what others are saying?",
"Do you frequently pause mid-conversation because you lose track of your thoughts?",
"Have you caught yourself repeating words or phrases unnecessarily?",
"Do you feel like you understand your current emotional or mental state?",
"Have you been making choices that you later realize were risky or poorly thought out?",
"Do you often regret your decisions soon after making them?",
"Have people told you that your recent behavior seems unusual or out of character?",
"Do you believe you need help with your mental health, or do you feel everything is fine?",
"Do you ever feel confused about where you are or what day it is?",
"Have you found yourself forgetting names of familiar people or places?",
"Do you ever feel like you’re in a different time or place, even when you know logically that you're not?",
"Have you recently experienced moments where you completely lose track of time?",
"Do you sometimes feel like you’re watching yourself from outside your body?",
"Have you been struggling to recall events that happened recently but can easily remember things from years ago?",
"Do you frequently forget what you were just talking about or doing?",
"Have you had difficulty remembering new information, like someone’s name right after they introduce themselves?",
"Have you been relying more on reminders or notes recently because your memory isn’t as sharp as before?",
"Have you ever experienced a sudden gap in memory where you can’t remember what happened for a period of time?",
"Have you noticed yourself becoming unusually suspicious or distrustful of people around you?",
"Do you feel like people are intentionally trying to provoke or manipulate you?",
"Do you struggle to maintain relationships?",
"Have you felt overly dependent on someone for emotional or decision-making support?",
"Do you find it difficult to resist temptations or urges, even when you know they might harm you?",
"Have you had outbursts of anger that you later regretted?",
"Do you frequently interrupt conversations or struggle to wait for your turn to speak?",
"Do you find it difficult to think of solutions when faced with a complex problem?",
"Have you had strong beliefs about being followed, spied on, or targeted without clear evidence?",
"Have you found yourself freezing up or being unable to move during stressful moments?",
"Do you sometimes make repetitive movements (like tapping, rocking, or pacing) without realizing it?",
"Have you been struggling with coordination or balance more than usual?",
"Do you feel overwhelmed by responsibilities?",
"Have you been more sensitive to noise, light, or other sensations lately?"
]

# Convert the list to a numpy array
questions_array = np.array(questions)

def get_random_close_questions():
    questions_array = np.array(questions)
    return np.random.choice(questions_array, 5, replace=False) # Always select 50 questions

import numpy as np

# List of questions
questions = [
"How would you describe your mood over the last few days?",
"How would you describe your friend circle?",
"How would you describe your daily energy levels?",
" Have you ever felt just miserable for no reason? Describe when it happened.",
"If you have ever wished you were dead, when was it and what led to that thought?",
"What is the most interesting thing you heard this week?",
"What’s the one thing you really want to do but have never done, and why?",
"Would you take a shot if the chance of failure and success is 50-50?",
"Which one would you prefer; taking a luxurious trip alone or having a picnic with people you love?",
"If your life was a book, what would the title be?",
"If you could be any animal, what would you be and why?",
"What is your favorite day of the week and why?",
"What do you do when you’re bored?",
"Shoe size?",
"Favorite color?",
"Favorite band (or artist)?",
"Favorite animal?",
"Favorite food?",
"One food you dislike?",
"Favorite condiment?",
"Favorite movie?",
"Last movie you saw in a theater?",
"Last book read?",
"Best vacation?",
"Favorite toy as a child?",
"One item you should throw away, but probably never will?",
"Superman, Batman, Spiderman, or Wonder Woman?",
"Chocolate or vanilla?",
"Morning person or night owl?",
"Cats or dogs?",
"Sweet or salty?",
"Breakfast or dinner?",
"Coffee or tea?",
"American food, Italian food, Mexican food, Chinese food, or other?",
"Clean or messy?",
"What is your favorite breakfast food?",
"What vegetable would you like to grow in a garden?",
"Tell about a childhood game you loved.",
"What’s your favorite dessert?",
"What’s your favorite month of the year and why?",
"Who is your favorite celebrity?",
"Which celebrity do you most resemble?",
"If you could go anywhere in the world, where would you go and why?",
"Share about one of your hobbies.",
"What’s a unique talent that you have?",
"Introvert or extrovert?",
"Describe yourself in three words.",
"Tell about a happy childhood memory.",
"Name three things (or people) that make you smile.",
"Are you doing what you truly want in life?",
"What are your aspirations in life?",
"How many promises have you made this past year and how many of them have you fulfilled?",
"Are you proud of what you’re doing with your life or what you’ve done in the past? Explain.",
"Have you ever abandoned a creative idea that you believed in because others thought you were a fool? Explain.",
"What would you prefer? Stable but boring work or interesting work with lots of workload?",
"Are you making an impact or constantly being influenced by the world?",
"Which makes you happier, to forgive someone or to hold a grudge? Explain.",
"Who do you admire and why?",
"What are your strengths?",
"What are your weaknesses?",
"Are you doing anything that makes you and people around you happy?",
"Tell about a short-term goal you have.",
"Tell about a health goal you have.",
"Tell about a long-term goal you have.",
"Tell about a value that is currently important to you.",
"What do you like most about yourself?",
"What do you like least about yourself?",
"What in life brings you joy?",
"What are you grateful for?",
"Who is the most influential person in your life and why?",
"Tell about one dream you have always had, but are too afraid to chase.",
"What is something you want to change about yourself and what are two things you can do to accomplish this?",
"Describe your perfect world. (Who would be in it, what would you be doing, etc.)",
"Where were you one year ago, where are you now, and where do you want to be a year from today?",
"Share about a character flaw you have.",
"What kind of a person do you want to be?",
"When is the last time you helped someone and what did you do?",
"Tell about a problem you have right now. What can you do to solve it?",

"Have you ever failed anyone who you loved or loved you? Explain.",
"Who is your favorite person?",
"What was it like growing up in your family?",
"What makes someone a good friend?",
"What happens when you’re rejected?",
"What makes a relationship healthy or unhealthy?",
"Would you rather break someone’s heart or have your heart broken?",

"As a child, what did you want to be when you grew up?",
"Tell about something you do well.",
"What’s your dream job?",
"What are your career goals?",
"What classes would you be most interested in taking?",
"Tell about a job you would hate doing.",
"Would you prefer to work with people or by yourself?",
"Would you ever do a job that was dangerous if it paid a lot of money?",
"Would you still work if you didn’t have to?",
"What do you want to do when you retire?",
"If you have a job, what do you like about it? Dislike?",
"How do you deal with difficult co-workers?",
"What qualities would you like your supervisor to have?",

"When was the last time you laughed, and what did you laugh at?",
"If happiness was a currency, how rich would you be?",
"How do you express happiness?",
"What are three healthy ways you can cope with anger?",
"What are three healthy ways you can cope with anxiety?",
"What does being happy mean to you?",
"If your mood was a weather forecast, what would it be?",
"Tell about a time you were happy.",
"Tell about a time you were heartbroken.",
"What is the difference between guilt and shame?",
"Is guilt a healthy emotion?",
"Can guilt be excessive?",
"Is there a such thing as “healthy shame”?",
"What makes you happy?",
"What makes you mad?",
"When do you feel afraid?",
"When do you feel lonely?",
"Share about the last time you felt guilty.",
"What embarrasses you?",

"How does one practice forgiveness (of self and others) from a religious point of view and from a non-religious point of view?",
"What does it mean to forgive?",
"Do you have to forgive to move forward?",
"What brings you meaning in life?",
"How do you define spirituality?",
"What’s the difference between religion and spirituality?",
"When do you feel most at peace?",
"Do you meditate? Why or why not?",

"If you could travel to the past in a time machine, what advice would you give to the 6-year-old you?",
"Would you break the rules because of something/someone you care about?",
"Are you afraid of making mistakes? Why or why not?",
"If you cloned yourself, which of your characteristics would you not want cloned?",
"What’s the difference between you and most other people?",
"Consider the thing you last cried about; does it matter to you now or will it matter to you 5 years from now?",
"What do you need to let go of in life?",
"Do you remember anyone you hated 10 years ago? Does it matter now?",
"What are you worrying about and what happens if you stop worrying about it?",
"If you died now, would you have any regrets?",
"What’s the one thing you’re most satisfied with?",
"If today was the end of the world, what would you do?",
"What would you do if you won the lottery?",
"If you could change one thing about yourself, what would it be?",
"How do you think others see you?",
"How do you get someone’s attention?",
"What masks do you wear?",
"Tell about a poor decision you made.",
"When is the last time you failed at something? How did you handle it?",
]

# Convert the list to a numpy array
questions_array = np.array(questions)

def get_random_open_questions():
    questions_array = np.array(questions)  # Convert list of questions to an array
    num_questions_to_select =10  # Always select 50 questions
    return np.random.choice(questions_array, num_questions_to_select, replace=False)

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