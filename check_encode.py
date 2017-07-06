'''	
Convert Url to string to Base62 string

Base62 used instead of base 64 , to preserve URL format 
and not convert spaces and special characters to HTML chars 
'''
import string
from math import floor
from urlparse import urlparse
import random

BASE_LIST = string.digits + string.letters
BASE_DICT = dict((c,i) for i,c in enumerate(BASE_LIST)) 

'''
def encode_to_base62(num , base = 62):
	if base<0 or base>62:
		return 0
	rem = num % base
	result = BASE_LIST[rem]
	qnt = floor(num / base)
	while qnt:
		rem = qnt % base
		qnt = floor(qnt / base)
		result = BASE_LIST[int(rem)] + result
	return result

def decode_to_base10(num ,base):
	limit = len(num)
	result = 0
	for i in range(limit):
		result = base*result + BASE_LIST.find(num[i])
	return result
'''

def random_token(size = 6):
	token = ''.join((random.choice(BASE_LIST)) for char in range(size))
	return token

def url_check(url):
	parse = urlparse(url)
	if not parse.scheme in ('https' , 'http'):
		url = ''.join('https://' , url)
		return url
		error = "Not a valid URL"
	else:
		# If URL is valid , encode to base64
		return url