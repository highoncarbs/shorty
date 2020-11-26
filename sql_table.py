import MySQLdb

'''
    SQL Table Create Statement,
    Follow the same order as given.
'''

mysql_table = '''
        CREATE TABLE WEB_URL(
        ID INT AUTO_INCREMENT,
        URL VARCHAR(512),
        S_URL VARCHAR(80),
        TAG VARCHAR(80),
        COUNTER INT DEFAULT 0,
        CHROME INT DEFAULT 0,
        FIREFOX INT DEFAULT 0,
        SAFARI INT DEFAULT 0,
        OTHER_BROWSER INT DEFAULT 0,
        ANDROID INT DEFAULT 0,
        IOS INT DEFAULT 0,
        WINDOWS INT DEFAULT 0,
        LINUX INT DEFAULT 0,
        MAC INT DEFAULT 0,
        OTHER_PLATFORM INT DEFAULT 0,
        PRIMARY KEY(ID));
'''


def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False


def ensureTableExists(host, user, passwrd, db):
    conn = MySQLdb.connect(host, user, passwrd, db)
    if not checkTableExists(conn, "WEB_URL"):
        create_table = mysql_table
        cursor = conn.cursor()
        cursor.execute(create_table)

        conn.close()
