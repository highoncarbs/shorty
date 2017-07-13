from flask import Flask , request , jsonify , make_response
import MySQLdb
import config
from check_encode import random_token , url_check
from display_list import list_data

shorty_api = Flask(__name__)
shorty_api.config.from_object('config')

shorty_host = config.domain

# MySQL configurations

host = config.host
user = config.user
passwrd = config.passwrd
db = config.db

# api Block

@shorty_api.route('/api/v1/shorten' , methods= ['POST'])
def create_short_url():	
	'''
		Takes long _url as url, custom string(opt), 
		tag(opt) for input and returns short_url  
	'''	
	if request.method == 'POST':
		if 'url' in request.args :
			og_url = request.args['url']
			
			if url_check(og_url) is True:
				if 'custom' in request.args :
					token_string = request.args['custom']
					if 'tag' in request.args:
						tag_url = request.args['tag']
					else:
						tag_url = ''
				else:
					token_string = random_token()

					if 'tag' in request.args:
						tag_url = request.args['tag']
					else:
						tag_url = ''

				conn = MySQLdb.connect(host , user , passwrd , db)
				cursor = conn.cursor()
				check_row = "SELECT S_URL FROM WEB_URL WHERE S_URL = %s FOR UPDATE"
				cursor.execute(check_row,(token_string,))
				check_fetch = cursor.fetchone()

				if (check_fetch is None):
					insert_row = """
						INSERT INTO WEB_URL(URL , S_URL , TAG) VALUES( %s, %s , %s)
						"""
					result_cur = cursor.execute(insert_row ,(og_url , token_string , tag_url,))
					
					conn.commit()
					conn.close()

					short_url = shorty_host+token_string 
					long_url = og_url
					data = jsonify({
						'long_url' : og_url,
						'short_url' : short_url,
						'custom' : token_string,
						'tag' : tag_url
					})
				
					return make_response(data , 200)
				else:
					data = jsonify({'error':'suffix already present'})
					return make_response(data , 200)
			else:
				data = jsonify({'error':'URL given is not valid . Enter a valid URL.'})
				return make_response(data , 200)
		else:
			data = jsonify({'error':'invalid request'})
			return make_response(data , 405)
	else:
		data = jsonify({'error':'Invalid Method Used'})
		return make_response(data , 405)

@shorty_api.route('/api/v1/expand' , methods= ['GET'])
def retrieve_short_url():
	'''
		Takes api input as short url and returns 
		long_url with analytics such as 
		total clicks , platform and browser clicks
	'''
	if request.method == 'GET':
		if 'custom' in request.args:
			token_string = request.args['custom']
			conn = MySQLdb.connect(host , user , passwrd , db)
			cursor = conn.cursor()
			check_row = "SELECT S_URL FROM WEB_URL WHERE S_URL = %s FOR UPDATE"
			cursor.execute(check_row,(token_string,))
			check_fetch = cursor.fetchone()

			if (check_fetch is None):
				data = jsonify({
					'error' : 'Custom string given not available as shortened url.'
					})
				return make_response(data,200)
			else:
				info , counter , browser , platform = list_data(token_string)
				data = jsonify({
						'clicks' : counter[0],
						'custom' : info[1],
						'long_url' : info[0],
						'click_browser' : {
							'CHROME' : browser[0] ,
							'FIREFOX' : browser[1],
							'SAFARI' : browser[2],
							'OTHER_BROWSER': browser[3]
							},
						'click_platform' : {
							'ANDROID' : platform[0],
							'IOS' : platform[1],
							'WINDOWS' : platform[2],
							'LINUX' : platform[3],
							'MAC' : platform[4],
							'OTHER_PLATFORM' :platform[5]
							},
						'tag' : info[2] 
					})
				return make_response(data,200)
		else:
			data = jsonify({'error' : 'Follow the API format ',
							})
			return make_response(data,405)
	else:
		data = jsonify({'error':'Invalid Method Used , Use GET .'})
		return make_response(data , 405)

# api error Handlers

@shorty_api.errorhandler(404)
def not_found(error):
	data = jsonify({'error' : 'Not Found'})
	return make_response(data,404)

@shorty_api.errorhandler(400)
def invaid_response(error):
	data = jsonify({'error' : 'Invaid Request'})
	return make_response(data,400)

@shorty_api.errorhandler(500)
def invaid_response_five(error):
	data = jsonify({'error' : 'Internal error'})
	return make_response(data,500)

@shorty_api.errorhandler(405)
def invaid_response_five(error):
	data = jsonify({'error' : 'Follow the API format ',
					'Desc' : 'Use POST for API requests . url= < your url > , custom = < custom url> , tag = < URL tag >'})
	return make_response(data,405)

# End API Block

if __name__ == '__main__':

	shorty_api.run(port= 5454 , host='127.0.0.1')
