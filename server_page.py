from datetime import datetime, timedelta
import requests
from PIL import Image
from customtkinter import CTkFrame, CTkScrollableFrame, CTkLabel, CTkButton, CTkImage
from components import PlotFrame, PlotTableFrame, Tab
from tkcalendar import DateEntry

from data_object import Helper


def time_table(number_days:int):
    end = datetime.now()
    start = end - timedelta(days=number_days)
    return start,end

def datetime_to_string(date: datetime):
    return date.strftime("%d-%m-%Y")

class GenServerFrame(CTkFrame):
    def __init__(self,parent,server):
        super().__init__(parent)
        self.part = parent
        self.days = 7
        self.day_start, self.day_end = time_table(self.days)
        self.server = server
        self.create()

    def create(self):
        server = self.server
        frame = CTkScrollableFrame(self)
        CTkLabel(frame, text=f"{server.name}").pack(pady=1)
        ServerBarFrame(frame, server)
        ServerButtonBarFrame(frame,self.part,server)
        ServerDateSelectFrame(frame)
        self.member = MemberServerFrame(frame, self.days, server)
        self.text = TextServerFrame(frame, self.days, server)
        self.voice = VoiceServerFrame(frame, self.days, server)
        frame.pack(side='top', expand=True, fill='both')
        self.frame = frame

class MemberServerFrame(CTkFrame):
    def __init__(self,parent,x,server):
        super().__init__(parent,border_width=1)
        self.starts,self.ends = time_table(x)
        self.server = server
        self.content = self.create()
        self.pack(side = 'top', expand = True, fill = 'x')

    def create(self):
        days, members, log, labels = self.member_data()
        CTkLabel(self, text=f"Członkowie:", anchor="w").pack(pady=5, padx=5, expand=True, fill='x')
        PlotFrame(self, days, [members], ['Liczba członków'], "Liczba członków serwera:")
        PlotFrame(self, days, log, labels,
                  "Liczba użytkowników,\n która dołaczyła, opuściła\n albo została zbanowan\n z serwera:")

    def member_data(self):
        data = self.server.return_members_log_sum(self.starts, self.ends)
        dataKeys = list(data.keys())
        dataKeys.sort()
        newdata = {i: data[i] for i in dataKeys}
        data1 = {}
        data2 = [[],[],[],[]]
        data3 = dataKeys
        acc = self.server.members
        for d in newdata:
            data1[d] = acc - data[d]["left"] + data[d]["join"]
            data2[0].append(data[d]["join"])
            data2[1].append(data[d]["left"])
            data2[2].append(data[d]["ban"])
            data2[3].append(data[d]["unban"])
        return data3,list(data1.values()),data2,["Dołączył","Opuścił","Ban","Unban"]

class TextServerFrame(CTkFrame):
    def __init__(self,parent,x,server):
        super().__init__(parent,border_width=1)
        self.starts,self.ends = time_table(x)
        self.server = server
        self.content = self.create()
        self.pack(side = 'top', expand = True, fill = 'x')

    def create(self):
        message, days, label1 = self.message_data()
        member, mem_data = self.member_data()
        CTkLabel(self, text=f"Wiadomości:", anchor="w").pack(pady=5, padx=5, expand=True, fill='x')
        PlotFrame(self, days, message, label1, "Liczba wiadomości \nw skali całego serwera:")
        gg = [sum(i) for i in mem_data]
        gg, member = (list(t) for t in zip(*sorted(zip(gg, member))))
        PlotTableFrame(self, days, mem_data, member[-7:], gg[-7:], "Top członkowie")
        sad1, sad2 = self.channel_data()
        ss = [sum(i) for i in sad2]
        ss, sad1 = (list(t) for t in zip(*sorted(zip(ss, sad1))))
        PlotTableFrame(self, days, sad2, sad1[-7:], ss[-7:], "Top kanały")

    def message_data(self):
        data1 = [[],[],[]]
        data = self.server.return_sum_text_channel_message(self.starts,self.ends)
        data2 = data.keys()
        for d in data:
            data1[0].append(data[d]["send"])
            data1[1].append(data[d]["mod"])
            data1[2].append(data[d]["del"])
        return data1, list(data2), ["Wysłane","Modyfikowane","Usunięte"]

    def member_data(self):
        data1 = []
        data = self.server.return_sum_member_text_message(self.starts, self.ends)
        for k,d in data.items():
            temp = []
            for v in d:
                temp.append(d[v]["send"])
            data1.append(temp)
        data2 = list(data.keys())
        data2 = [self.server.return_member(i) for i in data2]
        data3 = []
        for i in data2:
            if i is None:
                data3.append(' ')
            else:
                data3.append(i['name'])
        return data3, data1

    def channel_data(self):
        data1 = []
        data = self.server.return_all_text_channel_message(self.starts, self.ends)
        for k,d in data.items():
            temp = []
            for v in d:
                temp.append(d[v]["send"])
            data1.append(temp)
        data2 = list(data.keys())
        data2 = [self.server.return_text(i) for i in data2]
        data3 = []
        for i in data2:
            if i is None:
                data3.append(' ')
            else:
                data3.append(i['name'])
        return data3, data1

