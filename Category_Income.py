from pathlib import Path
from tkinter import Button
from PIL import Image, ImageTk
import Controller
from abc import ABC, abstractmethod

ASSETS_PATH = Path(__file__).parent / "assets" / "assets_categories_income"

class BaseCategoryView(ABC):
    """Abstract base class for category views (Abstraction)"""
    def __init__(self, parent_frame, username, tab_instance):
        self._parent_frame = parent_frame
        self._username = username
        self._tab_instance = tab_instance
        self._images = {}
        self._load_assets()
        self._setup_view()

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

    @abstractmethod
    def _load_assets(self):
        """Load required images/assets"""
        pass

    @abstractmethod
    def _setup_view(self):
        """Setup the category view"""
        pass

    def clear_all_content(self):
        """Clear all widgets from parent frame"""
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

class IncomeCategoryView(BaseCategoryView):
    """Income category view implementation (Inheritance)"""
    def _load_assets(self):
        """Load all income category images (Encapsulation)"""
        self.category_assets = [
            ("salary", "Salary"), ("investment", "Investment"), 
            ("bonus", "Bonus"), ("receipt", "Receipt"),
            ("dividend", "Dividend"), ("gifts", "Gifts"),
            ("borrowing", "Borrowing"), ("allowance", "Allowance"),
            ("more", "More")
        ]
        
        for img_name, _ in self.category_assets:
            img_path = ASSETS_PATH / f"{img_name}.png"
            img = Image.open(img_path)
            self.images[img_name] = ImageTk.PhotoImage(img)

    def _setup_view(self):
        """Create the income category buttons grid"""
        positions = [
            (44, 37), (176, 37), (307, 37),
            (44, 194), (176, 194), (307, 194),
            (44, 345), (176, 345), (307, 345)
        ]
        
        for (img_name, category), (x, y) in zip(self.category_assets, positions):
            self._create_category_button(img_name, category, x, y)

    def _create_category_button(self, img_name, category, x, y):
        btn = Button(
            self.parent_frame,
            image=self.images[img_name],
            command=lambda c=category: self._on_category_select(c),
            borderwidth=0,
            activebackground="#DFF7E2",
            bg="#DFF7E2"
        )
        btn.place(x=x, y=y)

    def _on_category_select(self, category):
        """Handle category selection (Polymorphism)"""
        self.clear_all_content()
        Controller.UIController.switch_category(
            self.parent_frame, 
            category, 
            self.username, 
            "Income", 
            self.tab_instance
        )
        self.tab_instance.update_balance_labels()
