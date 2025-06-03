from datetime import datetime, timedelta
import tkinter.messagebox as tkmb
from venv import create

import requests
from PIL import Image
from customtkinter import CTk, CTkFrame, CTkButton, CTkImage, CTkScrollableFrame, CTkToplevel, CTkLabel, CTkEntry, \
    CTkCheckBox
from qbstyles import mpl_style

from members_page import MembersServerFrame
from server_page import GenServerFrame
from start_page import StartFrame
mpl_style(dark=True)
from data_object import Base, Server, Member, MembersServer


def logowanie(app):
    def login():

        username = "Geeks"
        password = "12345"
        new_window = CTkToplevel(app)

        new_window.title("New Window")

        new_window.geometry("350x150")

        if user_entry.get() == username and user_pass.get() == password:
            tkmb.showinfo(title="Login Successful", message="You have logged in Successfully")
            CTkLabel(new_window, text="GeeksforGeeks is best for learning ANYTHING !!").pack()
            return True
        elif user_entry.get() == username and user_pass.get() != password:
            tkmb.showwarning(title='Wrong password', message='Please check your password')
        elif user_entry.get() != username and user_pass.get() == password:
            tkmb.showwarning(title='Wrong username', message='Please check your username')
        else:
            tkmb.showerror(title="Login Failed", message="Invalid Username and password")

    label = CTkLabel(app, text="This is the main UI page")

    label.pack(pady=20)

    frame = CTkFrame(master=app)
    frame.pack(pady=20, padx=40, fill='both', expand=True)

    label = CTkLabel(master=frame, text='Modern Login System UI')
    label.pack(pady=12, padx=10)

    user_entry = CTkEntry(master=frame, placeholder_text="Username")
    user_entry.pack(pady=12, padx=10)

    user_pass = CTkEntry(master=frame, placeholder_text="Password", show="*")
    user_pass.pack(pady=12, padx=10)

    button = CTkButton(master=frame, text='Login', command=login)
    button.pack(pady=12, padx=10)

    checkbox = CTkCheckBox(master=frame, text='Remember Me')
    checkbox.pack(pady=12, padx=10)


class App(CTk):
    def __init__(self, objects,start):
        super().__init__()
        self.title("ServerEye")
        self.objects = objects
        self.start = start
        self.create()

    def create(self):
        self.geometry(f'{1200}x{600}')
        self.minsize(500, 300)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.side_menu = SideMenu(self, self.objects)
        self.side_menu.grid(row=0, column=0, sticky="ns")
        self.main = MainFrame(self, self.objects, self.start)
        self.main.grid(row=0, column=1, sticky="nsew")

class SideMenu(CTkScrollableFrame):
    def __init__(self, parent, objects):
        super().__init__(parent, width = 70, fg_color = "transparent")
        self.objects = objects
        self.parent = parent
        self.masterio = parent
        self.create()

    def create(self):
        for obj in self.objects:
           LogoButton(self,obj,self.masterio)

class MainFrame(CTkFrame):
    def __init__(self, parent,objects,start):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for o in objects:
            if type(o) == Base:
                frame = StartFrame(self)
                self.frames[o.id] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            elif type(o) == Server:
                frame = GenServerFrame(self,o)
                self.frames[o.id] = frame
                frame.grid(row=0, column=0, sticky="nsew")
                members = MembersServer((o.id*10),o)
                frame2 = MembersServerFrame(self,members)
                self.frames[members.id] = frame2
                frame2.grid(row=0, column=0, sticky="nsew")


        self.change_frame(start)

    def change_frame(self,cont):
        frame = self.frames[cont.id]
        frame.tkraise()

class LogoButton(CTkButton):
    def __init__(self, parent, object, masterio):
        self.object = object
        self.masterio = masterio
        super().__init__(master=parent,text="",corner_radius=10,
                         image=self.get_image(),width=50,height=50,
                         fg_color="transparent",command=self.callback)
        self.pack()

    def get_image(self):
        if type(self.object) == Server or type(self.object) == Member:
            img = Image.open(requests.get(self.object.image, stream=True).raw)
        else:
            img = Image.open(f"images/{self.object.image}")
        return CTkImage(light_image=img, dark_image=img, size=(50, 50))

    def callback(self):
        self.masterio.main.change_frame(self.object)



