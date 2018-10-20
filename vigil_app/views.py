from flask import render_template
from flask import request, redirect
from flask import session, flash
from vigil_app import app, db
from vigil_app.models import Question, Person
from sqlalchemy import exists

@app.route('/', methods=['GET'])
def home():	
	if not session.get('logged_in'):
		return render_template('login.html')
	else:	
		username = session['username']
		person = Person.query.filter_by(username=username).first()
		userid = person.id
		num_questions_answered = person.number_of_ques_answered
		questions = Question.query.all()
		num_questions_total = len(questions)
		num_questions_left = num_questions_total - num_questions_answered

		questions_filtered = []

		for question in questions:
			question_id = question.id
			answered_before = person.check_if_answered(question_id)
			print(answered_before)
			if (not answered_before):
				questions_filtered.append(question)	

		questions = Question.query.all()

		if (len(questions_filtered)>0):
			questions_display = [questions_filtered[0]]

		context = {'questions': questions_display, 'number_of_questions': len(questions_filtered), 'username':session['username']}
		return render_template('index_truncated.html',**context)

@app.route('/participant_home', methods=['GET'])
def participant_home(username):
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		person = Person.query.filter_by(username=username).first()
		userid = person.id
		num_questions_answered = person.number_of_ques_answered
		questions = Question.query.all()
		num_questions_total = len(questions)
		num_questions_left = num_questions_total - num_questions_answered

		questions_filtered = []

		for question in questions:
			question_id = question.id
			answered_before = person.check_if_answered(question_id)
			print(answered_before)
			if (not answered_before):
				questions_filtered.append(question)

		if (len(questions_filtered)>0):
			questions_display = [questions_filtered[0]]
		context = {'questions': questions_display, 'number_of_questions': len(questions_filtered), 'username':session['username'], 'userid':userid}
		return render_template('index_truncated.html',**context)


@app.route('/login', methods=['POST'])
def do_admin_login(): 

	valid_usernames_passwords = {'1':'pass', '2':'pass', '3':'pass','4':'pass','5':'pass'}

	if request.form['password'] == 'password' and request.form['username'] == 'admin':
		session['logged_in'] = True
		session['username'] = request.form['username']
	elif request.form['username'] in valid_usernames_passwords:
		if valid_usernames_passwords.get(request.form['username'])==request.form['password']:
			session['logged_in'] = True
			session['username'] = request.form['username']

			# if person is first time logging in, log person to database
			old_person = db.session.query(exists().where(Person.username==request.form['username'])).scalar()
			if (not old_person):
				new_person_object = Person(username=request.form['username'])
				db.session.add(new_person_object)
				db.session.commit()
				message = "Welcome to the first login " + request.form['username'] 
				print(message)
			return participant_home(request.form['username'])

	else:
		flash('wrong password!')
	return home()



@app.route('/logout')
def logout():
	session['logged_in'] = False
	return home()

@app.route('/questions/new', methods=['GET'])
def new_questions():
    return render_template('new.html')

@app.route('/questions', methods=['POST'])
def create_questions():
	if request.form["question_text"].strip() != "":
		new_question = Question(question_text=request.form["question_text"])
		db.session.add(new_question)
		db.session.commit()
		message = "Succefully added a new poll!"
	else:
		message = "Poll question should not be an empty string!"

	questions = Question.query.all()

	#-----extract filtered questions
	username = session['username']
	person = Person.query.filter_by(username=username).first()
	userid = person.id
	num_questions_answered = person.number_of_ques_answered
	questions = Question.query.all()
	num_questions_total = len(questions)
	num_questions_left = num_questions_total - num_questions_answered

	questions_filtered = []

	for question in questions:
		question_id = question.id
		answered_before = person.check_if_answered(question_id)
		print(answered_before)
		if (not answered_before):
			questions_filtered.append(question)	
	#-------
	if (len(questions_filtered)>0):
		questions_display = [questions_filtered[0]]

	context = {'questions': questions_display,'number_of_questions': len(questions_filtered),'message': message}
	return render_template('index_truncated.html',**context)


@app.route('/questions/<int:question_id>', methods=['GET'])
def show_questions(question_id):
    context = {'question': Question.query.get(question_id)}
    return render_template('show.html', **context)


@app.route('/questions/<int:question_id>', methods=['PUT'])
def update_questions(question_id):
    question = Question.query.get(question_id)
    if request.form["question_text"].strip() != "":
        question.question_text = request.form["question_text"]
        db.session.add(question)
        db.session.commit()
        message = "Successfully updated a poll!"
    else:

        message = "Question cannot be empty!"

    context = {'question': question,
               'message': message}

    return render_template('show.html', **context)


@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_questions(question_id):
    question = Question.query.get(question_id)
    db.session.delete(question)
    db.session.commit()
    context = {'questions': Question.query.all(),
               'message': 'Successfully deleted'}
    return render_template('index.html', **context)


@app.route('/questions/<int:question_id>/vote', methods=['GET'])
def new_vote_questions(question_id):
    question = Question.query.get(question_id)
    context = {'question': question}
    return render_template('vote.html', **context)

@app.route('/questions/<int:question_id>/vote', methods=['POST'])
def create_vote_questions(question_id):
    question = Question.query.get(question_id)

    if request.form["vote"] in ["yes", "no", "maybe"]:
		print(session)
		username = session['username']
		person = Person.query.filter_by(username=username).first()
		userid = person.id
		question.vote(request.form["vote"],userid)  # record userid in questions database
		# record questions in person database
		person.answer_question(question_id)


    db.session.add(question)
    db.session.commit()
    db.session.add(person)
    db.session.commit()

    return redirect("/questions/%d" % question.id)



