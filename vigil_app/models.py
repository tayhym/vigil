from vigil_app import db, app
class Question(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	question_text = db.Column(db.String(200))
	number_of_yes_votes = db.Column(db.Integer, default=0)
	number_of_no_votes = db.Column(db.Integer, default=0)
	number_of_maybe_votes = db.Column(db.Integer, default=0)
	id_of_yes_voters = db.Column(db.String(500)) # store a string, each number separated by 0 is a user id that voted yes for this question
	id_of_no_voters =  db.Column(db.String(500))
	id_of_maybe_voters = db.Column(db.String(500))

	def __init__(self, question_text, \
	number_of_yes_votes=0, \
	number_of_no_votes=0, \
	number_of_maybe_votes=0, \
	id_of_yes_voters='', \
	id_of_no_voters='', \
	id_of_maybe_voters=''):

		self.question_text = question_text
		self.number_of_yes_votes = number_of_yes_votes
		self.number_of_no_votes = number_of_no_votes
		self.number_of_maybe_votes = number_of_maybe_votes
		self.id_of_yes_voters = id_of_yes_voters
		self.id_of_no_voters = id_of_no_voters
		self.id_of_maybe_voters = id_of_maybe_voters

	def vote(self, vote_type, voter_id):
		if vote_type=='yes':
			self.number_of_yes_votes += 1
			self.id_of_yes_voters += ' ' + str(voter_id) 
		elif vote_type=='no':
			self.number_of_no_votes += 1
			self.id_of_no_voters += ' ' + str(voter_id)
		elif  vote_type=='maybe':
			self.number_of_maybe_votes += 1 
			self.id_of_maybe_voters += ' ' + str(voter_id)
		else:
			raise Exception("Invalid vote type")


class Person(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	username = db.Column(db.String(500))
	ques_answered = db.Column(db.String(10))
	number_of_ques_answered = db.Column(db.Integer, default=0)

	def __init__(self, username):
		tmp = ['0']*10
		self.ques_answered = ''.join(tmp)
		self.number_of_ques_answered = 0
		self.username = username

	def answer_question(self, question_id):
		print("person answering question "+ str(question_id))
		zero_list = ['0']*10
		zero_list[question_id] = '1'

		existing_list = list(self.ques_answered)


		# check that question was not answered before
		if ((question_id+1 > len(existing_list)) or (existing_list[question_id] == '0')):
			print("new question; answering now")
			print("question_answered before: "+ (self.ques_answered))

			existing_list[question_id] = '1' 
			self.ques_answered = ''.join(existing_list)
			self.number_of_ques_answered += 1
			print("question_answered after: "+ (self.ques_answered))
			print("num questions answered: "+str(self.number_of_ques_answered))

	def check_if_answered(self, question_id):

		# check if have answered this question before
		existing_list = list(self.ques_answered)
		print('checking if answered, existing answered:'+ self.ques_answered)		
		# question id starts from 1. list length starts from 1 when empty
		if (question_id+1 > len(existing_list)):
			return False
		elif (existing_list[question_id] == '0'):
			return False

		# True if answered before
		return True







