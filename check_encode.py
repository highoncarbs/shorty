from urllib.parse import urlparse
import random
import string
import traceback


def random_token(size=6):
    """
    Generates a random string of 6 chars, use size argument
    to change the size of token.
    Returns a valid token of desired size,
    *default is 6 chars
    """
    BASE_LIST = string.digits + string.ascii_letters

    token = ''.join((random.choice(BASE_LIST)) for char in range(size))
    return token


def url_check(url):
    """
    Expects a string as argument.
    Retruns True , if URL is valid else False.
    For detailed docs look into urlparse.
    """
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return True
        else:
            return False
    except Exception:
        traceback.print_exc()
        return False
