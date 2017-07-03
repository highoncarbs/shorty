from flask import Flask , request , redirect , render_template
from sqlite3 import OperationalError
from check_encode import random_token
from check_encode import url_check
import sqlite3
import sys
# from display_list import list_data
reload(sys)
sys.setdefaultencoding('UTF-8')

import os
os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)

shorty_host = "http://localhost:5454/"

# url.db -> root folder * Db check fuction*
def table_check():
	create_table = '''
		CREATE TABLE WEB_URL(
		ID INTEGER PRIMARY KEY AUTOINCREMENT,
		URL TEXT ,
		S_URL TEXT ,
		COUNTER INTEGER DEFAULT 0,
		CHROME INTEGER DEFAULT 0, 
		FIREFOX INTEGER DEFAULT 0, 
		SAFARI INTEGER DEFAULT 0, 
		OTHER_BROWSER INTEGER DEFAULT 0, 
		ANDROID INTEGER DEFAULT 0, 
		IOS INTEGER DEFAULT 0, 
		WINDOWS INTEGER DEFAULT 0, 
		LINUX INTEGER DEFAULT 0, 
		MAC INTEGER DEFAULT 0, 
		OTHER_PLATFORM INTEGER DEFAULT 0

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

@app.route('/test')
def testing():
	display_sql = list_data("87lF96")
	return render_template("table.html" , t_clicks = display_sql)


@app.route('/' , methods=['GET' , 'POST'])
def index():
	if request.method == 'POST':
		og_url = request.form.get('url_input')
		custom_suff = request.form.get('url_custom')
		
		if custom_suff == '':
			token_string =  random_token()
		else:
			token_string = custom_suff

		conn = sqlite3.connect('url.db')
		cursor = conn.cursor()
		insert_row = """
			INSERT INTO WEB_URL(URL , S_URL) VALUES('%s' , '%s')
			"""%(og_url , token_string)
		
		result_cur = cursor.execute(insert_row)
		conn.commit()
		conn.close()
		
		return render_template('index.html' ,shorty_url = shorty_host+token_string)
	
	else:	
		return render_template('index.html')

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

if __name__ == '__main__':
	table_check()
	app.run(port=5454 ,debug=True)

# To implement Analytics
# Delete Trigger
# QR Code 