from pathlib import Path
from tkinter import Text, Entry, Button, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
from datetime import datetime
import pygame
import Controller
from abc import ABC, abstractmethod

ASSETS_PATH = Path(__file__).parent / "assets" / "assets_categories_entry"
NOTIF_PATH = Path(__file__).parent / "assets" / "assets_notification"

class BaseEntryForm(ABC):
    """Abstract base class for entry forms (Abstraction)"""
    def __init__(self, parent_frame, category, transaction_type, username, tab_instance):
        self._parent_frame = parent_frame
        self._category = category
        self._transaction_type = transaction_type 
        self._username = username
        self._tab_instance = tab_instance
        self._images = {}
        self._entries = {}
        self.interval()

    @property
    def parent_frame(self):
        return self._parent_frame

    @property
    def category(self):
        return self._category

    @property
    def transaction_type(self):
        return self._transaction_type

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

    @property
    def entries(self):
        """Encapsulated access to entries dictionary."""
        return self._entries
    
    @abstractmethod
    def interval(self):
        pass

    @abstractmethod
    def _setup_form(self):
        pass

    @abstractmethod
    def _create_form_fields(self):
        pass

    @abstractmethod
    def _create_save_button(self):
        pass

    def clear_all_content(self):
        """Clear all widgets from parent frame"""
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

