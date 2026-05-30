import unittest
from datetime import datetime
from pathlib import Path
import sys
parent = Path(__file__).resolve().parent.parent
sys.path.append(str(parent))
from Database import SQLiteDatabase

class TestSQLiteDatabase(unittest.TestCase):
    def setUp(self):
        # Setup in-memory database for tests
        self.db = SQLiteDatabase(":memory:")
        # Register a test user
        self.username = "testuser"
        self.password = "password123"
        self.db.register_user(self.username, self.password)

    def tearDown(self):
        self.db.close_connection()

    def test_register_user_success(self):
        result = self.db.register_user("newuser", "newpass")
        self.assertTrue(result)

    def test_register_existing_user(self):
        result = self.db.register_user(self.username, self.password)
        self.assertFalse(result)

    def test_authenticate_user_success(self):
        result = self.db.authenticate_user(self.username, self.password)
        self.assertTrue(result)

    def test_authenticate_user_wrong_password(self):
        result = self.db.authenticate_user(self.username, "wrongpass")
        self.assertFalse(result)

    def test_authenticate_nonexistent_user(self):
        result = self.db.authenticate_user("nonexistent", "pass")
        self.assertFalse(result)

    def test_add_transaction_income(self):
        date = datetime.now().isoformat()
        result = self.db.add_transaction(self.username, date, "Income", "Job", 1000, "Salary", "Monthly salary")
        self.assertTrue(result)
        transactions = self.db.get_income_data(self.username)
        self.assertTrue(any(txn[3] == 1000 and txn[4] == "Salary" for txn in transactions))

    def test_add_transaction_expense(self):
        date = datetime.now().isoformat()
        result = self.db.add_transaction(self.username, date, "Expense", "Food", 50, "Lunch", "Lunch with colleagues")
        self.assertTrue(result)
        expenses = self.db.get_expense_data(self.username)
        self.assertTrue(any(txn[3] == 50 and txn[4] == "Lunch" for txn in expenses))

    def test_add_transaction_invalid_type(self):
        date = datetime.now().isoformat()
        result = self.db.add_transaction(self.username, date, "Donation", "Charity", 100, "Gift", "Charity donation")
        self.assertFalse(result)

    def test_sort_transaction_type(self):
        date = datetime.now().isoformat()
        self.db.add_transaction(self.username, date, "Income", "Job", 1000, "Salary", "Monthly salary")
        self.db.add_transaction(self.username, date, "Expense", "Food", 50, "Dinner", "Dinner expense")
        result = self.db.sort_transaction_type(self.username)
        self.assertTrue(result)
        income = self.db.get_income_data(self.username)
        expense = self.db.get_expense_data(self.username)
        self.assertTrue(len(income) > 0)
        self.assertTrue(len(expense) > 0)

    def test_edit_transaction_success(self):
        date = datetime.now().isoformat()
        self.db.add_transaction(self.username, date, "Income", "Job", 1000, "Old Title", "Old Desc")
        transactions = self.db.get_general_transactions(self.username)
        txn_id = transactions[0][0]
        new_date = datetime.now().isoformat()
        result = self.db.edit_transaction(txn_id, self.username, new_date, "Income", "Job", 1500, "New Title", "New Desc")
        self.assertTrue(result)
        updated = self.db.get_general_transactions(self.username)
        updated_txn = next((t for t in updated if t[0] == txn_id), None)
        self.assertEqual(updated_txn[5], 1500)
        self.assertEqual(updated_txn[6], "New Title")

    def test_edit_transaction_invalid_id(self):
        result = self.db.edit_transaction(9999, self.username, "2023-01-01", "Income", "Job", 100, "Title", "Desc")
        self.assertTrue(result)  # SQLite execute still succeeds but no rows updated

    def test_add_notification_and_get_data(self):
        date = datetime.now().date().isoformat()
        time = datetime.now().time().isoformat(timespec='seconds')
        result = self.db.add_notification(self.username, date, time, "Income", "Job", "You got paid", "Salary credited", 1000)
        self.assertTrue(result)
        notifications = self.db.get_data_notification(self.username)
        self.assertTrue(len(notifications) >= 1)
        first = notifications[0]
        self.assertEqual(first[3], "You got paid")

    def test_update_password_success(self):
        new_pass = "newpassword"
        result = self.db.update_password(self.username, new_pass)
        self.assertTrue(result)
        # Now authenticate with new password
        auth_result = self.db.authenticate_user(self.username, new_pass)
        self.assertTrue(auth_result)

    def test_delete_user_success(self):
        # Add some transactions and notifications
        date = datetime.now().isoformat()
        self.db.add_transaction(self.username, date, "Income", "Job", 1000, "Salary", "Monthly salary")
        self.db.add_notification(self.username, date, "12:00:00", "Income", "Job", "Paid", "Salary", 1000)
        # Delete user
        result = self.db.delete_user(self.username)
        self.assertTrue(result)
        # Try to authenticate deleted user
        auth_result = self.db.authenticate_user(self.username, self.password)
        self.assertFalse(auth_result)
        # Check transactions count - should be zero
        transactions = self.db.get_general_transactions(self.username)
        self.assertEqual(len(transactions), 0)

    def test_get_balance(self):
        date = datetime.now().isoformat()
        self.db.add_transaction(self.username, date, "Income", "Job", 1000, "Salary", "Monthly salary")
        self.db.add_transaction(self.username, date, "Expense", "Food", 400, "Groceries", "Weekly groceries")
        balance = self.db.get_balance(self.username)
        self.assertEqual(balance, 600)  # 1000 - 400

    def test_fetch_total_income_and_expense(self):
        date = datetime.now().isoformat()
        self.db.add_transaction(self.username, date, "Income", "Job", 800, "Bonus", "Performance bonus")
        self.db.add_transaction(self.username, date, "Expense", "Travel", 200, "Taxi", "Taxi fare")
        income = self.db.fetch_total_income(self.username)
        expense = self.db.fetch_total_expense(self.username)
        self.assertGreaterEqual(income, 800)
        self.assertGreaterEqual(expense, 200)

    def test_get_password(self):
        pw = self.db.get_password(self.username)
        self.assertEqual(pw, self.password)

    def test_get_general_transactions_empty(self):
        username2 = "emptyuser"
        self.db.register_user(username2, "pass")
        txns = self.db.get_general_transactions(username2)
        self.assertEqual(txns, [])

    def test_get_income_data_empty(self):
        username2 = "emptyuser"
        self.db.register_user(username2, "pass")
        data = self.db.get_income_data(username2)
        self.assertEqual(data, [])

    def test_get_expense_data_empty(self):
        username2 = "emptyuser"
        self.db.register_user(username2, "pass")
        data = self.db.get_expense_data(username2)
        self.assertEqual(data, [])

    def test_get_data_notification_empty(self):
        username2 = "emptyuser"
        self.db.register_user(username2, "pass")
        data = self.db.get_data_notification(username2)
        self.assertEqual(data, [])

if __name__ == '__main__':
    unittest.main()

