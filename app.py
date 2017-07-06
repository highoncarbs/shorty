#!/usr/bin/env python2.7

import sqlite3
import sys
import os

# Flask Import
from flask import Flask , request , redirect , render_template
from sqlite3 import OperationalError

# token gen import
from check_encode import random_token
from check_encode import url_check

# WTFForm Imports

from sql_table import *

# Setting UTF-8 encoding

reload(sys)
sys.setdefaultencoding('UTF-8')
os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
app.config.from_object('config')
shorty_host = "http://localhost:5454/"

'''
# FLask wtf init
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class Search_tag(Form):
	search_input = StringField('search_url' , validators=[DataRequired()])

'''
# url.db -> root folder * Db check fuction*
def table_check():
	create_table = create_table_per_user
	conn =  sqlite3.connect('url.db')
	cursor = conn.cursor()
	try:
		cursor.execute(create_table)
		conn.commit()
		conn.close()
	except OperationalError:
		error = str(OperationalError)
	pass

@app.route('/analytics/<short_url>')
def testing():
	display_sql = list_data("short_url")
	return render_template("table.html" , t_clicks = display_sql)

'''
# Not in use

@app.route('/login')
def login_user():

	return render_template('login_page.html')

'''

@app.route('/' , methods=['GET' , 'POST'])
def index():

	'''
	search = Search_tag()
	if search.validate_on_submit():
		return render_template('/search/<search_input>')
	else:
		error = "Oops ! The search seems broken."
		return render_template('index.html' ,form = search)
	'''

	conn = sqlite3.connect('url.db')
	cursor = conn.cursor()
	
	list_sql = "SELECT * FROM WEB_URL;"
	result_cur = cursor.execute(list_sql)
	result_all_fetch = result_cur.fetchall()
		
	if request.method == 'POST':
		og_url = request.form.get('url_input')
		custom_suff = request.form.get('url_custom')
		tag_url = request.form.get('url_tag')
		
		if custom_suff == '':
			token_string =  random_token()
		else:
			token_string = custom_suff

		# conn = sqlite3.connect('url.db')
		# cursor = conn.cursor()
		insert_row = """
			INSERT INTO WEB_URL(URL , S_URL , TAG) VALUES( ?, ? , ?)
			"""
		result_cur = cursor.execute(insert_row ,(og_url , token_string , tag_url,))

		list_sql = "SELECT * FROM WEB_URL;"
		result_cur = cursor.execute(list_sql)
		result_all_fetch = result_cur.fetchall()
		conn.commit()
		conn.close()
			
		return render_template('index.html' ,shorty_url = shorty_host+token_string )
	else:	
		return render_template('index.html',table = result_all_fetch )
	
# Rerouting funciton	

@app.route('/<short_url>')
def reroute(short_url):

	conn = sqlite3.connect('url.db')
	cursor = conn.cursor()
	platform = request.user_agent.platform
	browser =  request.user_agent.browser
	counter = 1

	# Platform , Browser vars
	
	browser_dict = {'firefox': 0 , 'chrome':0 , 'safari':0 , 'other':0}
	platform_dict = {'windows':0 , 'iphone':0 , 'android':0 , 'linux':0 , 'macos':0 , 'other':0}

	# Analytics
	if browser in browser_dict:
		browser_dict[browser] += 1
	else:	
		browser_dict['other'] += 1
	
	if platform in platform_dict.iterkeys():
		platform_dict[platform] += 1
	else:
		platform_dict['other'] += 1
			
	result_cur = cursor.execute("SELECT URL FROM WEB_URL WHERE S_URL = ?;" ,(short_url,) )
	print result_cur

	try:
		new_url = result_cur.fetchone()[0]
		print new_url

		# Update Counters 
		
		counter_sql = "\
				UPDATE {tn} SET COUNTER = COUNTER + {og_counter} , CHROME = CHROME + {og_chrome} , FIREFOX = FIREFOX+{og_firefox} ,\
				SAFARI = SAFARI+{og_safari} , OTHER_BROWSER =OTHER_BROWSER+ {og_oth_brow} , ANDROID = ANDROID +{og_andr} , IOS = IOS +{og_ios},\
				WINDOWS = WINDOWS+{og_windows} , LINUX = LINUX+{og_linux}  , MAC =MAC+ {og_mac} , OTHER_PLATFORM =OTHER_PLATFORM+ {og_plat_other} WHERE S_URL = '{surl}';".\
				format(tn = "WEB_URL" , og_counter = counter , og_chrome = browser_dict['chrome'] , og_firefox = browser_dict['firefox'],\
				og_safari = browser_dict['safari'] , og_oth_brow = browser_dict['other'] , og_andr = platform_dict['android'] , og_ios = platform_dict['iphone'] ,\
				og_windows = platform_dict['windows'] , og_linux = platform_dict['linux'] , og_mac = platform_dict['macos'] , og_plat_other = platform_dict['other'] ,\
				surl = short_url)
		print counter_sql
		res_update = cursor.execute(counter_sql)
		conn.commit()
		conn.close()

		return redirect(new_url)

	except Exception as e:
		print e
		return render_template('index.html' , error = e)

# Search results

@app.route('/search' ,  methods=['GET' , 'POST'])
def search():
	s_tag = request.form.get('search_url')
	conn = sqlite3.connect('url.db')
	cursor = conn.cursor()

	search_tag_sql = "SELECT * FROM WEB_URL WHERE TAG = 'music'" 
	result_cur = cursor.execute(search_tag_sql )
	search_tag_fetch = result_cur.fetchall()
	conn.close()
	return render_template('search.html' , search_tag = s_tag , table = search_tag_fetch )

if __name__ == '__main__':
	table_check()
	app.run(port=5454 ,debug=True)

# Delete Trigger
# QR Code 