import MySQLdb



server_address = "localhost"
username = "root"
password = "windows2014"

def dbConnect(db_name):
	print 'dbConnect...'
	return MySQLdb.connect(server_address, username, password, db_name)

def dbCreateTable(conn, tbl_name, cmd):
	cursor = conn.cursor()
	x = "DROP TABLE IF EXISTS"
	cursor.execute("DROP TABLE IF EXISTS " + tbl_name)
	cursor.execute(cmd)
	return

def dbInsertTable(conn, cmd):
	cursor = conn.cursor()
	cursor.execute(cmd)
	return

def dbCommit(conn):
	return conn.commit()
	
def dbClose(con):
	return con.close()


