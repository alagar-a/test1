import pymysql
import yaml

config = {}
db_conn = None
db_cursor = None

def initialize_connection():
	global config, db_conn, db_cursor
	try:
		conf = yaml.load(open("/project/backend/conf/db_conf.yaml"))
		db_conn = pymysql.connect(host=conf['host'], port=3306, user=conf['user'], passwd=conf['password'], db=conf['database'])
	except Exception as e:
		print str(e)
		sys.exit(0)

def execute_query(sql,params=None):
	try:
		db_cursor = db_conn.cursor(pymysql.cursors.DictCursor)
		db_cursor.execute(sql,params)
		result = db_cursor.fetchall();
		db_conn.commit()
		db_cursor.close()
		return result
	except:
		initialize_connection()

def get_monitor_objects():
	query = "select * from monitor_objects"
	return execute_query(query)

		
