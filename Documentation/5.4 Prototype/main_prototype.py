import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
import yfinance as yf #VERSION 0.1.70
import mplfinance as mpf #VERSION 0.12.9b7
import sv_ttk
from data_access_prototype import *
from datetime import datetime
import re
import warnings

# Ignore warnigns for compatability with future versions of yfinance, use version 0.1.70
warnings.filterwarnings("ignore", category=FutureWarning, module="yfinance")

# Function to handle login
def login():

    global customer_id, customer_balance

    # get username from entry
    username = entry_username.get()
    password = entry_password.get()
    
    #Login Logic
    if not username or not password:
        messagebox.showerror("Login Error", "All fields must be filled.")
        return
    if get_login_details(username, password):
        messagebox.showinfo("Login Successful", f"Welcome, {username}.")
        open_home()
    elif get_login_details_staff(username, password):
        messagebox.showinfo("Login Successful", "Admin Login Successful!")
        open_home_staff()
    else:
        messagebox.showerror("Login Error", "Invalid username or password")

    customer_id, customer_balance = get_customer_details(username, password)

# Function to open homepage
def open_home():

    # Hide the main login window
    root.withdraw()
    
    # Create a new window
    new_window = tk.Toplevel(root)
    new_window.title("Welcome")
    new_window.geometry("400x600")
    sv_ttk.set_theme("light") 
    
    # Add some content to the home page
    home_label = tk.Label(new_window, text='Home', font=("Helvetica", 20))
    home_label.pack(padx=10, pady=20)

    welcome_label = tk.Label(new_window, text="Welcome to Investor Centre LTD!", font=("Helvetica", 14))
    welcome_label.pack(padx=10, pady=20)
   
    # Chart button to bring up the chart configurer
    chart_button = ttk.Button(new_window, text="Chart", command=new_window.destroy(), width=11)
    chart_button.pack(padx=10, pady=20)

    # Manage orders button to bring up the order menu
    order_button = ttk.Button(new_window, text="Manage Orders", command=manage_orders_window, width=11)
    order_button.pack(padx=10, pady=20)

    # Button to close the new window and bring back the login window
    close_button = ttk.Button(new_window, text="Logout", command=lambda: (new_window.destroy(), root.deiconify()), width=11)
    close_button.pack(padx=10, pady=20)

    # Button to add customer balance
    balance_button = ttk.Button(new_window, text="Balance", command=balance_window, width=11)
    balance_button.pack(padx=10, pady=20)

    # Button to view trade history
    history_button = ttk.Button(new_window, text="View history", command=history_window, width=11)
    history_button.pack(padx=10, pady=20)

# function to open home page as an admin
def open_home_staff():

    # Hide the main login window
    root.withdraw()
    
    # Create a new window
    new_window = tk.Toplevel(root)
    new_window.title("Welcome")
    new_window.geometry("600x400")
    sv_ttk.set_theme("light") 
    
    # Add some content to the home page
    home_label = tk.Label(new_window, text='Home', font=("Helvetica", 20))
    home_label.pack(padx=10, pady=20)

    # Welcome label
    welcome_label = tk.Label(new_window, text="Welcome to Investor Centre LTD!", font=("Helvetica", 14))
    welcome_label.pack(padx=10, pady=20)
   
    # Chart button to bring up the chart configurer
    chart_button = ttk.Button(new_window, text="Chart", command=new_window.destroy(), width=10)
    chart_button.pack(padx=10, pady=20)

    # Manage orders button to bring up the order menu
    order_button = ttk.Button(new_window, text="Manage Orders", command=manage_orders_window, width=10)
    order_button.pack(padx=10, pady=20)

    # Staff account creation button
    order_button = ttk.Button(new_window, text="Create Staff account", command=createAccountWindowStaff, width=10)
    order_button.pack(padx=10, pady=20)

    # Button to close the new window and bring back the login window
    close_button = ttk.Button(new_window, text="Logout", command=lambda: (new_window.destroy(), root.deiconify()), width=10)
    close_button.pack(padx=10, pady=20)

