"""
CONTROLLER
"""
from system.core.controller import *

class Users(Controller):
	def __init__(self, action):
		super(Users, self).__init__(action)
		self.load_model('User')
	def index(self):
		return self.load_view('index.html')

	def create_user(self):
		info = {
		'name':request.form['name'], 
		'alias':request.form['alias'],
		'email':request.form['email'],
		'password':request.form['password'],
		'pw_confirmation':request.form['pw_confirmation'],
		'birthday': request.form['birthday']
		}
		create_status = self.models['User'].create_user(info)

		if create_status['status'] == True:
			session['id'] = create_status['user']['id']
			session['name'] = create_status['user']['name']
			alias = session['name']
			flash('Success! Please log in.')
			return redirect('/')
		else:
			for message in create_status['errors']:
				flash( message, 'regis_errors')
			return redirect('/')

	def login(self):
		info = {
		'email':request.form['email'],
		'password':request.form['password']
		}
		login_status = self.models['User'].login_user(info)

		if login_status['status'] == True:
			session['alias'] = login_status['user']['alias']
			alias = session['alias']
			session['id'] = login_status['user']['id']
			print login_status['user']
			return redirect('/quotes')
		else:
			for message in login_status['errors']:
				flash( message, 'login_errors')
			return redirect('/')

	def quotes(self):
		alias = session['alias']
		quotes = self.models['User'].show_all_quotes()
		print quotes
		return self.load_view('quotes.html', alias=alias, quotes=quotes)



	def add_quote(self):
		info = {
		'name': request.form['name'],
		'quote': request.form['quote'],
		'id': session['id']
		}
		create_status = self.models['User'].add_quote(info)
		if create_status['status'] == True:
			return redirect('/quotes')
		else:
			for message in create_status['errors']:
				flash( message, 'quote_errors' )
			return redirect('/quotes')

	def user_by_id(self, user_id):
		user = self.models['User'].show_user_by_id(user_id)
		quotes = self.models['User'].show_user_by_id(user_id)
		user = user[0]
		return self.load_view('users.html', user=user, quotes=quotes)    



	def clear(self):
		session.clear()
		return redirect('/')








