import customtkinter as ctk
from pathlib import Path
from PIL import Image
import Controller
from tkinter import END, Entry, Button, messagebox, PhotoImage

ASSETS_PATH = Path(__file__).parent / "assets" / "assets_change_password"

class ChangePassword:
    def __init__(self, current_frame, username, settings_handler):
        self.current_frame = current_frame
        self.username = username
        self.settings_handler = settings_handler
        self.entry_widgets = {}
        self.images = {}
        self.password_visible = {
            "new_password": False,
            "confirm_password": False
        }

        self.change_password(self.current_frame)

    def load_image(self, filename, size):
        image_path = ASSETS_PATH / filename
        if not image_path.exists():
            print(f"Image file not found: {image_path}")
            return None
        pil_image = Image.open(image_path)
        return ctk.CTkImage(light_image=pil_image, size=size)

    def toggle_password_visibility(self, field_name):
        if field_name in self.password_visible:
            entry = self.entry_widgets[field_name]
            current_text = entry.get()
            
            self.password_visible[field_name] = not self.password_visible[field_name]
            
            entry.delete(0, END)
            if self.password_visible[field_name]:
                entry.config(show="")
            else:
                entry.config(show="*")
            
            # Restore text
            entry.insert(0, current_text)

    def change_password(self, current_frame):
        current_frame.configure(cursor="arrow")
        for widget in current_frame.winfo_children():
            widget.destroy()

        self.images['back_button'] = self.load_image("back_button.png", (38, 40))
        if self.images['back_button']:
            back_button = ctk.CTkLabel(current_frame, text="", image=self.images['back_button'])
            back_button.place(x=9, y=10)

        fields = [
            ("current_password", "Current Password", 74),
            ("new_password", "New Password", 147),
            ("confirm_password", "Confirm Password", 227)
        ]

        for key, label_text, y_pos in fields:
            self.images[key] = self.load_image("entry_box.png", (276, 32))

            if self.images[key]:
                bg_label = ctk.CTkLabel(current_frame, text="", image=self.images[key])
                bg_label.place(x=31, y=y_pos)

            show_char = "*" if key in ["new_password", "confirm_password"] else ""
            entry_widget = Entry(current_frame, font=("Inter", 12 * -1), bd=0, bg="#F1FFF3", show=show_char)
            entry_widget.place(x=40, y=y_pos + 5, width=258, height=22)
            self.entry_widgets[key] = entry_widget

            field_label = ctk.CTkLabel(current_frame, text=label_text, font=("Inter Medium", 12, "bold"), text_color="black")
            field_label.place(x=34, y=y_pos - 28)

        self.images['show_password'] = self.load_image("show_password.png", (25, 25))

        # New password show button (with toggle functionality)
        if self.images['show_password']:
            show_new_password = ctk.CTkLabel(current_frame, text="", image=self.images['show_password'], bg_color="#F1FFF3")
            show_new_password.place(x=270, y=151)
            show_new_password.bind("<Button-1>", lambda e: self.toggle_password_visibility("new_password"))
            show_new_password.bind("<Enter>", lambda e: current_frame.configure(cursor="hand2"))
            show_new_password.bind("<Leave>", lambda e: current_frame.configure(cursor=""))

        # Confirm password show button (with toggle functionality)
        if self.images['show_password']:
            show_confirm_password = ctk.CTkLabel(current_frame, text="", image=self.images['show_password'], bg_color="#F1FFF3")
            show_confirm_password.place(x=270, y=231)
            show_confirm_password.bind("<Button-1>", lambda e: self.toggle_password_visibility("confirm_password"))
            show_confirm_password.bind("<Enter>", lambda e: current_frame.configure(cursor="hand2"))
            show_confirm_password.bind("<Leave>", lambda e: current_frame.configure(cursor=""))

        image_path = ASSETS_PATH / "button_password.png"
        self.images['button_password'] = PhotoImage(file=image_path)

        if self.images['button_password']:
            button_password = Button(
                current_frame, 
                image=self.images['button_password'], 
                borderwidth=0, 
                activebackground="#CFF6CD", 
                bg="#CFF6CD", 
                command=self.submit_password_change
            )
            button_password.place(x=87, y=274)

        back_button.bind("<Button-1>", lambda e: self.on_click_back())
        back_button.bind("<Enter>", lambda e: current_frame.configure(cursor="hand2"))
        back_button.bind("<Leave>", lambda e: current_frame.configure(cursor=""))

    def on_click_back(self):
        self.current_frame.configure(cursor="arrow")

        for widget in self.current_frame.winfo_children():
            widget.unbind("<Enter>")
            widget.unbind("<Leave>")

        self.settings_handler.setting_features()

    def submit_password_change(self):
        current_password = self.entry_widgets["current_password"].get()
        new_password = self.entry_widgets["new_password"].get()
        confirm_password = self.entry_widgets["confirm_password"].get()

        if not current_password or not new_password or not confirm_password:
            messagebox.showwarning("Warning", "All fields are required!")
            return

        password = Controller.Controller.get_password(self.username)

        if password != current_password:
            messagebox.showerror("Error", "Current password is incorrect!")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "New password and confirm password do not match!")
            return

        try:
            results = Controller.Controller.update_password(self.username, new_password)
            
            if results:
                messagebox.showinfo("Success", "Password changed successfully!")
                self.on_click_back()
            else:
                messagebox.showerror("Error", "Failed to update password!")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error changing password: {e}")