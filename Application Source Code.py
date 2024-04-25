import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2
import tkinter.simpledialog as simpledialog

class OnlineShoppingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Online Shopping Application")
        self.geometry("1000x800")
        self.configure(background="#f0f0f0")  # Soft gray background

        # Create a database connection
        self.conn = psycopg2.connect(
            dbname="DDD Project",
            user="postgres",
            password="12345",
            host="localhost"
        )
        self.cursor = self.conn.cursor()

        # Set the theme for better styling
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure the style for different widgets
        self.style.configure("TButton", font=("Helvetica", 14), background="#333333", foreground="#ffffff")
        self.style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0")
        self.style.configure("TEntry", font=("Helvetica", 12), background="#ffffff")

        # Create the main menu screen
        self.main_menu_screen = MainMenuScreen(self)
        self.main_menu_screen.pack(fill=tk.BOTH, expand=True)

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def switch_to_customer_screen(self, user_id):
        self.main_menu_screen.pack_forget()
        self.customer_screen = CustomerScreen(self, user_id)
        self.customer_screen.pack(fill=tk.BOTH, expand=True)

    def switch_to_staff_screen(self, staff_id):
        self.main_menu_screen.pack_forget()
        self.staff_screen = StaffScreen(self, staff_id)
        self.staff_screen.pack(fill=tk.BOTH, expand=True)

    def __del__(self):
        # Close database connection when the application exits
        self.cursor.close()
        self.conn.close()

class MainMenuScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background="#f0f0f0")
        self.configure(background="#f0f0f0")  # Consistent background with the main app

        # Stylish buttons for the main menu
        self.customer_button = ttk.Button(self, text="Customer", command=self.customer_options)
        self.staff_button = ttk.Button(self, text="Staff", command=self.staff_options)
        self.exit_button = ttk.Button(self, text="Exit", command=self.master.quit)

        # Pack buttons with some visual enhancements
        self.customer_button.pack(pady=20, padx=20, fill='x')
        self.staff_button.pack(pady=20, padx=20, fill='x')
        self.exit_button.pack(pady=20, padx=20, fill='x')

    def customer_options(self):
        # Open a new window for customer options
        customer_options_window = tk.Toplevel(self.master)
        customer_options_window.title("Customer Options")
        customer_options_window.configure(background="#87CEEB")  # Set background color

        # Create style for buttons in the customer options window
        customer_button_style = ttk.Style()
        customer_button_style.configure("CustomerOptions.TButton", font=("Helvetica", 12), background="#2196F3", foreground="black")

        # Create buttons for customer login and sign up
        login_button = ttk.Button(customer_options_window, text="Login", style="CustomerOptions.TButton", command=self.customer_login)
        signup_button = ttk.Button(customer_options_window, text="Sign Up", style="CustomerOptions.TButton", command=self.customer_signup)

        # Pack buttons
        login_button.pack(pady=10)
        signup_button.pack(pady=10)

    def customer_login(self):
        # Window setup
        login_window = tk.Toplevel(self.master)
        login_window.title("Customer Login")
        login_window.configure(background="#87CEEB")

        # Username
        username_label = ttk.Label(login_window, text="Username:", background="#87CEEB")
        username_entry = ttk.Entry(login_window)
        username_label.pack(pady=5)
        username_entry.pack(pady=5)

        # Password
        password_label = ttk.Label(login_window, text="Password:", background="#87CEEB")
        password_entry = ttk.Entry(login_window, show="*")
        password_label.pack(pady=5)
        password_entry.pack(pady=5)

        # Login Button
        login_button = ttk.Button(login_window, text="Login", command=lambda: self.verify_login(
            username_entry.get(), password_entry.get()
        ))
        login_button.pack(pady=10)

    def verify_login(self, username, password):
        query = "SELECT customer_id, name FROM public.customer WHERE username = %s AND password = %s"
        params = (username, password)
        try:
            self.master.execute_query(query, params)
            result = self.master.cursor.fetchone()
            if result:
                self.master.switch_to_customer_screen(result[0])
                messagebox.showinfo("Login Success", f"Welcome, {result[1]}")
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error: {e.pgerror}")

    def customer_signup(self):
        # Open a new window for customer sign up
        signup_window = tk.Toplevel(self.master)
        signup_window.title("Customer Sign Up")
        signup_window.configure(background="#87CEEB")

        # Create entry fields and labels
        label_style = ttk.Style()
        label_style.configure("SignupLabel.TLabel", font=("Helvetica", 12), background="#87CEEB")
        entry_style = ttk.Style()
        entry_style.configure("SignupEntry.TEntry", font=("Helvetica", 12))

        # Name
        name_label = ttk.Label(signup_window, text="Name:", style="SignupLabel.TLabel")
        name_entry = ttk.Entry(signup_window, style="SignupEntry.TEntry")
        name_label.pack(pady=5)
        name_entry.pack(pady=5)

        # Username
        username_label = ttk.Label(signup_window, text="Username:", style="SignupLabel.TLabel")
        username_entry = ttk.Entry(signup_window, style="SignupEntry.TEntry")
        username_label.pack(pady=5)
        username_entry.pack(pady=5)

        # Password
        password_label = ttk.Label(signup_window, text="Password:", style="SignupLabel.TLabel")
        password_entry = ttk.Entry(signup_window, style="SignupEntry.TEntry", show="*")
        password_label.pack(pady=5)
        password_entry.pack(pady=5)

        # Signup Button
        signup_button = ttk.Button(signup_window, text="Sign Up", style="SignupButton.TButton", command=lambda: self.submit_signup_details(
            name_entry.get(), username_entry.get(), password_entry.get()
        ))
        signup_button.pack(pady=5)

        # Create a button to submit the sign up details
        signup_button = ttk.Button(signup_window, text="Sign Up", style="SignupButton.TButton", command=lambda: self.submit_signup_details(
        name_entry.get(), username_entry.get(), password_entry.get()
        ))
        signup_button.pack(pady=5)


    def submit_signup_details(self, name, username, password):
        if name and username and password:
            # Insert the new customer into the database
            query = "INSERT INTO public.customer (name, username, password) VALUES (%s, %s, %s)"
            params = (name, username, password)
            try:
                self.master.execute_query(query, params)
                messagebox.showinfo("Success", "Signup successful! Please login.")
            except psycopg2.Error as e:
                messagebox.showerror("Error", f"Database error: {e.pgerror}")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def staff_options(self):
        # Open a new window for staff options
        staff_options_window = tk.Toplevel(self.master)
        staff_options_window.title("Staff Options")
        staff_options_window.configure(background="#87CEEB")  # Set background color

        # Create style for buttons in the staff options window
        staff_button_style = ttk.Style()
        staff_button_style.configure("StaffOptions.TButton", font=("Helvetica", 12), background="#2196F3", foreground="black")

        # Create button for staff login
        login_button = ttk.Button(staff_options_window, text="Login", style="StaffOptions.TButton", command=self.staff_login)

        # Pack button
        login_button.pack(pady=10)

    def staff_login(self):
        # Open a new window for staff login
        staff_login_window = tk.Toplevel(self.master)
        staff_login_window.title("Staff Login")
        staff_login_window.configure(background="#87CEEB")

        # Create style for labels and buttons
        label_style = ttk.Style()
        label_style.configure("StaffLabel.TLabel", font=("Helvetica", 12), background="#87CEEB")
        button_style = ttk.Style()
        button_style.configure("Login.TButton", font=("Helvetica", 12), background="#4CAF50", foreground="black")

        # Create entry field for staff ID
        staff_id_label = ttk.Label(staff_login_window, text="Staff ID:", style="StaffLabel.TLabel")
        staff_id_entry = ttk.Entry(staff_login_window)
        staff_id_label.pack(pady=5)
        staff_id_entry.pack(pady=5)

        # Password entry
        password_label = ttk.Label(staff_login_window, text="Password:", style="StaffLabel.TLabel")
        password_entry = ttk.Entry(staff_login_window, show="*")
        password_label.pack(pady=5)
        password_entry.pack(pady=5)

        # Create a button to login as staff
        login_button = ttk.Button(
            staff_login_window, 
            text="Login", 
            style="Login.TButton", 
            command=lambda: self.verify_staff_login(
                staff_id_entry.get(), 
                password_entry.get()
            )
        )
        login_button.pack(pady=5)

    def verify_staff_login(self, staff_id, password):

        query = "SELECT staff_id, name FROM public.staffmembers WHERE staff_id = %s AND password = %s"
        params = (staff_id, password)  # Assume the password is stored in plain text for demonstration

        try:
            self.master.execute_query(query, params)
            result = self.master.cursor.fetchone()
            if result:
                self.master.switch_to_staff_screen(result[0])
                messagebox.showinfo("Login Success", f"Welcome, {result[1]}")
            else:
                messagebox.showerror("Login Failed", "Invalid staff ID or password")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error: {e.pgerror}")

    def staff_signup(self):
        # Open a new window for staff sign up
        signup_window = tk.Toplevel(self.master)
        signup_window.title("Staff Sign Up")
        signup_window.configure(background="#87CEEB")  # Set background color

        # Create style for labels, entry fields, and buttons
        label_style = ttk.Style()
        label_style.configure("StaffSignupLabel.TLabel", font=("Helvetica", 12), background="#87CEEB")
        entry_style = ttk.Style()
        entry_style.configure("StaffSignupEntry.TEntry", font=("Helvetica", 12))
        button_style = ttk.Style()
        button_style.configure("SignupButton.TButton", font=("Helvetica", 12), background="#4CAF50", foreground="black")

        # Create entry fields for staff sign up details
        name_label = ttk.Label(signup_window, text="Name:", style="StaffSignupLabel.TLabel")
        name_entry = ttk.Entry(signup_window, style="StaffSignupEntry.TEntry")
        name_label.pack(pady=5)
        name_entry.pack(pady=5)

        # Create a button to submit the sign up details
        signup_button = ttk.Button(signup_window, text="Sign Up", style="SignupButton.TButton", command=lambda: self.submit_signup_details(
            name_entry.get()
            # Add more parameters for other sign up details
        ))
        signup_button.pack(pady=5)

    def submit_signup_details(self, name):
        # Placeholder for submitting staff sign up details to the database
        pass

