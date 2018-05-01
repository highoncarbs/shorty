import os

table_name = "WEB_URL"

# WTF config

WTF_CSRF_ENABLED = True
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'the_very_secure_secret_security_key_that_no_will_ever_guess')

# MySQL Config


host = os.getenv('MYSQL_HOST', 'localhost')
user = os.getenv('MYSQL_USER', 'root')
passwrd = os.getenv('MYSQL_PASSWORD', "password")
db = os.getenv('MYSQL_DB', "shorty")

# Domain Host

'''
For now , use http as using https returns a bad error message ,
For https , use a SSL certificate. ( under works)
'''
domain = os.getenv(
    'DOMAIN',
    "http://localhost:%s/" % os.getenv('WEB_PORT', '5000'))
