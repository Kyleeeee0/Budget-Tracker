import unittest
from unittest.mock import MagicMock, patch
from tkinter import Frame
from datetime import datetime
import sys
from pathlib import Path
parent = Path(__file__).resolve().parent.parent
sys.path.append(str(parent))
from Controller import (
    UserController, TransactionController, AnalysisTabController,
    UIController, NotificationTabController, Validate_Inputs, Controller)

class TestUserController(unittest.TestCase):
    def setUp(self):
        self.db_mock = MagicMock()
        self.user_controller = UserController()
        self.user_controller._UserController__db = self.db_mock
    
    def tearDown(self):
        del self.user_controller
    
    def test01_execute(self):
        self.db_mock.authenticate_user.return_value = True
        result = self.user_controller.execute('authenticate', 'test_user', 'test_pass')
        self.assertTrue(result)

    def test04_authenticate(self):
        self.db_mock.authenticate_user.return_value = True
        result = self.user_controller.authenticate('test_user', 'test_pass')
        self.assertTrue(result)

    def test02_register(self):
        self.db_mock.register_user.return_value = True
        result = self.user_controller.register('test_user', 'test_pass')
        self.assertTrue(result)
    
    def test03_invalid_register(self):
        self.db_mock.register_user.return_value = False
        result = self.user_controller.register('test_user', 'test_pass')
        self.assertFalse(result)

    def test05_update_password(self):
        self.db_mock.update_password.return_value = True
        result = self.user_controller.update_password('test_user', 'newpass')
        self.assertTrue(result)
    
    def test06_get_password(self):
        self.db_mock.get_password.return_value = 'newpass'
        result = self.user_controller.get_password('test_user')
        self.assertEqual(result, 'newpass')

    def test07_delete_account(self):
        self.db_mock.delete_account.return_value = True
        result = self.user_controller.delete_account('test_user')
        self.assertTrue(result)
        


class TestTransactionController(unittest.TestCase):
    def setUp(self):
        self.db_mock = MagicMock()
        self.transaction_controller = TransactionController()
        self.transaction_controller.db = self.db_mock
    
    def tearDown(self):
        del self.transaction_controller
    
    def test01_execute(self):
        self.db_mock.get_balance.return_value = 200
        result = self.transaction_controller.execute('get_balance', 'test_user')
        self.assertEqual(result, 200)    

    def test02_add_transaction(self):
        self.db_mock.add_transaction.return_value = True
        result = self.transaction_controller.add_transaction(
            'test_user', '09/06/2025', 'income', 'Food', 200, 'Chicken', 'Jollibee')
        self.assertTrue(result)

    def test03_add_transaction(self):
        self.db_mock.add_transaction.return_value = True
        result = self.transaction_controller.add_transaction(
            'test_user', '09/06/2025', 'income', 'Food', 200, 'Chicken', 'Jollibee')
        self.assertTrue(result)

    def test04_get_balance(self):
        self.db_mock.get_balance.return_value = 200
        result = self.transaction_controller.get_balance('test_user')
        self.assertEqual(result, 200)
    
    # Mocking get_expense, calls fetch_total_income
    # Mock straight to the fetch_total_income method
    def test05_get_income(self):
        self.db_mock.fetch_total_income.return_value = 1000
        result = self.transaction_controller.get_income('test_user')
        self.assertEqual(result, 1000)

    # Mocking get_expense, calls fetch_total_expense
    # Mock straight to the fetch_total_expense method
    def test06_get_expense(self):
        self.db_mock.fetch_total_expense.return_value = 2000
        result = self.transaction_controller.get_expense('test_user')
        self.assertEqual(result, 2000)

    # Test if error occurs when function is called with expected parameter
    def test07_sort_transaction(self):
        self.transaction_controller.sort_transaction('test_user')

    def test08_edit_transaction(self):
        self.db_mock.edit_transaction.return_value = True
        result = self.transaction_controller.edit_transaction(
            95, 'test_user', '09/06/2025', 'income', 'Food', 200, 'Chicken', 'Jollibee')
        self.assertTrue(result)



