import tkinter

from data_object import Base, User
from app import App


obj = Base(id=12334, name="test", image="servereye.png")



if __name__ == '__main__':
    user = User(683312181932195856)
    lista = [obj]
    lista += user.servers
    lista += user.other
    root = App( lista, obj)
    search_time = tkinter.IntVar(value=7)
    root.mainloop()
