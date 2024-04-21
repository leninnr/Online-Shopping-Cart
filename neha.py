import tkinter as tk
from tkinter import messagebox
import psycopg2
import tkinter.simpledialog as simpledialog

class OnlineShoppingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Online Shopping Application")
        self.geometry("800x600")

        # Create a database connection
        self.conn = psycopg2.connect(
            dbname="DDD Project",
            user="postgres",
            password="12345",
            host="localhost"
        )
        self.cursor = self.conn.cursor()

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
        super().__init__(master)
        self.master = master

        # Create buttons for customer and staff login
        self.customer_button = tk.Button(self, text="Customer Login", command=self.customer_login)
        self.staff_button = tk.Button(self, text="Staff Login", command=self.staff_login)

        # Pack buttons
        self.customer_button.pack()
        self.staff_button.pack()

    def customer_login(self):
        # Open a new window for customer registration/login
        customer_login_window = tk.Toplevel(self.master)
        customer_login_window.title("Customer Login")

        # Create entry field for customer ID
        customer_id_label = tk.Label(customer_login_window, text="Customer ID:")
        customer_id_entry = tk.Entry(customer_login_window)
        customer_id_label.pack()
        customer_id_entry.pack()

        # Create a button to login/register as customer
        login_button = tk.Button(customer_login_window, text="Login/Register", command=lambda: self.master.switch_to_customer_screen(customer_id_entry.get()))
        login_button.pack()

    def staff_login(self):
        # Open a new window for staff login
        staff_login_window = tk.Toplevel(self.master)
        staff_login_window.title("Staff Login")

        # Create entry field for staff ID
        staff_id_label = tk.Label(staff_login_window, text="Staff ID:")
        staff_id_entry = tk.Entry(staff_login_window)
        staff_id_label.pack()
        staff_id_entry.pack()

        # Create a button to login as staff
        login_button = tk.Button(staff_login_window, text="Login", command=lambda: self.master.switch_to_staff_screen(staff_id_entry.get()))
        login_button.pack()

