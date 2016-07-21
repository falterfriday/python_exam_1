"""
    Routes Configuration File

    Put Routing rules here
"""
from system.core.router import routes


routes['default_controller'] = 'Users'
routes['POST']['/register'] = 'Users#create_user'
routes['POST']['/login'] = 'Users#login'
routes['GET']['/quotes'] = 'Users#quotes'
routes['POST']['/add_quote'] = 'Users#add_quote'
routes['GET']['/user/<user_id>'] = 'Users#user_by_id'
routes['/clear'] = 'Users#clear'

