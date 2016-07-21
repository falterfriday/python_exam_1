""" 
MODEL
"""
from system.core.model import Model
import re
import bcrypt

class User(Model):
	def __init__(self):
		super(User, self).__init__()

	def create_user(self, info):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
		NAME_REGEX = re.compile(r'^[a-zA-Z ]*$')
		ALIAS_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]*$')
		errors = []
		if not info['name']:			
			errors.append('Name cannot be blank')
		elif len(info['name']) < 2:
			errors.append('Name must be at least 2 characters long')
		elif not NAME_REGEX.match(info['name']):
			errors.append('Name format must be valid!')
		if not info['alias']:
			errors.append('Alias cannot be blank')
		elif len(info['alias']) < 2:
			errors.append('Alias must be at least 2 characters long')
		elif not ALIAS_REGEX.match(info['alias']):
			errors.append('Alias format must be valid!')
		if not info['email']:
			errors.append('Email cannot be blank')
		elif not EMAIL_REGEX.match(info['email']):
			errors.append('Email format must be valid!')
		if not info['password']:
			errors.append('Password cannot be blank')
		elif len(info['password']) < 8:
			errors.append('Password must be at least 8 characters long')
		elif info['password'] != info['pw_confirmation']:
			errors.append('Passwords must match!')
		if not info['birthday']:
			errors.append('Date of Birth cannot be blank')
		if errors:
			return {"status": False, "errors": errors}
		else:
			password = info['password']
			hashed_pw = self.bcrypt.generate_password_hash(password)
			create_query = "INSERT INTO users (name, alias, email, pw_hash, created_at, updated_at) VALUES (:name, :alias, :email, :pw_hash, NOW(), NOW() )"
			create_data = {'name': info['name'], 'alias': info['alias'], 'email': info['email'], 'pw_hash': hashed_pw}
			self.db.query_db(create_query,create_data)
			get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
			users = self.db.query_db(get_user_query)
			return { "status": True, "user": users[0] }


	def login_user(self, info):
		EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
		errors = []
		if not info['email']:
			errors.append('Email cannot be blank')
		elif not EMAIL_REGEX.match(info['email']):
			errors.append('Email format must be valid!')
		if not info['password']:
			errors.append('Password cannot be blank')
		elif len(info['password']) < 8:
			errors.append('Password must be provided')
		if errors:
			return {"status": False, "errors": errors}
		else:
			password = info['password']
			user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
			user_data = {'email': info['email']}
			user = self.db.query_db(user_query, user_data)
			if user:
				print user[0]['pw_hash']
				if self.bcrypt.check_password_hash(user[0]['pw_hash'], password):

					return {"status": True, "user": user[0]}
				else:
					errors.append('Invalid login credentials!')
			else:
				errors.append('Invalid login credentials!')
			return {"status": False, "errors": errors}

	def show_all_quotes(self):
		return self.db.query_db("SELECT * FROM quotes JOIN users ON users.id = quotes.user_id ORDER BY quotes.created_at DESC")



	def add_quote(self, info):

		errors = []
		if not info['name']:
			errors.append('Quoted By cannot be blank!')
		elif len(info['name']) < 3:
			errors.append('Quoted By must be more than 3 characters!')
		if not info['quote']:
			errors.append('Message cannot be blank!')
		elif len(info['quote']) < 10:
				errors.append('Message must be more than 10 characters')
		if errors:
			return{"status":False, "errors": errors}
		else:
			quote_query = "INSERT INTO quotes (author, quote, user_id, created_at, updated_at) VALUES (:author, :quote, :user_id, NOW(), NOW() )"
			quote_data = {'author': info['name'], 'quote': info['quote'], 'user_id': info['id']}
			self.db.query_db(quote_query, quote_data)
			return {"status": True}

	def show_user_by_id(self, info):
		query = "SELECT * FROM users JOIN quotes ON quotes.user_id = users.id WHERE users.id = :info"
		data = { 'info': info }
		print data
		return self.db.query_db(query, data)















