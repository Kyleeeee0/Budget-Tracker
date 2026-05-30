import csv
from datetime import datetime
import os
import Log_In, Category_Entry
from Database import DatabaseService
from tkinter import Tk, Frame, filedialog, messagebox
from abc import ABC, abstractmethod


class BaseController(ABC):
    """Abstract base class for all controllers"""
    @abstractmethod
    def execute(self, *args, **kwargs):
        """Execute controller operation"""
        pass

class UserController(BaseController):
    """Handles user-related operations"""
    def __init__(self):
        self.__db = DatabaseService.get_instance()

    @property
    def db(self):
        return self.__db

    def execute(self, operation: str, *args, **kwargs):
        """Execute user-related operations"""
        operations = {
            'authenticate': self.authenticate,
            'register': self.register,
            'update_password': self.update_password,
            'delete_account': self.delete_account,
            'get_password': self.get_password
        }
        if operation in operations:
            return operations[operation](*args, **kwargs)
        raise ValueError(f"Unknown operation: {operation}")

    def authenticate(self, username, password):
        return self.db.authenticate_user(username, password)

    def register(self, username, password):
        return self.db.register_user(username, password)

    def update_password(self, username, new_password):
        return self.db.update_password(username, new_password)

    def get_password(self, username):
        return self.db.get_password(username)
    
    def delete_account(self, username, window=None):
        success = self.db.delete_user(username)
        if success:
            if window:
                self._navigate_to_login(window)
            return True
        return False

    def _navigate_to_login(self, window):
        window.destroy()
        new_window = Tk()
        Log_In.LogIn(new_window)

class TransactionController(BaseController):
    """Handles transaction operations"""
    def __init__(self):
        self.db = DatabaseService.get_instance()

    def execute(self, operation: str, *args, **kwargs):
        """Execute transaction-related operations"""
        operations = {
            'add_transaction': self.add_transaction,
            'get_balance': self.get_balance,
            'get_income': self.get_income,
            'get_expense': self.get_expense,
            'edit_transaction': self.edit_transaction
        }
        if operation in operations:
            return operations[operation](*args, **kwargs)
        raise ValueError(f"Unknown operation: {operation}")

    def add_transaction(self, username, date, transaction_type, category, amount, title, description):
        return self.db.add_transaction(username, date, transaction_type, category, amount, title, description)

    def get_balance(self, username):
        return self.db.get_balance(username)
    
    def get_income(self, username):
        return self.db.fetch_total_income(username)
    
    def get_expense(self, username):
        return self.db.fetch_total_expense(username)
    
    def sort_transaction(self, username):
        self.db.sort_transaction_type(username)

    def edit_transaction(self, id, username, date, transaction_type, category, amount, title, description):
        return self.db.edit_transaction(id, username, date, transaction_type, category, amount, title, description)


