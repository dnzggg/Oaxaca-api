from common import connector

enum_list = connector.execute_query('''
	SELECT type.typname,
	enum.enumlabel AS value
	FROM pg_enum AS enum
	JOIN pg_type AS type
	ON (type.oid = enum.enumtypid)
	GROUP BY enum.enumlabel,
	type.typname
	''')

print(enum_list)