class CustomerScreen(tk.Frame):
    def __init__(self, master, user_id):
        super().__init__(master)
        self.master = master
        self.user_id = user_id
        self.cart = []

        # Create widgets for customer screen
        self.back_button = tk.Button(self, text="Back", command=self.go_to_main_menu)
        self.label = tk.Label(self, text=f"Welcome, Customer {self.user_id}")
        self.search_label = tk.Label(self, text="Search:")
        self.search_entry = tk.Entry(self)
        self.search_button = tk.Button(self, text="Search", command=self.search_products)
        self.products_listbox = tk.Listbox(self, width=50, height=10)
        self.view_details_button = tk.Button(self, text="View Details", command=self.view_product_details)
        self.add_to_cart_button = tk.Button(self, text="Add to Cart", command=self.add_to_cart)
        self.remove_from_cart_button = tk.Button(self, text="Remove from Cart", command=self.remove_from_cart)
        self.cart_label = tk.Label(self, text="Cart:")
        self.cart_listbox = tk.Listbox(self, width=50, height=5)
        self.checkout_button = tk.Button(self, text="Checkout", command=self.initiate_checkout)
        
        # Pack widgets
        self.back_button.pack()
        self.label.pack()
        self.search_label.pack()
        self.search_entry.pack()
        self.search_button.pack()
        self.products_listbox.pack()
        self.view_details_button.pack()
        self.add_to_cart_button.pack()
        self.remove_from_cart_button.pack()
        self.cart_label.pack()
        self.cart_listbox.pack()
        self.checkout_button.pack()

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

        # Display product details in the window
        product_id_label = tk.Label(details_window, text="Product ID:")
        product_id_label.grid(row=0, column=0, sticky="e")
        tk.Label(details_window, text=product_details[0]).grid(row=0, column=1)

        name_label = tk.Label(details_window, text="Name:")
        name_label.grid(row=1, column=0, sticky="e")
        tk.Label(details_window, text=product_details[1]).grid(row=1, column=1)

        category_label = tk.Label(details_window, text="Category:")
        category_label.grid(row=2, column=0, sticky="e")
        tk.Label(details_window, text=product_details[2]).grid(row=2, column=1)

        type_label = tk.Label(details_window, text="Type:")
        type_label.grid(row=3, column=0, sticky="e")
        tk.Label(details_window, text=product_details[3]).grid(row=3, column=1)

        brand_label = tk.Label(details_window, text="Brand:")
        brand_label.grid(row=4, column=0, sticky="e")
        tk.Label(details_window, text=product_details[4]).grid(row=4, column=1)

        size_label = tk.Label(details_window, text="Size:")
        size_label.grid(row=5, column=0, sticky="e")
        tk.Label(details_window, text=product_details[5]).grid(row=5, column=1)

        description_label = tk.Label(details_window, text="Description:")
        description_label.grid(row=6, column=0, sticky="e")
        tk.Label(details_window, text=product_details[6]).grid(row=6, column=1)

        price_label = tk.Label(details_window, text="Price:")
        price_label.grid(row=7, column=0, sticky="e")
        tk.Label(details_window, text=product_details[7]).grid(row=7, column=1)

    def add_to_cart(self):
        # Get the selected product from the listbox
        selected_product_index = self.products_listbox.curselection()
        if not selected_product_index:
            messagebox.showwarning("Warning", "Please select a product to add to the cart.")
            return
        selected_product_id, selected_product_details = self.products_listbox.get(selected_product_index)

        # Add the selected product to the cart
        self.cart.append((selected_product_id, selected_product_details))
        self.update_cart_listbox()

    def remove_from_cart(self):
        # Get the selected product from the cart listbox
        selected_cart_item_index = self.cart_listbox.curselection()
        if not selected_cart_item_index:
            messagebox.showwarning("Warning", "Please select a product from the cart to remove.")
            return
        del self.cart[selected_cart_item_index[0]]
        self.update_cart_listbox()

    def update_cart_listbox(self):
        # Clear the cart listbox before updating
        self.cart_listbox.delete(0, tk.END)

        # Update the cart listbox with current cart items
        for item in self.cart:
            self.cart_listbox.insert(tk.END, item)

    def initiate_checkout(self):
        # Ask for payment method
        payment_method = simpledialog.askstring("Payment Method", "Enter your payment method (e.g., Credit Card, PayPal):")
        if payment_method:
            # If payment method is provided, proceed with checkout
            self.checkout(payment_method)

    def checkout(self, payment_method):
        # Placeholder for the checkout process
        # You need to implement the checkout process, including calculating the total order amount, collecting customer information, and updating the database
        # Once the checkout is complete, you can clear the cart and display a success message
        self.cart.clear()
        self.update_cart_listbox()
        messagebox.showinfo("Success", f"Checkout completed successfully. Payment method: {payment_method}")        

    def place_order(self):
        # Placeholder for placing an order
        # You need to implement the order placement process, including collecting customer information, calculating the total order amount, and updating the database
        messagebox.showinfo("Success", "Order placed successfully.")

class StaffScreen(tk.Frame):
    def __init__(self, master, staff_id):
        super().__init__(master)
        self.master = master
        self.staff_id = staff_id

        # Create widgets for staff screen
        self.back_button = tk.Button(self, text="Back", command=self.go_to_main_menu)
        self.label = tk.Label(self, text=f"Welcome, Staff {self.staff_id}")
        self.add_product_button = tk.Button(self, text="Add Product", command=self.add_product)
        self.delete_product_button = tk.Button(self, text="Delete Product", command=self.delete_product)
        self.modify_product_button = tk.Button(self, text="Modify Product", command=self.modify_product)
        self.add_stock_button = tk.Button(self, text="Add Stock", command=self.add_stock)
        
        # Pack widgets
        self.back_button.pack()
        self.label.pack()
        self.add_product_button.pack()
        self.delete_product_button.pack()
        self.modify_product_button.pack()
        self.add_stock_button.pack()

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

    def add_stock_to_db(self, product_id, warehouse_id, quantity):
        # Placeholder for adding stock to the database
        pass

if __name__ == "__main__":
    app = OnlineShoppingApp()
    app.mainloop()
