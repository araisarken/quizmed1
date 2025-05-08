from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'araisarken'

USERNAME = 'Arailym'
PASSWORD = '2005'

CORRECT_ANSWERS = {
    'q1': 'b',
    'q2': 'b',
    'q3': 'c'
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('quiz', question=1))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/quiz/<int:question>', methods=['GET', 'POST'])
def quiz(question):
    if 'username' not in session:
        return redirect(url_for('login'))

    questions = {
        1: {
            "text": "Where is Narxoz University located?",
            "options": {'a': 'Astana', 'b': 'Almaty', 'c': 'Aktau'}
        },
        2: {
            "text": "What is Narxoz University mostly known for?",
            "options": {'a': 'Digital technologies', 'b': 'Economics and Business', 'c': 'Medicine'}
        },
        3: {
            "text": "Which language is commonly used in Narxoz University classes?",
            "options": {'a': 'Kazakh', 'b': 'Russian', 'c': 'All of the above'}
        }
    }

    if question not in questions:
        return redirect(url_for('result'))

    if request.method == 'POST':
        answer = request.form.get('answer')
        session[f'q{question}'] = answer
        return redirect(url_for('quiz', question=question + 1))

    return render_template('quiz.html', question_num=question, question=questions[question])

@app.route('/result')
def result():
    if 'username' not in session:
        return redirect(url_for('login'))

    score = 0
    total = 3
    user_answers = {}
    for i in range(1, 4):
        user_answer = session.get(f'q{i}')
        user_answers[f'q{i}'] = {
            'your': user_answer,
            'correct': CORRECT_ANSWERS[f'q{i}'],
            'is_correct': user_answer == CORRECT_ANSWERS[f'q{i}']
        }
        if user_answer == CORRECT_ANSWERS[f'q{i}']:
            score += 1

    username = session['username']
    flash('Quiz completed!', 'info')
    return render_template('result.html', username=username, score=score, total=total, user_answers=user_answers)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'warning')
    return redirect(url_for('login'))

@app.route('/try-again')
def try_again():
    for i in range(1, 4):
        session.pop(f'q{i}', None)
    return redirect(url_for('quiz', question=1))

if __name__ == '__main__':
    app.run(debug=True)
