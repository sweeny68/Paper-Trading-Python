import sqlite3
import requests

currency_pairs = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/CHF": "USDCHF=X",
    "AUD/USD": "AUDUSD=X",
    "USD/CAD": "USDCAD=X",
    "NZD/USD": "NZDUSD=X",
    "EUR/GBP": "EURGBP=X"
}

# Contains functions to interact with the database

DB_FILE = 'main.db'

def create_account(dob, first_name, surname, username, password, email, phone):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO customers (dob, first_name, surname, username, password, email, phone) 
        VALUES (?, ?, ?, ?, ?, ?, ?)''', (dob, first_name, surname, username, password, email, phone))

        conn.commit()
        return True  # Account created successfully

    except sqlite3.IntegrityError:
        return False  # Username already exists
    except Exception as e:
        print(f"Error creating account: {e}")
        return False  # Error occurred
    finally:
        conn.close()

def create_account_staff(dob, first_name, surname, username, password):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO staff (dob, first_name, surname, username, password) 
        VALUES (?, ?, ?, ?, ?)''', (dob, first_name, surname, username, password))

        conn.commit()
        return True  # Account created successfully

    except sqlite3.IntegrityError:
        return False  # Username already exists
    except Exception as e:
        print(f"Error creating account: {e}")
        return False  # Error occurred
    finally:
        conn.close()

def get_login_details(username, password):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Check if the username and password match  record in the customers table
        cursor.execute('''
            SELECT *
            FROM customers 
            WHERE username = ? AND password = ?''', (username, password))

        result = cursor.fetchone()  # Fetch one matching record

        if result:
            return True  # Username and password match
        else:
            return False  # No match found

    except Exception as e:
        print(f"Error verifying login: {e}")
        return False  # Some error occurred
    finally:
        conn.close()

def get_login_details_staff(username, password):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Check if the username and password match  record in the customers table
        cursor.execute('''
            SELECT *
            FROM staff 
            WHERE username = ? AND password = ?''', (username, password))

        result = cursor.fetchone()  # Fetch one matching record

        if result:
            return True  # Username and password match
        else:
            return False  # No match found

    except Exception as e:
        print(f"Error verifying login: {e}")
        return False  # Some error occurred
    finally:
        conn.close()

def store_order(customer_id, currency_pair, order_type, amount, price, order_time):

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO orders (customer_id, currency_pair, order_type, amount, price, order_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (customer_id, currency_pair, order_type, amount, price, order_time))

        # Commit the transaction
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e  # Re-raise the exception to handle it in the caller function

def get_customer_details(username, password):
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        # Verify the username and password
        cursor.execute('''
            SELECT customer_id, balance
            FROM customers 
            WHERE username = ? AND password = ?
        ''', (username, password))
        result = cursor.fetchone()

        if result:
            # Store the logged-in customer's ID and Balance
            customer_id, customer_balance = result

            # Return details
            return customer_id, customer_balance
        else:
            raise ValueError("Invalid username or password")
        
def fetch_orders():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()
    conn.close()
    return orders

def get_exchange_rate(base, target):
    url = f"https://api.exchangerate.host/convert?from={base}&to={target}&amount=1&access_key=759cb4e113f619c524583646dfdef32e"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Debug Info - Status Code: {response.status_code}, Response: {response.text}")
        data = response.json()
        return data.get('result', None)
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None

def close_trade(order_id, closing_price):

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Fetch the order details to move to the history table
        cursor.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,))
        order = cursor.fetchone()

        if not order:
            raise ValueError("Order not found.")

        # Extract order details
        open_price = order[5] 
        major = order[2]
        major_ticker = currency_pairs[major] # Convert to ticker value for calculations and api download
        print(major_ticker)
        amount = order[4]  
        order_type = order[3]

        # Account size (default to 100,000)
        account_size = 100000

        # Format base and quote currency
        base_currency, quote_currency = major_ticker[:3], major_ticker[3:6]
        base_currency = base_currency.upper()
        quote_currency = quote_currency.upper()

        # Fetch the exchange rate for base to gbp and quote to gbp
        rate_quote = get_exchange_rate(quote_currency, 'GBP')
        rate_base = get_exchange_rate(base_currency, 'GBP')
        if rate_quote:
            print(f"Exchange Rate quote {quote_currency} to 'GBP': {rate_quote}")
        if rate_base:
            print(f"Exchange Rate base {base_currency} to 'GBP': {rate_base}")
        else:
            print("Failed to fetch exchange rate.")

        # check if base currency gbp, if not then convert
        if base_currency == 'GBP':
            return
        else:
            amount_gbp = amount * rate_base
            print(f'{amount} {base_currency} is now {amount_gbp}GBP. ')

        # Calculate the pip difference based on the price movement
        pip_multiplier = 100
        pip_difference = (open_price-closing_price) * pip_multiplier

        # Calculate profit/loss:
        price_diff = closing_price - open_price
        profit_loss_quote_currency = (price_diff / open_price) * amount_gbp
        
        profit_loss_gbp = profit_loss_quote_currency * rate_quote

        # If the order was a sell, we reverse the profit/loss sign
        if order_type == 'SELL':
            profit_loss_gbp = -profit_loss_gbp
        

        # Insert the trade details into the history table
        print(f"Values to Insert: Order ID: {order[0]}, Major: {major}, Customer ID: {order[1]}, "
        f"Order Type: {order_type}, Amount: {amount_gbp}, Closing Price: {closing_price}, "
        f"Pip Difference: {pip_difference}, Profit/Loss: {profit_loss_gbp}")


        cursor.execute('''
            INSERT INTO history (order_id, currency_pair, customer_id, order_type, amount, price, 
                                 order_time_close, pip_difference, profit_loss)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?)
        ''', (order[0], major, order[1], order_type, amount_gbp, closing_price, pip_difference, profit_loss_gbp))

        # Remove the order from the orders table
        cursor.execute('DELETE FROM orders WHERE order_id = ?', (order_id,))

        # Commit changes
        conn.commit()

        print(f"Trade closed. Pip difference: {pip_difference:.2f}, Profit/Loss: {profit_loss_gbp:.2f}")
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_currency_pair(order_id):

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT currency_pair FROM orders WHERE order_id = ?', (order_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        raise ValueError("Currency pair not found for the given order ID.")
    except Exception as e:
        raise e

