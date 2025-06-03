from PIL import ImageTk, Image
from customtkinter import CTkFrame, CTkLabel
import tkinter as tk

class StartFrame(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        CTkLabel(self, text="Strona główna").pack()
        StartFrameContent(self).pack( expand = True, fill = 'both',pady = 10)

class StartFrameContent(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent,border_width=1,border_color="#ffffff",fg_color="transparent")
        CTkLabel(self, text="Witaj w ServerEye", font=("Segoe UI",20)).pack(pady = 10)
        CTkLabel(self, text="ServerEye jest to aplikacja umożliwiająca swobodne przegladanie i śledzenie aktywności twoich serwerów i ich członków!").pack(pady = 10)
        canvas = tk.Canvas(self,background="#313030",borderwidth=0)
        canvas.pack(expand=True,fill="both")
        global image
        image = ImageTk.PhotoImage(Image.open('images/img.png').resize((canvas.winfo_reqwidth(), canvas.winfo_reqheight())))
        image_canvas = canvas.create_image((canvas.winfo_reqwidth()/1.5,0), anchor = 'nw',image=image)