class VoiceServerFrame(CTkFrame):
    def __init__(self,parent,x,server):
        super().__init__(parent,border_width=1)
        self.starts,self.ends = time_table(x)
        self.server = server
        self.content = self.create()
        self.pack(side = 'top', expand = True, fill = 'x')

    def create(self):
        voice, days, label1 = self.voice_data()
        member, voice_data = self.member_data()
        CTkLabel(self, text=f"Audio:", anchor="w").pack(pady=5, padx=5, expand=True, fill='x')
        PlotFrame(self, days, voice, label1, "Liczba godzin \nw skali całego serwera:")
        gg = [sum(i) for i in voice_data]
        gg, member = (list(t) for t in zip(*sorted(zip(gg, member))))
        PlotTableFrame(self, days, voice_data, member[-7:], gg[-7:], "Top członkowie")
        sad1, sad2 = self.channel_data()
        ss = [sum(i) for i in sad2]
        ss, sad1 = (list(t) for t in zip(*sorted(zip(ss, sad1))))
        PlotTableFrame(self, days, sad2, sad1[-7:], ss[-7:], "Top kanały")

    def voice_data(self):
        temp = {}
        data = self.server.return_sum_member_voice_channel_hours(self.starts,self.ends)
        for d,values in data.items():
            for v in values:
                if v not in temp.keys():
                    temp[v] = 0
                temp[v] = values[v]

        data1 = temp.values()
        data2 = temp.keys()
        return [data1], list(data2), ["Liczba godzin spedzonych na czatach głosowych"]

    def member_data(self):
        data1 = []
        data = self.server.return_sum_member_voice_channel_hours(self.starts, self.ends)
        for value in data.values():
            data1.append(value.values())

        data2 = list(data.keys())
        data2 = [self.server.return_member(i) for i in data2]
        data3 = []
        for i in data2:
            if i is None:
                data3.append(' ')
            else:
                data3.append(i['name'])
        return data3, data1

    def channel_data(self):
        data1 = []
        data = self.server.return_all_member_voice_channel_hours(self.starts, self.ends)
        temp = {}
        for k,value in data.items():
            if data[k] != {}:
                temp[k] = {}
            for v in value.values():
                for key, val in v.items():
                    if key not in temp[k].keys():
                        temp[k][key] = 0
                    temp[k][key] += val
        for i in temp.values():
            data1.append(i.values())
        data2 = list(temp.keys())
        data2 = [self.server.return_voice(i) for i in data2]
        data3 = []
        for i in data2:
            if i is None:
                data3.append(' ')
            else:
                data3.append(i['name'])
        return data3, data1

class ServerButtonBarFrame(CTkFrame):
    def __init__(self,parent,masterio,server):
        super().__init__(parent,fg_color="#313030")
        FrameButton(self,server,masterio,"Członkowie serwera")
        FrameButton(self,server,masterio, "Kanały serwera")
        self.pack()

class FrameButton(CTkButton):
    def __init__(self, parent,object, masterio,text):
        self.masterio = masterio
        self.object = object
        super().__init__(master=parent, text=text, corner_radius=10,
                         image=self.get_image(), width=20, height=20,
                         fg_color="transparent", command=self.callback)
        self.pack(side="left")

    def callback(self):
        obj = Helper(self.object.id * 10)
        self.masterio.change_frame(obj)

    def get_image(self):
        img = Image.open("images/arrow_right.png")
        return CTkImage(light_image=img,dark_image=img,size=(20,20))

class ServerBarFrame(CTkFrame):
    def __init__(self,parent,server):
        super().__init__(parent,border_width=1,fg_color="#313030")
        self.server = server
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure((1,2), weight=2)
        self.create()
        self.pack(expand=True,fill="x")

    def create(self):
        label1 = CTkLabel(self, image=self.get_image(),text="",fg_color="#313030")
        label1.grid(row=0,column=0,sticky = 'nsew')
        label2 = Tab(self,["Nazwa serwera:","ID serwera:"],[self.server.name,self.server.id])
        label2.grid(row=0,column=1)
        label2 = Tab(self, ["Liczba członków:","Liczba kanałów tekstowych:","Liczba kanałów głosowych:"], [self.server.members,self.server.text,self.server.voice])
        label2.grid(row=0, column=2)

    def get_image(self):
        img = Image.open(requests.get(self.server.image, stream=True).raw)
        return CTkImage(light_image=img,dark_image=img,size=(70,70))

class ServerDateSelectFrame(CTkFrame):
    def __init__(self,parent):
        super().__init__(parent,border_width=1,fg_color="#313030")
        self.paren = parent
        self.start_date = DateEntry(self, date_pattern="yyyy-mm-dd")
        self.start_date.set_date((datetime.now()-timedelta(days=7)))
        self.start_date.pack(side="left")
        self.end_date = DateEntry(self, date_pattern="yyyy-mm-dd")
        self.end_date.pack(side="left")
        self.button = CTkButton(self, text="Szukaj", command=self.callback)
        self.button.pack(side="left")
        self.pack()

    def callback(self):
        date1 = self.start_date.get()
        date2 = self.end_date.get()
        self.paren.day_start = datetime.strptime(date1,"%Y-%m-%d")
        self.paren.day_end = datetime.strptime(date2,"%Y-%m-%d")
        print(self.paren.day_start,self.paren.day_end)


