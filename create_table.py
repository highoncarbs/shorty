# Script to build mysql table

import config
import MySQLdb
from sql_table import mysql_table

'''
Create_table.py looks for MySQL Config in config.py 
Creates a connection to the database using the supplied config

Creates a TABLE named WEB_URL with the specified rows.
Needs to RUN once when setting up the application on local or
web server.

You need to have a database already defined ( SHORTY for e.g is 
already present .).
'''
host = config.host
user = config.user
passwrd = config.passwrd
db = config.db

create_table = mysql_table
conn = MySQLdb.connect(host , user , passwrd, db)
cursor = conn.cursor()
cursor.execute(create_table)

conn.close()