class CustomerScreen(tk.Frame):
    def __init__(self, master, user_id):
        super().__init__(master)
        self.master = master
        self.user_id = user_id
        self.cart = []
        self.configure(background="#87CEEB")  # Set background color

        # Create widgets for customer screen
        self.back_button = ttk.Button(self, text="Back", style="MainMenu.TButton", command=self.go_to_main_menu)
        self.label = ttk.Label(self, text=f"Welcome, Customer {self.user_id}", font=("Helvetica", 16), background="#87CEEB")
        self.search_label = ttk.Label(self, text="Search:", background="#87CEEB")
        self.search_entry = ttk.Entry(self)
        self.search_button = ttk.Button(self, text="Search", style="MainMenu.TButton", command=self.search_products)
        self.products_listbox = tk.Listbox(self, width=50, height=10)
        self.view_details_button = ttk.Button(self, text="View Details", style="MainMenu.TButton", command=self.view_product_details)
        self.add_to_cart_button = ttk.Button(self, text="Add to Cart", style="MainMenu.TButton", command=self.add_to_cart)
        self.remove_from_cart_button = ttk.Button(self, text="Remove from Cart", style="MainMenu.TButton", command=self.remove_from_cart)
        self.cart_label = ttk.Label(self, text="Cart:", background="#87CEEB")
        self.cart_listbox = tk.Listbox(self, width=50, height=5)
        self.checkout_button = ttk.Button(self, text="Checkout", style="MainMenu.TButton", command=self.initiate_checkout)

        # Pack widgets
        self.back_button.pack(pady=10)
        self.label.pack(pady=10)
        self.search_label.pack(pady=5)
        self.search_entry.pack(pady=5)
        self.search_button.pack(pady=5)
        self.products_listbox.pack()
        self.view_details_button.pack(pady=5)
        self.add_to_cart_button.pack(pady=5)
        self.remove_from_cart_button.pack(pady=5)
        self.cart_label.pack(pady=5)
        self.cart_listbox.pack()
        self.checkout_button.pack(pady=10)

        # Add a label to display the total bill
        self.total_bill_label = ttk.Label(self, text="Total Bill: $0.00", background="#87CEEB", font=("Helvetica", 12))
        self.total_bill_label.pack(pady=5)

        # Update the label text whenever the cart is updated
        self.update_total_bill_label()

    def go_to_main_menu(self):
        self.master.customer_screen.pack_forget()
        self.master.main_menu_screen.pack(fill=tk.BOTH, expand=True)

    def search_products(self):
        # Clear the products listbox before displaying new results
        self.products_listbox.delete(0, tk.END)

        # Get the search query entered by the user
        search_query = self.search_entry.get()

        # Construct the SQL query to search for products
        query = "SELECT * FROM Product WHERE name ILIKE %s OR category ILIKE %s"
        params = (f"%{search_query}%", f"%{search_query}%")

        try:
            # Execute the SQL query
            self.master.execute_query(query, params)
            
            # Fetch all rows returned by the query
            rows = self.master.cursor.fetchall()

            # Display the products in the listbox
            for row in rows:
                self.products_listbox.insert(tk.END, (row[0], f"{row[1]} - {row[2]} - {row[3]}"))
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def view_product_details(self):
        # Get the selected product from the listbox
        selected_product_index = self.products_listbox.curselection()
        if not selected_product_index:
            messagebox.showwarning("Warning", "Please select a product to view details.")
            return
        selected_product_id, _ = self.products_listbox.get(selected_product_index)

        # Fetch product details from the database
        query = "SELECT * FROM Product WHERE product_id = %s"
        try:
            self.master.execute_query(query, (selected_product_id,))
            product_details = self.master.cursor.fetchone()
            if product_details:
                # Display product details in a new window
                self.show_product_details_window(product_details)
            else:
                messagebox.showerror("Error", "Product details not found.")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def show_product_details_window(self, product_details):
        details_window = tk.Toplevel(self.master)
        details_window.title("Product Details")
        details_window.configure(background="#87CEEB")  # Set background color

        # Display product details in the window
        product_id_label = ttk.Label(details_window, text="Product ID:", style="StaffLabel.TLabel")
        product_id_label.grid(row=0, column=0, sticky="e")
        ttk.Label(details_window, text=product_details[0], background="#87CEEB").grid(row=0, column=1)

        name_label = ttk.Label(details_window, text="Name:", style="StaffLabel.TLabel")
        name_label.grid(row=1, column=0, sticky="e")
        ttk.Label(details_window, text=product_details[1], background="#87CEEB").grid(row=1, column=1)

        category_label = ttk.Label(details_window, text="Category:", style="StaffLabel.TLabel")
        category_label.grid(row=2, column=0, sticky="e")
        ttk.Label(details_window, text=product_details[2], background="#87CEEB").grid(row=2, column=1)

        type_label = ttk.Label(details_window, text="Type:", style="StaffLabel.TLabel")
        type_label.grid(row=3, column=0, sticky="e")
        ttk.Label(details_window, text=product_details[3], background="#87CEEB").grid(row=3, column=1)

        brand_label = ttk.Label(details_window, text="Brand:", style="StaffLabel.TLabel")
        brand_label.grid(row=4, column=0, sticky="e")
        ttk.Label(details_window, text=product_details[4], background="#87CEEB").grid(row=4, column=1)

        size_label = ttk.Label(details_window, text="Size:", style="StaffLabel.TLabel")
        size_label.grid(row=5, column=0, sticky="e")
        ttk.Label(details_window, text=product_details[5], background="#87CEEB").grid(row=5, column=1)

        description_label = ttk.Label(details_window, text="Description:", style="StaffLabel.TLabel")
        description_label.grid(row=6, column=0, sticky="e")
        ttk.Label(details_window, text=product_details[6], background="#87CEEB").grid(row=6, column=1)

        price_label = ttk.Label(details_window, text="Price:", style="StaffLabel.TLabel")
        price_label.grid(row=7, column=0, sticky="e")
        ttk.Label(details_window, text=product_details[7], background="#87CEEB").grid(row=7, column=1)

    def add_to_cart(self):
        # Get the selected product from the listbox
        selected_product_index = self.products_listbox.curselection()
        if not selected_product_index:
            messagebox.showwarning("Warning", "Please select a product to add to the cart.")
            return
        selected_product_id, selected_product_details = self.products_listbox.get(selected_product_index)

        # Fetch the price of the selected product from the database
        query = "SELECT price FROM Product WHERE product_id = %s"
        try:
            self.master.execute_query(query, (selected_product_id,))
            product_price = self.master.cursor.fetchone()[0]

            # Add the selected product and its price to the cart
            self.cart.append((selected_product_id, selected_product_details, product_price))
            self.update_cart_listbox()

            # Update the total bill label
            self.update_total_bill_label()
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def calculate_total_bill(self):
        total_bill = sum(item[2] for item in self.cart)  # Sum of prices of all items in the cart
        return total_bill
    
    def update_total_bill_label(self):
        total_bill = self.calculate_total_bill()
        self.total_bill_label.config(text=f"Total Bill: ${total_bill:.2f}")

    def remove_from_cart(self):
        # Get the selected product from the cart listbox
        selected_cart_item_index = self.cart_listbox.curselection()
        if not selected_cart_item_index:
            messagebox.showwarning("Warning", "Please select a product from the cart to remove.")
            return
        del self.cart[selected_cart_item_index[0]]
        self.update_cart_listbox()

        # Update the total bill label
        self.update_total_bill_label()

    def update_cart_listbox(self):
        # Clear the cart listbox before updating
        self.cart_listbox.delete(0, tk.END)

        # Update the cart listbox with current cart items
        for item in self.cart:
            self.cart_listbox.insert(tk.END, item[1])

    def initiate_checkout(self):
        # Ask for payment method
        payment_method = simpledialog.askstring("Payment Method", "Enter your payment method (e.g., Credit Card, PayPal):")
        if payment_method:
            if payment_method.lower() == "credit card":
                self.ask_credit_card_details()
            else:
                self.checkout(payment_method)

    def ask_credit_card_details(self):
        cc_window = tk.Toplevel(self.master)
        cc_window.title("Credit Card Details")
        cc_window.configure(background="#87CEEB")

        # Entry for Card Holder Name
        cc_name_label = ttk.Label(cc_window, text="Card Holder Name:", background="#87CEEB")
        cc_name_entry = ttk.Entry(cc_window)
        cc_name_label.pack(pady=5)
        cc_name_entry.pack(pady=5)

        # Entry for Credit Card Number
        cc_number_label = ttk.Label(cc_window, text="Credit Card Number:", background="#87CEEB")
        cc_number_entry = ttk.Entry(cc_window)
        cc_number_label.pack(pady=5)
        cc_number_entry.pack(pady=5)

        # Entry for Expiry Date
        cc_expiry_label = ttk.Label(cc_window, text="Expiry Date (MM/YYYY):", background="#87CEEB")
        cc_expiry_entry = ttk.Entry(cc_window)
        cc_expiry_label.pack(pady=5)
        cc_expiry_entry.pack(pady=5)

        # Submit button for credit card details
        submit_button = ttk.Button(cc_window, text="Save Card", command=lambda: self.save_credit_card_details(
            self.user_id, cc_number_entry.get(), cc_name_entry.get(), cc_expiry_entry.get()
        ))
        submit_button.pack(pady=10)

    def save_credit_card_details(self, customer_id, cc_number, cc_name, cc_expiry):
        # Insert card details into the creditcards table
        query = """
            INSERT INTO public.creditcards (customer_id, credit_card_number, card_holder_name, expiry_date)
            VALUES (%s, %s, %s, TO_DATE(%s, 'MM/YYYY'))
        """
        params = (customer_id, cc_number, cc_name, cc_expiry)
        try:
            self.master.execute_query(query, params)
            messagebox.showinfo("Success", "Credit card details saved successfully.")
            # Call checkout method here to show receipt
            self.checkout('Credit Card', cc_number=cc_number, cc_cvv=None, cc_expiry=cc_expiry, cc_address=None)
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error: {e.pgerror}")

    def choose_payment_method(self):
        choose_method_window = tk.Toplevel(self.master)
        choose_method_window.title("Choose Payment Method")
        choose_method_window.configure(background="#87CEEB")

        query = "SELECT credit_card_id, credit_card_number FROM public.creditcards WHERE customer_id = %s"
        self.master.execute_query(query, (self.user_id,))
        cards = self.master.cursor.fetchall()

        label = ttk.Label(choose_method_window, text="Select a card to use for payment:", background="#87CEEB")
        label.pack(pady=5)

        for card in cards:
            card_num_display = f"**** **** **** {card[1][-4:]}"
            card_button = ttk.Button(choose_method_window, text=card_num_display, command=lambda c=card[0]: self.use_credit_card(c))
            card_button.pack(pady=2)

        new_card_button = ttk.Button(choose_method_window, text="Use a new card", command=self.ask_credit_card_details)
        new_card_button.pack(pady=10)

    def checkout(self, payment_method, cc_number=None, cc_cvv=None, cc_expiry=None, cc_address=None):
        # Placeholder for receipt generation
        receipt = f"Receipt\n\nPayment Method: {payment_method}\n"

        if payment_method == "Credit Card":
            receipt += f"Credit Card Number: {cc_number[-4:]}\n"  # Display only last 4 digits for security
            receipt += f"Billing Address: {cc_address}\n"

        # Add each item in the cart to the receipt
        for item in self.cart:
            receipt += f"{item[1]} - ${item[2]:.2f}\n"

        # Calculate and display the total bill
        total_bill = self.calculate_total_bill()
        receipt += f"\nTotal Bill: ${total_bill:.2f}"

        # Clear the cart and update the cart listbox
        self.cart.clear()
        self.update_cart_listbox()

        # Display the receipt in a messagebox
        messagebox.showinfo("Receipt", receipt)

    def place_order(self):
        # Placeholder for placing an order
        messagebox.showinfo("Success", "Order placed successfully.")