class TestAnalysisTabController(unittest.TestCase):
    def setUp(self):
        self.db_mock = MagicMock()
        self.analysis_controller = AnalysisTabController()
        self.analysis_controller.db = self.db_mock
        self.mock_transaction_controller = MagicMock()
        self.analysis_controller.transaction_controller = self.mock_transaction_controller

    def tearDown(self):
        del self.analysis_controller
    
    def test01_execute(self):
        self.db_mock.get_income_data.return_value = [
            ("test_user", "09/17/2025", "Salary", 6000, "2nd June Salary", "Bi-monthly salary"),
            ("test_user", "09/18/2025", "Bonus", 200, "Extra", "Overtime")
        ]
        result = self.analysis_controller.execute('get_income_data', 'test_user')
        self.assertEqual(result, [
            ("test_user", "09/17/2025", "Salary", 6000, "2nd June Salary", "Bi-monthly salary"),
            ("test_user", "09/18/2025", "Bonus", 200, "Extra", "Overtime")
        ]) 
    
    def test02_get_income_data(self):
        self.db_mock.get_income_data.return_value = [
            ("test_user", "09/17/2025", "Salary", 6000, "2nd June Salary", "Bi-monthly salary"),
            ("test_user", "09/18/2025", "Bonus", 200, "Extra", "Overtime")
        ]
        result = self.analysis_controller.get_income_data('test_user')
        self.assertEqual(result, [
            ("test_user", "09/17/2025", "Salary", 6000 , "2nd June Salary", "Bi-monthly salary"),
            ("test_user", "09/18/2025", "Bonus", 200, "Extra", "Overtime")
        ]) 

    def test03_get_expense_data(self):
        self.db_mock.get_expense_data.return_value = [
            ("test_user", "09/17/2025", "Food", 60, "Burger", "Mcdo"),
            ("test_user", "09/18/2025", "Transport", 20, "Tricycle", "Going Home")
        ]
        result = self.analysis_controller.get_expense_data('test_user')
        self.assertEqual(result, [
            ("test_user", "09/17/2025", "Food", 60, "Burger", "Mcdo"),
            ("test_user", "09/18/2025", "Transport", 20, "Tricycle", "Going Home")
        ]) 
    
    def test04_get_general_transactions(self):
        self.db_mock.get_general_transactions.return_value = [
            (20, "test_user", "09/17/2025", "Income", "Salary", 6000, "2nd June Salary", "Bi-monthly salary"),
            (69, "test_user", "09/18/2025", "Expense", "Transport", 20, "Tricycle", "Going Home")
        ]
        result = self.analysis_controller.get_general_transactions('test_user')
        self.assertEqual(result, [
            (20, "test_user", "09/17/2025", "Income", "Salary", 6000, "2nd June Salary", "Bi-monthly salary"),
            (69, "test_user", "09/18/2025", "Expense", "Transport", 20, "Tricycle", "Going Home")
        ]) 
    
    # mock an opening of a mock file that acts like a real file
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test05_save_transactions_to_csv(self, mock_file):
        self.db_mock.get_general_transactions.return_value = [(69, "test_user", "09/18/2025", "Expense", "Transport", 20, "Tricycle", "Going Home")]
        self.db_mock.get_income_data.return_value = [("test_user", "09/18/2025", "Bonus", 200, "Extra", "Overtime")]
        self.db_mock.get_expense_data.return_value = [("test_user", "09/17/2025", "Food", 60, "Burger", "Mcdo")]

        # use 'with patch...' line to prevent pop-ups from appearing on screen
        # assert that a file was written
        with patch('Controller.messagebox.showinfo'):
            self.analysis_controller.save_transactions_to_csv("test_user")
            mock_file.assert_any_call("test_user.transaction_file.csv", "w", newline="", encoding="utf-8")
            mock_file.assert_any_call("test_user.income_file.csv", "w", newline="", encoding="utf-8")
            mock_file.assert_any_call("test_user.expense.csv", "w", newline="", encoding="utf-8")
    
    # mock an opening of a mock file that acts like a real file
    # specify the data written on the mock file
    @patch('Controller.Controller.validate_date', return_value=True)
    @patch('Controller.Controller.validate_transaction_type', return_value=True)
    @patch('Controller.Controller.validate_amount', return_value=True)
    @patch('Controller.filedialog.askopenfilename', return_value='dummy.csv')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=
           "Date,Transactiontype,Category,Amount,Title,Description\n"
           "17/09/2025,Income,Salary,1000,Extra,Overtime\n")
    @patch('Controller.messagebox.showinfo')
    def test06_load_transaction_to_csv(
        self, mock_msg_info, mock_open_file, mock_askopenfilename, mock_validate_amount,
        mock_validate_transaction_type, mock_validate_date):
        self.analysis_controller.transaction_controller = MagicMock()

        self.analysis_controller.load_transaction_to_csv("test_user")
        self.analysis_controller.transaction_controller.add_transaction.assert_called_once_with(
        "test_user", "2025-09-17", "Income", "Salary", "1000", "Extra", "Overtime")
            


