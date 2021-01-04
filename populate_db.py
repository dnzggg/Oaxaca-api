# SQL_DATA FILE LOCATION:
db_data_loc = "sql/db_data/"
##################################################################################################

import psycopg2
import sys
import re
import os
import csv
from common import connector

# initialise new connectoin
connection = connector.get_connection()
cursor = connection.cursor()
verbose = False

def get_column_names(table_name):
	col_names = []

	# Get the column names for the table from given tables info schema
	cursor.execute("""SELECT column_name
					FROM INFORMATION_SCHEMA.COLUMNS
					WHERE table_name=%s""", (table_name,))
	results = cursor.fetchall()

	# compose the results into a list and return it
	for r in results:
		col_names.append(r[0])

	return col_names

def insert_many(table_name, col_names, csv_file):
	# Open a new csv.reader object, very handy package that reads lines of csv
	# straight in as iterable objects
	reader = csv.reader(csv_file)

	if verbose:
		print("INSERTING VALUES INTO %s" % table_name)

	# For each row in the csv file
	for row in reader:
		try:
			# Generate insertion statement based on values given
			query = "INSERT INTO " + table_name + " (" + ", ".join(col_names) + ")"
			query += " VALUES(" + ", ".join(["%s"] * len(col_names)) + ")"
			# "mogrify" to input the values into the query, only required for logs
			# normally you can just do cursor.execute(query, (,<tuple_of_values>,)
			rendered_query = cursor.mogrify(query, row)
			cursor.execute(rendered_query)
			if verbose: print("INSERTION SUCCESSFUL FOR VALUES " + ", ".join(row))
		# If the row already exists in db, skip it and restart transaction with commit()
		# required because psycopg2 will ignore all queries after a failure within the same transaction
		except psycopg2.errors.UniqueViolation:
			if verbose:
				print("Entry already exists in database, skipping")
			connection.commit()

	connection.commit()


def insert_from_csv(data_location, table_name=None, serial_id=False):
	try:
		# Open the csv file
		source = open(data_location)

		# If table name isn't given, assume file name IS table name
		if table_name == None:
			# Scary regex, strips the path (.*/) and extension (.csv) from file name
			table_name = re.sub(r"(.*/)|(.csv)", "", data_location)

		# Fetch column names for insert, currently redundant but needed for serial inserts
		col_names = get_column_names(table_name)

		# i
		if serial_id == False:
			insert_many(table_name, col_names, source)
		else:
			# TODO Implement alternative to ignore first column of col_names during insert
			return

	except FileNotFoundError:
		print("ERROR\nCOULD NOT FIND: %s" % data_location)

def populate():
	# Turn on verbose mode if "v" is given as argument to give more detailed logs
	if len(sys.argv) > 1 and sys.argv[1] == "v":
		verbose = True

	print("Initialising schema for database...")
	cursor.execute(open("sql/db_schema.sql").read())
	print("DB schema inserted")

	print("Initialising function schema for database...")
	cursor.execute(open("sql/func_schema.sql").read())
	print("Function schema inserted")

	print("Initialising view schema for database...")
	cursor.execute(open("sql/view_schema.sql").read())
	print("View schema inserted")

	# FOR EACH file in the source folder, pass it to insert_from_csv to decompose and insert
	# TODO Currently no validation to check if files in source are .csv
	print("INSERTING FILES FROM %s INTO DATABASE: %s" % (db_data_loc, connector.db_name))
	for data_file in os.listdir(db_data_loc):
		if data_file != "table_details.csv":
			print("FOUND FILE: %s" % data_file)
			insert_from_csv(db_data_loc + data_file)
			print("%s INSERTED INTO DATABASE" % data_file)

	# temporary fix to allow for email being PK on waiter table
	print("FOUND FILE: %s" % "table_details.csv")
	insert_from_csv("./sql/db_data/" + "table_details.csv")
	print("%s INSERTED INTO DATABASE" % "table_details.csv")

	print("FINISHED...")

if __name__ == "__main__":
	populate()
