import config
import MySQLdb


# MySQL configurations
host = config.host
user = config.user
passwrd = config.passwrd
db = config.db


def list_data(shorty_url):
    """
        Takes short_url for input.
        Returns counter , browser , platform ticks.
    """
    conn = MySQLdb.connect(host, user, passwrd, db)
    cursor = conn.cursor()
    su = [shorty_url]
    info_sql = "SELECT URL, S_URL ,TAG FROM WEB_URL WHERE S_URL = %s;"
    counter_sql = "SELECT COUNTER FROM WEB_URL WHERE S_URL = %s;"
    browser_sql = "SELECT CHROME, FIREFOX, SAFARI, OTHER_BROWSER FROM WEB_URL WHERE S_URL = %s;"
    platform_sql = "SELECT ANDROID, IOS, WINDOWS, LINUX, MAC, OTHER_PLATFORM FROM WEB_URL WHERE S_URL = %s;"

    # MySQLdb's execute() function expects a list
    # of objects to be converted so we use [arg ,]
    # But for sqlite ( args,) works.

    cursor.execute(info_sql, su)
    info_fetch = cursor.fetchone()
    cursor.execute(counter_sql, su)
    counter_fetch = cursor.fetchone()
    cursor.execute(browser_sql, su)
    browser_fetch = cursor.fetchone()
    cursor.execute(platform_sql, su)
    platform_fetch = cursor.fetchone()
    conn.close()

    return info_fetch, counter_fetch, browser_fetch, platform_fetch
