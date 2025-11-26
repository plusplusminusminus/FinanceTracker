"""Transaction history window for viewing and filtering transactions."""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timezone, timedelta
from .base_window import MainWindow
from ..window_constants import INCOME_CATEGORIES, EXPENSE_CATEGORIES


class TransactionHistoryWindow(MainWindow):
    """Window for viewing transaction history."""
    def __init__(self, app):
        """Initialize the transaction history window."""
        super().__init__(app)
        self.root.title("Transaction History Window")
        self.root.geometry("900x650") # Set the dimensions of the window

        nav_bar = tk.Frame(self.root)
        nav_bar.pack(fill="x", pady=8)
        tk.Button(nav_bar, text="Back to Dashboard", command=self.return_back).pack(side="left", padx=6)

        self.transaction_history_frame = tk.LabelFrame(self.root, text="TRANSACTION HISTORY")
        self.transaction_history_frame.pack(fill="both", expand=True, padx=16, pady=8)
        # frame for the tree view of the list of transactions

        self.all_categories = sorted(set(INCOME_CATEGORIES + EXPENSE_CATEGORIES))
        self.income_categories = list(INCOME_CATEGORIES)
        self.expense_categories = list(EXPENSE_CATEGORIES)

        self.filtering_frame = tk.Frame(self.transaction_history_frame)
        self.filtering_frame.pack(fill="x", padx=8, pady=(8, 8))
        tk.Label(self.filtering_frame, text="Filter by Type:").pack(side="left", padx=4)
        self.filter_type_var = tk.StringVar(value="All")
        self.filter_type_menu = tk.OptionMenu(self.filtering_frame, self.filter_type_var, "All", "Income", "Expense", command=self.on_filter_type_change)
        self.filter_type_menu.pack(side="left", padx=4)

        tk.Label(self.filtering_frame, text="Category:").pack(side="left", padx=4)
        self.filter_category_var = tk.StringVar(value="All")
        self.filter_category_menu = tk.OptionMenu(self.filtering_frame, self.filter_category_var, "All")
        self.filter_category_menu.pack(side="left", padx=4)
        self.update_category_options("All")

        self.from_date = tk.StringVar()
        self.to_date = tk.StringVar()
        tk.Label(self.filtering_frame, text="From Date (YYYY-MM-DD):").pack(side="left", padx=4)
        self.from_date_entry = tk.Entry(self.filtering_frame, textvariable=self.from_date, width=10)
        self.from_date_entry.pack(side="left", padx=4)
        tk.Label(self.filtering_frame, text="To Date (YYYY-MM-DD):").pack(side="left", padx=4)
        self.to_date_entry = tk.Entry(self.filtering_frame, textvariable=self.to_date, width=10)
        self.to_date_entry.pack(side="left", padx=4)

        tk.Button(self.filtering_frame, text="Apply Filters", command=self.apply_transaction_filters).pack(side="left", padx=4)

        transaction_history_tree_frame = tk.Frame(self.transaction_history_frame)
        transaction_history_tree_frame.pack(fill="both", expand=True, padx=8, pady=8)

        current_scroll_bar = ttk.Scrollbar(transaction_history_tree_frame, orient="vertical")
        current_scroll_bar.pack(side="right", fill="y")

        self.transaction_history_tree = ttk.Treeview(transaction_history_tree_frame, columns=("category", "amount", "type", "description", "created_on"),show="headings", yscrollcommand=current_scroll_bar.set, height=6,selectmode="extended")
        current_scroll_bar.config(command=self.transaction_history_tree.yview)
        self.transaction_history_tree.heading("category", text="Category")
        self.transaction_history_tree.heading("amount", text="Amount")
        self.transaction_history_tree.heading("type", text="Type")
        self.transaction_history_tree.heading("description", text="Description")
        self.transaction_history_tree.heading("created_on", text="Created On")
        self.transaction_history_tree.column("category", width=180)
        self.transaction_history_tree.column("amount", width=120)
        self.transaction_history_tree.column("type", width=100)
        self.transaction_history_tree.column("description", width=180)
        self.transaction_history_tree.column("created_on", width=110)
        self.transaction_history_tree.pack(side="left", fill="both", expand=True)
        self.transaction_history_tree.bind("<<TreeviewSelect>>", self.on_transaction_history_select)

        transaction_actions_frame = tk.Frame(self.transaction_history_frame)
        transaction_actions_frame.pack(fill="x", padx=8, pady=(0, 8))
        self.delete_transaction_button = tk.Button(transaction_actions_frame, text="Delete Selected Transactions", command=self.delete_selected_transactions, state="disabled")
        self.delete_transaction_button.pack(side="left", padx=4)
        
        self.refresh_transaction_history()
        self.root.mainloop()

    
    def apply_transaction_filters(self):
        """Apply filters to the transaction history to show the most updated list of transactions based on the filters the user wants to apply."""
        type_filter = self.filter_type_var.get()
        category_filter = self.filter_category_var.get()
        from_date_str = self.from_date.get().strip()
        to_date_str = self.to_date.get().strip()

        current_user = self.app.session_manager.current_user
        if not current_user:
            messagebox.showerror("Error", "Need to be logged in to filter transactions.")
            return

        user_id = current_user.id

        # filter by the transaction type first so either its all, income, or expense, then we can filter it by category
        if type_filter == "All":
            transactions_by_type = self.app.transactions.get_user_transactions(user_id)
        else:
            transactions_by_type = self.app.transactions.get_transactions_by_type(user_id, type_filter.lower())

        filtered_transactions = transactions_by_type
        #if the option is not all then filter the transactions by the category
        if category_filter != "All":
            category_obj = self.app.category_crud.get_category_by_name(category_filter)
            if not category_obj:
                messagebox.showerror("Error", f"Category '{category_filter}' not found.")
                return

            transactions_by_category = self.app.transactions.get_transactions_by_category(user_id, category_obj.id)

            #if the type is all then we can filter the transactions by the category without having to filter by type first
            if type_filter == "All":
                filtered_transactions = transactions_by_category
            else: 
                #if the type is not all then we will filter by type first and then fitler by category            
                type_ids = set()
                for transaction in filtered_transactions:
                    type_ids.add(transaction.id)
                #filter the transaction by category after fitlering by type
                filtered_transactions = []
                for transaction in transactions_by_category:
                    if transaction.id in type_ids:
                        filtered_transactions.append(transaction)

        #filter the trsnsaction history by a date range if the user wants to also
        start_date = None
        end_date = None

        if from_date_str:
            try:
                start_date = datetime.strptime(from_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            except ValueError:
                messagebox.showerror("Error", "Invalid From Date format. Use YYYY-MM-DD.")
                return

        if to_date_str:
            try:
                to_date = datetime.strptime(to_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                #end date is the end of the day since we wnat to incldue the entire day of that date right before it become the next day
                end_date = (to_date + timedelta(days=1) - timedelta(microseconds=1)).replace(tzinfo=timezone.utc)
            except ValueError:
                messagebox.showerror("Error", "Invalid To Date format. Use YYYY-MM-DD.")
                return

        if start_date and end_date and start_date > end_date:
            messagebox.showerror("Error", "From Date must be earlier than To Date.")
            return
        #if both the start and end date are given then we can filter the history based on that date range
        #if the start date is given then we filter from that date to the most recent date
        #if end date is given then we filter from earliest date to the end date
        if start_date or end_date:
            transactions_by_date = self.app.transactions.get_transactions_by_date(user_id, start_date, end_date)
            date_ids = {transaction.id for transaction in transactions_by_date}
            date_ids = set()
            for transaction in transactions_by_date:
                date_ids.add(transaction.id)
            filtered_result = []
            for transaction in filtered_transactions:
                if transaction.id in date_ids:
                    filtered_result.append(transaction)
            filtered_transactions = filtered_result

        self.refresh_transaction_history(filtered_transactions)

    def on_filter_type_change(self, selected_type):
        """Update the list of categories options depending on the type of transaction the user wants to filter by."""
        self.update_category_options(selected_type)

    def update_category_options(self, selected_type):
        """Update what the list of categories options are depending on the type of transaction the user wants to filter by."""
        if selected_type == "Income":
            categories = self.income_categories
        elif selected_type == "Expense":
            categories = self.expense_categories
        else:
            categories = self.all_categories

        menu = self.filter_category_menu["menu"]
        menu.delete(0, "end")
        menu.add_command(label="All", command=lambda value="All": self.filter_category_var.set(value))
        for category in categories:
            menu.add_command(label=category, command=lambda value=category: self.filter_category_var.set(value))

        self.filter_category_var.set("All")
    
    def refresh_transaction_history(self, transactions=None):
        """Refresh the transaction history tree view to show the most updated list of transactions."""
        for item in self.transaction_history_tree.get_children():
            self.transaction_history_tree.delete(item)

        if transactions is None:
            current_user = self.app.session_manager.current_user
            if not current_user:
                return
            
            user_id = current_user.id
            transactions = self.app.transactions.get_user_transactions(user_id)
        
        # Sort transactions by created_on date to show the most recent one first and the oldest one last
        transactions = sorted(transactions, key=lambda t: t.created_on, reverse=True)
        
        # Add the transactions to the tree view for the transaction history
        for transaction in transactions:
            if transaction.category:
                category_name = transaction.category.name
            else:
                category_name = "Unknown"
            amount = f"${transaction.amount:.2f}"
            transaction_type = transaction.type.capitalize()
            if transaction.description:
                description = transaction.description
            else:
                description = ""
            if transaction.created_on:
                created_on = transaction.created_on.strftime("%Y-%m-%d %H:%M:%S")
            else:
                created_on = ""
            
            self.transaction_history_tree.insert("", "end", values=(
                category_name, amount, transaction_type, description, created_on
            ), tags=(str(transaction.id),))

    def on_transaction_history_select(self, event):
        """Enable the delete transaction button if the user selects a transaction in the transaction history tree view."""
        selected_transaction = self.transaction_history_tree.selection()
        if selected_transaction:
            self.delete_transaction_button.config(state="normal")
        else:
            self.delete_transaction_button.config(state="disabled")

    def get_selected_transaction_id(self, tree):
        """Get the ids of the selected transactions from the tree view using their tags."""
        selected_transaction = tree.selection()
        transaction_ids = []

        for transaction in selected_transaction:
            transaction_tags = tree.item(transaction, "tags")
            if transaction_tags:
                transaction_ids.append(int(transaction_tags[0]))
        return transaction_ids

    def delete_selected_transactions(self):
        """Delete the selected transactions in the transaction history tree view."""
        selected_transaction_id = self.get_selected_transaction_id(self.transaction_history_tree)
        if not selected_transaction_id:
            messagebox.showerror("Error", "There are no transactions selected to delete")
            return
        try:
            current_user = self.app.session_manager.current_user
            if not current_user:
                messagebox.showerror("Error", "Need to be logged in to delete transactions.")
                return
            
            for transaction_id in selected_transaction_id:
                status, message = self.app.transactions.delete_user_transaction(current_user.id, transaction_id)
                if not status:
                    messagebox.showerror("Error", message)
            messagebox.showinfo("Success", f"Successfully deleted {len(selected_transaction_id)} selected transaction(s)")
            self.refresh_transaction_history()
            self.delete_transaction_button.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def return_back(self):
        """Return to the dashboard window."""
        from .dashboard_window import DashboardWindow
        
        self.root.destroy()
        DashboardWindow(self.app)