class StaffScreen(tk.Frame):
    def __init__(self, master, staff_id):
        super().__init__(master)
        self.master = master
        self.staff_id = staff_id
        self.configure(background="#87CEEB")  # Set background color

        # Create widgets for staff screen
        self.back_button = tk.Button(self, text="Back", command=self.go_to_main_menu)
        self.label = tk.Label(self, text=f"Welcome, Staff {self.staff_id}")
        self.add_product_button = tk.Button(self, text="Add Product", command=self.add_product)
        self.delete_product_button = tk.Button(self, text="Delete Product", command=self.delete_product)
        self.modify_product_button = tk.Button(self, text="Modify Product", command=self.modify_product)
        self.add_stock_button = tk.Button(self, text="Add Stock", command=self.add_stock)
        self.back_button = ttk.Button(self, text="Back", style="MainMenu.TButton", command=self.go_to_main_menu)
        self.label = ttk.Label(self, text=f"Welcome, Staff {self.staff_id}", font=("Helvetica", 16), background="#87CEEB")
        self.manage_stock_button = ttk.Button(self, text="Manage Stock", style="MainMenu.TButton", command=self.manage_stock)


        # Pack widgets
        self.back_button.pack()
        self.label.pack()
        self.add_product_button.pack()
        self.delete_product_button.pack()
        self.modify_product_button.pack()
        self.add_stock_button.pack()
        self.back_button.pack(pady=10)
        self.label.pack(pady=10)
        self.manage_stock_button.pack(pady=10)

    def go_to_main_menu(self):
        self.master.staff_screen.pack_forget()
        self.master.main_menu_screen.pack(fill=tk.BOTH, expand=True)

    def add_product(self):
        # Open a new window to input product details
        add_product_window = tk.Toplevel(self.master)
        add_product_window.title("Add Product")

        # Create entry fields for product details
        product_name_label = tk.Label(add_product_window, text="Name:")
        product_name_entry = tk.Entry(add_product_window)
        product_name_label.grid(row=0, column=0, sticky="e")
        product_name_entry.grid(row=0, column=1)

        product_category_label = tk.Label(add_product_window, text="Category:")
        product_category_entry = tk.Entry(add_product_window)
        product_category_label.grid(row=1, column=0, sticky="e")
        product_category_entry.grid(row=1, column=1)

        product_type_label = tk.Label(add_product_window, text="Type:")
        product_type_entry = tk.Entry(add_product_window)
        product_type_label.grid(row=2, column=0, sticky="e")
        product_type_entry.grid(row=2, column=1)

        product_brand_label = tk.Label(add_product_window, text="Brand:")
        product_brand_entry = tk.Entry(add_product_window)
        product_brand_label.grid(row=3, column=0, sticky="e")
        product_brand_entry.grid(row=3, column=1)

        product_size_label = tk.Label(add_product_window, text="Size:")
        product_size_entry = tk.Entry(add_product_window)
        product_size_label.grid(row=4, column=0, sticky="e")
        product_size_entry.grid(row=4, column=1)

        product_description_label = tk.Label(add_product_window, text="Description:")
        product_description_entry = tk.Entry(add_product_window)
        product_description_label.grid(row=5, column=0, sticky="e")
        product_description_entry.grid(row=5, column=1)

        product_price_label = tk.Label(add_product_window, text="Price:")
        product_price_entry = tk.Entry(add_product_window)
        product_price_label.grid(row=6, column=0, sticky="e")
        product_price_entry.grid(row=6, column=1)

        # Create a button to add the product to the database
        add_button = tk.Button(add_product_window, text="Add", command=lambda: self.add_product_to_db(
            product_name_entry.get(),
            product_category_entry.get(),
            product_type_entry.get(),
            product_brand_entry.get(),
            product_size_entry.get(),
            product_description_entry.get(),
            product_price_entry.get()
        ))
        add_button.grid(row=7, columnspan=2)

    def add_product_to_db(self, name, category, type, brand, size, description, price):
        query = "INSERT INTO Product (name, category, type, brand, size, description, price) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        params = (name, category, type, brand, size, description, price)
        try:
            self.master.execute_query(query, params)
            messagebox.showinfo("Success", "Product added successfully.")
        except psycopg2.Error as e:
            messagebox.showerror("Error", "Failed to add product to the database. Please try again.")

    def delete_product(self):
        # Open a new window to select the product to delete
        delete_product_window = tk.Toplevel(self.master)
        delete_product_window.title("Delete Product")

        # Fetch products from the database
        query = "SELECT product_id, name FROM Product"
        try:
            self.master.execute_query(query)
            products = self.master.cursor.fetchall()

            # Create a listbox to display products
            product_listbox = tk.Listbox(delete_product_window)
            product_listbox.pack()

            # Insert products into the listbox
            for product in products:
                product_listbox.insert(tk.END, f"{product[0]}: {product[1]}")

            # Create a button to delete the selected product
            delete_button = tk.Button(delete_product_window, text="Delete", command=lambda: self.delete_selected_product(
                product_listbox.get(tk.ACTIVE).split(":")[0]
            ))
            delete_button.pack()
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def delete_selected_product(self, product_id):
        query = "DELETE FROM Product WHERE product_id = %s"
        try:
            self.master.execute_query(query, (product_id,))
            messagebox.showinfo("Success", "Product deleted successfully.")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def modify_product(self):
        # Open a new window to select the product to modify
        modify_product_window = tk.Toplevel(self.master)
        modify_product_window.title("Modify Product")

        # Fetch products from the database
        query = "SELECT product_id, name FROM Product"
        try:
            self.master.execute_query(query)
            products = self.master.cursor.fetchall()

            # Create a listbox to display products
            product_listbox = tk.Listbox(modify_product_window)
            product_listbox.pack()

            # Insert products into the listbox
            for product in products:
                product_listbox.insert(tk.END, f"{product[0]}: {product[1]}")

            # Create a button to modify the selected product
            modify_button = tk.Button(modify_product_window, text="Modify", command=lambda: self.modify_selected_product(
                product_listbox.get(tk.ACTIVE).split(":")[0]
            ))
            modify_button.pack()
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def modify_selected_product(self, product_id):
        # Placeholder for modifying the selected product
        pass

    def modify_product(self):
        # Open a new window to select the product to modify
        modify_product_window = tk.Toplevel(self.master)
        modify_product_window.title("Modify Product")

        # Fetch products from the database
        query = "SELECT product_id, name FROM Product"
        try:
            self.master.execute_query(query)
            products = self.master.cursor.fetchall()

            # Create a listbox to display products
            product_listbox = tk.Listbox(modify_product_window)
            product_listbox.pack()

            # Insert products into the listbox
            for product in products:
                product_listbox.insert(tk.END, f"{product[0]}: {product[1]}")

            # Create a button to modify the selected product
            modify_button = tk.Button(modify_product_window, text="Modify", command=lambda: self.show_modify_product_window(
                modify_product_window, product_listbox.get(tk.ACTIVE).split(":")[0]
            ))
            modify_button.pack()
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def show_modify_product_window(self, modify_product_window, product_id):
        # Close the product selection window
        modify_product_window.destroy()

        # Open a new window to modify the product
        modify_window = tk.Toplevel(self.master)
        modify_window.title("Modify Product")

        # Fetch product details from the database
        query = "SELECT * FROM Product WHERE product_id = %s"
        try:
            self.master.execute_query(query, (product_id,))
            product_details = self.master.cursor.fetchone()

            # Create entry fields pre-filled with existing product details
            name_label = tk.Label(modify_window, text="Name:")
            name_entry = tk.Entry(modify_window)
            name_entry.insert(tk.END, product_details[1])
            name_label.grid(row=0, column=0, sticky="e")
            name_entry.grid(row=0, column=1)

            category_label = tk.Label(modify_window, text="Category:")
            category_entry = tk.Entry(modify_window)
            category_entry.insert(tk.END, product_details[2])
            category_label.grid(row=1, column=0, sticky="e")
            category_entry.grid(row=1, column=1)

            type_label = tk.Label(modify_window, text="Type:")
            type_entry = tk.Entry(modify_window)
            type_entry.insert(tk.END, product_details[3])
            type_label.grid(row=2, column=0, sticky="e")
            type_entry.grid(row=2, column=1)

            brand_label = tk.Label(modify_window, text="Brand:")
            brand_entry = tk.Entry(modify_window)
            brand_entry.insert(tk.END, product_details[4])
            brand_label.grid(row=3, column=0, sticky="e")
            brand_entry.grid(row=3, column=1)

            size_label = tk.Label(modify_window, text="Size:")
            size_entry = tk.Entry(modify_window)
            size_entry.insert(tk.END, product_details[5])
            size_label.grid(row=4, column=0, sticky="e")
            size_entry.grid(row=4, column=1)

            description_label = tk.Label(modify_window, text="Description:")
            description_entry = tk.Entry(modify_window)
            description_entry.insert(tk.END, product_details[6])
            description_label.grid(row=5, column=0, sticky="e")
            description_entry.grid(row=5, column=1)

            price_label = tk.Label(modify_window, text="Price:")
            price_entry = tk.Entry(modify_window)
            price_entry.insert(tk.END, product_details[7])
            price_label.grid(row=6, column=0, sticky="e")
            price_entry.grid(row=6, column=1)

            # Create a button to apply modifications
            apply_button = tk.Button(modify_window, text="Apply", command=lambda: self.apply_modifications(
                product_id,
                name_entry.get(),
                category_entry.get(),
                type_entry.get(),
                brand_entry.get(),
                size_entry.get(),
                description_entry.get(),
                price_entry.get()
            ))
            apply_button.grid(row=7, columnspan=2)
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def apply_modifications(self, product_id, name, category, type, brand, size, description, price):
        query = "UPDATE Product SET name = %s, category = %s, type = %s, brand = %s, size = %s, description = %s, price = %s WHERE product_id = %s"
        params = (name, category, type, brand, size, description, price, product_id)
        try:
            self.master.execute_query(query, params)
            messagebox.showinfo("Success", "Product modified successfully.")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Failed to modify product: {e}")

    def add_stock(self):
        # Open a new window to select the product and warehouse to add stock
        add_stock_window = tk.Toplevel(self.master)
        add_stock_window.title("Add Stock")

        # Fetch products from the database
        query_products = "SELECT product_id, name FROM Product"
        try:
            self.master.execute_query(query_products)
            products = self.master.cursor.fetchall()

            # Create a listbox to display products
            product_listbox = tk.Listbox(add_stock_window)
            product_listbox.pack()

            # Insert products into the listbox
            for product in products:
                product_listbox.insert(tk.END, f"{product[0]}: {product[1]}")

            # Fetch warehouses from the database
            query_warehouses = "SELECT warehouse_id, address FROM Warehouse"
            self.master.execute_query(query_warehouses)
            warehouses = self.master.cursor.fetchall()

            # Create a listbox to display warehouses
            warehouse_listbox = tk.Listbox(add_stock_window)
            warehouse_listbox.pack()

            # Insert warehouses into the listbox
            for warehouse in warehouses:
                warehouse_listbox.insert(tk.END, f"{warehouse[0]}: {warehouse[1]}")

            # Create entry for quantity
            quantity_label = tk.Label(add_stock_window, text="Quantity:")
            quantity_entry = tk.Entry(add_stock_window)
            quantity_label.pack()
            quantity_entry.pack()

            # Create a button to add stock
            add_button = tk.Button(add_stock_window, text="Add Stock", command=lambda: self.add_stock_to_db(
                product_listbox.get(tk.ACTIVE).split(":")[0],
                warehouse_listbox.get(tk.ACTIVE).split(":")[0],
                quantity_entry.get()
            ))
            add_button.pack()
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def manage_stock(self):
        manage_stock_window = tk.Toplevel(self.master)
        manage_stock_window.title("Manage Stock")
        manage_stock_window.configure(background="#87CEEB")

        self.display_stock(manage_stock_window)

        add_stock_button = ttk.Button(manage_stock_window, text="Add Stock", command=lambda: self.add_stock(manage_stock_window))
        go_back_button = ttk.Button(manage_stock_window, text="Go Back", command=manage_stock_window.destroy)

        add_stock_button.pack(pady=10)
        go_back_button.pack(pady=10)

    def display_stock(self, window):
        # Modified query to sum quantities by warehouse and compare against warehouse capacity
        self.master.execute_query("""
            SELECT w.warehouse_name, SUM(s.quantity) AS total_quantity, w.warehouse_capacity
            FROM public.stock s
            JOIN public.warehouses w ON s.warehouse_id = w.warehouse_id
            GROUP BY w.warehouse_name, w.warehouse_capacity
            ORDER BY w.warehouse_name
        """)
        stock_info = self.master.cursor.fetchall()

        if stock_info:
            for info in stock_info:
                tk.Label(window, text=f"Warehouse: {info[0]}, Stocked: {info[1]}/{info[2]}", background="#87CEEB").pack()
        else:
            tk.Label(window, text="No stock information available.", background="#87CEEB").pack()

    def add_stock(self):
        add_stock_window = tk.Toplevel(self.master)
        add_stock_window.title("Add Stock to Warehouse")
        add_stock_window.configure(background="#87CEEB")

        self.master.execute_query("SELECT product_id, name FROM public.product")
        products = self.master.cursor.fetchall()

        product_label = ttk.Label(add_stock_window, text="Select Product:")
        product_combobox = ttk.Combobox(add_stock_window, values=[f"{prod[0]} - {prod[1]}" for prod in products])
        product_label.pack(pady=5)
        product_combobox.pack(pady=5)

        quantity_label = ttk.Label(add_stock_window, text="Quantity:")
        quantity_entry = ttk.Entry(add_stock_window)
        quantity_label.pack(pady=5)
        quantity_entry.pack(pady=5)

        self.master.execute_query("SELECT warehouse_id, warehouse_name FROM public.warehouses")
        warehouses = self.master.cursor.fetchall()

        warehouse_label = ttk.Label(add_stock_window, text="Select Warehouse:")
        warehouse_combobox = ttk.Combobox(add_stock_window, values=[f"{wh[0]} - {wh[1]}" for wh in warehouses])
        warehouse_label.pack(pady=5)
        warehouse_combobox.pack(pady=5)

        submit_button = ttk.Button(add_stock_window, text="Add Stock", command=lambda: self.submit_stock(
            product_combobox.get().split(" - ")[0],
            quantity_entry.get(),
            warehouse_combobox.get().split(" - ")[0]
        ))
        submit_button.pack(pady=10)

    def submit_stock(self, product_id, quantity, warehouse_id):
        if not quantity.isdigit():
            messagebox.showerror("Error", "Please enter a valid quantity.")
            return

        query = "INSERT INTO public.stock (product_id, warehouse_id, quantity) VALUES (%s, %s, %s)"
        params = (product_id, warehouse_id, quantity)
        try:
            self.master.execute_query(query, params)
            messagebox.showinfo("Success", "Items added successfully to the warehouse.")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error: {e.pgerror}")



    def add_stock_to_db(self, product_id, warehouse_id, quantity):
        # Placeholder for adding stock to the database
        pass

if __name__ == "__main__":
    app = OnlineShoppingApp()
    app.mainloop()
