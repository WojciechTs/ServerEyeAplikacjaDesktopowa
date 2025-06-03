from tkinter.ttk import Treeview
from customtkinter import CTkFrame, CTkLabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class PlotFrame(CTkFrame):
    def __init__(self,parent,x,data: dict,labels,text):
        super().__init__(parent)
        self.text = text
        self.x =x
        self.data = data
        self.labels = labels
        self.create()
        self.pack(pady=5, padx=5,side = 'top', expand = True, fill = 'x')

    def create(self):
        text = self.text
        data = self.data
        labels = self.labels
        x = self.x
        CTkLabel(self, text=f"{text}").pack(side="left", padx=5)
        fig = Figure(figsize=(7, 3), dpi=100)
        plot = fig.add_subplot()

        for v, lab in zip(data, labels):
            plot.plot(x, v, label=lab)
        plot.legend()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", expand=True, fill="x")


class PlotTableFrame(CTkFrame):
    def __init__(self, parent, x, data: dict, members,extra,text):
        super().__init__(parent)
        frame = CTkFrame(self)
        CTkLabel(frame, text=f"{text}").pack(pady=1)
        TableFrame(frame, members,extra)
        frame.pack(side="left")
        fig = Figure(figsize=(7,3),dpi = 100)
        plot = fig.add_subplot()
        for v, lab in zip(data, members):
            plot.plot(x, v, label=lab)
        plot.legend()

        canvas = FigureCanvasTkAgg(fig,master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", expand=True,fill="x")
        self.pack(pady=5, padx=5,side = 'top', expand = True, fill = 'x')

class TableFrame(Treeview):
    def __init__(self,parent,data,extra):
        super().__init__(parent,columns=('middle','last'), show = 'headings')
        self.heading('middle', text='Nick')
        self.column('middle',width=120)
        self.heading('last', text='Ilośc')
        self.column('last',  width=70)
        self.pack(side="left")
        for d,e in zip(data,extra):
            x = d
            dd = (x,e)
            self.insert(parent='', index=0, values=dd)

class Tab(CTkFrame):
    def __init__(self,parent, data1, data2):
        super().__init__(parent,fg_color="#313030")
        for x, y in zip(data1,data2):
            CTkLabel(self,text=f"{str(x)} {str(y)}").pack()
