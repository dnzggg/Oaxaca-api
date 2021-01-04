# GUIDE TO USING THE API

## Contents

* [Starting the API](#starting-the-api)
* [Outline of usage](#outline-of-usage)
* [API Endpoints](#api-endpoints)
    * [User Authentication & User Creation](#user-authentication--user-creation)
        * [/login](#login)
        * [/logout](#logout)
        * [/signup](#signup)
        * [/waiter_signup](#waiter_signup)
    * [Menu](#menu)
        * [/menu](#menu)
        * [/menu_item_availability](#menu_item_availability)
    * [Notifications](#notifications)
        * [/add_waiter_notification](#add_waiter_notification)
        * [/get_waiter_notifications](#get_waiter_notifications)
        * [/clear_waiter_notifications](#clear_waiter_notifications)
    * [Orders](#orders)
        * [/create_order](#create_order)
        * [/order_event](#order_event)
        * [/get_order](#get_order)
        * [/get_orders](#get_orders)
        * [/get_waiter_orders](#get_waiter_orders)
        * [/get_cust_orders](#get_cust_orders)
        * [/get_old_cust_orders](#get_old_cust_orders)
    * [Payments](#payments)
        * [/verify_payment](#verify_payment)
    * [Sessions](#sessions)
        * [/create_session](#create_session)
        * [/get_session_id](#get_session_id)
        * [/get_session_is_staff](#get_session_is_staff)
        * [/remove_session](#remove_session)
    * [Tables](#tables)
        * [/get_tables](#get_tables)
        * [/get_tables_and_waiters](#get_tables_and_waiters)
        * [/get_unassigned_tables](#get_unassigned_tables)
        * [/table_assignment_event](#table_assignment_event)
        * [/get_waiter_assigned_to_table](#get_waiter_assigned_to_table)
         
        
        
## Starting the api

- In order to start the api, you'll first need all the related python packages.

- start a python virtual environment with  python3 -m venv venv  (from terminal)

- then start working in the environment with  source <your_venv_file>/bin/activate

- now install the requirements with  pip3 install -r requirements.txt

- run main.py to start the server, it should be running on localhost:5000

## Outline of usage
- ALMOST every endpoint in the api is expecting a JSON object along with the request
- ALMOST every endpoint will return a JSON object describing the result, or the requested data.
- ALMOST every endpoint will return an error object of the following form if it fails:

```json
{
  "error" : {
    "success" : false,
    "message" : "A description of the error"
  }
}
```
- This object describes the nature of the error (a call could succeed but still give a warning), and a brief description.

## API endpoints:

## User Authentication & User Creation:

### /login
EXPECTS: JSON object containing username:password pair, and whether or not it is a staff account password
should be a valid sha256 hash:

```json
{
  "email" : "example@example.com",
  "password" : "sha256hash",
  "staff_login" : true
}
```

RETURNS: JSON object containing username of the account that was logged in and a boolean for success

```json
{
  "data" : {
    "username" : "example_username",
    "valid_credentials" : true
  }
}
```

	or an error object

### /logout
EXPECTS: Does not expect any data, but will only execute if their is an active session

RETURNS: JSON object describing success and a message:

  ```json
  {
	"data": {
	  "success" : true,
	  "message" : "Message describing what happened"
	}
  }
  ```

### /signup
EXPECTS: JSON object containing the email, password, firstname and lastname

```json
{
  "email" : "test@customer.com",
  "firstname" : "John",
  "lastname" : "Doe",
  "password" : "super secret password"
}
```

RETURNS: JSON object describing success

  ```json
  {
    "data": {
      "success": true
    }
  }
  ```

	or an error object

### /waiter_signup
EXPECTS: JSON object containing the email, password, firstname, lastname and phone number

```json
{
  "email" : "test@waiter.com",
  "firstname" : "Foo",
  "lastname" : "Bar",
  "password" : "super extra secret password",
  "phone_number" : "07123456789"
}
```

RETURNS: JSON object describing success

  ```json
  {
    "data": {
      "success": true
    }
  }

  ```

	or an error object

## Menu:

### /menu:
+EXPECTS: JSON object containing true or false value for getAll, which determines
if it returns all available items or not respectively. If getAll is not specified it returns only
available menu items

  ```json
  {
    "getAll" : true
  }
  ```

+RETURNS: JSON object containing list of item ids in the form:

  ```json
  {
	"data" : {
	  "items": [
        {
          "available": true,
          "calories": 600,
          "description": "Crips mexican doughnuts with rich chocolate sauce",
          "gluten_free": false,
          "id": 16,
          "image": " http://personal.rhul.ac.uk/zfac/242/Team16/Churros.jpg",
          "name": "Churros",
          "price": "$5.25",
          "type": "dessert",
          "vegan": false,
          "vegetarian": true
        }
      ]
	}
  }
  ```
	or an error object, error object will contain a list valid_events if a bad event argument is given.

### /menu_item_availability:
+EXPECTS: JSON object containing newState which is either true or false, then the id of the menu item

  ```json
  {
    "newState": false,
    "menuId": 1
  }
  ```

+RETURNS: JSON object containing success is true

  ```json
  {
	"data" : {
	   "success": true
	}
  }
  ```
	or an error object, error object will contain a list valid_events if a bad event argument is given.

## Notifications:

### add\_waiter\_notification
EXPECTS: JSON object containing the email of the waiter, customer email and notificiation message:

  ```json
{
    "waiter_email" : "waiter@waiter.com",
    "customer_email" : "example@example.com",
    "message" : "notif. message"
}
  ```

RETURNS: Data object outlining the notification which was added:

```json
{
  "data" : {
    "added_message" : "notif. message",
    "from" : "customer email",
    "to" : "waiter email",
    "success" : true
  }
}
```

	or an error object


### get\_waiter\_notifications
EXPECTS: JSON object containing the waiter\_email:

```json
{
  "waiter_email" : "waiter@waiter.com"
}
```

RETURNS: JSON object containing list of their notifications:

  ```json
  {
    "data": {
      "notifications": [
        [
          2,
          "example@example.com",
          "waiter@waiter.com",
          "notification message for waiter"
        ]
      ],
      "success": true
    }
  }
  ```

	or an error object

### clear\_waiter\_notifications
Clears all notifications from a waiter.
EXPECTS: JSON object containing the waiter\_email:

```json
{
  "waiter_email" : "waiter@waiter.com"
}
```

RETURNS: JSON object describing success

	or an error object

## Orders:

### /create\_order:
EXPECTS: JSON object containing a table number, customer email and a list of item ids in the form:

```json
{
  "table_num" : 1,
  "items" : [1, 2, 3],
  "customer" : "example@example.com"
}
```

RETURNS: JSON object

  ```json
  {
    "data": {
      "items_added": [1, 2, 3],
      "order_id" : 1,
      "success" : true
    }
  }
   ```

	or an error object, will generate an error if one of the item ids given was invalid

### /order\_event:
EXPECTS: JSON object containing an order id and an event in the form, the given event will
be added to the database if it passes the event validation:

```json
{
  "order_id" : 1,
  "order_event" : "request"
}
```

RETURNS: JSON object containing whether or not event was successfully performed:

```json
{
  "data" : {
    "success" : true
  }
}
```

	or an error object

### /get\_order:
EXPECTS: JSON object containing the order id and the customer id (their email)

```json
{
  "order_id": 1,
  "cust_id": "customer@example.com"
}
```

RETURNS: JSON object containing the data requested, if no data exists an empty array will be returned
It also returns the ordered items in a json object containing the quantity ordered and
the price of each item times the quantity

  ```json
  {
    "data": {
      "order": [
        {
          "id": 18,
          "items": [
            {
              "cumulative_price": "$21.00",
              "name": "Churros",
              "quantity": 4
            }
          ],
          "ordered_time": "13:00",
          "price": "$21.00",
          "state": "requested",
          "table_number": 3
        }
      ]
    }
  }
  ```

	or an error object


### /get\_orders:
EXPECTS: JSON object containing the list of states you'd like to get orders for. If you want to
retrieve all orders, then pass an empty array:

  ```json
  {
    "states": ["start", "cooking", "requested"]
  }
  ```

RETURNS: JSON object containing the data requested, if no data exists an empty array will be returned
It also returns the ordered items in a json object containing the quantity ordered and
the price of each item times the quantity. 

**NOTE** - this will only return orders from that day, if you want to get older orders see [get_old_cust_orders](#get_old_cust_orders)

```json
{
  "data": {
    "orders": [
      {
        "id": 1,
        "items": [
          {
            "cumulative_price": "$10.50",
            "name": "Veggie nachos",
            "quantity": 2
          }
        ],
        "ordered_time": "20:46",
        "price": "$10.50",
        "state": "start",
        "table_number": 1
      }
    ]
  }
}
```

	or an error object

### /get\_waiter\_orders:
EXPECTS: JSON object containing the list of states you'd like to get orders for. If you want to
retrieve all orders, then pass an empty array, and the waiter id:  

  ```json
  {
    "states": ["start", "cooking", "requested"],
    "waiter_id" : "waiter@waiter.com"
  }
  ```

RETURNS: JSON object containing the data requested, for that specific waiter

  ```json
  {
  "data": {
    "orders": [
      {
        "id": 1,
        "items": [
          {
            "cumulative_price": "$10.50",
            "name": "Veggie nachos",
            "quantity": 2
          }
        ],
        "ordered_time": "20:46",
        "price": "$10.50",
        "state": "start",
        "table_number": 1
        }
      ]
    }
  }
  ```

	or an error object

### /get\_cust\_orders:
EXPECTS: JSON object containing the email of the customer:

**NOTE** - this will only return orders from that day, if you want to get older orders see [get_old_cust_orders](#get_old_cust_orders)

  ```json
  {
    "cust_id" : "customer@example.com"
  }
  ```

RETURNS: JSON object containing all the orders for that customer

  ```json
  {
  "data": {
    "orders": [
      {
        "id": 1,
        "items": [
          {
            "cumulative_price": "$10.50",
            "name": "Veggie nachos",
            "quantity": 2
          }
        ],
        "ordered_time": "20:46",
        "price": "$10.50",
        "state": "start",
        "table_number": 1
        }
      ]
    }
  }
  ```

	or an error object


### /get\_old\_cust\_orders:
EXPECTS: JSON object containing the email of the customer:

  ```json
  {
    "cust_id" : "customer@example.com"
  }
  ```

RETURNS: JSON object containing all the orders for that customer ever. 

**NOTE** - this will get all orders that are not from the current day related to the customer, 
to get orders from today see all other order endpoints

  ```json
  {
  "data": {
    "orders": [
      {
        "id": 1,
        "items": [
          {
            "cumulative_price": "$10.50",
            "name": "Veggie nachos",
            "quantity": 2
          }
        ],
        "ordered_time": "20:46:54",
        "price": "$10.50",
        "state": "start",
        "table_number": 1
        }
      ]
    }
  }
  ```

	or an error object


## Payments:

### /verify\_payment
EXPECTS: JSON object containing the card number, CVV, sort number and the expiry date of the form month year with
nothing separating the month and year

```json
{
  "card_num" : "123456789123456",
  "cvv" : "123",
  "sort_num" : "123456",
  "expiry_date" : "0821"
}
```

RETURNS: JSON object describing success

  ```json
  {
    "data": {
      "success" : true 
    }
  }

  ```

	or an error object

## Sessions:

### /create\_session
EXPECTS: JSON object containing the email and staff:

```json
{
  "email" : "example@example.com",
  "staff" : false
}
```

RETURNS: JSON object describing success

  ```json
  {
    "data": {
      "session_id": "example@example.com",
      "staff":  false
    }
  }

  ```

	or an error object

### /get\_session\_id
EXPECTS: Does not expect any data but will return error if no session is active

RETURNS: JSON
```json
{
  "data" : {
    "session_id" : "example@example.com"
  }
}
```

	or an error object

### /get\_session\_is\_staff
EXPECTS: Does not expect any data but will return error if no session is active

RETURNS: JSON
```json
{
  "data" : {
    "staff" : true
  }
}
```

	or an error object

### /remove\_session
EXPECTS: Does not expect any data but will return error if no session is active

RETURNS: JSON
```json
{
  "data" : {
    "removed_session_id" : "example@example.com",
    "success" : true
  }
}
```

	or an error object

## Tables:

### /get\_tables
EXPECTS: Does not expect any data

RETURNS: JSON with an array of every table in order
```json
{
  "data" : {
    "tables" : [
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
      9,
      10
    ]
  }
}
```

### /get\_tables\_and\_waiters
EXPECTS: Does not expect any data

RETURNS: JSON with an object containing the email, firstname, lastname and table number the waiter is assigned to
```json
{
  "data" : {
    "tables" : {
      "email": "test@waiter.com",
      "firstname": "test",
      "lastname": "user",
       "table_number": 1
    }
  }
}
```
  
  
### /get\_unassigned\_tables
EXPECTS: Does not expect any data

RETURNS: JSON with an array of every table that does not have a waiter assigned to it
```json
{
  "data" : {
    "tables" : [
      {
        "table_number" : 2
      },{
        "table_number" : 6
      }
    ]
  }
}
```
  
### /table\_assignment\_event
EXPECTS: JSON object containing the waiter email and the table number which the waiter is going to be assigned to

```json
{
  "data" : {
    "waiter_id" : "waiter@example.com",
    "table_id" : "1"
  }
}
```

RETURNS: JSON with an array of every table that does not have a waiter assigned to it
  ```json
    {
      "data" : {
        "success" : true
      }
    }
  ```
  
  	or an error object
  	
### /get\_waiter\_assigned_to_table
EXPECTS: JSON object containing the table number to get the waiter associated with it

```json
{
  "data" : {
    "table_id" : "1"
  }
}
```

RETURNS: JSON with an array of every table that does not have a waiter assigned to it
```json
{
  "data" : {
    "waiter_id" : "waiter@example.com"
  }
}
```
  
  	or an error object 	
