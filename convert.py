'''
Convert Url to string to Base62 string

Base62 used instead of base 64 , to preserve URL format 
and not convert spaces and special characters to HTML chars 
'''
import string
from math import floor

BASE_LIST = string.digits + string.letters
BASE_DICT = dict((c,i) for i,c in enumerate(BASE_LIST)) 

def encode_to_base62(data , base = 62):
	if base<0 or base>62:
		return 0
	rem = data % base
	result = BASE_LIST[rem]
	qnt = floor(data / base)
	while qnt:
		rem = qnt % base
		qnt = floor(qnt / base)
		result = BASE_LIST[int(r)] + result
	return result

def decode_to_base10(data ,base):
	if base<0 or base>62:
		return 0

print(encode_to_base62('heeleoleoe0505050'))