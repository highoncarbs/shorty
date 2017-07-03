import sqlite3
from config import *
from flask import render_template

# def list_data(shorty_url):

# 	conn = sqlite3.connect('url.db')
	# cursor = conn.cursor()
# 	counter_sql = cursor.execute("SELECT COUNTER FROM WEB_URL WHERE S_URL = ?;" ,(shorty_url,) )
# 	browser_sql = cursor.execute("SELECT CHROME , FIREFOX , SAFARI, OTHER_BROWSER FROM WEB_URL WHERE S_URL = ?;" ,(shorty_url,) )
# 	platform_sql = cursor.execute("SELECT ANDROID , IOS , WINDOWS, LINUX , MAC , OTHER_PLATFORM FROM WEB_URL WHERE S_URL = ?;" ,(shorty_url,) ) 
# 	counter_fetch = counter_sql.fetchall()
# 	browser_fetch = browser_sql.fetchone()
# 	platform_fetch = platform_sql.fetchone()
# 	conn.close()
	
# 	return counter_fetch , browser_fetch , platform_fetch

# c ,b ,p = list_data("87lF96")
