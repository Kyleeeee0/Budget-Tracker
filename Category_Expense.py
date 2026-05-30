from pathlib import Path
from tkinter import Button
from PIL import Image, ImageTk
import Controller
from Category_Income import BaseCategoryView

ASSETS_PATH = Path(__file__).parent / "assets" / "assets_categories_expense"

class ExpenseCategoryView(BaseCategoryView):

    def _load_assets(self):
        self.category_assets = [
            ("food.png", "Food"),
            ("transport.png", "Transport"),
            ("medicine.png", "Medicine"),
            ("groceries.png", "Groceries"),
            ("rent.png", "Rent"),
            ("gifts.png", "Gifts"),
            ("savings.png", "Savings"),
            ("entertainment.png", "Entertainment"),
            ("more.png", "More")
        ]
        
        self._images = {}
        for img_file, category in self.category_assets:
            try:
                img_path = ASSETS_PATH / img_file
                img = Image.open(img_path)
                self.images[category] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading image {img_file}: {str(e)}")
                self.images[category] = ImageTk.PhotoImage(Image.new('RGBA', (100, 100), (0,0,0,0)))

    @property
    def images(self):
        """Encapsulated access to images dictionary."""
        return self._images

    def _setup_view(self):
        """Create the expense category buttons grid"""
        positions = [
            (45, 36), (175, 36), (302, 36),
            (45, 190), (175, 190), (302, 190),
            (45, 343), (172, 343), (302, 343)
        ]
        
        for (img_file, category), (x, y) in zip(self.category_assets, positions):
            self._create_category_button(category, x, y)

    def _create_category_button(self, category, x, y):
        """Create a category button with image"""
        btn = Button(
            self.parent_frame,
            image=self.images[category],
            command=lambda c=category: self._on_category_select(c),
            borderwidth=0,
            highlightthickness=0,
            activebackground="#DFF7E2",
            bg="#DFF7E2"
        )
        btn.image = self.images[category]
        btn.place(x=x, y=y)

    def _on_category_select(self, category):
        """Handle category selection"""
        self.clear_all_content()
        Controller.UIController.switch_category(
            self.parent_frame, 
            category, 
            self.username, 
            "Expense", 
            self.tab_instance
        )
        self.tab_instance.update_balance_labels()