class AnalysisTabController(BaseController):

    def __init__(self):
        self.db = DatabaseService.get_instance()
        self.transaction_controller = TransactionController()
        
    def execute(self, operation: str, *args, **kwargs):
        operations = {
            'get_general_transactions': self.get_general_transactions,
            'get_income_data': self.get_income_data,
            'get_expense_data': self.get_expense_data
        }
        if operation in operations:
            return operations[operation](*args, **kwargs)
        raise ValueError(f"Unknown operation: {operation}")
        
    def get_income_data(self, username):
        return self.db.get_income_data(username)

    def get_expense_data(self, username):
        return self.db.get_expense_data(username)

    def get_general_transactions(self, username):
        return self.db.get_general_transactions(username)

    def save_transactions_to_csv(self, usernames):
        header_transaction = ["Username", "Date", "Transaction_type", "Category", "Amount", "Title", "Description"]
        header = ["Username", "Date", "Category", "Amount", "Title", "Description"]

        try:
            data_transaction = self.get_general_transactions(usernames)
            data_income = self.get_income_data(usernames)
            data_expense = self.get_expense_data(usernames)

            with open(f"{usernames}.transaction_file.csv", "w", newline="", encoding="utf-8") as file:
                file.write(",".join(header_transaction) + "\n")
                for data in data_transaction:
                    datas = data[1:]
                    file.write(",".join(map(str, datas)) + "\n")

            with open(f"{usernames}.income_file.csv", "w", newline="", encoding="utf-8") as income_file:
                income_file.write(",".join(header) + "\n")
                for data in data_income:
                    income_file.write(",".join(map(str, data)) + "\n")

            with open(f"{usernames}.expense.csv", "w", newline="", encoding="utf-8") as expense_file:
                expense_file.write(",".join(header) + "\n")
                for data in data_expense:
                    expense_file.write(",".join(map(str, data)) + "\n")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showinfo("Complete", "Data saving process completed.")

    def load_transaction_to_csv(self, usernames):
        initial_directory = os.path.expanduser("~")
        filepath = filedialog.askopenfilename(
            initialdir=initial_directory,
            title="Open CSV File",
            filetypes=[("CSV files", "*.csv")]
        )

        if not filepath:
            print("No file selected.")
            return

        transaction_data = []
        error_occured = False
        try:
            income_expense_data = ["Food", "Transport", "Medicine", "Groceries", "Rent", "Gifts", "Savings",
                                   "Entertainment", "Salary", "Investment", "Bonus", "Receipt", "Dividend",
                                   "Borrowing", "Allowance"]

            with open(filepath, "r", newline="", encoding="utf-8") as read_file:
                reader = csv.reader(read_file)
                # next(reader)
                header = next(reader)
                header = [col.capitalize() for col in header]

                if header != ["Date", "Transactiontype", "Category", "Amount", "Title", "Description"]:
                    messagebox.showerror("Invalid Header", "Invalid Header. Please follow the format for header")
                    return

                for row in reader:
                    if len(row) < 6:
                        print(f"Skipping invalid row: {row}")
                        continue

                    date, transaction_type, category, amount, title, description = row

                    if not category.isalpha():
                        messagebox.showerror("Input Error", "Invalid category. Please enter only letters.")
                        error_occured = True
                        continue

                    capitalized_category = category.capitalize()

                    if capitalized_category not in income_expense_data:
                        capitalized_category = "More"

                    formatted_date = datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")

                    validate_date = Controller.validate_date(formatted_date)
                    validate_transaction_type = Controller.validate_transaction_type(transaction_type)
                    validate_amount = Controller.validate_amount(float(amount))
                    validate_category = Controller.validate_category(capitalized_category, transaction_type)

                    if validate_date and validate_transaction_type and validate_amount and validate_category:
                        if float(amount) > 0:
                            transaction_data.append((usernames, formatted_date, transaction_type,
                                                    capitalized_category, amount, title, description))
                        else:
                            error_occured = True
                            messagebox.showerror("Invalid Amount", "Amount must be a positive number (avoid negative values or text).")
                            return
                    else:
                        error_occured = True
                        if not validate_date:
                            messagebox.showerror("Invalid Date", "The date must follow the format YYYY-MM-DD (e.g., 2025-06-15).")
                        elif not validate_transaction_type:
                            messagebox.showerror("Invalid Transaction Type", "Transaction type must be either 'Income' or 'Expense'.")
                        elif not validate_category:
                            messagebox.showerror("Invalid Category", "This category is not valid for the selected transaction type.")
                        return

            if error_occured:
                messagebox.showerror("Error Occurred", "An error was encountered in the file. Transaction loading halted.")
            else:
                for data in transaction_data:
                    self.transaction_controller.add_transaction(*data)
                messagebox.showinfo("Complete", "Transaction loading process completed.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


class UIController(BaseController):
    """Handles UI operations"""
    @staticmethod
    def execute(operation: str, *args, **kwargs):
        """Execute UI-related operations"""
        operations = {
            'toggle_password': UIController.toggle_password,
            'logout': UIController.logout,
            'switch_tab': UIController.switch_tab,
            'toggle_notification': UIController.toggle_notification,
            'toggle_settings': UIController.toggle_settings,
            'switch_category': UIController.switch_category
        }
        if operation in operations:
            return operations[operation](*args, **kwargs)
        raise ValueError(f"Unknown operation: {operation}")

    @staticmethod
    def toggle_password(entry, show_var):
        """Toggle password visibility"""
        entry.config(show="" if show_var.get() else "*")

    @staticmethod
    def logout(window):
        """Handle logout process"""
        if window.winfo_exists():
            try:
                task_ids = window.tk.call('after', 'info')
                for task_id in task_ids:
                    window.after_cancel(task_id)
            except Exception as e:
                print(f"Error canceling background processes: {e}")

            window.destroy()

            new_window = Tk()
            Log_In.LogIn(new_window)
            new_window.mainloop()
        
    @staticmethod
    def switch_tab(settings_handler, notif_handler, tab_class, home_instance, username: str) -> None:
        """Switch between tabs in the application"""
        home_instance.clear_all_content()
        home_instance.current_tab_frame = Frame(home_instance.main_window, bg="#F4F4F4")
        home_instance.current_tab_frame.place(x=200, y=112, width=1051, height=621)
        home_instance.current_tab = tab_class(home_instance.current_tab_frame, username)

        settings_handler.lift_settings()
        notif_handler.lift_notification()

    @staticmethod
    def toggle_notification(notif_handler, settings_handler) -> None:
        """Toggle notification panel"""
        if settings_handler.settings_visible:
            settings_handler.hide_settings()
        notif_handler.notification()

    @staticmethod
    def toggle_settings(notif_handler, settings_handler) -> None:
        """Toggle settings panel"""
        if notif_handler.notif_visible:
            notif_handler.hide_notification()
        settings_handler.settings()

    @staticmethod
    def switch_category(frame, category_name: str, username: str,
                       transaction_type: str, categories_tab_instance) -> None:

        frame.configure(fg_color="#D7E6C5", bg_color="#9FD39C")
        return Category_Entry.CategoryEntryForm(frame, category_name,
                                           transaction_type, username,
                                           categories_tab_instance)
    

class NotificationTabController(BaseController):
    def __init__(self):
        self.db = DatabaseService.get_instance()

    def execute(self, operation: str, *args, **kwargs):
        operations = {
            'Notification_Handler': self.Notification_Handler,
            'get_Notification': self.Get_Notification,
            'get_alerts_to_generate': self.get_alerts_to_generate
        }
        if operation in operations:
            return operations[operation](*args, **kwargs)
        raise ValueError(f"Unknown operation: {operation}")

    def Notification_Handler(self, username, date, time, transaction_type, category=None, amount=0, message=None, description=None):
        if transaction_type == "Income":
            message = "Income Added"
            description = f"You received ₱{amount} in {category} today. Time to plan your savings!"
        elif transaction_type == "Expense":
            message = "Expense Added"
            description = f"You added ₱{amount} in {category} today. Keep an eye on your budget!"

        # Fallback for system events
        if message is None:
            message = "Notification"
        if description is None:
            description = "No additional details provided."

        self.db.add_notification(username, date, time, transaction_type, category, message, description, amount)

    def Get_Notification(self, username):
        return self.db.get_data_notification(username)

    def get_alerts_to_generate(self, username, conditions=None):
        today = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M')

        balance = self.db.get_balance(username)
        income = self.db.fetch_total_income(username)
        notif_data = self.Get_Notification(username)

        existing_today = {n[3] for n in notif_data if n[0] == today}
        alerts = []

        if 0 <= balance < 0.1 * income:
            msg = "Your balance is running low!"
            if balance == 0:
                msg = "Your balance is depleted! Add funds immediately."

            alerts.append({
                "transaction_type": "Balance",
                "category": "System",
                "amount": 0,
                "message": "Balance Alert",
                "description": f"{msg} You have only ₱{balance:.2f} left.",
                "date": today,
                "time": current_time
            })

        if balance < 0 and "Negative Balance Alert" not in existing_today:
            alerts.append({
                "transaction_type": "Balance",
                "category": "System",
                "amount": 0,
                "message": "Negative Balance Alert",
                "description": f"Your balance has dropped below ₱0. You're currently at ₱{balance:.2f}. Please review your recent expenses.",
                "date": today,
                "time": current_time
            })

        if conditions:
            alerts.append({
                "transaction_type": "Transaction Edit",
                "category": "System",
                "amount": 0,
                "message": "Transaction Edit",
                "description": f"You have successfully edited your transaction. Changes are now saved.",
                "date": today,
                "time": current_time
            })

        return alerts

class Validate_Inputs(BaseController):
    def __init__(self):
        self.db = DatabaseService.get_instance()

    def execute(self, operation: str, *args, **kwargs):
        operations = {
            'validate_date': self.validate_date,
            'validate_amount': self.validate_amount,
            'validate_category': self.validate_category,
            'validate_transaction_type': self.validate_transaction_type
        }
        if operation in operations:
            return operations[operation](*args, **kwargs)
        raise ValueError(f"Unknown operation: {operation}")
    
    def validate_date(self, inputs):
        try:
            datetime.strptime(inputs, "%Y-%m-%d")
            return True
        except ValueError:
            return False
        
    def validate_amount(self, inputs):
        try:
            if float(inputs) >= 0:
                return True
            else:
                return True
        except ValueError:
            return False
        
    def validate_category(self, category, transaction_type):
        income_category = ["Salary", "Investment", "Bonus", "Receipt", "Dividend", "Gifts", "Borrowing", "Allowance", "More"]
        expense_category =["Food", "Transport", "Medicine", "Groceries", "Rent", "Gifts", "Savings", "Entertainment", "More"]
    
        transaction_type = transaction_type.capitalize()

        if transaction_type == "Income":
            if category in income_category:
                return True
            else:
                return False
            
        elif transaction_type == "Expense":
            if category in expense_category:
                return True
            else:
                return False
            
    def validate_transaction_type(self, transaction_type):

        transaction_type = transaction_type.capitalize()

        if transaction_type in ["Income", "Expense"]:
            return True
        else:
            return False

class Controller:
    """Facade providing simplified access to all controllers"""
    _user_controller = UserController()
    _transaction_controller = TransactionController()
    _ui_controller = UIController()
    _analysis_controller = AnalysisTabController()
    _NotificationTabController = NotificationTabController()
    _Validate_Inputs = Validate_Inputs()

    @classmethod
    def authenticate_user(cls, username, password):
        return cls._user_controller.authenticate(username, password)

    @classmethod
    def register_user(cls, username, password):
        return cls._user_controller.register(username, password)

    @classmethod
    def toggle_password(cls, entry, show_var):
        cls._ui_controller.toggle_password(entry, show_var)

    @classmethod
    def logout_user(cls, window):
        cls._ui_controller.logout(window)

    @classmethod
    def add_transaction(cls, username, date, transaction_type, category, amount, title, description):
        return cls._transaction_controller.add_transaction(
            username, date, transaction_type, category, amount, title, description
        )

    @classmethod
    def get_balance(cls, username):
        return cls._transaction_controller.get_balance(username)

    @classmethod
    def update_password(cls, username, new_password):
        return cls._user_controller.update_password(username, new_password)

    @classmethod
    def delete_account(cls, username, window=None):
        return cls._user_controller.delete_account(username, window)
    
    @classmethod
    def switch_tab(cls, settings_handler, notif_handler, tab_class, home_instance, username: str) -> None:
        cls._ui_controller.switch_tab(settings_handler, notif_handler, tab_class, home_instance, username)

    @classmethod
    def toggle_notification(cls, notif_handler, settings_handler) -> None:
        cls._ui_controller.toggle_notification(notif_handler, settings_handler)

    @classmethod
    def toggle_settings(cls, notif_handler, settings_handler) -> None:
        cls._ui_controller.toggle_settings(notif_handler, settings_handler)

    @classmethod
    def switch_category(cls, frame, category_name: str, username: str,
                       transaction_type: str, categories_tab_instance):
        return cls._ui_controller.switch_category(frame, category_name, username,
                                                 transaction_type, categories_tab_instance)
    
    @classmethod
    def get_income(cls, username):
        return cls._transaction_controller.get_income(username)
    
    @classmethod
    def get_expense(cls, username):
        return cls._transaction_controller.get_expense(username)
    
    @classmethod
    def get_password(cls, username):
        return cls._user_controller.get_password(username)
    
    @classmethod
    def get_income_data(cls, username):
        return cls._analysis_controller.get_income_data(username)

    @classmethod
    def get_expense_data(cls, username):
        return cls._analysis_controller.get_expense_data(username)

    @classmethod
    def get_general_transactions(cls, username):
        return cls._analysis_controller.get_general_transactions(username)

    @classmethod
    def save_transactions_to_csv(cls, username):
        return cls._analysis_controller.save_transactions_to_csv(username)

    @classmethod
    def load_transaction_to_csv(cls, username):
        return cls._analysis_controller.load_transaction_to_csv(username)
    
    @classmethod
    def Notification_Handler(cls, username, date, time, transaction_type, category, amount, message, description):
        return cls._NotificationTabController.Notification_Handler(username, date, time, transaction_type, category, amount, message, description)
    
    @classmethod
    def Get_Notification(cls, username):
        return cls._NotificationTabController.Get_Notification(username)
    
    @classmethod
    def get_alerts_to_generate(cls, username, conditions=None):
        return cls._NotificationTabController.get_alerts_to_generate(username, conditions)
    
    @classmethod
    def validate_date(cls, inputs):
        return cls._Validate_Inputs.validate_date(inputs)
    
    @classmethod
    def validate_amount(cls, inputs):
        return cls._Validate_Inputs.validate_amount(inputs)
    
    @classmethod
    def sort_transaction(cls, username):
        return cls._transaction_controller.sort_transaction(username)
    
    @classmethod
    def edit_transaction(cls, id, username, date, category, transaction_type, amount, title, description):
        return cls._transaction_controller.edit_transaction(id, username, date, category, transaction_type, amount, title, description)
    
    @classmethod
    def validate_category(cls, category, transaction_type):
        return cls._Validate_Inputs.validate_category(category, transaction_type)
    
    @classmethod
    def validate_transaction_type(cls,transaction_type):
        return cls._Validate_Inputs.validate_transaction_type(transaction_type)
