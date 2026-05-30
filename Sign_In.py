from pathlib import Path
from tkinter import *
from tkinter import messagebox
import Controller

ASSETS_PATH = Path(__file__).parent / "assets" / "assets_user_authentication"

class SignInForm:
    def __init__(self, parent_frame, switch_to_login_callback):
        self._parent_frame = parent_frame
        self._switch_to_login = switch_to_login_callback
        self._images = {}
        self._username_entry = None
        self._password_entry = None
        self.create_form()

    @property
    def parent_frame(self):
        return self._parent_frame

    @property
    def username(self):
        """Return the current username string."""
        if self._username_entry:
            return self._username_entry.get()
        return None

    @property
    def password(self):
        """Return the current password string."""
        if self._password_entry:
            return self._password_entry.get()
        return None

    def create_form(self):
        self.canvas = Canvas(
            self.parent_frame,
            bg="#F4F4F4",
            height=625,
            width=750,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.pack(fill="both", expand=True)

        self._create_form_elements()
        self._create_buttons()

    def _create_form_elements(self):
        self.canvas.create_text(43.0, 48.0, anchor="nw", text="Welcome!", fill="#000000", 
                              font=("Montserrat", 30 * -1, "bold"))
        self.canvas.create_text(220.0, 153.0, anchor="nw", text="Create Account", 
                              fill="#000000", font=("Montserrat", 26 * -1, "bold"))
        self.canvas.create_text(100.0, 230.0, anchor="nw", text="Username", 
                              fill="#000000", font=("Montserrat", 17 * -1))
        self.canvas.create_text(100.0, 341.0, anchor="nw", text="Password", 
                              fill="#000000", font=("Montserrat", 17 * -1))
        self.canvas.create_text(230.0, 551.0, anchor="nw", text="Already a user?", 
                              fill="#000000", font=("Inter", 17 * -1))

        self._images["entry_1"] = PhotoImage(file=ASSETS_PATH / "entry_1.png")
        self.canvas.create_image(315.0, 290.5, image=self._images["entry_1"])
        self._username_entry = Entry(self.parent_frame, bd=0, bg="#D9D9D9", fg="#000716", 
                                  highlightthickness=0, font=("Inter", 17 * -1))
        self._username_entry.place(x=115.0, y=270.0, width=400.0, height=40.0)

        self._images["entry_2"] = PhotoImage(file=ASSETS_PATH / "entry_2.png")
        self.canvas.create_image(315.0, 400, image=self._images["entry_2"])
        self._password_entry = Entry(self.parent_frame, bd=0, bg="#D9D9D9", fg="#000716", 
                                  highlightthickness=0, show="*", font=("Inter", 17 * -1))
        self._password_entry.place(x=115.0, y=380.0, width=400.0, height=40.0)

    def _create_buttons(self):
        self._images["button_1"] = PhotoImage(file=ASSETS_PATH / "button_1.png")
        button_1 = Button(
            self.parent_frame,
            command=self._register_user,
            image=self._images["button_1"],
            text="SIGN UP",
            font=("Inter", 25 * -1, "bold"),
            fg="#333333",
            borderwidth=0,
            highlightthickness=0,
            compound="center",
            relief="flat"
        )
        button_1.place(x=85.0, y=480.0, width=458.0, height=55.0)

        self._create_password_toggle()
        self._create_login_link()

    def _create_password_toggle(self):
        self.show_password_var = IntVar(value=0)
        Checkbutton(
            self.parent_frame,
            text="Show Password",
            variable=self.show_password_var,
            command=lambda: Controller.Controller.toggle_password(self._password_entry, self.show_password_var),
            bg="#F4F4F4",
            font=("Montserrat", 17 * -1),
            fg="#000000",
            activebackground="#F4F4F4",
            activeforeground="#000000",
            highlightthickness=0,
            bd=0
        ).place(x=395.2, y=445.12)

    def _create_login_link(self):
        register_text = self.canvas.create_text(350.0, 551.0, anchor="nw", 
                                             text="LOGIN", fill="#000000", 
                                             font=("Inter", 17 * -1, "underline"))
        self.canvas.tag_bind(register_text, "<Button-1>", lambda e: self._switch_to_login())
        self.canvas.tag_bind(register_text, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(register_text, "<Leave>", lambda e: self.canvas.config(cursor=""))

    def _register_user(self):
        username = self.username
        password = self.password
        
        if Controller.Controller.register_user(username, password):
            messagebox.showinfo("Account Created", "Your account has been successfully created!")
            self._username_entry.delete(0, END)
            self._password_entry.delete(0, END)
        else:
            messagebox.showerror("Error", "Username already exists! Please choose another.")
            self._username_entry.delete(0, END)
            self._password_entry.delete(0, END)

class Sign_In:
    def __init__(self, main_window, right_frame, _switch_to_login_callback):
        self.main_window = main_window
        self.right_frame = right_frame
        self.form = SignInForm(self.right_frame, _switch_to_login_callback)
