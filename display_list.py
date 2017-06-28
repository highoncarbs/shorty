import sqlite3
from config import *
from flask import render_template

def list_data(shorty_url):

	conn = sqlite3.connect('url.db')
	cursor = conn.cursor()
	display_sql = cursor.execute("SELECT COUNTER FROM WEB_URL WHERE S_URL = ?;" ,(shorty_url,) )
	cc = display_sql.fetchone()[0]

	
	conn.close()
	return cc
