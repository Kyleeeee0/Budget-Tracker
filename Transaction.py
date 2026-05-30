from pathlib import Path
from tkinter import *
import customtkinter as ctk
import Controller
from PIL import Image, ImageTk
from Analysis import BaseTab

ASSETS_PATH = Path(__file__).parent / "assets" / "assets_transaction"

class TransactionTab(BaseTab):
    
    def __init__(self, main_window, username):
        super().__init__(main_window, username)
        self._initialize_ui()

    @property
    def username(self):
        return self._username
    
    def _initialize_ui(self):
        self._frame = Frame(self.main_window, bg="#F4F4F4")
        self._frame.place(x=0, y=0, width=1051, height=621)

        self.frame_canvas = Canvas(
            self._frame,
            bg="#F4F4F4",
            height=621,
            width=1051,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.frame_canvas.place(x=0, y=0)
        self._images = {}
        self._current_view = None
        self._load_content()

    @property
    def frame(self):
        return self._frame

    @property
    def images(self):
        return self._images

    @property
    def current_view(self):
        return self._current_view

    @current_view.setter
    def current_view(self, view):
        self._current_view = view

    def _load_content(self):
        self._create_main_container()
        self._create_section_labels()
        self._load_ui_images()
        self._setup_transaction_display()
        self._create_balance_display()
        self._create_view_switcher()
        self._load_default_category_view()

    def _create_main_container(self):
        """Create the main container frame"""
        self.transaction_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=26,
            width=1002,
            height=565,
            fg_color="#9FD39C",
            bg_color="#F4F4F4"
        )
        self.transaction_frame.place(x=26, y=27)

    def _create_section_labels(self):
        """Create section labels"""
        transaction_label = ctk.CTkLabel(
            self.transaction_frame,
            text="Transaction",
            font=("Poppins", 20, "bold")
        )
        transaction_label.place(x=35, y=20)

    def _load_ui_images(self):
        self.images['income_frame'] = self._load_tk_image("income_frame.png")
        self.images['expense_frame'] = self._load_tk_image("expense_frame.png")

    def _load_tk_image(self, image_name):
        img_path = ASSETS_PATH / image_name
        img = Image.open(img_path)
        return ImageTk.PhotoImage(img)

    def _setup_transaction_display(self):
        self.transaction_display_frame = ctk.CTkScrollableFrame(
            self.transaction_frame,
            corner_radius=26,
            width=410,
            height=450,
            fg_color="#DFF7E2",
            bg_color="#9FD39C"
        )
        self.transaction_display_frame.place(x=535, y=33)

    def _create_balance_display(self):
        """Create the balance display section"""
        self.balance_frame = ctk.CTkFrame(
            self.transaction_frame,
            corner_radius=14,
            width=430,
            height=90,
            fg_color="#F1FFF3"
        )
        self.balance_frame.place(x=57, y=130)
        
        ctk.CTkLabel(
            self.balance_frame, 
            text="Total Balance", 
            font=("Inter Medium", 17)
        ).place(relx=0.5, rely=0.28, anchor="center")
        
        self.balance_value = ctk.CTkLabel(
            self.balance_frame,
            text=Controller.Controller.get_balance(self.username),
            font=("Arial Black", 26)
        )
        self.balance_value.place(relx=0.5, rely=0.6, anchor="center")

    def _create_view_switcher(self):
        """Create the income/expense view switcher"""
        self.switcher_frame = ctk.CTkFrame(
            self.transaction_frame,
            corner_radius=14,
            width=430,
            height=50,
            fg_color="#F1FFF3"
        )
        self.switcher_frame.place(x=57, y=261)

        self.selected_frame = ctk.CTkFrame(
            self.switcher_frame,
            corner_radius=26,
            width=130,
            height=39,
            fg_color="#9FD39C"
        )
        self.selected_frame.place(x=41, y=8)

        self.income_label = ctk.CTkLabel(
            self.switcher_frame,
            text="Income",
            font=("Poppins", 17),
            bg_color="#9FD39C"
        )
        self.income_label.place(x=80, y=12)
        self.income_label.bind("<Button-1>", lambda e: self._switch_to_income_view())
        
        self.expense_label = ctk.CTkLabel(
            self.switcher_frame,
            text="Expense",
            font=("Poppins", 17)
        )
        self.expense_label.place(x=300, y=12)
        self.expense_label.bind("<Button-1>", lambda e: self._switch_to_expense_view())

        for label in [self.income_label, self.expense_label]:
            label.bind("<Enter>", lambda e: self.main_window.config(cursor="hand2"))
            label.bind("<Leave>", lambda e: self.main_window.config(cursor=""))

    def _load_default_category_view(self):
        """Load the default category view (income)"""
        self.selected_frame.place(x=41, y=5)
        
        self.income_image = Label(
            self.transaction_frame,
            text=Controller.Controller.get_income(self.username),
            image=self.images['income_frame'],
            font=("Poppins", 20 * -1, "bold"),
            compound="center",
            bg="#9FD39C"
        )
        self.income_image.place(x=57, y=340)

        self.expense_image = Label(
            self.transaction_frame,
            text=Controller.Controller.get_expense(self.username),
            image=self.images['expense_frame'],
            font=("Poppins", 20 * -1, "bold"),
            compound="center",
            bg="#9FD39C"
        )
        self.expense_image.place(x=289, y=340)

        self.separator_line = ctk.CTkFrame(
            self.transaction_frame,
            width=3,
            height=106.5,
            fg_color="#DFF7E2"
        )
        self.separator_line.place(x=272, y=335)

        self._load_category_data("Income")

    def _switch_to_income_view(self):
        """Switch the view to show income categories"""
        self._update_view_switcher_position(is_income=True)
        self._load_category_data("Income")

    def _switch_to_expense_view(self):
        """Switch the view to show expense categories"""
        self._update_view_switcher_position(is_income=False)
        self._load_category_data("Expense")

    def _update_view_switcher_position(self, is_income):
        """Update the switcher position based on current view"""
        x_pos = 41 if is_income else 265
        self.selected_frame.place(x=x_pos, y=5)
        self.income_label.configure(bg_color="#9FD39C" if is_income else "#F1FFF3")
        self.expense_label.configure(bg_color="#9FD39C" if not is_income else "#F1FFF3")

    def _load_category_data(self, view_type):
        if view_type == "Income":
            self.current_view = self.Transaction_Income()
        else:
            self.current_view = self.Transaction_Expense()

    def clear_all_content(self):
        for widget in self.transaction_display_frame.winfo_children():
            widget.destroy()

    def Transaction_Income(self):
        self.clear_all_content()
        existing = Controller.Controller.get_income_data(self.username)
        for notif in reversed(existing):
            if len(notif) >= 5:
                date, category, amount, title, description = notif[1:]
                self.show_transaction_frame(date, "Income", category, amount, title, description)

    def Transaction_Expense(self):
        self.clear_all_content()
        existing = Controller.Controller.get_expense_data(self.username)
        for notif in reversed(existing):
            if len(notif) >= 5:
                date, category, amount, title, description = notif[1:]
                self.show_transaction_frame(date, "Expense", category, amount, title, description)

    def show_transaction_frame(self, date, transaction_type, category, amount, title, description):
        frame = ctk.CTkFrame(self.transaction_display_frame, width=400, height=80, fg_color="#DFF7E2", bg_color="#DFF7E2")
        frame.pack(pady=10)

        ctk.CTkLabel(
            frame,
            text=f"{date}   •   {transaction_type} - {category}",
            font=("Segoe UI", 14, "bold"),
            text_color="black"
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            frame,
            text=f"₱{amount:,.2f}   •   {title}",
            font=("Segoe UI", 14),
            text_color="#1C6B34"
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))

        ctk.CTkLabel(
            frame,
            text=f"{description}",
            font=("Segoe UI", 14),
            wraplength=360,
            justify="left",
            text_color="black"
        ).grid(row=2, column=0, sticky="w", pady=(2, 0))

        ctk.CTkFrame(self.transaction_display_frame, 
                     width=400, 
                     height=3, 
                     fg_color="#9FD39C",
                ).pack()

    def update_financial_displays(self):
        """Update all financial displays"""
        self.balance_value.configure(text=Controller.Controller.get_balance(self.username))
        self.income_image.configure(text=Controller.Controller.get_income(self.username))
        self.expense_image.configure(text=Controller.Controller.get_expense(self.username))

