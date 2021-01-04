# CHANGE DB NAME:
db_name = "det863at6goa6t"
# CHANGE USER:
user = "gqyafrbphewugd"
# CHANGE DB PASSWORD:
password = "f1365952e1828e5775397e682500bd1fd1a04297effd3eb40c240c0884a28cfb"
# CHANGE DB HOST:
host  = "ec2-54-217-204-34.eu-west-1.compute.amazonaws.com"
# CHANGE PORT:
port = "5432"

##################################################################################################

import psycopg2

val = None
connection = None


# closes the connection
def exit():
	global connection
	if connection:
		connection.close()
		connection = None


# performs query to the database and returns the result
# takes arguments that are substituted for '%s' in the query
def execute_query(query_string, args=None):
	global connection
	if not connection:
		connection = get_connection()
	cursor = connection.cursor()
	result = None
	try:
		if args:
			cursor.execute(query_string, args)  # flasks equivalent to prepared statement prevents sql injections
		else:
			cursor.execute(query_string)
		connection.commit()
		result = cursor.fetchall()

	except:  # catches errors in the query or connection
		print("Query failed")
		cursor.close()
		raise
		result = None

	finally:
		cursor.close()

	return result


# this is necessary because insert query's return None on most occasions
# we also need to handle insert statement failures differently
def execute_insert_query(query_string, args=None):
	global connection
	if not connection:
		connection = get_connection()
	cursor = connection.cursor()
	try:
		if args:
			cursor.execute(query_string, args)
		else:
			cursor.execute(query_string)
		connection.commit()
	except (Exception, psycopg2.Error) as error:
		print("Query failed")
		cursor.execute("ROLLBACK")
		raise
		connection.commit()
		return False
	finally:
		cursor.close()

	return True


# makes the connection to the database
def get_connection():
	global connection
	if connection:
		return connection
	connection = psycopg2.connect(database=db_name, user=user, password=password, host=host)
	return connection


# initialises connection upon startup
def __init__():
	global connection
	connection = psycopg2.connect(database=db_name, user=user, password=password, host=host)
