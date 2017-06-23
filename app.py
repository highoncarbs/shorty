from flask import Flask , request , redirect , render_template
from sqlite3 import OperationalError
from check_encode import random_token
from check_encode import url_check
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

import os
os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)

shorty_host = "https://localhost:5454/"

# url.db -> root folder * Db check fuction*
def table_check():
	create_table = '''
		CREATE TABLE WEB_URL(
		ID INTEGER PRIMARY KEY AUTOINCREMENT,
		URL TEXT ,
		S_URL TEXT ,
		COUNTER INT DEFAULT 0
		);
		'''
	conn =  sqlite3.connect('url.db')
	cursor = conn.cursor()
	try:
		cursor.execute(create_table)
		conn.commit()
		conn.close()
	except OperationalError:
		error = str(OperationalError)
	pass

@app.route('/' , methods=['GET' , 'POST'])
def index():
	if request.method == 'POST':
		og_url = request.form.get('url_input')
		conn = sqlite3.connect('url.db')
		cursor = conn.cursor()
		token_string = random_token()
		
		insert_row = """
			INSERT INTO WEB_URL(URL , S_URL) VALUES('%s' , '%s')
			"""%(og_url , token_string)
		print(insert_row)
		result_cur = cursor.execute(insert_row)
		conn.commit()
		conn.close()
		return render_template('index.html' ,shorty_url = shorty_host+token_string)
	else:	
		return render_template('index.html')

# Rerouting funciton

@app.route('/<short_url>')
def redirect(short_url):
	conn = sqlite3.connect('url.db')
	cursor = conn.cursor()
	select_row = '''
		SELECT URL FROM WEB_URL WHERE S_URL = %s
		'''%(short_url)
	result_cur = cursor.execute(select_row)
	try:
		redirect_url = result_cur.fetchnone()[0]
		conn.commit()
		conn.close()
		return redirect(redirect_url)	
	except Exception as e:
		error  = e 
		return render_template('index.html' , error = error)

if __name__ == '__main__':
	table_check()
	app.run(port=5454 ,debug=True)