class CategoryEntryForm(BaseEntryForm):
    """Concrete entry form implementation (Inheritance)"""

    def interval(self):
        self.parent_frame.after(300, lambda: self._setup_form())

    def _setup_form(self):
        """Setup the complete entry form (Encapsulation)"""
        self.parent_frame.configure(fg_color="#D7E6C5")
        self._create_back_button()
        self._create_form_fields()
        self._create_save_button()

    def _create_back_button(self):
        self.images['back'] = ImageTk.PhotoImage(
            Image.open(ASSETS_PATH / "button_back.png").resize((45, 45))
        )
        Button(
            self.parent_frame,
            image=self.images['back'],
            command=self._navigate_back,
            borderwidth=0,
            bg="#D7E6C5",
            activebackground="#D7E6C5",
            cursor="hand2"
        ).place(x=20, y=25)

    def _create_form_fields(self):
        """Create all form input fields"""
        fields = [
            ("date", "Date", 99, 69, 35, self._create_date_entry),
            ("amount", "Amount", 182, 150, 35, self._create_numeric_entry),
            ("title", "Title", 265, 233, 35, self._create_text_entry),
            ("description", "Description", 350, 317, 54, self._create_description_entry)
        ]

        for field in fields:
            self._create_field(*field)

    def _create_field(self, key, label, y_entry, y_label, height, creator_fn):

        ctk.CTkLabel(
            self.parent_frame,
            text=label,
            font=("Inter Medium", 18, "bold")
        ).place(x=60, y=y_label)

        frame = ctk.CTkFrame(
            self.parent_frame,
            width=334,
            height=height,
            fg_color="#F1FFF3",
            corner_radius=8
        )
        frame.place(x=53, y=y_entry)

        self.entries[key] = creator_fn(frame)

    def _create_date_entry(self, parent):
        return self._make_placeholder_entry(parent, "YYYY-MM-DD")

    def _create_numeric_entry(self, parent):
        return self._make_placeholder_entry(parent, "Philippine peso only")

    def _create_text_entry(self, parent):
        return self._make_placeholder_entry(parent, "Title (Optional)")

    def _create_description_entry(self, parent):
        return self._make_placeholder_text(parent, "Description (Optional)")
    
    def _make_placeholder_entry(self, parent, placeholder):
        entry = Entry(
            parent,
            borderwidth=0,
            font=("Inter", 10),
            fg='gray',
            bg="#F1FFF3"
        )
        entry.insert(0, placeholder)

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(fg="black")

        def on_focus_out(event):
            if not entry.get().strip():
                entry.insert(0, placeholder)
                entry.config(fg="gray")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        entry.place(x=12, y=5, width=310, height=25)
        return entry

    def _make_placeholder_text(self, parent, placeholder):
        text = Text(
            parent,
            borderwidth=0,
            font=("Inter", 10),
            fg='gray',
            bg="#F1FFF3",
            wrap="word"
        )
        text.insert("1.0", placeholder)

        def on_focus_in(event):
            if text.get("1.0", "end-1c") == placeholder:
                text.delete("1.0", "end")
                text.config(fg="black")

        def on_focus_out(event):
            if not text.get("1.0", "end-1c").strip():
                text.insert("1.0", placeholder)
                text.config(fg="gray")

        text.bind("<FocusIn>", on_focus_in)
        text.bind("<FocusOut>", on_focus_out)
        text.place(x=12, y=10, width=310, height=34)
        return text

    def _create_save_button(self):
        self.images['save'] = ImageTk.PhotoImage(
            Image.open(ASSETS_PATH / "button_save.png").resize((130, 50))
        )
        Button(
            self.parent_frame,
            image=self.images['save'],
            command=self._save_transaction,
            borderwidth=0,
            bg="#D7E6C5",
            activebackground="#D7E6C5",
            cursor="hand2"
        ).place(x=155, y=425)

    def _save_transaction(self):
        data = {
            'date': self._get_entry_value('date', 'YYYY-MM-DD'),
            'amount': self._get_entry_value('amount', 'Philippine peso only'),
            'title': self._get_entry_value('title', 'Title (Optional)'),
            'description': self._get_text_value('description', 'Description (Optional)')
        }

        fields_to_reset = {
            "date": "YYYY-MM-DD",
            "amount": "Philippine peso only",
            "title": "Title (Optional)",
            "description": "Description (Optional)"
        }

        required_fields = {
        "date": "YYYY-MM-DD",
        "amount": "Philippine peso only"
        }

        for key, placeholder in required_fields.items():
            widget = self.entries[key]
            if isinstance(widget, Entry):
                value = widget.get().strip()
                if not value or value == placeholder:
                    messagebox.showerror("Missing Fields", "Please fill in both the date and amount fields.")
                    self._reset_fields(required_fields)
                    return

        validate_date = Controller.Controller.validate_date(data["date"])
        validate_amount = Controller.Controller.validate_amount(data["amount"])

        if validate_date and validate_amount:
            if float(data["amount"]) > 0:
                Controller.Controller.add_transaction(
                    self.username,
                    data['date'],
                    self.transaction_type,
                    self.category,
                    data['amount'],
                    data['title'],
                    data['description']
                )

            else:
                messagebox.showerror("Invalid Amount", "Amount must be greater than zero.")
                self._reset_fields(fields_to_reset)
                return
        else:
            if not validate_date and not validate_amount:
                messagebox.showerror("Invalid Input", "Please enter a valid date in YYYY-MM-DD format and a numeric, positive amount.")
            elif not validate_date:
                messagebox.showerror("Invalid Date", "Please enter a valid date in the format YYYY-MM-DD.")
            elif not validate_amount:
                messagebox.showerror("Invalid Amount", "Please enter a numeric value for the amount.")
                
            self._reset_fields(fields_to_reset)
            return


        self.notification_generator()
        self.tab_instance.update_balance_labels()
        self._navigate_back()

    def _reset_fields(self, fields_to_reset):
        for key, placeholder in fields_to_reset.items():
            widget = self.entries[key]
            if isinstance(widget, Entry):
                widget.delete(0, "end")
                widget.insert(0, placeholder)
                widget.config(fg="gray")
            elif isinstance(widget, Text):
                widget.delete("1.0", "end")
                widget.insert("1.0", placeholder)
                widget.config(fg="gray")


    def _get_entry_value(self, key, placeholder):
        """Get entry value, returning empty string if it's still placeholder"""
        value = self.entries[key].get().strip()
        return "" if value == placeholder else value

    def _get_text_value(self, key, placeholder):
        """Get text widget value, returning empty string if it's still placeholder"""
        value = self.entries[key].get("1.0", "end-1c").strip()
        return "" if value == placeholder else value

    def notification_generator(self):
        self.current_time = datetime.now().strftime("%H:%M")

        data = {
            'amount': self._get_entry_value('amount', 'Philippine peso only'),
            'date': self._get_entry_value('date', 'YYYY-MM-DD')
        }

        Controller.Controller.Notification_Handler(
            username=self.username, 
            date=data["date"], 
            time=self.current_time, 
            transaction_type=self.transaction_type, 
            category=self.category, 
            amount=data['amount'],
            message=None,
            description=None
        )

        notif_sound_path = NOTIF_PATH / "notif.wav"
        if notif_sound_path.exists():
            pygame.mixer.init()
            pygame.mixer.Sound(notif_sound_path).play()

    def _navigate_back(self):
        """Navigate back to category view (Polymorphism)"""
        self.clear_all_content()
        self.parent_frame.configure(fg_color="#DFF7E2")
        
        if self.transaction_type == "Income":
            from Category_Income import IncomeCategoryView
            IncomeCategoryView(self.parent_frame, self.username, self.tab_instance)
        else:
            from Category_Expense import ExpenseCategoryView
            ExpenseCategoryView(self.parent_frame, self.username, self.tab_instance)