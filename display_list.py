import sqlite3
from config import *
 
# !!IMP!!
# Confirm for SQL Injection adn security ! 
# USe of ' ? ' replaced with format()
def list_data(shorty_url):

	conn = sqlite3.connect('url.db')
	cursor = conn.cursor()
	su = shorty_url
	counter_sql = "SELECT URL FROM WEB_URL WHERE S_URL= ?; "
	browser_sql = "SELECT CHROME , FIREFOX , SAFARI, OTHER_BROWSER FROM WEB_URL WHERE S_URL =?;"
	platform_sql = "SELECT ANDROID , IOS , WINDOWS, LINUX , MAC , OTHER_PLATFORM FROM WEB_URL WHERE S_URL = ?;"	
	counter_fetch = cursor.execute(counter_sql , (su,)).fetchone()
	browser_fetch = cursor.execute(browser_sql, (su,)).fetchone()
	platform_fetch = cursor.execute(platform_sql, (su,)).fetchone()
	conn.close()
	return counter_fetch , browser_fetch , platform_fetch

# Test playground
# c , b , p = list_data("tiktok")
# print c
