#!/usr/bin/env python2.7

# * Duplicate s_url entry to be

import sys
import os

# Flask Import
from flask import Flask , request , redirect , render_template , url_for
import MySQLdb
# Toekn and URL check import
from check_encode import random_token , url_check
from display_list import list_data

from sql_table import mysql_table

# Setting UTF-8 encoding

reload(sys)
sys.setdefaultencoding('UTF-8')
os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
app.config.from_object('config')
shorty_host = "http://localhost:5454/"

# MySQL configurations

localhost = "localhost"
user = "root"
passwrd = "pass"
db = "SHORTY"


# url.db -> root folder * Db check fuction*

def mysql_table_check():
	
	create_table = mysql_table
	conn = MySQLdb.connect(localhost , user , passwrd, db)
	cursor = conn.cursor()
	cursor.execute(create_table)
	conn.close()


@app.route('/analytics/<short_url>')
def analytics(short_url):

	info_fetch , counter_fetch , browser_fetch , platform_fetch = list_data(short_url)
	return render_template("data.html" , info = info_fetch ,counter = counter_fetch , browser = browser_fetch , platform = platform_fetch)


@app.route('/' , methods=['GET' , 'POST'])
def index():

	conn = MySQLdb.connect(localhost , user , passwrd, db)
	cursor = conn.cursor()
	
	list_sql = "SELECT * FROM WEB_URL;"
	cursor.execute(list_sql)
	result_all_fetch = cursor.fetchall()

		
	if request.method == 'POST':
		og_url = request.form.get('url_input')
		custom_suff = request.form.get('url_custom')
		tag_url = request.form.get('url_tag')
		
		if og_url != '':
			print url_check(og_url)

			if url_check(og_url) == True:
				if custom_suff == '':
					token_string =  random_token()
				else:
					token_string = custom_suff

				insert_row = """
					INSERT INTO WEB_URL(URL , S_URL , TAG) VALUES( %s, %s , %s)
					"""
				result_cur = cursor.execute(insert_row ,(og_url , token_string , tag_url,))

				list_sql = "SELECT * FROM WEB_URL;"
				cursor.execute(list_sql)
				result_all_fetch = cursor.fetchall()
				print result_all_fetch
				conn.commit()
				conn.close()
				e = ''
				return render_template('index.html' ,shorty_url = shorty_host+token_string , error = e )
			else:
				e = "URL entered doesn't seem valid  , Enter a valid URL."
				return render_template('index.html' ,table = result_all_fetch, error = e)

		else:
			e = "Enter a URL."
			return render_template('index.html' , table = result_all_fetch,error = e)
	else:	
		e = ''
		return render_template('index.html',table = result_all_fetch , error = e )
	
# Rerouting funciton	

@app.route('/<short_url>')
def reroute(short_url):

	conn = MySQLdb.connect(localhost , user , passwrd, db)
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
			
	cursor.execute("SELECT URL FROM WEB_URL WHERE S_URL = %s;" ,(short_url,) )

	try:
		new_url = cursor.fetchone()[0]
	
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
		e = "Something went wrong.Please try again."
		return render_template('404.html') ,404

# Search results
@app.route('/search' ,  methods=['GET' , 'POST'])
def search():
	s_tag = request.form.get('search_url')
	if s_tag == "":
		return render_template('index.html' ,table = result_all_fetch , error = "Please enter a search term")
	else:
		conn = MySQLdb.connect(localhost , user , passwrd, db)
		cursor = conn.cursor()
		
		search_tag_sql = "SELECT * FROM WEB_URL WHERE TAG = %s" 
		cursor.execute(search_tag_sql , (s_tag, ) )
		search_tag_fetch = cursor.fetchall()
		conn.close()
		return render_template('search.html' , search_tag = s_tag , table = search_tag_fetch )

if __name__ == '__main__':
	app.run(debug=True)


# TODO's
# Add delete button