import requests
from PIL import Image
from customtkinter import CTkFrame, CTkScrollableFrame, CTkLabel, CTkImage, CTkButton, CTkToplevel

from components import Tab, PlotFrame, PlotTableFrame
from data_object import MembersServer
from server_page import ServerDateSelectFrame, time_table
from tests.test7 import member


class MembersServerFrame(CTkFrame):
    def __init__(self,parent,member_server: MembersServer):
        super().__init__(parent)
        self.member_server = member_server
        self.create()


    def create(self):
        frame = CTkScrollableFrame(self)
        CTkLabel(frame, text=f"{self.member_server.server.name} - Członkowie").pack(side="top",pady=1)
        MemberContainerFrame(frame,self.member_server.members)
        frame.pack(side='top', expand=True, fill='both')
        self.frame = frame


class MemberContainerFrame(CTkFrame):
    def __init__(self,parent,members):
        super().__init__(parent,border_width=1)
        self.members = members
        self.content = self.create()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure([i for i in range(10)], weight=1)
        self.pack(side = 'top', expand = True, fill = 'x')

    def create(self):
        n = 0
        row = 0
        col =0
        for member in self.members:
            if n <50:
                frame = MemberCardFrame(self, member)
                frame.grid(row=row, column=col, sticky="nsew")
                col += 1
                if col == 9:
                    col = 0
                    row += 1
                n+=1



class MemberCardFrame(CTkButton):
    def __init__(self,parent,member):
        self.member = member
        super().__init__(master=parent, text=f"{self.member.member}\n\n{self.member.name}", corner_radius=10,
                         image=self.get_image(), width=50, height=50,
                         fg_color="transparent", command=self.callback,compound="top")



    def get_image(self):
        try:
            img = Image.open(requests.get(self.member.image, stream=True).raw)
        except:
            img = Image.open(f"images/default.png")
        return CTkImage(light_image=img, dark_image=img, size=(70, 70))

    def callback(self):
        MemberWindow(self,self.member)


class MemberWindow(CTkToplevel):
    def __init__(self,parent,member):
        super().__init__(parent)
        self.member = member
        self.days = 7
        self.day_start, self.day_end = time_table(self.days)
        self.title = f"ServerEye - {member.member}"
        self.geometry("1200x600")
        self.create()

    def create(self):
        frame = CTkScrollableFrame(self)
        CTkLabel(frame, text=f"{self.member.member}").pack(pady=1)
        UserBarFrame(frame, self.member)
        ServerDateSelectFrame(frame)
        self.text = TextMemberFrame(frame, self.days, self.member)
        #self.voice = VoiceServerFrame(frame, self.days, member)
        frame.pack(side='top', expand=True, fill='both')
        self.frame = frame

class UserBarFrame(CTkFrame):
    def __init__(self, parent, member):
        super().__init__(parent)
        self.member = member
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure((1, 2), weight=2)
        self.create()
        self.pack(expand=True, fill="x")

    def create(self):
        label1 = CTkLabel(self, image=self.get_image(), text="", fg_color="#313030")
        label1.grid(row=0, column=0, sticky='nsew')
        label2 = Tab(self, ["Nazwa członka:","Nick członka", "ID:"], [self.member.member, self.member.name,self.member.id])
        label2.grid(row=0, column=1)


    def get_image(self):
        img = Image.open(requests.get(self.member.image, stream=True).raw)
        return CTkImage(light_image=img, dark_image=img, size=(70, 70))

class TextMemberFrame(CTkFrame):
    def __init__(self,parent,x,member):
        super().__init__(parent,border_width=1)
        self.starts,self.ends = time_table(x)
        self.member = member
        self.content = self.create()
        self.pack(side = 'top', expand = True, fill = 'x')

    def create(self):
        message, days, label1 = self.message_data()
        CTkLabel(self, text=f"Wiadomości:", anchor="w").pack(pady=5, padx=5, expand=True, fill='x')
        PlotFrame(self, days, message, label1, "Liczba wiadomości \nw skali całego serwera:")
        sad1, sad2 = self.channel_data()
        ss = [sum(i) for i in sad2]
        ss, sad1 = (list(t) for t in zip(*sorted(zip(ss, sad1))))
        PlotTableFrame(self, days, sad2, sad1[-7:], ss[-7:], "Top kanały")

    def message_data(self):
        data1 = [[],[],[]]
        data = self.member.server.return_sum_text_channel_message(self.starts,self.ends)
        data2 = data.keys()
        print(data)
        for d in data:
            data1[0].append(data[d]["send"])
            data1[1].append(data[d]["mod"])
            data1[2].append(data[d]["del"])
        return data1, list(data2), ["Wysłane","Modyfikowane","Usunięte"]



    def channel_data(self):
        data1 = []
        data = self.member.server.return_all_text_channel_message(self.starts, self.ends)
        for k,d in data.items():
            temp = []
            for v in d:
                temp.append(d[v]["send"])
            data1.append(temp)
        data2 = list(data.keys())
        data2 = [self.member.server.return_text(i) for i in data2]
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
