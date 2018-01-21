import MySQLdb as sql

_USER = 'nilrogen'
_PASS = 'password'

conn = sql.connect(db='BStock', user=_USER, passwd=_PASS)

curs = conn.cursor()
curs.execute('''INSERT INTO marketplace (mktpName, mktpDescriptor)
                VALUES ('testname', 23);''')


conn.commit()
conn.close()
