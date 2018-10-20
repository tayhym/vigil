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


# class Person(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)

# 	N_ques_answered = db.Column(db.Integer,default=0)
	

# 	def __init__(self,)