import populate_db
import requests


def populate_tables():
	
	populate_db.populate()
	create_data()

def create_data():
	
	url = "http://localhost:5000/create_order"

	print("ADDING ORDERS")

	order_data = [
		{"table_num" : 1, "items" : [1, 2, 3], "customer" : "example@example.com"},
		{"table_num" : 2, "items" : [4, 4, 5], "customer" : "example@example.com"},
		{"table_num" : 3, "items" : [11, 2, 12, 2, 10, 3], "customer" : "example@example.com"},
		{"table_num" : 4, "items" : [10, 16, 4, 4, 5], "customer" : "example@example.com"},
	]

	for order in order_data:
		r = requests.post(url, json=order)
		print(r.text)

if __name__ == "__main__":
	populate_tables()
