#!python3
import traceback

# Flask Import
from flask import Flask, request, redirect, render_template
from flask import make_response, abort

import MySQLdb

# Token and URL check import
from check_encode import random_token, url_check
from display_list import list_data

from sql_table import ensureTableExists

# Config import
import config

# Import Loggers
import logging
from time import strftime
from config import host, user, passwrd, db, token

app = Flask(__name__)
app.config.from_object('config')

shorty_host = config.domain
ensureTableExists(host, user, passwrd, db)


def access_control(request):
    if not token:
        return

    if 'token' not in request.args:
        abort(403)

    if request.args['token'] != token:
        abort(403)


@app.route('/analytics/<short_url>')
def analytics(short_url):
    access_control(request)

    info_fetch, counter_fetch, browser_fetch, platform_fetch = list_data(short_url)
    return render_template(
        "data.html", host=shorty_host,
        info=info_fetch, counter=counter_fetch,
        browser=browser_fetch, platform=platform_fetch,
        token=token)


@app.route('/delete/<short_url>')
def delete(short_url):
    access_control(request)

    conn = MySQLdb.connect(host, user, passwrd, db)
    cursor = conn.cursor()

    delete_sql = """
        DELETE FROM WEB_URL WHERE S_URL = %s
    """
    cursor.execute(delete_sql, (short_url,))
    conn.commit()
    conn.close()
    return render_template('index.html', token=token, error="Deleted")


# Search results
@app.route('/search', methods=['GET', 'POST'])
def search():
    access_control(request)

    s_tag = request.form.get('search_url')
    if s_tag == "":
        return render_template('index.html', token=token, error="Please enter a search term")
    else:
        conn = MySQLdb.connect(host, user, passwrd, db)
        cursor = conn.cursor()

        search_tag_sql = "SELECT * FROM WEB_URL WHERE TAG = %s"
        cursor.execute(search_tag_sql, (s_tag, ))
        search_tag_fetch = cursor.fetchall()
        conn.close()
        return render_template('search.html', host=shorty_host, search_tag=s_tag, table=search_tag_fetch, token=token)


@app.route('/', methods=['GET', 'POST'])
def index():
    access_control(request)

    conn = MySQLdb.connect(host, user, passwrd, db)
    cursor = conn.cursor()

    # Return the full table to displat on index.
    list_sql = "SELECT * FROM WEB_URL;"
    cursor.execute(list_sql)
    result_all_fetch = cursor.fetchall()

    if request.method == 'POST':
        og_url = request.form.get('url_input')
        custom_suff = request.form.get('url_custom')
        tag_url = request.form.get('url_tag')
        if custom_suff == '':
            token_string = random_token()
        else:
            token_string = custom_suff
        if og_url != '':
            if url_check(og_url):

                # Check's for existing suffix
                check_row = "SELECT S_URL FROM WEB_URL WHERE S_URL = %s FOR UPDATE"
                cursor.execute(check_row, (token_string,))
                check_fetch = cursor.fetchone()

                if (check_fetch is None):
                    insert_row = """
                        INSERT INTO WEB_URL(URL , S_URL , TAG) VALUES( %s, %s, %s)
                    """
                    cursor.execute(insert_row, (og_url, token_string, tag_url,))
                    conn.commit()
                    conn.close()
                    e = ''
                    su = shorty_host + token_string
                    return render_template('index.html', shorty_url=su, token=token, error=e)
                else:
                    e = "The Custom suffix already exists . Please use another suffix or leave it blank for random suffix."
                    return render_template('index.html', table=result_all_fetch, host=shorty_host, token=token, error=e)
            else:
                e = "URL entered doesn't seem valid , Enter a valid URL."
                return render_template('index.html', table=result_all_fetch, host=shorty_host, token=token, error=e)

        else:
            e = "Enter a URL."
            return render_template('index.html', table=result_all_fetch, host=shorty_host, token=token, error=e)
    else:
        e = ''
        return render_template('index.html', table=result_all_fetch, host=shorty_host, token=token, error=e)


# Rerouting funciton
@app.route('/<short_url>')
def reroute(short_url):
    print("REROUTE {}".format(shorty_host))

    conn = MySQLdb.connect(host, user, passwrd, db)
    cursor = conn.cursor()
    platform = request.user_agent.platform
    browser = request.user_agent.browser
    counter = 1

    # Platform , Browser vars

    browser_dict = {'firefox': 0, 'chrome': 0, 'safari': 0, 'other': 0}
    platform_dict = {'windows': 0, 'iphone': 0, 'android': 0, 'linux': 0, 'macos': 0, 'other': 0}

    # Analytics
    if browser in browser_dict:
        browser_dict[browser] += 1
    else:
        browser_dict['other'] += 1

    if platform in iter(platform_dict.keys()):
        platform_dict[platform] += 1
    else:
        platform_dict['other'] += 1

    cursor.execute("SELECT URL FROM WEB_URL WHERE S_URL = %s;", (short_url,))

    try:
        new_url = cursor.fetchone()[0]
        print(new_url)

        # Update Counters
        counter_sql = """
                UPDATE {tn} SET COUNTER = COUNTER + {og_counter},
                CHROME = CHROME + {og_chrome}, FIREFOX = FIREFOX + {og_firefox},
                SAFARI = SAFARI + {og_safari}, OTHER_BROWSER = OTHER_BROWSER + {og_oth_brow},
                ANDROID = ANDROID + {og_andr}, IOS = IOS + {og_ios},
                WINDOWS = WINDOWS + {og_windows} , LINUX = LINUX + {og_linux},
                MAC = MAC + {og_mac} , OTHER_PLATFORM = OTHER_PLATFORM + {og_plat_other} WHERE S_URL = %s;
        """.format(
            tn="WEB_URL",
            og_counter=counter,
            og_chrome=browser_dict['chrome'],
            og_firefox=browser_dict['firefox'],
            og_safari=browser_dict['safari'],
            og_oth_brow=browser_dict['other'],
            og_andr=platform_dict['android'],
            og_ios=platform_dict['iphone'],
            og_windows=platform_dict['windows'],
            og_linux=platform_dict['linux'],
            og_mac=platform_dict['macos'],
            og_plat_other=platform_dict['other'])
        cursor.execute(counter_sql, (short_url, ))
        conn.commit()
        conn.close()

        return redirect(new_url)

    except Exception:
        traceback.print_exc()
        return render_template('404.html'), 404


@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logging.error(
        '%s %s %s %s %s %s', timestamp, request.remote_addr,
        request.method, request.scheme, request.full_path, response.status)

    return response


@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logging.error(
        '%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
        timestamp, request.remote_addr, request.method,
        request.scheme, request.full_path, tb)
    return make_response(e, 405)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