class TestUIController(unittest.TestCase):
    def test01_execute(self):
        mock_entry = MagicMock()
        mock_show_var = MagicMock()
        mock_show_var.get.return_value = True

        # Test toggle_password operation via execute
        UIController.execute('toggle_password', mock_entry, mock_show_var)
        mock_entry.config.assert_called_with(show="")


    def test02_toggle_password(self):
        entry = MagicMock()
        show_var = MagicMock()
        show_var.get.return_value = True  # show password
        UIController.toggle_password(entry, show_var)
        entry.config.assert_called_with(show="")

        show_var.get.return_value = False  # hide password
        UIController.toggle_password(entry, show_var)
        entry.config.assert_called_with(show="*")

    @patch('Controller.Log_In.LogIn')
    @patch('Controller.Tk')
    def test03_valid_logout(self, mock_tk, mock_login):
        window = MagicMock()
        window.winfo_exists.return_value = True # creates new window
        window.tk.call.return_value = ['task1', 'task2']

        UIController.logout(window)

        window.after_cancel.assert_any_call('task1')
        window.after_cancel.assert_any_call('task2')
        window.destroy.assert_called_once()

        mock_tk.assert_called_once()
        mock_login.assert_called_once()
        mock_tk.return_value.mainloop.assert_called_once()

        window = MagicMock()
        window.winfo_exists.return_value = False # test if window not created
        UIController.logout(window)
        window.destroy.assert_not_called()

    @patch('Controller.Frame')
    def test04_switch_tab(self, mock_frame_class):
        settings_handler = MagicMock()
        notif_handler = MagicMock()
        home_instance = MagicMock()
        mock_frame = MagicMock()
        mock_frame_class.return_value = mock_frame = mock_frame
        tab_class = MagicMock(return_value='tab_instance')

        UIController.switch_tab(settings_handler, notif_handler, tab_class, home_instance, "test_user")

        home_instance.clear_all_content.assert_called_once()
        mock_frame.place.assert_called_once_with(x=200, y=112, width=1051, height=621)
        self.assertEqual(home_instance.current_tab, 'tab_instance')
        settings_handler.lift_settings.assert_called_once()
        notif_handler.lift_notification.assert_called_once()


    def test05_toggle_notification(self):
        settings_handler = MagicMock(settings_visible=True) # test when settings visible
        notif_handler = MagicMock()
        UIController.toggle_notification(notif_handler, settings_handler)
        settings_handler.hide_settings.assert_called_once()
        notif_handler.notification.assert_called_once()

        settings_handler = MagicMock(settings_visible=False) # test when settings not visible
        notif_handler = MagicMock()
        UIController.toggle_notification(notif_handler, settings_handler)
        settings_handler.hide_settings.assert_not_called()
        notif_handler.notification.assert_called_once()

    def test06_toggle_settings_when_notif_visible(self):
        notif_handler = MagicMock(notif_visible=True) # test when notification visible
        settings_handler = MagicMock()
        UIController.toggle_settings(notif_handler, settings_handler)
        notif_handler.hide_notification.assert_called_once()
        settings_handler.settings.assert_called_once()

        notif_handler = MagicMock(notif_visible=False) # test when notification not visible
        settings_handler = MagicMock()
        UIController.toggle_settings(notif_handler, settings_handler)
        notif_handler.hide_notification.assert_not_called()
        settings_handler.settings.assert_called_once()

    @patch('Controller.Category_Entry.CategoryEntryForm')
    def test07_switch_category(self, mock_category_entry_form):
        frame = MagicMock()
        mock_category_entry_form.return_value = 'category_entry_instance'

        result = UIController.switch_category(frame, "Food", "test_user", "Income", "categories_tab")

        frame.configure.assert_called_once_with(fg_color="#D7E6C5", bg_color="#9FD39C")
        mock_category_entry_form.assert_called_once_with(frame, "Food", "Income", "test_user", "categories_tab")
        self.assertEqual(result, 'category_entry_instance')



