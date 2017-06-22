from flask import Flask , request , redirect , render_template
from sqlite3 import OperationalError
import check_encode

app = Flask(__name__)

# url.db -> root folder * Db check fuction*
def table_check():
	create_table = '''
		CREATE TABLE X_URL(
		ID INT PRIMARY KEY AUTOINCREMENT,
		URL TEXT NOT NULL
		);
		'''
	with sqlite3.connect('url.db') as conn:
		cursor = conn.cursor();
		try:
			cursor.execute(create_table)
		except OperationalError:
			error = str(OperationalError)
			pass

@app.route('/' , methods=['GET' , 'POST'])
def index():
	if request.method == 'POST':
		og_url = request.form.get('url_input')
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)