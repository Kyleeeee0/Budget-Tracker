from pathlib import Path
import customtkinter as ctk
from PIL import Image
import Controller
import Category_Income
import Category_Expense

ASSETS_PATH = Path(__file__).parent / "assets" / "assets_categories_income"

class CategoriesTab:
    def __init__(self, main_window, username):
        self._main_window = main_window
        self._username = username
        self._images = {}
        self._current_view = None
        
        self._create_main_container()
        self._create_balance_section()
        self._create_category_switcher()
        self._create_category_display_area()
        
        self._load_images()
        self._load_default_view()

    @property
    def main_window(self):
        return self._main_window

    @property
    def username(self):
        return self._username

    @property
    def images(self):
        return self._images

    @property
    def current_view(self):
        return self._current_view

    @current_view.setter
    def current_view(self, view):
        self._current_view = view

    def _create_main_container(self):
        """Create the main frame container"""
        self.main_frame = ctk.CTkFrame(
            self.main_window,
            corner_radius=26,
            width=1002,
            height=565,
            fg_color="#9FD39C"
        )
        self.main_frame.place(x=26, y=27)

    def _load_images(self):
        """Load all required images"""
        # Load income/expense frames
        self.images['income_frame'] = self._load_ctk_image("income_frame.png", (198, 95))
        self.images['expense_frame'] = self._load_ctk_image("expense_frame.png", (198, 95))

    def _load_ctk_image(self, image_name, size):
        """Helper to load CTk compatible images"""
        img = Image.open(ASSETS_PATH / image_name)
        return ctk.CTkImage(img, size=size)

    def _create_balance_section(self):
        """Create the balance display section"""
        self.balance_frame = ctk.CTkFrame(
            self.main_frame,
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

    def _create_category_switcher(self):
        """Create the income/expense toggle switcher"""
        self.switcher_frame = ctk.CTkFrame(
            self.main_frame,
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
        self.income_label.bind("<Button-1>", lambda e: self.show_income_view())
        
        self.expense_label = ctk.CTkLabel(
            self.switcher_frame,
            text="Expense",
            font=("Poppins", 17)
        )
        self.expense_label.place(x=300, y=12)
        self.expense_label.bind("<Button-1>", lambda e: self.show_expense_view())

        for label in [self.income_label, self.expense_label]:
            label.bind("<Enter>", lambda e: self.main_window.config(cursor="hand2"))
            label.bind("<Leave>", lambda e: self.main_window.config(cursor=""))

    def _create_category_display_area(self):
        self.Income_Expense_Frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=26,
            width=440,
            height=500,
            fg_color="#DFF7E2",
            bg_color="#9FD39C"
        )
        self.Income_Expense_Frame.place(x=535, y=33)

    def _load_default_view(self):
        """Load the default income view with images"""
        self.selected_frame.place(x=41, y=5)
        
        self.income_image = ctk.CTkLabel(
            self.main_frame,
            text=Controller.Controller.get_income(self.username),
            image=self.images['income_frame'],
            font=("Poppins", 20, "bold"),
            compound="center"
        )
        self.income_image.place(x=57, y=340)

        self.expense_image = ctk.CTkLabel(
            self.main_frame,
            text=Controller.Controller.get_expense(self.username),
            image=self.images['expense_frame'],
            font=("Poppins", 20, "bold"),
            compound="center"
        )
        self.expense_image.place(x=289, y=340)

        self.line = ctk.CTkFrame(
            self.main_frame,
            width=3,
            height=106.5,
            fg_color="#DFF7E2"
        )
        self.line.place(x=272, y=335)

        self._load_category_view("Income")

    def show_income_view(self):
        self._update_switcher_state(is_income=True)
        self._load_category_view("Income")

    def show_expense_view(self):
        self._update_switcher_state(is_income=False)
        self._load_category_view("Expense")

    def _update_switcher_state(self, is_income):
        x_pos = 41 if is_income else 265
        self.selected_frame.place(x=x_pos, y=5)
        self.income_label.configure(bg_color="#9FD39C" if is_income else "#F1FFF3")
        self.expense_label.configure(bg_color="#9FD39C" if not is_income else "#F1FFF3")
        self.Income_Expense_Frame.configure(fg_color="#DFF7E2")
        
    def _load_category_view(self, view_type):
        """Load the appropriate category view"""
        if self.current_view:
            self.current_view.clear_all_content()
        
        if view_type == "Income":
            self.current_view = Category_Income.IncomeCategoryView(
                self.Income_Expense_Frame,
                self.username,
                self
            )
        else:
            self.current_view = Category_Expense.ExpenseCategoryView(
                self.Income_Expense_Frame,
                self.username,
                self
            )

    def update_balance_labels(self):
        """Update all balance-related displays"""
        self.balance_value.configure(text=Controller.Controller.get_balance(self.username))
        self.income_image.configure(text=Controller.Controller.get_income(self.username))
        self.expense_image.configure(text=Controller.Controller.get_expense(self.username))













