import sqlite3 as sql
from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close_connection(self):
        pass

    @abstractmethod
    def register_user(self, username, password):
        pass

    @abstractmethod
    def authenticate_user(self, username, password):
        pass

    @abstractmethod
    def add_transaction(self, username, date, transaction_type, category, amount, title, description):
        pass

    @abstractmethod
    def add_notification(self, username, date, time, transaction_type, category, amount, message):
        pass

    @abstractmethod
    def update_password(self, username, new_password):
        pass

    @abstractmethod
    def delete_user(self, username):
        pass

    @abstractmethod
    def get_balance(self, username):
        pass
    
    @abstractmethod
    def fetch_total_income(self, username):
        pass

    @abstractmethod
    def fetch_total_expense(self, username):
        pass

    @abstractmethod
    def get_password(self, username):
        pass

    @abstractmethod
    def get_general_transactions(self, username):
        pass

    @abstractmethod
    def get_income_data(self, username):
        pass

    @abstractmethod
    def get_expense_data(self, username):
        pass

    @abstractmethod
    def get_data_notification(self, username):
        pass

    @abstractmethod
    def sort_transaction_type(self, username):
        pass

    @abstractmethod
    def edit_transaction(self, username, id):
        pass

class SQLiteDatabase(DatabaseInterface):
    def __init__(self, db_name="database.db"):
        self.__db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()
        self._initialize_tables()

    @property
    def db_name(self):
        return self.__db_name

    def connect(self):
        """Establish database connection"""
        self.connection = sql.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def _initialize_tables(self):
        """Initialize database tables"""
        tables = {
            'UserAuthentication': '''
                CREATE TABLE IF NOT EXISTS UserAuthentication (
                    username TEXT PRIMARY KEY,
                    password TEXT
                )''',
            'User_Transaction': '''
                CREATE TABLE IF NOT EXISTS User_Transaction (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    date TEXT,
                    transaction_type TEXT,
                    category TEXT,
                    amount INTEGER,
                    title TEXT,
                    description TEXT,
                    FOREIGN KEY (username) REFERENCES UserAuthentication(username)
                )''',
            'User_Income': '''
                CREATE TABLE IF NOT EXISTS User_Income (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    date TEXT,
                    category TEXT,
                    amount INTEGER,
                    title TEXT,
                    description TEXT,
                    FOREIGN KEY (username) REFERENCES UserAuthentication(username)
                )''',
            'User_Expense': '''
                CREATE TABLE IF NOT EXISTS User_Expense (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    date TEXT,
                    category TEXT,
                    amount INTEGER,
                    title TEXT,
                    description TEXT,
                    FOREIGN KEY (username) REFERENCES UserAuthentication(username)
                )''',
            'User_Notification': '''
                CREATE TABLE IF NOT EXISTS User_Notification (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    date TEXT,
                    time TEXT,
                    transaction_type TEXT,
                    category TEXT,
                    message TEXT,
                    description TEXT,
                    amount INTEGER,
                    FOREIGN KEY (username) REFERENCES UserAuthentication(username)
                )'''
        }
        
        for table_name, query in tables.items():
            self.cursor.execute(query)
        self.connection.commit()

    def register_user(self, username, password):
        try:
            self.cursor.execute("SELECT username FROM UserAuthentication WHERE username = ?", (username,))
            if self.cursor.fetchone():
                return False

            # Proceed with insertion
            self.cursor.execute(
                "INSERT INTO UserAuthentication (username, password) VALUES (?, ?)",
                (username, password)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error during registration: {e}")
            return False


    def authenticate_user(self, username, password):
        """Authenticate user credentials"""
        self.cursor.execute(
            "SELECT * FROM UserAuthentication WHERE username = ? AND password = ?",
            (username, password)
        )
        result = self.cursor.fetchall()
        return bool(result)

    def add_transaction(self, username, date, transaction_type, category, amount, title, description):
        """Add a new transaction"""
        try:
            if transaction_type.lower() == 'income':
                table = 'User_Income'
            elif transaction_type.lower() == 'expense':
                table = 'User_Expense'
            else:
                return False

            self.cursor.execute(
                f'''
                INSERT INTO {table} (username, date, category, amount, title, description)
                VALUES (?, ?, ?, ?, ?, ?)
                ''',
                (username, date, category, amount, title, description)
            )

            self.cursor.execute(
                '''
                INSERT INTO User_Transaction (username, date, transaction_type, category, amount, title, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (username, date, transaction_type, category, amount, title, description)
            )

            self.connection.commit()
            return True
        except sql.Error as e:
            print(f"Database error: {str(e)}")
            return False
        
    def sort_transaction_type(self, username):
        try:    
            self.cursor.execute("DELETE FROM User_Income WHERE username = ?", (username,))
            self.cursor.execute("DELETE FROM User_Expense WHERE username = ?", (username,))

            transactions = self.cursor.execute('''
                SELECT * FROM User_Transaction
                WHERE username = ?
                ORDER BY 
                    CASE transaction_type
                        WHEN 'Income' THEN 0
                        WHEN 'Expense' THEN 1
                    END
            ''', (username,)).fetchall()

            for txn in transactions:
                if txn[3] == "Income":
                    self.cursor.execute('''
                        INSERT INTO User_Income (username, date, category, amount, title, description)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (txn[1], txn[2], txn[4], txn[5], txn[6], txn[7]))
                elif txn[3] == "Expense":
                    self.cursor.execute('''
                        INSERT INTO User_Expense (username, date, category, amount, title, description)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (txn[1], txn[2], txn[4], txn[5], txn[6], txn[7]))

            self.connection.commit()
            return True

        except sql.Error as e:
            print(f"[DB Error] sort_transaction_type: {e}")
            self.connection.rollback()
            return False
        
    def edit_transaction(self, id, username, date, transaction_type, category, amount, title, description):
        try:
            self.cursor.execute("""
                UPDATE User_Transaction 
                SET date = ?, category = ?, transaction_type = ?, amount = ?, title = ?, description = ? 
                WHERE id = ? AND username = ?
            """, (date, category, transaction_type, amount, title, description, id, username))
            
            self.connection.commit()
            return True
        
        except sql.Error as e:
            print(f"Database error: {str(e)}")
            self.connection.rollback()
            return False


    def add_notification(self, username, date, time, transaction_type, category, message, description, amount):
        try:

            self.cursor.execute(
                f'''
                INSERT INTO  User_Notification (username, date, time, transaction_type, category, message, description, amount)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (username, date, time, transaction_type, category, message, description, amount)
                )

            self.connection.commit()
            return True
        except sql.Error as e:
            print(f"Database error: {str(e)}")
            return False
        
    def get_data_notification(self, username):
        try:
            self.cursor.execute(
                "SELECT date, time, category, message, description, amount FROM User_Notification WHERE username = ?",
                (username,)
            )
            return self.cursor.fetchall() 
        except sql.Error as e:
            print(f"Database error: {str(e)}")
            return []
        
    def get_general_transactions(self, username):
        """Get all transactions for a user"""
        try:
            self.cursor.execute(
                "SELECT id, username, date, transaction_type, category, amount, title, description FROM User_Transaction WHERE username = ?",
                (username,)
            )
            return self.cursor.fetchall()
        except sql.Error as e:
            print(f"Database error: {str(e)}")
            return []
        
    def get_income_data(self, username):
        try:
            self.cursor.execute(
                "SELECT username, date, category, amount, title, description FROM User_Income WHERE username = ?",
                (username,)
            )
            return self.cursor.fetchall()
        except sql.Error as e:
            print(f"Database error: {str(e)}")
            return []
        
    def get_expense_data(self, username):
        try:
            self.cursor.execute(
                "SELECT username, date, category, amount, title, description FROM User_Expense WHERE username = ?",
                (username,)
            )
            return self.cursor.fetchall()
        except sql.Error as e:
            print(f"Database error: {str(e)}")
            return []

    def update_password(self, username, new_password):
        """Update user password"""
        try:
            self.cursor.execute(
                "UPDATE UserAuthentication SET password = ? WHERE username = ?",
                (new_password, username)
            )
            self.connection.commit()
            return True
        except sql.Error as e:
            print(f"Database error: {str(e)}")
            return False

    def delete_user(self, username):
        """Delete user and all associated data"""
        try:
            self.cursor.execute("SELECT username FROM UserAuthentication WHERE username = ?", (username,))
            if not self.cursor.fetchone():
                return False
            
            tables = ['UserAuthentication', 'User_Transaction', 'User_Income', 'User_Expense', 'User_Notification']
            for table in tables:
                self.cursor.execute(f"DELETE FROM {table} WHERE username = ?", (username,))
            self.connection.commit()
            return True
        except sql.Error as e:
            print(f"Database error: {str(e)}")
            return False

    def get_balance(self, username):
        """Calculate user balance (income - expenses)"""
        try:
            income = self._get_transaction_total('User_Income', username)
            expenses = self._get_transaction_total('User_Expense', username)
            return income - expenses
        except sql.Error as e:
            print(f"Database error: {str(e)}")
            return 0

    def fetch_total_income(self, username):
        try:
            income = self._get_transaction_total('User_Income', username)
            return income
        except sql.Error as e:
             print(f"Database error: {str(e)}")
             return 0
        
    def fetch_total_expense(self, username):
        try:
            expense = self._get_transaction_total('User_Expense', username)
            return expense
        except sql.Error as e:
             print(f"Database error: {str(e)}")
             return 0
        
    def get_password(self, username):
        self.cursor.execute("SELECT password FROM UserAuthentication WHERE username = ?",(username,))
        return self.cursor.fetchone()[0]

    def _get_transaction_total(self, table, username):
        """Helper method to get transaction totals"""
        self.cursor.execute(
            f"SELECT SUM(amount) FROM {table} WHERE username = ?",
            (username,)
        )
        return self.cursor.fetchone()[0] or 0
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

class DatabaseService:
    _instance = None

    @classmethod
    def get_instance(cls, db_name="database.db"):
        if cls._instance is None:
            cls._instance = SQLiteDatabase(db_name)
        return cls._instance