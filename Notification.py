import customtkinter as ctk
import Controller
from pathlib import Path

ASSETS_PATH = Path(__file__).parent / "assets" / "assets_notification"

class NotificationHandler:
    def __init__(self, main_window, username):
        self._main_window = main_window
        self._username = username
        self._images = {}
        self._notif_frame = None
        self._notif_visible = False

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
    def notif_frame(self):
        return self._notif_frame

    @notif_frame.setter
    def notif_frame(self, frame):
        self._notif_frame = frame

    @property
    def notif_visible(self):
        return self._notif_visible

    @notif_visible.setter
    def notif_visible(self, visible):
        self._notif_visible = visible

    def notification(self):
        # Toggle notification visibility
        if self.notif_visible:
            self.hide_notification()
        else:
            self.show_notification()

    def show_notification(self):
        if not self.notif_visible:
            self.notif_frame = ctk.CTkScrollableFrame(
                self.main_window,
                corner_radius=26,
                width=350,
                height=400,
                fg_color="#CFF6CD",
                bg_color="#9FD39C"
            )
            
            self.NotificationGenerator()

            self.notif_frame.place(x=821, y=93)
            self.notif_frame.lift()
            self.notif_visible = True

    def NotificationGenerator(self):

        new_alerts = Controller.Controller.get_alerts_to_generate(self.username, None)

        for alert in new_alerts:
            Controller.Controller.Notification_Handler(
                self.username,
                alert["date"],
                alert["time"],
                alert["transaction_type"],
                alert["category"],
                alert["amount"],
                message=alert["message"],
                description=alert["description"]
            )

        existing = Controller.Controller.Get_Notification(self.username)
        for notif in reversed(existing):
            self.show_alert_frame(notif[2], notif[3], notif[4], notif[0], notif[1])


    def show_alert_frame(self, category, message, description, date, time):
        frame = ctk.CTkFrame(self.notif_frame, width=400, height=80, fg_color="#CFF6CD", bg_color="#CFF6CD")
        frame.pack(pady=10)

        ctk.CTkLabel(frame, 
                    text=message, 
                    font=("Poppins", 14, "bold")
                ).pack(anchor="w", padx=12, pady=(6, 2))
        
        ctk.CTkLabel(frame, 
                     text=description, 
                     font=("Segoe UI", 13), 
                     wraplength=330, 
                     justify="left", anchor="w"
                ).pack(anchor="w", padx=12, fill="both")
        
        ctk.CTkLabel(frame, 
                     text=f"{category} | {date} | {time}", 
                     font=("Segoe UI", 11, "italic")
                ).pack(anchor="e", padx=12, pady=(4, 2))

        ctk.CTkFrame(self.notif_frame, 
                     width=400, 
                     height=3, 
                     fg_color="#9FD39C",
                ).pack()

    def hide_notification(self):
        if self.notif_visible and self.notif_frame and self.notif_frame.winfo_exists():
            self.notif_frame.place_forget()
            self.notif_frame.destroy()
            self.notif_frame = None
        self.notif_visible = False

    def lift_notification(self):
        if self.notif_visible and self.notif_frame and self.notif_frame.winfo_exists():
            self.notif_frame.lift()