# Function to bring up account creation window
def create_account_window():
    # Create the account window
    new_window = tk.Toplevel()
    new_window.title("Create Account")
    new_window.geometry('400x520')
    sv_ttk.set_theme("light") 

    # Define padding and styles
    padding = {'padx': 15, 'pady': 10}

    # Add a title label
    title_label = ttk.Label(new_window, text="Create Account", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

    # First name label and entry
    label_first = ttk.Label(new_window, text="First Name:")
    label_first.grid(row=1, column=0, sticky="w", **padding)
    entry_first = ttk.Entry(new_window)
    entry_first.grid(row=1, column=1, **padding)

    # Surname label and entry
    label_second = ttk.Label(new_window, text="Surname:")
    label_second.grid(row=2, column=0, sticky="w", **padding)
    entry_second = ttk.Entry(new_window)
    entry_second.grid(row=2, column=1, **padding)

    # DOB label and entry
    label_dob = ttk.Label(new_window, text="Date of Birth (xx/xx/xx):")
    label_dob.grid(row=3, column=0, sticky="w", **padding)
    entry_dob = ttk.Entry(new_window)
    entry_dob.grid(row=3, column=1, **padding)

    # Email label and entry
    label_email = ttk.Label(new_window, text="Email:")
    label_email.grid(row=4, column=0, sticky="w", **padding)
    entry_email = ttk.Entry(new_window)
    entry_email.grid(row=4, column=1, **padding)

    # Phone number label and entry
    label_phone = ttk.Label(new_window, text="Phone Number:")
    label_phone.grid(row=5, column=0, sticky="w", **padding)
    entry_phone = ttk.Entry(new_window)
    entry_phone.grid(row=5, column=1, **padding)

    # Username label and entry
    label_user = ttk.Label(new_window, text="Username:")
    label_user.grid(row=6, column=0, sticky="w", **padding)
    entry_user = ttk.Entry(new_window)
    entry_user.grid(row=6, column=1, **padding)

    # Password label and entry
    label_pass = ttk.Label(new_window, text="Password:")
    label_pass.grid(row=7, column=0, sticky="w", **padding)
    entry_pass = ttk.Entry(new_window, show="*")  
    entry_pass.grid(row=7, column=1, **padding)

    # Create account button
    create_button = ttk.Button(new_window, text="Create Account", command=lambda: create_new_account(), width=11)
    create_button.grid(row=8, column=1, columnspan=1, pady=(20, 10))

    # Button to close the window
    close_button = ttk.Button(new_window, text="Close", command=new_window.destroy, width=11)
    close_button.grid(row=8, column=0, columnspan=1, pady=(20, 10)) 

    # Function to handle account creation
    def create_new_account():
        dob = entry_dob.get()
        first = entry_first.get()
        surname = entry_second.get()
        username = entry_user.get()
        password = entry_pass.get()
        email = entry_email.get()
        phone = entry_phone.get()

        # Validation patterns
        dob_pattern = r'^\d{2}/\d{2}/\d{4}$'
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phone_pattern = r'^\d{11}$'  

        # Validate fields

        # Check if all fields are filled
        if not dob or not first or not surname or not username or not password or not email or not phone:
            messagebox.showinfo('Error', "All fields must be filled.")
            return
        
        if not first.isalpha():
            messagebox.showinfo('Error', "First name must contain only alphabetic characters.")
            return

        if not surname.isalpha():
            messagebox.showinfo('Error', "Surname must contain only alphabetic characters.")
            return
        
        if not re.match(dob_pattern, dob):
            messagebox.showinfo('Error', "Date of Birth must be in the format DD/MM/YYYY.")
            return

        if not re.match(email_pattern, email):
            messagebox.showinfo('Error', "Invalid email format.")
            return

        if not re.match(phone_pattern, phone):
            messagebox.showinfo('Error', "Phone number must contain only digits 11 characters long.")
            return

        # Call create_account() from data_access.py
        if create_account(dob, first, surname, username, password, email, phone):
            messagebox.showinfo("Success", "Account created successfully!")
        else:
            messagebox.showerror("Error", "Failed to create account. Username may already exist.")

        new_window.destroy()

# Function to open staff account creation window
def createAccountWindowStaff():

    # Function to help handle account creation
    def create_new_account_staff():
        dob = entry_dob.get()
        first = entry_first.get()
        surname = entry_second.get()
        username = entry_user.get()
        password = entry_pass.get()

        # Call create_account() from data_access.py
        if create_account_staff(dob, first, surname, username, password):
            messagebox.showinfo("Success", "Account created successfully!")
        else:
            messagebox.showerror("Error", "Failed to create account. Username may already exist.")

    # Create the main window
    new_window = tk.Toplevel()
    new_window.title("Create Staff Account")
    new_window.geometry('300x300')
    sv_ttk.set_theme("light") # Set theme

    # first name label and entry
    label_first = tk.Label(new_window, text="First name")
    label_first.grid(row=1, column=1)  
    entry_first = tk.Entry(new_window)
    entry_first.grid(row=1, column=2)

    # Surname label and entry
    label_second = tk.Label(new_window, text="Surname")
    label_second.grid(row=2, column=1)  
    entry_second = tk.Entry(new_window)
    entry_second.grid(row=2, column=2)

    # DOB label and entry
    label_dob = tk.Label(new_window, text="DOB")
    label_dob.grid(row=3, column=1)  
    entry_dob = tk.Entry(new_window)
    entry_dob.grid(row=3, column=2)

    # Username label and entry
    label_user = tk.Label(new_window, text="Username")
    label_user.grid(row=4, column=1)  
    entry_user = tk.Entry(new_window)
    entry_user.grid(row=4, column=2) 

    # Password label and entry
    label_pass = tk.Label(new_window, text="Password")
    label_pass.grid(row=5, column=1)  
    entry_pass = tk.Entry(new_window)
    entry_pass.grid(row=5, column=2)

    # Create account button
    create_button = ttk.Button(new_window, text="Create account", command=create_new_account_staff)
    create_button.grid(row=6, column=1, pady=20)

# Function to open a window to manage orders
def manage_orders_window():

    # Function to BUY
    def manage_orders_buy():

        # Specify order type
        order_type = 'BUY'

        #Get gbp value with validation
        try:
            gbp_value = int(gbp_entry.get())
        except:
            messagebox.showerror("Error", "Please enter a valid amount in GBP.")
            return
        
        if gbp_value > customer_balance:
           messagebox.showerror("Error", "Insufficient funds")
           return
         
        # Get selected currency pair
        major = major_dropdown.get()

        # validate selection is in the list
        if major not in major_options:
            tk.messagebox.showerror("Input Error", f"Invalid Currency Pair '{major}'. Please make a valid selection.")
            return

        # Get ticker value from pair
        major_ticker = currency_pairs[major]

        # Create the new window for order confirmation
        new_window = tk.Toplevel()
        new_window.title(f"Order for {major[:6]}")
        new_window.geometry('250x250')
        new_window.resizable(width=False, height=False)
        sv_ttk.set_theme("light")  # Set theme

        # Fetch the latest price data for the selected pair
        try:
            forex_data_minute = yf.download(major_ticker, period='1d', interval='1m')
            open_price = forex_data_minute['Open'].iloc[-1]
        except:
            print('Failed to retrieve data from yfinance.')

        # Round to 4dp
        open_price = round(open_price, 4)

        # To nearest second
        time = datetime.now().replace(microsecond=0)

        # Display the current open, close price, and time
        label_time = tk.Label(new_window, text=f"Time: {time}")
        label_time.pack(pady=10)

        label_major = tk.Label(new_window, text=f"Pair: {major}")
        label_major.pack(pady=10)

        label_open = tk.Label(new_window, text=f"Current price: {open_price}")
        label_open.pack(pady=10)

        # Validation to ensure an amount has been entered
        if gbp_value:

            label_gbp_amount = tk.Label(new_window, text=f"Order size: £{gbp_value}")
            label_gbp_amount.pack(pady=10)
        
        print(major)

        # Store the order ddetails in the database
        try:
            store_order(customer_id=customer_id, currency_pair=major, order_type=order_type, amount=gbp_value, price=open_price, order_time=time)
            tk.Label(new_window, text="Order placed successfully!", fg="green").pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to store order: {e}")

    # Function to SELL
    def manage_orders_sell():
        
        # Specify order type
        order_type = 'SELL'

        #Get gbp value with validation
        try:
            gbp_value = int(gbp_entry.get())
        except:
            messagebox.showerror("Error", "Please enter a valid amount in GBP.")
            return
        
        if gbp_value > customer_balance:
           messagebox.showerror("Error", "Insufficient funds")
           return

        # Get selected currency pair
        major = major_dropdown.get()

        # Get ticker value from pair
        major_ticker = currency_pairs[major]

        # Create the new window for order confirmation
        new_window = tk.Toplevel()
        new_window.title(f"Order for {major[:6]}")
        new_window.geometry('300x300')
        sv_ttk.set_theme("light")  # Set theme

        # Fetch the latest price data for the selected pair
        try:
            forex_data_minute = yf.download(major_ticker, period='1d', interval='1m')
            open_price = forex_data_minute['Open'].iloc[-1]
        except:
            print('Failed to retrieve data from yfinance.')

        # Round to 4dp
        open_price = round(open_price, 4)

        # To nearest second
        time = datetime.now().replace(microsecond=0)

        # Display the current open, close price, and time
        label_time = tk.Label(new_window, text=f"Time: {time}")
        label_time.pack(pady=10)

        label_major = tk.Label(new_window, text=f"Pair: {major}")
        label_major.pack(pady=10)

        label_open = tk.Label(new_window, text=f"Current price: {open_price}")
        label_open.pack(pady=10)

        # Validation to ensure an amount has been entered
        if gbp_value:

            label_gbp_amount = tk.Label(new_window, text=f"Order size: £{gbp_value}")
            label_gbp_amount.pack(pady=10)
        
        print(major)

        # Store the order ddetails in the database
        try:
            store_order(customer_id=customer_id, currency_pair=major, order_type=order_type, amount=gbp_value, price=open_price, order_time=time)
            tk.Label(new_window, text="Order placed successfully!", fg="green").pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to store order: {e}")

    # function to update the price when a pair is selected
    def update_open_price(event):
        selected_pair = selected_major.get()
        ticker = currency_pairs[selected_pair]
    
        # Fetch the latest data
        forex_data_minute = yf.download(ticker, period='1d', interval='1m')
        open_price = forex_data_minute['Open'].iloc[-1]
    
        # Update the label with the new open price
        label_open.config(text=f"Current price: {open_price}")

    # Currency pair options
    major_options = list(currency_pairs.keys())

    selected_major = tk.StringVar(value=major_options[0])

    # Create the new window
    new_window = tk.Toplevel()
    new_window.title("Manage Orders")
    new_window.geometry('400x515')
    sv_ttk.set_theme("light")  # Set theme

    # Fetch initial price data for the default selected pair
    ticker = currency_pairs[selected_major.get()]  # Get the value "EURUSD=X"
    forex_data_minute = yf.download(ticker, period='1d', interval='1m')
    open_price = forex_data_minute['Open'].iloc[-1]
    open_price = round(open_price, 4) #round to 4dp

    # Dropdown for selecting currency pair
    major_label = tk.Label(new_window, text="Select Pair:")
    major_label.pack(pady=5)

    major_dropdown = ttk.Combobox(new_window, textvariable=selected_major, values=major_options)
    major_dropdown.pack(pady=5)

    # link selected pair to open price
    major_dropdown.bind("<<ComboboxSelected>>", update_open_price)

    # Labels to display open and close price
    label_open = tk.Label(new_window, text=f"Current price: {open_price}")
    label_open.pack(pady=10)

    # Entry box for pip value input
    pip_label = tk.Label(new_window, text="Enter GBP Amount:")
    pip_label.pack(pady=5)

    gbp_entry = tk.Entry(new_window)
    gbp_entry.pack(pady=5)

    # Button to buy
    buy_button = ttk.Button(new_window, text="Buy", command=manage_orders_buy, width=11)
    buy_button.pack(padx=10, pady=20)

    # Button to sell
    sell_button = ttk.Button(new_window, text="Sell", command=manage_orders_sell, width=11)
    sell_button.pack(padx=10, pady=20)

    # Current orders
    current_orders_button = ttk.Button(new_window, text="Current orders", command=current_orders_window, width=11)
    current_orders_button.pack(padx=10, pady=20)

    # Button to close the window
    close_button = ttk.Button(new_window, text="Close", command=new_window.destroy, width=11)
    close_button.pack(padx=10, pady=20)

# Function to open balance window
def balance_window():
    
    # Create the new window
    new_window = tk.Toplevel()
    new_window.title("Balance")
    new_window.geometry('400x400')
    sv_ttk.set_theme("light")  # Set theme 
    
    # Display the current balance
    label_balance = tk.Label(new_window, text=f"£ {customer_balance}")
    label_balance.pack(pady=10)

    # Button to top up balance
    buy_button = ttk.Button(new_window, text="Add money", width=10)
    buy_button.pack(padx=10, pady=20)

    # Button to withdraw balance
    withdraw_button = ttk.Button(new_window, text="Withdraw money", width=10)
    withdraw_button.pack(padx=10, pady=20)

# Function to view ongoing orders
def current_orders_window():
    # Create the new window for order confirmation
    new_window = tk.Toplevel()
    new_window.title("Current Orders")
    new_window.geometry('870x440')
    sv_ttk.set_theme("light")  # Set theme

    # Create Treeview
    tree = ttk.Treeview(new_window, columns=("Order ID", "Customer ID", "Currency Pair",
                                            "Order Type", "Amount", "Price", "Order Time"),
                        show="headings")

    # Define column headings
    tree.heading("Order ID", text="Order ID")
    tree.heading("Customer ID", text="Customer ID")
    tree.heading("Currency Pair", text="Currency Pair")
    tree.heading("Order Type", text="Order Type")
    tree.heading("Amount", text="Amount")
    tree.heading("Price", text="Price")
    tree.heading("Order Time", text="Order Time")

    # Define column widths
    tree.column("Order ID", width=100, anchor=tk.CENTER)
    tree.column("Customer ID", width=100, anchor=tk.CENTER)
    tree.column("Currency Pair", width=150, anchor=tk.W)
    tree.column("Order Type", width=100, anchor=tk.CENTER)
    tree.column("Amount", width=100, anchor=tk.CENTER)
    tree.column("Price", width=100, anchor=tk.CENTER)
    tree.column("Order Time", width=200, anchor=tk.W)

    # Fetch orders from your database or data source
    orders = fetch_orders()  # Assuming you have a function to fetch orders

    # Add data to the Treeview
    for order in orders:
        tree.insert("", tk.END, values=order)

    # Pack Treeview into the window
    tree.pack(fill=tk.BOTH, expand=True)

    # Button to modify trades
    modify_button = ttk.Button(new_window, text="Modify trades",command=modify_orders_window, width=10)
    modify_button.pack(padx=10, pady=20)

    # Button to close the window
    close_button = ttk.Button(new_window, text="Back", command=new_window.destroy, width=10)
    close_button.pack(padx=10)

    # Run the Tkinter main loop for the new window
    new_window.mainloop()

# Function to manage onging orders, Close order etc
def modify_orders_window():
    # Create the new window for order modification
    new_window = tk.Toplevel()
    new_window.title("Modify Order")
    new_window.geometry('870x400')
    sv_ttk.set_theme("light")  # Set theme

    # Fetch current orders
    try:
        orders = fetch_orders()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch orders: {e}")
        return

    if not orders:
        messagebox.showinfo("No Orders", "No current orders available.")
        return

    # Dropdown label
    tk.Label(new_window, text="Select an Order to Modify:").pack(pady=10)

    # Create a dictionary for dropdown mapping
    orders_dict = {
        f"Order ID {order[0]}: {order[2]} {order[3]} {order[4]} units @ {order[5]}": order[0]
        for order in orders
    }

    # Dropdown menu
    selected_order = tk.StringVar(new_window)
    order_dropdown = ttk.Combobox(new_window, textvariable=selected_order, state="readonly")
    order_dropdown['values'] = list(orders_dict.keys())
    order_dropdown.pack(pady=10)

    # Function to work alongside close_trade() in data_access.py to help close tardes and store data in database
    def close_trade_handler():

        global order_id
        
        order_desc = selected_order.get()
        order_id = orders_dict[order_desc]

        # Fetch major from db
        major = get_currency_pair(order_id)

        # convert to ticker value for yfinance
        major_ticker = currency_pairs[major]

        # download from yfinance
        forex_data_minute = yf.download(major_ticker, period='1d', interval='1m')
        close_price = forex_data_minute['Open'].iloc[-1]

        # validate an order has been selected
        if not order_desc:
            messagebox.showwarning("Warning", "Please select an order to close.")
            return

        try:
            # Close the trade using the db function
            close_trade(order_id, close_price)
            messagebox.showinfo("Success", "Trade closed successfully.")

            # Refresh the dropdown by removing the closed trade
            del orders_dict[order_desc]
            order_dropdown['values'] = list(orders_dict.keys())
            selected_order.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to close trade: {e}")

    # Close Trade Button
    ttk.Button(new_window, text="Close Trade", command=close_trade_handler).pack(pady=10)
    
    # Button to close the window
    close_button = ttk.Button(new_window, text="Back", command=new_window.destroy, width=10)
    close_button.pack()

# Function to open history window
def history_window():
    # Create the new window for order history
    new_window = tk.Toplevel()
    new_window.title("Trade History")
    new_window.geometry('870x400')
    sv_ttk.set_theme("light")  # Set theme

    # Create Treeview widget
    tree = ttk.Treeview(new_window, columns=("History ID", "Order ID", "Currency Pair", "Order Type", "Amount", 
                                              "Price", "Order Time Close", "Pip Difference", "Profit/Loss"),
                        show="headings")

    # Define column headings
    tree.heading("History ID", text="History ID")
    tree.heading("Order ID", text="Order ID")
    tree.heading("Currency Pair", text="Currency Pair")
    tree.heading("Order Type", text="Order Type")
    tree.heading("Amount", text="Amount")
    tree.heading("Price", text="Price")
    tree.heading("Order Time Close", text="Order Time Close")
    tree.heading("Pip Difference", text="Pip Difference")
    tree.heading("Profit/Loss", text="Profit/Loss")

    # Define column widths
    tree.column("History ID", width=100, anchor=tk.CENTER)
    tree.column("Order ID", width=100, anchor=tk.CENTER)
    tree.column("Currency Pair", width=150, anchor=tk.W)
    tree.column("Order Type", width=100, anchor=tk.CENTER)
    tree.column("Amount", width=100, anchor=tk.CENTER)
    tree.column("Price", width=100, anchor=tk.CENTER)
    tree.column("Order Time Close", width=200, anchor=tk.W)
    tree.column("Pip Difference", width=120, anchor=tk.CENTER)
    tree.column("Profit/Loss", width=120, anchor=tk.CENTER)

    # Fetch history records from the database
    try:
        conn = sqlite3.connect("main.db")  # Update with your database file path if needed
        cursor = conn.cursor()
        
        # Select relevant columns from history table
        cursor.execute("SELECT history_id, order_id, currency_pair, order_type, amount, price, order_time_close, pip_difference, profit_loss FROM history")
        history_records = cursor.fetchall()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch history records: {e}")
        return
    finally:
        conn.close()

    # Add data to the Treeview
    for record in history_records:
        tree.insert("", tk.END, values=record)

    # Pack Treeview into the window
    tree.pack(fill=tk.BOTH, expand=True)

    # Button to close the window
    close_button = ttk.Button(new_window, text="Close", command=new_window.destroy, width=10)
    close_button.pack(pady=10)

    # Run the Tkinter main loop for the new window
    new_window.mainloop()

# Create the main window
root = tk.Tk()
root.title("Investor Centre LTD")
root.geometry("600x400")
sv_ttk.set_theme("light")

# Define a custom font
custom_font = font.Font(family="Helvetica", size=28, weight="bold")

# Configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)

# Title page
title_label = tk.Label(root, text='Investor Centre LTD', font=custom_font, padx=20, pady=20)
title_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

# Username label and entry
label_username = tk.Label(root, text="Username")
label_username.grid(row=1, column=0, sticky="e", pady=10, padx=5)

entry_username = tk.Entry(root)
entry_username.grid(row=1, column=1, sticky="w", pady=10, padx=5)

# Password label and entry
label_password = tk.Label(root, text="Password")
label_password.grid(row=2, column=0, sticky="e", pady=10, padx=5)

entry_password = tk.Entry(root, show="*")
entry_password.grid(row=2, column=1, sticky="w", pady=10, padx=5)

# Login button
login_button = ttk.Button(root, text="Login", command=login)
login_button.grid(row=3, column=2, pady=20, padx=5, sticky="w")

# Create account button
create_button = ttk.Button(root, text="Create account", command=create_account_window)
create_button.grid(row=3, column=0, pady=20, padx=5, sticky="e")

# Make sure the main window is centered on the screen
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Run the application
root.mainloop()



