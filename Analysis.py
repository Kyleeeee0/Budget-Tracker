from pathlib import Path
from tkinter import Frame, Canvas, Button, Label
from PIL import Image, ImageTk
import customtkinter as ctk
import Controller
from abc import ABC, abstractmethod
import Analysis_Income_Charts, Analysis_Expense_Charts

ASSETS_PATH = Path(__file__).parent / "assets" / "assets_analysis"

class BaseTab(ABC):
    """Abstract base class for all tabs (Abstraction)"""
    def __init__(self, main_window, username):
        self._main_window = main_window
        self._username = username
        self._images = {}
        self._current_view = None
        self._initialize_ui()
        
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

    @abstractmethod
    def _initialize_ui(self):
        """Initialize the UI components"""
        pass

    @abstractmethod
    def _load_content(self):
        """Load the tab content"""
        pass

    def clear_frame_content(self):
        """Clear the content inside the Income_Expense_Frame"""
        for widget in self.Income_Expense_Frame.winfo_children():
            widget.destroy()

class AnalysisTab(BaseTab):
    """Analysis tab implementation (Inheritance)"""
    def _initialize_ui(self):
        """Initialize the analysis tab UI (Encapsulation)"""
        self.frame = Frame(self.main_window, bg="#F4F4F4")
        self.frame.place(x=0, y=0, width=1051, height=621)

        self.frame_canvas = Canvas(
            self.frame,
            bg="#F4F4F4",
            height=621,
            width=1051,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.frame_canvas.place(x=0, y=0)
        self._load_content()

    def _load_content(self):
        """Load analysis tab content (Encapsulation)"""
        self._create_frames()
        self._create_labels()
        self._create_balance_section()
        self._create_analysis_switcher()
        self._load_images()
        self._create_analysis_display_area()
        self._load_default_view()

    def _load_images(self):
        """Load all required images without resizing"""
        self.images['bar_graph'] = self._load_tk_image("bar_graph.png")
        self.images['pie_chart'] = self._load_tk_image("pie_chart.png")
        self.images['income_frame'] = self._load_tk_image("income_frame.png")
        self.images['expense_frame'] = self._load_tk_image("expense_frame.png")
        self.images['save_file'] = self._load_tk_image("save_file.png")
        self.images['load_file'] = self._load_tk_image("load_file.png")

    def _load_tk_image(self, image_name):
        """Load images using ImageTk for tkinter without resizing"""
        img_path = ASSETS_PATH / image_name
        img = Image.open(img_path)
        return ImageTk.PhotoImage(img)

    def _create_frames(self):
        """Create the analysis frames"""
        self.analysis_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=26,
            width=490,
            height=570,
            fg_color="#9FD39C",
            bg_color="#F4F4F4"
        )
        self.analysis_frame.place(x=26, y=37)

        self.analysis_frame_1 = ctk.CTkFrame(
            self.frame,
            corner_radius=26,
            width=490,
            height=570,
            fg_color="#9FD39C",
            bg_color="#F4F4F4"
        )
        self.analysis_frame_1.place(x=536, y=37)

    def _create_labels(self):
        """Create analysis labels"""
        analysis_label = ctk.CTkLabel(
            self.analysis_frame, 
            text="Analysis", 
            font=("Poppins", 22, "bold")
        )
        analysis_label.place(x=35, y=20)

    def _create_balance_section(self):
        """Create the balance display section"""
        self.balance_frame = ctk.CTkFrame(
            self.analysis_frame,
            corner_radius=14,
            width=430,
            height=90,
            fg_color="#F1FFF3"
        )
        self.balance_frame.place(x=27, y=89)
        
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

    def _create_analysis_switcher(self):
        """Create the income/expense toggle switcher"""
        self.switcher_frame = ctk.CTkFrame(
            self.analysis_frame,
            corner_radius=14,
            width=430,
            height=50,
            fg_color="#F1FFF3"
        )
        self.switcher_frame.place(x=27, y=220)

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

    def _create_analysis_display_area(self):
        """Create the analysis display area with graphs"""
        self.graph_label = ctk.CTkLabel(
            self.analysis_frame_1,
            text="Graphical Representation of Data",
            font=("Poppins", 18, "bold")
        )
        self.graph_label.place(x=23, y=19)

        self.Income_Expense_Frame = ctk.CTkFrame(
            self.analysis_frame_1,
            corner_radius=26,
            width=440,
            height=400,
            fg_color="#DFF7E2",
            bg_color="#9FD39C"
        )
        self.Income_Expense_Frame.place(x=25, y=54)

        self.bar_graph_image = Button(
            self.analysis_frame_1,
            image=self.images['bar_graph'],
            bd=0,
            bg="#9FD39C",
            activebackground="#9FD39C",
            relief="flat"
        )
        self.bar_graph_image.place(x=16, y=461)

        self.pie_chart_image = Button(
            self.analysis_frame_1,
            image=self.images['pie_chart'],
            bd=0,
            bg="#9FD39C",
            activebackground="#9FD39C",
            relief="flat"
        )
        self.pie_chart_image.place(x=245, y=461)

        self.save_load_frame = ctk.CTkFrame(
            self.analysis_frame,
            corner_radius=26,
            width=440,
            height=118,
            fg_color="#F1FFF3",
            bg_color="#9FD39C"
        )
        self.save_load_frame.place(x=27, y=420)

        self.save_file = Button(
            self.save_load_frame,
            image=self.images['save_file'],
            bd=0,
            command=self.on_click_save_file,
            bg="#F1FFF3",
            activebackground="#F1FFF3",
            relief="flat"
        )
        self.save_file.place(x=10, y=12)

        self.load_file = Button(
            self.save_load_frame,
            image=self.images['load_file'],
            bd=0,
            command=self.on_click_load_file,
            bg="#F1FFF3",
            activebackground="#F1FFF3",
            relief="flat"
        )
        self.load_file.place(x=224, y=12)

    def _load_default_view(self):
        """Load the default income view with images"""
        # Position selector for income
        self.selected_frame.place(x=41, y=5)
        
        self.income_image = Label(
            self.analysis_frame,
            text=Controller.Controller.get_income(self.username),
            image=self.images['income_frame'],
            font=("Poppins", 20 * -1, "bold"),
            compound="center",
            bg="#9FD39C"
        )
        self.income_image.place(x=27, y=299)

        self.expense_image = Label(
            self.analysis_frame,
            text=Controller.Controller.get_expense(self.username),
            image=self.images['expense_frame'],
            font=("Poppins", 20 * -1, "bold"),
            compound="center",
            bg="#9FD39C"
        )
        self.expense_image.place(x=259, y=299)

        # Separator line
        self.line = ctk.CTkFrame(
            self.analysis_frame,
            width=3,
            height=106.5,
            fg_color="#DFF7E2"
        )
        self.line.place(x=242, y=295)

        # Load default income view
        self._load_category_view("Income")

    def show_income_view(self):
        """Show income analysis view"""
        self._update_switcher_state(is_income=True)
        self._load_category_view("Income")

    def show_expense_view(self):
        """Show expense analysis view"""
        self._update_switcher_state(is_income=False)
        self._load_category_view("Expense")

    def _update_switcher_state(self, is_income):
        """Update the visual state of the income/expense switcher"""
        x_pos = 41 if is_income else 265
        self.selected_frame.place(x=x_pos, y=5)
        self.income_label.configure(bg_color="#9FD39C" if is_income else "#F1FFF3")
        self.expense_label.configure(bg_color="#9FD39C" if not is_income else "#F1FFF3")

    def _load_category_view(self, view_type):
        """Load the appropriate category view"""
        if self.current_view:
            self.current_view.clear_frame_content()
        
        if view_type == "Income":
            self.current_view = Analysis_Income_Charts.AnalysisIncomeView(
                self.analysis_frame_1,
                self.username,
                self
            )
        else:
            self.current_view = Analysis_Expense_Charts.AnalysisExpenseView(
                self.analysis_frame_1,
                self.username,
                self
            )
        
    def update_balance_labels(self):
        """Update all balance-related displays"""
        self.balance_value.configure(text=Controller.Controller.get_balance(self.username))
        self.income_image.configure(text=Controller.Controller.get_income(self.username))
        self.expense_image.configure(text=Controller.Controller.get_expense(self.username))
    
    def on_click_save_file(self):
        Controller.Controller.save_transactions_to_csv(self.username)

    def on_click_load_file(self):
        Controller.Controller.load_transaction_to_csv(self.username)
        self.update_balance_labels()