class TestNotificationTabController(unittest.TestCase):
    def setUp(self):
        self.db_mock = MagicMock()
        self.patcher = patch('Controller.DatabaseService.get_instance', return_value=self.db_mock)
        self.mock_get_instance = self.patcher.start()
        self.controller = NotificationTabController()
        

    def tearDown(self):
        self.patcher.stop()
    
    def test01_execute(self):
        self.controller.Notification_Handler = MagicMock()
        self.controller.execute('Notification_Handler', 'test_user', '2025-06-20', '4:00', 'Income')
        self.controller.Notification_Handler.assert_called_once()
    
    def test02_notification_handler_income(self):
        self.controller.Notification_Handler('test_user', '2025-06-20', '4:00', 'Income', 'Salary', 5000)
        self.db_mock.add_notification.assert_called_once_with(
            'test_user', '2025-06-20', '4:00', 'Income', 'Salary',
            'Income Added', 'You received ₱5000 in Salary today. Time to plan your savings!', 5000
        )

    def test03_notification_handler_expense(self):
        self.controller.Notification_Handler('test_user', '2025-06-20', '4:00', 'Expense', 'Food', 300)
        self.db_mock.add_notification.assert_called_once_with(
            'test_user', '2025-06-20', '4:00', 'Expense', 'Food',
            'Expense Added', 'You added ₱300 in Food today. Keep an eye on your budget!', 300
        )

    def test04_get_notification(self):
        self.db_mock.get_data_notification.return_value = ['notif1', 'notif2']
        result = self.controller.Get_Notification('test_user')
        self.assertEqual(result, ['notif1', 'notif2'])

    @patch('Controller.datetime')
    def test05_get_alerts_to_generate_balance_alert(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2025, 6, 20, 12, 0)

        # mock balance less than 10% of income and no alerts yet
        self.db_mock.get_balance.return_value = 90
        self.db_mock.fetch_total_income.return_value = 1000
        self.db_mock.get_data_notification.return_value = []

        #check if balance alert generates
        alerts = self.controller.get_alerts_to_generate("test_user")
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]['message'], "Balance Alert")

    @patch('Controller.datetime')
    def test06_get_alerts_to_generate_negative_balance(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2025, 6, 20, 12, 0)

        # mock negative balance and no alerts yet
        self.db_mock.get_balance.return_value = -50
        self.db_mock.fetch_total_income.return_value = 1000
        self.db_mock.get_data_notification.return_value = []

        #check if balance alert generates
        alerts = self.controller.get_alerts_to_generate("test_user")
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]['message'], "Negative Balance Alert")

    @patch('Controller.datetime')
    def test07_get_alerts_to_generate_with_conditions(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2025, 6, 20, 12, 0)

        # mock no alerts yet
        self.db_mock.get_balance.return_value = 1000
        self.db_mock.fetch_total_income.return_value = 5000
        self.db_mock.get_data_notification.return_value = []

        # mock having a condition
        alerts = self.controller.get_alerts_to_generate("test_user", conditions=True)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]['message'], "Transaction Edit")


