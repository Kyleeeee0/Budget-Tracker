from tkinter import *
from pathlib import Path
from tkinter import messagebox
import Controller, Sign_In, Main

ASSETS_PATH = Path(__file__).parent /"assets" / "assets_user_authentication"

class LoginForm:
    def __init__(self, parent_frame, switch_to_signin_callback):
        self._parent_frame = parent_frame
        self._switch_to_signin = switch_to_signin_callback
        self._images = {}
        self._username_entry = None
        self._password_entry = None
        self.create_form()

    @property
    def parent_frame(self):
        return self._parent_frame

    @property
    def images(self):
        return self._images

    @property
    def username_entry(self):
        return self._username_entry

    @username_entry.setter
    def username_entry(self, widget):
        self._username_entry = widget

    @property
    def password_entry(self):
        return self._password_entry

    @password_entry.setter
    def password_entry(self, widget):
        self._password_entry = widget

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
        self.canvas.create_text(190.0, 153.0, anchor="nw", text="Login Your Account", 
                              fill="#000000", font=("Montserrat", 26 * -1, "bold"))
        self.canvas.create_text(100.0, 230.0, anchor="nw", text="Username", 
                              fill="#000000", font=("Montserrat", 17 * -1))
        self.canvas.create_text(100.0, 341.0, anchor="nw", text="Password", 
                              fill="#000000", font=("Montserrat", 17 * -1))

        self._images["entry_1"] = PhotoImage(file=ASSETS_PATH / "entry_1.png")
        self.canvas.create_image(315.0, 290.5, image=self._images["entry_1"])
        self.username_entry = Entry(self.parent_frame, bd=0, bg="#D9D9D9", fg="#000716", 
                                  highlightthickness=0, font=("Inter", 17 * -1))
        self.username_entry.place(x=115.0, y=270.0, width=400.0, height=38.0)

        self._images["entry_2"] = PhotoImage(file=ASSETS_PATH / "entry_2.png")
        self.canvas.create_image(315.0, 400, image=self._images["entry_2"])
        self.password_entry = Entry(self.parent_frame, bd=0, bg="#D9D9D9", fg="#000716", 
                                  highlightthickness=0, show="*", font=("Inter", 17 * -1))
        self.password_entry.place(x=115.0, y=380.0, width=400.0, height=38.0)

    def _create_buttons(self):
        self._images["button_1"] = PhotoImage(file=ASSETS_PATH / "button_1.png")
        button_1 = Button(
            self.parent_frame,  
            command=self._authenticate_user,
            image=self._images["button_1"],
            text="SIGN IN",
            font=("Inter", 25 * -1, "bold"),
            fg="#333333",
            borderwidth=0,
            highlightthickness=0,
            compound="center",
            relief="flat"
        )
        button_1.place(x=85.0, y=480.0, width=458.0, height=55.0)

        self._create_password_toggle()
        self._create_register_link()

    def _create_password_toggle(self):
        self.show_password_var = IntVar(value=0)
        Checkbutton(
            self.parent_frame,
            text="Show Password",
            variable=self.show_password_var,
            command=lambda: Controller.Controller.toggle_password(self.password_entry, self.show_password_var),
            bg="#F4F4F4",
            font=("Montserrat", 17 * -1),
            fg="#000000",
            activebackground="#F4F4F4",
            activeforeground="#000000",
            highlightthickness=0,
            bd=0
        ).place(x=395.2, y=445.12)

    def _create_register_link(self):
        register_text = self.canvas.create_text(248.0, 551.0, anchor="nw", 
                                             text="Register Account?", fill="#000000", 
                                             font=("Inter", 17 * -1, "underline"))
        self.canvas.tag_bind(register_text, "<Button-1>", lambda e: self._switch_to_signin())
        self.canvas.tag_bind(register_text, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(register_text, "<Leave>", lambda e: self.canvas.config(cursor=""))

    def _authenticate_user(self):
        username = self.username
        password = self.password
        if Controller.Controller.authenticate_user(username, password):
            Main.Home(self.parent_frame.master, username)
        else:
            if self.username_entry:
                self.username_entry.delete(0, END)
            if self.password_entry:
                self.password_entry.delete(0, END)
            messagebox.showerror("Error", "Account doesn't exist!")


class LogIn(LoginForm):
    def __init__(self, main_window):
        self.__main_window = main_window
        self._setup_main_window()
        self._create_frames()
        self.show_login_form()
        self.__main_window.protocol("WM_DELETE_WINDOW", self.on_closing)

    @property
    def main_window(self):
        return self.__main_window

    def _setup_main_window(self):
        self.__main_window.title("Budget Tracker")
        self.__main_window.geometry("1250x750")
        self.__main_window.configure(bg="#FFFFFF")
        self.__main_window.resizable(False, False)

        window_width = 1250
        window_height = 750
        y_offset = -40

        screen_width = self.__main_window.winfo_screenwidth()
        screen_height = self.__main_window.winfo_screenheight()

        x_coordinate = (screen_width // 2) - (window_width // 2)
        y_coordinate = (screen_height // 2) - (window_height // 2) + y_offset

        self.__main_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    def _create_frames(self):
        # Left frame (green background)
        self.left_frame = Frame(self.__main_window, bg="#9FD39C")
        self.left_frame.place(x=0, y=0, width=625, height=750)
        
        # Right frame (will hold forms)
        self.right_frame = Frame(self.__main_window, bg="#F4F4F4")
        self.right_frame.place(x=625, y=0, width=625, height=750)
        
        self._create_left_content()

    def _create_left_content(self):
        self.bg_canvas = Canvas(
            self.left_frame,
            bg="#FFFFFF",
            height=625,
            width=750,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.bg_canvas.place(x=0, y=0)
        self.bg_canvas.create_rectangle(0.0, 0.0, 625.0, 750.0, fill="#9FD39C", outline="")
        self.bg_canvas.create_text(190.0, 93.0, anchor="nw", text="Nice to see you again", 
                                 fill="#333333", font=("DMSans", 25 * -1))
        self.bg_canvas.create_text(155.0, 123.0, anchor="nw", text="Welcome back", 
                                 fill="#333333", font=("DMSans", 45 * -1, "bold"))
    
    def show_login_form(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        self.login_form = LoginForm(self.right_frame, self.show_signin_form)

    def show_signin_form(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        self.signin_form = Sign_In.SignInForm(self.right_frame, self.show_login_form)
    
    def on_closing(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to close the app?"):
            self.__main_window.destroy()

if __name__ == "__main__":
    main_window = Tk()
    log_in_system = LogIn(main_window)
    main_window.mainloop()

