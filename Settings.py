import customtkinter as ctk
from pathlib import Path
from PIL import Image
import Change_Password
from tkinter import messagebox
import Controller

ASSETS_PATH = Path(__file__).parent / "assets" / "assets_settings"

class SettingsHandler:
    def __init__(self, main_window, username):
        self._main_window = main_window
        self._username = username
        self._settings_frame_features = None
        self._settings_visible = False
        self._images = {}

    @property
    def main_window(self):
        return self._main_window

    @property
    def username(self):
        return self._username

    @property
    def settings_frame_features(self):
        return self._settings_frame_features

    @settings_frame_features.setter
    def settings_frame_features(self, frame):
        self._settings_frame_features = frame

    @property
    def settings_visible(self):
        return self._settings_visible

    @settings_visible.setter
    def settings_visible(self, visible):
        self._settings_visible = visible

    @property
    def images(self):
        return self._images

    def is_visible(self):
        return self.settings_visible and self.settings_frame_features is not None \
               and self.settings_frame_features.winfo_exists()

    def settings(self):
        if self.is_visible():
            self.hide_settings()
        else:
            self.show_settings()

    def show_settings(self):
        if self.settings_frame_features and self.settings_frame_features.winfo_exists():
            self.settings_frame_features.destroy()

        self.settings_frame_features = ctk.CTkFrame(
            self.main_window,
            corner_radius=26,
            width=340,
            height=340,
            fg_color="#CFF6CD",
            bg_color="#9FD39C"
        )
        self.settings_frame_features.place(x=861, y=93)
        self.settings_frame_features.lift()
        self.settings_visible = True

        # Load and place images with labels
        self.images['logout'] = self.load_image("logout.png", (70, 70))
        if self.images['logout']:
            label_image_1 = ctk.CTkLabel(self.settings_frame_features, text="", image=self.images['logout'])
            label_image_1.place(x=20, y=220)

        logout_label = ctk.CTkLabel(self.settings_frame_features, text="Logout", font=("Poppins", 16, "bold"))
        logout_label.place(x=104, y=240)

        self.images['settings'] = self.load_image("settings.png", (70, 70))
        if self.images['settings']:
            label_image_2 = ctk.CTkLabel(self.settings_frame_features, text="", image=self.images['settings'])
            label_image_2.place(x=20, y=130)

        settings_label = ctk.CTkLabel(self.settings_frame_features, text="Settings", font=("Poppins", 16, "bold"))
        settings_label.place(x=104, y=150)

        self.images['account'] = self.load_image("account.png", (50, 50))
        if self.images['account']:
            label_image_3 = ctk.CTkLabel(self.settings_frame_features, text="", image=self.images['account'])
            label_image_3.place(x=147, y=30)

        user_label = ctk.CTkLabel(self.settings_frame_features, text=self.username, font=("Poppins", 16, "bold"))
        user_label.place(relx=0.5, rely=0.3, anchor="center")

        # Bind events
        logout_label.bind("<Button-1>", lambda e: self.on_click_logout())
        settings_label.bind("<Button-1>", lambda e: self.on_click_settings())

        for element in [logout_label, settings_label]:
            element.bind("<Enter>", lambda e: self.settings_frame_features.configure(cursor="hand2"))
            element.bind("<Leave>", lambda e: self.settings_frame_features.configure(cursor=""))

    def setting_features(self):
        for widget in self.settings_frame_features.winfo_children():
            widget.destroy()

        self.images['back'] = self.load_image("back.png", (30, 30))
        if self.images['back']:
            arrow_image = ctk.CTkLabel(self.settings_frame_features, text="", image=self.images['back'])
            arrow_image.place(x=20, y=20)

        settings_title = ctk.CTkLabel(self.settings_frame_features, text="Settings", font=("Poppins", 18, "bold"))
        settings_title.place(x=130, y=20)

        self.images['change_pass'] = self.load_image("change_pass.png", (70, 70))
        if self.images['change_pass']:
            password_settings_image = ctk.CTkLabel(self.settings_frame_features, text="", image=self.images['change_pass'])
            password_settings_image.place(x=20, y=120)

        password_settings_label = ctk.CTkLabel(self.settings_frame_features, text="Change Password", font=("Poppins", 16, "bold"))
        password_settings_label.place(x=105, y=140)

        self.images['delete'] = self.load_image("delete.png", (70, 70))
        if self.images['delete']:
            delete_account_image = ctk.CTkLabel(self.settings_frame_features, text="", image=self.images['delete'])
            delete_account_image.place(x=20, y=210)

        delete_account_label = ctk.CTkLabel(self.settings_frame_features, text="Delete Account", font=("Poppins", 16, "bold"))
        delete_account_label.place(x=105, y=230)

        password_settings_label.bind("<Button-1>", lambda e: self.on_click_change_password())
        delete_account_label.bind("<Button-1>", lambda e: self.on_click_delete_account())
        arrow_image.bind("<Button-1>", lambda e: self.on_click_back())

        for element in [password_settings_label, delete_account_label, arrow_image]:
            element.bind("<Enter>", lambda e: self.settings_frame_features.configure(cursor="hand2"))
            element.bind("<Leave>", lambda e: self.settings_frame_features.configure(cursor=""))

    def hide_settings(self):
        """Hide and destroy any visible settings frame and update flag."""
        if self.settings_frame_features and self.settings_frame_features.winfo_exists():
            self.settings_frame_features.place_forget()
            self.settings_frame_features.destroy()
            self.settings_frame_features = None
        self.settings_visible = False

    def lift_settings(self):
        if self.settings_frame_features and self.settings_frame_features.winfo_exists():
            self.settings_frame_features.lift()

    def load_image(self, filename, size):
        image_path = ASSETS_PATH / filename
        if not image_path.exists():
            print(f"Image file not found: {image_path}")
            return None
        pil_image = Image.open(image_path)
        return ctk.CTkImage(light_image=pil_image, size=size)

    def on_click_logout(self):
        Controller.Controller.logout_user(self.main_window)

    def on_click_settings(self):
        self.setting_features()

    def on_click_delete_account(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete your account?\nThis action cannot be undone.")
        if confirm:
            Controller.Controller.delete_account(self.username, self.main_window)

    def on_click_change_password(self):
        Change_Password.ChangePassword(self.settings_frame_features, self.username, self)

    def on_click_back(self):
        self.show_settings()