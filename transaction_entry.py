from pathlib import Path
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
from abc import ABC, abstractmethod
import pygame
import Controller

ASSETS_PATH = Path(__file__).parent / "assets" / "assets_transaction"
NOTIF_PATH = Path(__file__).parent / "assets" / "assets_notification"

class BaseTransactionView(ABC):
    """Abstract base class for category views (Abstraction)"""
    def __init__(self, parent_frame, id, username, transaction_tab_instance):
        self._parent_frame = parent_frame
        self._id = id
        self._username = username
        self._transaction_tab_instance = transaction_tab_instance
        self._images = {}
        self._entries = {}
        self._setup_form()

    @property
    def parent_frame(self):
        return self._parent_frame

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username
    
    @property
    def entries(self):
        return self._entries
    
    @abstractmethod
    def _setup_form(self):
        pass

    def clear_all_content(self):
        """Clear all content from the parent frame"""
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

class TransactionEntryForm(BaseTransactionView):

    def _setup_form(self):
        """Setup the complete entry form (Encapsulation)"""
        self.parent_frame.configure(fg_color="#D7E6C5")
        self._create_main_frame()
        self._create_back_button()
        self._create_form_fields()
        self._create_save_button()

    def _create_main_frame(self):
        """Create the main container frame"""
        self.entry_frame = ctk.CTkFrame(
            self.parent_frame,
            width=410,
            height=550,
            fg_color="#D7E6C5"
        )
        self.entry_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.entry_frame.pack_propagate(False)

    def _create_back_button(self):
        """Create back button with proper image loading"""
        back_img = Image.open(ASSETS_PATH / "button_back.png").resize((45, 45))
        self._images['back'] = ctk.CTkImage(light_image=back_img, dark_image=back_img, size=(45, 45))
        
        back_button = ctk.CTkButton(
            self.entry_frame,
            image=self._images['back'],
            command=self._navigate_back,
            text="",
            fg_color="#D7E6C5",
            hover_color="#D7E6C5",
            width=45,
            height=45,
            corner_radius=8
        )
        back_button.place(x=10, y=10)

    def _create_form_fields(self):
        """Create all form input fields with proper alignment"""
        fields = [
            ("date", "Date", 90, "YYYY-MM-DD", self._create_date_entry),
            ("category", "Category", 150, "E.g Food, Salary, Gifts", self._create_category_entry),
            ("transaction_type", "Transaction Type", 210, "E.g Income, Expense", self._create_transaction_type_entry),
            ("amount", "Amount", 270, "Philippine peso only", self._create_numeric_entry),
            ("title", "Title", 330, "Title (Optional)", self._create_text_entry),
            ("description", "Description", 390, "Description (Optional)", self._create_description_entry)
        ]

        for field_key, label, y_pos, placeholder, creator_fn in fields:
            self._create_field(field_key, label, y_pos, placeholder, creator_fn)

    def _create_field(self, key, label, y_pos, placeholder, creator_fn):
        """Create a form field with label and proper alignment"""
        # Create label
        label_widget = ctk.CTkLabel(
            self.entry_frame,
            text=label,
            font=("Inter", 14, "bold"),
            text_color="#2B2B2B"
        )
        label_widget.place(x=25, y=y_pos - 25)

        if key == "description":
            field_height = 50
        else:
            field_height = 35

        field_frame = ctk.CTkFrame(
            self.entry_frame,
            width=350,
            height=field_height,
            fg_color="#F1FFF3",
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0"
        )
        field_frame.place(x=25, y=y_pos)
        field_frame.pack_propagate(False)

        self._entries[key] = creator_fn(field_frame, placeholder)

    def _create_date_entry(self, parent, placeholder):
        return self._make_placeholder_entry(parent, placeholder)
    
    def _create_transaction_type_entry(self, parent, placeholder):
        return self._make_placeholder_entry(parent, placeholder)
    
    def _create_category_entry(self, parent, placeholder):
        return self._make_placeholder_entry(parent, placeholder)

    def _create_numeric_entry(self, parent, placeholder):
        return self._make_placeholder_entry(parent, placeholder)

    def _create_text_entry(self, parent, placeholder):
        return self._make_placeholder_entry(parent, placeholder)

    def _create_description_entry(self, parent, placeholder):
        return self._make_placeholder_text(parent, placeholder)
    
    def _make_placeholder_entry(self, parent, placeholder):
        """Create entry widget with placeholder functionality"""
        entry = ctk.CTkEntry(
            parent,
            border_width=0,
            font=("Inter", 12),
            text_color='#888888',
            fg_color="transparent",
            width=330,
            height=25
        )
        entry.insert(0, placeholder)
        entry.place(x=10, y=5)

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.configure(text_color="#2B2B2B")

        def on_focus_out(event):
            if not entry.get().strip():
                entry.insert(0, placeholder)
                entry.configure(text_color="#888888")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        return entry

    def _make_placeholder_text(self, parent, placeholder):
        """Create text widget with placeholder functionality"""
        text = ctk.CTkTextbox(
            parent,
            border_width=0,
            font=("Inter", 12),
            text_color='#888888',
            fg_color="transparent",
            wrap="word",
            width=330,
            height=40
        )
        text.insert("1.0", placeholder)
        text.place(x=10, y=5)

        def on_focus_in(event):
            if text.get("1.0", "end-1c") == placeholder:
                text.delete("1.0", "end")
                text.configure(text_color="#2B2B2B")

        def on_focus_out(event):
            if not text.get("1.0", "end-1c").strip():
                text.insert("1.0", placeholder)
                text.configure(text_color="#888888")

        text.bind("<FocusIn>", on_focus_in)
        text.bind("<FocusOut>", on_focus_out)
        
        return text

    def _create_save_button(self):
        """Create save button with proper image loading"""
        save_img = Image.open(ASSETS_PATH / "button_save.png").resize((130, 50))
        self._images['save'] = ctk.CTkImage(light_image=save_img, dark_image=save_img, size=(130, 50))
        
        save_button = ctk.CTkButton(
            self.entry_frame,
            image=self._images['save'],
            command=self.update_transaction,
            text="",
            fg_color="#D7E6C5",
            hover_color="#D7E6C5",
            width=130,
            height=50,
            corner_radius=8
        )
        save_button.place(x=130, y=450)

    def update_transaction(self):
        data = {
            'date': self._get_entry_value('date', 'YYYY-MM-DD'),
            'category': self._get_entry_value('category', 'E.g Food, Salary, Gifts'),
            'transaction_type': self._get_entry_value('transaction_type', 'E.g Income, Expense'),
            'amount': self._get_entry_value('amount', 'Philippine peso only'),
            'title': self._get_entry_value('title', 'Title (Optional)'),
            'description': self._get_text_value('description', 'Description (Optional)')
        }

        required_fields = {
            "date": "YYYY-MM-DD",
            "category": "E.g Food, Salary, Gifts",
            "transaction_type": "E.g Income, Expense",
            "amount": "Philippine peso only"
        }

        missing_fields = []
        for key, placeholder in required_fields.items():
            widget = self.entries[key]
            if isinstance(widget, ctk.CTkEntry):
                value = widget.get().strip()
                if not value or value == placeholder:
                    missing_fields.append(key)
        
        if missing_fields:
            messagebox.showerror("Missing Fields", f"Please fill in the following fields: {', '.join(missing_fields)}.")
            return

        income_category = ["Salary", "Investment", "Bonus", "Receipt", "Dividend", "Gifts", "Borrowing", "Allowance", "More"]
        expense_category = ["Food", "Transport", "Medicine", "Groceries", "Rent", "Gifts", "Savings", "Entertainment", "More"]

        validate_date = Controller.Controller.validate_date(data["date"])
        validate_amount = Controller.Controller.validate_amount(data["amount"])
        validate_category = Controller.Controller.validate_category(data["category"], data["transaction_type"])
        validate_transaction_type = Controller.Controller.validate_transaction_type(data["transaction_type"])

        if validate_date and validate_amount:
            if validate_transaction_type:
                if validate_category:
                    if float(data["amount"]) > 0:
                        value = Controller.Controller.edit_transaction(
                            self.id,
                            self.username,
                            data["date"],
                            data["transaction_type"],
                            data["category"],
                            data["amount"],
                            data["title"],
                            data["description"]
                        )

                        if value:
                            Controller.Controller.sort_transaction(self.username)
                            conditions = Controller.Controller.get_alerts_to_generate(self.username, True)

                            for condition in conditions:
                                Controller.Controller.Notification_Handler(
                                    self.username,
                                    condition["date"],
                                    condition["time"],
                                    condition["transaction_type"],
                                    condition["category"],
                                    condition["amount"],
                                    message=condition["message"],
                                    description=condition["description"]
                                )
                                
                                notif_sound_path = NOTIF_PATH / "notif.wav"
                                if notif_sound_path.exists():
                                    pygame.mixer.init()
                                    pygame.mixer.Sound(notif_sound_path).play()
                            
                            self._navigate_back()
                    else:
                        messagebox.showerror("Invalid Amount", "Amount must be greater than zero.")
                        return
                else:
                    if data["transaction_type"] == "Income":
                        messagebox.showerror("Invalid Category", f"Category must be one of: {', '.join(income_category)}")
                    elif data["transaction_type"] == "Expense":
                        messagebox.showerror("Invalid Category", f"Category must be one of: {', '.join(expense_category)}")
                    return
            else:
                messagebox.showerror("Invalid Transaction Type", "Transaction type must be either 'Income' or 'Expense'.")
                return
        else:
            if not validate_date and not validate_amount:
                messagebox.showerror("Invalid Input", "Please enter a valid date in YYYY-MM-DD format and a numeric, positive amount.")
            elif not validate_date:
                messagebox.showerror("Invalid Date", "Please enter a valid date in the format YYYY-MM-DD.")
            elif not validate_amount:
                messagebox.showerror("Invalid Amount", "Please enter a numeric value for the amount.")
                
            return

    def _get_entry_value(self, key, placeholder):
        """Get entry value, returning empty string if it's still placeholder"""
        value = self._entries[key].get().strip()
        return "" if value == placeholder else value

    def _get_text_value(self, key, placeholder):
        """Get text widget value, returning empty string if it's still placeholder"""
        value = self._entries[key].get("1.0", "end-1c").strip()
        return "" if value == placeholder else value
    
    def _navigate_back(self):
        self.clear_all_content()
        self.parent_frame.configure(fg_color="#DFF7E2")
        self._transaction_tab_instance._content_transaction()