class TestController(unittest.TestCase):
    def setUp(self):
        # Patch all internal controllers
        self.user_controller_patch = patch.object(Controller, '_user_controller', autospec=True)
        self.transaction_controller_patch = patch.object(Controller, '_transaction_controller', autospec=True)
        self.ui_controller_patch = patch.object(Controller, '_ui_controller', autospec=True)
        self.analysis_controller_patch = patch.object(Controller, '_analysis_controller', autospec=True)
        self.notification_controller_patch = patch.object(Controller, '_NotificationTabController', autospec=True)
        self.validator_patch = patch.object(Controller, '_Validate_Inputs', autospec=True)

        self.mock_user = self.user_controller_patch.start()
        self.mock_transaction = self.transaction_controller_patch.start()
        self.mock_ui = self.ui_controller_patch.start()
        self.mock_analysis = self.analysis_controller_patch.start()
        self.mock_notif = self.notification_controller_patch.start()
        self.mock_validate = self.validator_patch.start()

        self.addCleanup(patch.stopall)

    def test01_authenticate_user(self):
        Controller.authenticate_user('test_user', 'test_pass')
        self.mock_user.authenticate.assert_called_once_with('test_user', 'test_pass')

    def test02_register_user(self):
        Controller.register_user('test_user', 'test_pass')
        self.mock_user.register.assert_called_once_with('test_user', 'test_pass')
    
    def test03_toggle_password(self):
        entry, var = MagicMock(), MagicMock()
        Controller.toggle_password(entry, var)
        self.mock_ui.toggle_password.assert_called_once_with(entry, var)
    
    def test04_logout_user(self):
        win = MagicMock()
        Controller.logout_user(win)
        self.mock_ui.logout.assert_called_once_with(win)
    
    def test05_add_transaction(self):
        Controller.add_transaction("u", "d", "t", "c", "a", "ti", "de")
        self.mock_transaction.add_transaction.assert_called_once()
    
    def test06_get_balance(self):
        Controller.get_balance("u")
        self.mock_transaction.get_balance.assert_called_once_with("u")

    def test07_update_password(self):
        Controller.update_password('test_user', 'newpass')
        self.mock_user.update_password.assert_called_once_with('test_user', 'newpass')

    def test08_delete_account(self):
        Controller.delete_account('test_user')
        self.mock_user.delete_account.assert_called_once_with('test_user', None)
    
    def test09_switch_tab(self):
        Controller.switch_tab("s", "n", "tab", "home", "user")
        self.mock_ui.switch_tab.assert_called_once_with("s", "n", "tab", "home", "user")

    def test10_toggle_notification(self):
        Controller.toggle_notification("n", "s")
        self.mock_ui.toggle_notification.assert_called_once_with("n", "s")

    def test11_toggle_settings(self):
        Controller.toggle_settings("n", "s")
        self.mock_ui.toggle_settings.assert_called_once_with("n", "s")

    def test12_switch_category(self):
        Controller.switch_category("frame", "cat", "user", "t_type", "tab")
        self.mock_ui.switch_category.assert_called_once_with("frame", "cat", "user", "t_type", "tab")

    def test13_get_income(self):
        Controller.get_income("u")
        self.mock_transaction.get_income.assert_called_once_with("u")

    def test14_get_expense(self):
        Controller.get_expense("u")
        self.mock_transaction.get_expense.assert_called_once_with("u")

    def test15_get_password(self):
        Controller.get_password('test_user')
        self.mock_user.get_password.assert_called_once_with('test_user')

    def test16_get_income_data(self):
        Controller.get_income_data("u")
        self.mock_analysis.get_income_data.assert_called_once_with("u")

    def test17_get_expense_data(self):
        Controller.get_expense_data("u")
        self.mock_analysis.get_expense_data.assert_called_once_with("u")

    def test18_get_general_transactions(self):
        Controller.get_general_transactions("u")
        self.mock_analysis.get_general_transactions.assert_called_once_with("u")

    def test19_save_transactions_to_csv(self):
        Controller.save_transactions_to_csv("u")
        self.mock_analysis.save_transactions_to_csv.assert_called_once_with("u")

    def test20_load_transaction_to_csv(self):
        Controller.load_transaction_to_csv("u")
        self.mock_analysis.load_transaction_to_csv.assert_called_once_with("u")

    def test21_Notification_Handler(self):
        Controller.Notification_Handler("u", "d", "t", "tt", "c", 100, "m", "desc")
        self.mock_notif.Notification_Handler.assert_called_once()

    def test22_Get_Notification(self):
        Controller.Get_Notification("u")
        self.mock_notif.Get_Notification.assert_called_once_with("u")

    def test23_get_alerts_to_generate(self):
        Controller.get_alerts_to_generate("u", conditions=True)
        self.mock_notif.get_alerts_to_generate.assert_called_once_with("u", conditions=True)

    def test24_validate_date(self):
        Controller.validate_date("2025-06-20")
        self.mock_validate.validate_date.assert_called_once_with("2025-06-20")

    def test25_validate_amount(self):
        Controller.validate_amount("100")
        self.mock_validate.validate_amount.assert_called_once_with("100")

    def test26_sort_transaction(self):
        Controller.sort_transaction("u")
        self.mock_transaction.sort_transaction.assert_called_once_with("u")

    def test27_edit_transaction(self):
        Controller.edit_transaction(1, "u", "d", "c", "t", 100, "ti", "desc")
        self.mock_transaction.edit_transaction.assert_called_once()

    def test28_validate_category(self):
        Controller.validate_category("Salary", "Income")
        self.mock_validate.validate_category.assert_called_once_with("Salary", "Income")

    def test29_validate_transaction_type(self):
        Controller.validate_transaction_type("Income")
        self.mock_validate.validate_transaction_type.assert_called_once_with("Income")



if __name__ == '__main__':
    unittest.main(verbosity=2)