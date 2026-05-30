from pathlib import Path
from tkinter import *
import customtkinter as ctk
from datetime import datetime
from PIL import ImageTk, Image
import Notification, Settings, Analysis, Transaction, Categories
import Controller
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

ASSETS_PATH = Path(__file__).parent / "assets" / "assets_home"

class Home:
    def __init__(self, main_window, username):
        self._main_window = main_window
        self._username = username
        self._setup_window()
        self._initialize_components()
        self.open_home_new_window()

    @property
    def main_window(self):
        return self._main_window

    @property
    def username(self):
        return self._username

    @property
    def images(self):
        """Encapsulated access to images dictionary."""
        return self._images

    def _setup_window(self):
        """Encapsulated window setup logic"""
        self.main_window.title("Budget Tracker")
        self.main_window.configure(bg="#FFFFFF")
        self.main_window.resizable(False, False)
        
        # Center window
        window_width = 1250
        window_height = 750
        y_offset = -40
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2) + y_offset
        self.main_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def _initialize_components(self):
        """Initialize all components (Encapsulation)"""
        self._images = {}
        self.current_tab = None
        self.interactive_ID = []
        self.home_frame = None
        self.current_tab_frame = None
        
        # Initialize handlers
        self.notification_handler = Notification.NotificationHandler(self.main_window, self.username)
        self.settings_handler = Settings.SettingsHandler(self.main_window, self.username)

    def open_home_new_window(self):
        """Create the main home window (Abstraction)"""
        self._create_canvas()
        self._create_layout()
        self._load_ui_elements()
        self._start_auto_refresh()

    def _create_canvas(self):
        """Create main canvas"""
        self.canvas = Canvas(
            self.main_window,
            bg="#F4F4F4",
            height=1250,
            width=750,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.pack(fill="both", expand=True)

    def _create_layout(self):
        """Create the basic layout structure"""
        self.canvas.create_rectangle(0.0, 0.0, 200.0, 750.0, fill="#D7E6C5", outline="")
        self.canvas.create_rectangle(200.0, 0.0, 1251.0, 112.0, fill="#D7E6C5", outline="")
        
        self._create_home_frame()
        self._create_text_elements()

    def _create_home_frame(self):
        """Create the main content frame"""
        self.home_frame = Frame(self.main_window, bg="#F4F4F4")
        self.home_frame.place(x=200, y=112, width=1051, height=621)

        self.bg_canvas = Canvas(
            self.home_frame,
            bg="#F4F4F4", 
            height=621,
            width=1051,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.bg_canvas.place(x=0, y=0)

    def _create_text_elements(self):
        """Create all text elements"""
        self.canvas.create_text(32.0, 38.0, anchor="nw", text="Hi, Welcome Back", 
                              fill="#052224", font=("Poppins", 27 * -1, "bold"))
        self.text_id = self.canvas.create_text(32.0, 75, anchor="nw", text=self.update_greetings(), 
                              fill="#052224", font=("LeagueSpartan", 21 * -1, "normal"))

    def update_greetings(self):
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "Good Morning"
        elif 12 <= hour < 18:
            return "Good Afternoon"
        else:
            return "Good Evening"
        
    def refresh_greeting(self):
        self.canvas.itemconfig(self.text_id, text=self.update_greetings())
        self.main_window.after(60000, self.refresh_greeting)

    def _load_ui_elements(self):
        """Load all UI elements"""
        self._load_images()
        self._create_frames()
        self._create_navigation_buttons()
        self._create_interactive_elements()
        self._transaction_scrollable_frame()
        self._content_transaction()
        self._content_analysis()

    def _load_images(self):
        """Load image assets"""
        self.images["container.png"] = PhotoImage(file=ASSETS_PATH / "container.png")
        self.canvas.create_image(1139.0, 59.0, image=self.images["container.png"])

        self.images['income_button'] = self._load_tk_image("income_button.png")
        self.images['expense_button'] = self._load_tk_image("expense_button.png")

    def _load_tk_image(self, image_name):
        """Load images using ImageTk for tkinter without resizing"""
        img_path = ASSETS_PATH / image_name
        img = Image.open(img_path)
        return ImageTk.PhotoImage(img)

    def _create_frames(self):
        """Create content frames"""
        self.Analysis_Frame = ctk.CTkFrame(
            self.home_frame,
            corner_radius=26,
            width=490,
            height=565,
            fg_color="#9FD39C",
            bg_color="#F4F4F4"
        )
        self.Analysis_Frame.place(x=26, y=22)

        self.Transaction_Frame = ctk.CTkFrame(
            self.home_frame,
            corner_radius=26,
            width=490,
            height=565,
            fg_color="#9FD39C",
            bg_color="#F4F4F4"
        )
        self.Transaction_Frame.place(x=536, y=22)

        # Using CTkLabel for consistency
        self.analysis_title = ctk.CTkLabel(
            self.Analysis_Frame,
            text="Analysis",
            font=("Poppins", 22, "bold"),
            text_color="#052224",
            bg_color="#9FD39C"
        )
        self.analysis_title.place(x=26, y=15)

        self.transaction_title = ctk.CTkLabel(
            self.Transaction_Frame,
            text="Transaction",
            font=("Poppins", 22, "bold"),
            text_color="#052224",
            bg_color="#9FD39C"
        )
        self.transaction_title.place(x=27, y=15) 

    def _create_navigation_buttons(self):
        """Create sidebar navigation buttons"""
        button_specs = [
            ("button_home.png", self.on_click_home, (1.0, 153.0)),
            ("button_analysis.png", self.on_click_analysis, (1.0, 233.0)),
            ("button_transaction.png", self.on_click_transaction, (1.0, 311.0)),
            ("button_categories.png", self.on_click_categories, (1.0, 389.0))
        ]

        for img_file, command, pos in button_specs:
            self.images[img_file] = PhotoImage(file=ASSETS_PATH / img_file)
            button = Button(
                image=self.images[img_file],
                borderwidth=0,
                highlightthickness=0,
                activebackground="#D7E6C5",
                activeforeground="#9FD39C",
                command=command,
                relief="flat"
            )
            button.place(x=pos[0], y=pos[1], width=199.0, height=70.0)

    def _create_interactive_elements(self):
        """Create interactive UI elements"""
        # Notification button
        self.images["notification"] = PhotoImage(file=ASSETS_PATH / "notification.png")
        notification = self.canvas.create_image(1109.0, 58.0, image=self.images["notification"])
        
        # Settings button
        self.images["settings"] = PhotoImage(file=ASSETS_PATH / "settings.png")
        settings = self.canvas.create_image(1168.0, 58.0, image=self.images["settings"])

        # Bind click events
        self.canvas.tag_bind(notification, "<Button-1>", lambda e: self.on_click_notification())
        self.canvas.tag_bind(settings, "<Button-1>", lambda e: self.on_click_settings())

        # Bind hover effects
        for element in [notification, settings]:
            self.canvas.tag_bind(element, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
            self.canvas.tag_bind(element, "<Leave>", lambda e: self.canvas.config(cursor=""))

    def clear_all_content(self):
        """Clear all dynamic content (Encapsulation)"""
        if self.home_frame and self.home_frame.winfo_exists():
            self.home_frame.place_forget()

        if self.current_tab_frame and self.current_tab_frame.winfo_exists():
            self.current_tab_frame.destroy()
            self.current_tab_frame = None

        if self.current_tab:
            if hasattr(self.current_tab, 'cleanup'):
                self.current_tab.cleanup()
            self.current_tab = None

        # Ensure handlers are in correct state
        self.settings_handler.lift_settings()
        self.notification_handler.lift_notification()

    def show_home(self):
        """Show the home view (Abstraction)"""
        self.clear_all_content()
        
        if not self.home_frame or not self.home_frame.winfo_exists():
            self._create_home_frame()
            self._create_frames()
            self._transaction_scrollable_frame()
            self._content_transaction()
            self._content_analysis()

        self.home_frame.place(x=200, y=112, width=1051, height=621)

    def on_click_home(self):
        self.show_home()

    def on_click_analysis(self):
        Controller.Controller.switch_tab(
            self.settings_handler, 
            self.notification_handler, 
            Analysis.AnalysisTab, 
            self, 
            self.username
        )

    def on_click_transaction(self):
        Controller.Controller.switch_tab(
            self.settings_handler,
            self.notification_handler,
            Transaction.TransactionTab,
            self,
            self.username
        )

    def on_click_categories(self):
        Controller.Controller.switch_tab(
            self.settings_handler,
            self.notification_handler,
            Categories.CategoriesTab,
            self,
            self.username
        )

    def on_click_notification(self):
        Controller.Controller.toggle_notification(self.notification_handler, self.settings_handler)

    def on_click_settings(self):
        Controller.Controller.toggle_settings(self.notification_handler, self.settings_handler)

    # =============================================================================================================================================== #

    def clear_frame_content(self):
        """Clear the content inside the balance_frame"""
        for widget in self.balance_frame.winfo_children():
            widget.destroy()

    def _delete_contents_scrollable_frame(self):
        for widget in self.transaction_display_frame.winfo_children():
            widget.destroy()

    def _transaction_scrollable_frame(self):
        self.transaction_display_frame = ctk.CTkScrollableFrame(
            self.Transaction_Frame,
            corner_radius=26,
            width=410,
            height=440,
            fg_color="#DFF7E2",
            bg_color="#9FD39C"
        )
        self.transaction_display_frame.place(x=25, y=55)

    def _content_transaction(self):
        self._delete_contents_scrollable_frame()
        transaction = Controller.Controller.get_general_transactions(self.username)
        for notif in reversed(transaction):
            if len(notif) >= 8:
                id, username, date, transaction_type, category, amount, title, description = notif[:]
                self._show_transaction_frame(id, date, transaction_type, category, amount, title, description)

    def _show_transaction_frame(self, id, date, transaction_type, category, amount, title, description):
        self.frame = ctk.CTkFrame(self.transaction_display_frame, width=400, height=80, fg_color="#DFF7E2", bg_color="#DFF7E2")
        self.frame.pack(pady=10)

        self.edit_button = ctk.CTkButton(self.frame, width=50, height=50, 
                                         fg_color="#9FD39C", 
                                         bg_color="#DFF7E2",
                                         font=("Segoe UI", 14, "bold"),
                                         text="Edit Transaction",
                                         command= lambda c=id: self._show_transaction_entry(c))
        self.edit_button.pack(side="right", padx=5)

        ctk.CTkLabel(
            self.frame,
            text=f"{date}   •   {transaction_type} - {category}   ",
            font=("Segoe UI", 14, "bold"),
            text_color="black"
        ).pack(anchor="w", padx=12, pady=(6, 2))

        ctk.CTkLabel(
            self.frame,
            text=f"₱{amount:,.2f}   •   {title}     ",
            font=("Segoe UI", 14),
            text_color="#1C6B34",
            wraplength=300
        ).pack(anchor="w", padx=12, pady=(6, 2))

        ctk.CTkLabel(
            self.frame,
            text=f"{description}     ",
            font=("Segoe UI", 14),
            wraplength=200,
            justify="left",
            text_color="black"
        ).pack(anchor="w", padx=12, pady=(6, 2))

        ctk.CTkFrame(self.transaction_display_frame, 
                     width=400, 
                     height=3, 
                     fg_color="#9FD39C",
                ).pack()

    def _show_transaction_entry(self, id):
        from transaction_entry import TransactionEntryForm

        self._delete_contents_scrollable_frame()
        
        print(id)
        self.transaction_display_frame._parent_canvas.yview_moveto(0)
        TransactionEntryForm(
            parent_frame=self.transaction_display_frame,
            id=id,
            username=self.username,
            transaction_tab_instance=self
        )

    def refresh_transactions(self):
        """Public method to refresh transaction display"""
        if hasattr(self, 'transaction_display_frame') and self.transaction_display_frame.winfo_exists():
            self._content_transaction()

    def _start_auto_refresh(self):
        """Start automatic refresh of transactions"""
        self._auto_refresh_transactions()

    def _auto_refresh_transactions(self):
        """Automatically refresh transactions every 2 seconds"""
        if hasattr(self, 'transaction_display_frame') and self.transaction_display_frame.winfo_exists():
            current_transactions = Controller.Controller.get_general_transactions(self.username)
            if not hasattr(self, '_last_transaction_count'):
                self._last_transaction_count = len(current_transactions)
            elif len(current_transactions) != self._last_transaction_count:
                self._content_transaction()
                self._last_transaction_count = len(current_transactions)
        
        self.main_window.after(2000, self._auto_refresh_transactions)

    def _content_analysis(self):
        self.balance_frame = ctk.CTkFrame(
            self.Analysis_Frame,
            corner_radius=26,
            width=440,
            height=400,
            fg_color="#DFF7E2"
        )
        self.balance_frame.place(x=26, y=53)

        self.income_button = Button(
            self.Analysis_Frame,
            image=self.images['income_button'],
            bd=0,
            bg="#9FD39C",
            activebackground="#9FD39C",
            relief="flat",
            command=self.Bar_Graph_Income
        )
        self.income_button.place(x=19, y=460)

        self.expense_button = Button(
            self.Analysis_Frame,
            image=self.images['expense_button'],
            bd=0,
            bg="#9FD39C",
            activebackground="#9FD39C",
            relief="flat",
            command=self.Bar_Graph_Expense
        )
        self.expense_button.place(x=248, y=460)

    def Bar_Graph_Income(self):
        self.clear_frame_content()

        income_data = Controller.Controller.get_income_data(self.username)

        category_totals = {}
        for record in income_data:
            category = record[2]
            amount = record[3]
            category_totals[category] = category_totals.get(category, 0) + amount

        if not category_totals:
            no_data_label = ctk.CTkLabel(
                self.balance_frame,
                text="No income data available",
                font=("Poppins", 14)
            )
            no_data_label.place(relx=0.5, rely=0.5, anchor="center")
            return

        categories = list(category_totals.keys())
        amounts = list(category_totals.values())

        fig, ax = plt.subplots(figsize=(5, 3.5))
        fig.patch.set_facecolor('#DFF7E2')
        ax.set_facecolor('#DFF7E2')

        bars = ax.bar(categories, amounts, color='#9fd39c', edgecolor='#7fbf7f', linewidth=1)
        ax.set_title('Income Sources', fontsize=12, fontweight='bold', pad=10)
        ax.set_ylabel('Amount', fontsize=10)
        ax.tick_params(axis='x', rotation=45, labelsize=8)
        ax.tick_params(axis='y', labelsize=8)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(amounts)*0.01,
                    f'₱{height:,.0f}', ha='center', va='bottom', fontsize=8)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self.balance_frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=10, y=10, width=420, height=380)
        plt.close(fig)

    def Bar_Graph_Expense(self):
        self.clear_frame_content()

        expense_data = Controller.Controller.get_expense_data(self.username)

        category_totals = {}
        for record in expense_data:
            category = record[2]
            amount = record[3]
            category_totals[category] = category_totals.get(category, 0) + amount

        if not category_totals:
            no_data_label = ctk.CTkLabel(
                self.balance_frame,
                text="No expense data available",
                font=("Poppins", 14)
            )
            no_data_label.place(relx=0.5, rely=0.5, anchor="center")
            return

        categories = list(category_totals.keys())
        amounts = list(category_totals.values())

        fig, ax = plt.subplots(figsize=(5, 3.5))
        fig.patch.set_facecolor('#DFF7E2')
        ax.set_facecolor('#DFF7E2')

        bars = ax.bar(categories, amounts, color='#9fd39c', edgecolor='#7fbf7f', linewidth=1)
        ax.set_title('Expense Sources', fontsize=12, fontweight='bold', pad=10)
        ax.set_ylabel('Amount', fontsize=10)
        ax.tick_params(axis='x', rotation=45, labelsize=8)
        ax.tick_params(axis='y', labelsize=8)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(amounts)*0.01,
                    f'₱{height:,.0f}', ha='center', va='bottom', fontsize=8)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self.balance_frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=10, y=10, width=420, height=380)
        plt.close(fig)

    