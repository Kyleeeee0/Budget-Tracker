from pathlib import Path
from tkinter import Button
from PIL import Image, ImageTk
import Controller
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

ASSETS_PATH = Path(__file__).parent / "assets" / "assets_analysis"

class BaseCategoryView:
    """Abstract base class for category views (Abstraction)"""
    def __init__(self, parent_frame, username, tab_instance):
        self._parent_frame = parent_frame
        self._username = username
        self._tab_instance = tab_instance
        self._images = {}
        self._initialize_view()

    @property
    def parent_frame(self):
        return self._parent_frame

    @property
    def username(self):
        return self._username

    @property
    def tab_instance(self):
        return self._tab_instance

    @property
    def images(self):
        """Encapsulated access to images dictionary."""
        return self._images

    def _initialize_view(self):
        """Initialize the view by loading images and creating the display area"""
        self._load_images()
        self._create_analysis_display_area()

    def clear_frame_content(self):
        """Clear the content inside the Income_Expense_Frame"""
        for widget in self.Income_Expense_Frame.winfo_children():
            widget.destroy()

class AnalysisIncomeView(BaseCategoryView):

    def _load_images(self):
        """Load all required images without resizing"""
        self.images['bar_graph'] = self._load_tk_image("bar_graph.png")
        self.images['pie_chart'] = self._load_tk_image("pie_chart.png")

    def _load_tk_image(self, image_name):
        """Load images using ImageTk for tkinter without resizing"""
        img_path = ASSETS_PATH / image_name
        img = Image.open(img_path)
        return ImageTk.PhotoImage(img)

    def _create_analysis_display_area(self):
        """Create the analysis display area with graphs"""
        self.graph_label = ctk.CTkLabel(
            self.parent_frame,
            text="Graphical Representation of Data",
            font=("Poppins", 18, "bold")
        )
        self.graph_label.place(x=23, y=19)

        self.Income_Expense_Frame = ctk.CTkFrame(
            self.parent_frame,
            corner_radius=26,
            width=440,
            height=400,
            fg_color="#DFF7E2",
            bg_color="#9FD39C"
        )
        self.Income_Expense_Frame.place(x=25, y=54)

        self.bar_graph_image = Button(
            self.parent_frame,
            image=self.images['bar_graph'],
            bd=0,
            bg="#9FD39C",
            activebackground="#9FD39C",
            relief="flat",
            command=self.bar_graph
        )
        self.bar_graph_image.place(x=16, y=461)

        self.pie_chart_image = Button(
            self.parent_frame,
            image=self.images['pie_chart'],
            bd=0,
            bg="#9FD39C",
            activebackground="#9FD39C",
            relief="flat",
            command=self.pie_chart
        )
        self.pie_chart_image.place(x=245, y=461)

    def bar_graph(self):
        self.clear_frame_content()

        income_data = Controller.Controller.get_income_data(self.username)

        category_totals = {}
        for record in income_data:
            date = record[1]
            amount = record[3]
            category_totals[date] = category_totals.get(date, 0) + amount

        if not category_totals:
            no_data_label = ctk.CTkLabel(
                self.Income_Expense_Frame,
                text="No income data available",
                font=("Poppins", 14)
            )
            no_data_label.place(relx=0.5, rely=0.5, anchor="center")
            return

        dates = list(category_totals.keys())
        amounts = list(category_totals.values())

        fig, ax = plt.subplots(figsize=(5, 3.5))
        fig.patch.set_facecolor('#DFF7E2')
        ax.set_facecolor('#DFF7E2')

        bars = ax.bar(dates, amounts, color='#9fd39c', edgecolor='#7fbf7f', linewidth=1)
        ax.set_title('Income Breakdown', fontsize=12, fontweight='bold', pad=10)
        ax.set_ylabel('Amount', fontsize=10)
        ax.set_xlabel('Date', fontsize=10)
        ax.tick_params(axis='x', rotation=45, labelsize=8)
        ax.tick_params(axis='y', labelsize=8)

        for bar in bars:
            x = bar.get_x() + bar.get_width() / 2
            y = bar.get_height()
            label = f'₱{y:,.0f}'
            ax.text(x, y + max(amounts) * 0.01, label, ha='center', va='bottom', fontsize=8)


        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self.Income_Expense_Frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=10, y=10, width=420, height=380)
        plt.close(fig)


    def pie_chart(self):
        self.clear_frame_content()

        COLORS = {
            'Salary': '#9fd39c',
            'Investment': "#a6dfa3",
            'Allowance': "#a3e8a2",
            'Bonus': '#dff7e2',
            'Dividend': "#b1e8ae",
            'Gifts': "#bfeec3",
            'Borrowing': "#bef6bb",
            'More': "#9ac798",
            'Receipt': '#dff7e2'
        }

        income_data = Controller.Controller.get_income_data(self.username)
        
        if not income_data:
            no_data_label = ctk.CTkLabel(
                self.Income_Expense_Frame,
                text="No income data available",
                font=("Poppins", 14)
            )
            no_data_label.place(relx=0.5, rely=0.5, anchor="center")
            return

        income_data_dict = {}
        for income in income_data:
            category = income[2]
            amount = income[3]
            income_data_dict[category] = income_data_dict.get(category, 0) + amount

        chart_data = pd.DataFrame(list(income_data_dict.items()), columns=['Category', 'Amount'])
        total_income = chart_data['Amount'].sum()

        fig, ax = plt.subplots(figsize=(5, 3.5))
        fig.patch.set_facecolor('#DFF7E2')

        wedges, texts, autotexts = ax.pie(
            chart_data['Amount'],
            labels=chart_data['Category'],
            autopct='%1.1f%%',
            colors=[COLORS[cat] for cat in chart_data['Category']],
            shadow=True,
            startangle=340,
            explode=[0.1 if cat == 'Salary' else 0.01 for cat in chart_data['Category']]
        )

        ax.text(0, 0, f'Total\n₱{total_income:,.2f}', ha='center', va='center',
                fontsize=9, fontweight='bold', color='#4C6B46')

        ax.set_title("Income Breakdown", fontsize=12, fontweight='bold', pad=10)

        for text in texts:
            text.set_fontsize(8)
        for autotext in autotexts:
            autotext.set_fontsize(7)
            autotext.set_color('white')
            autotext.set_weight('bold')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self.Income_Expense_Frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=10, y=10, width=420, height=380)
        plt.close(fig)
