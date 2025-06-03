import datetime
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
token = os.environ['TOKEN']
client = MongoClient(token)

def datetime_convert(date: datetime.datetime):
    return datetime.datetime(date.year,date.month,date.day)

def time_list(start: datetime.datetime ,end: datetime.datetime):
    sd = datetime.datetime(start.year,start.month,start.day)
    ed = datetime.datetime(end.year,end.month,end.day)
    d = []
    while sd <= ed:
        d.append(sd)
        sd += datetime.timedelta(days=1)
    return d

class Helper:
    def __init__(self,id):
        self.id = id

class User:
    def __init__(self, id):
        self.id = id
        self.obj = self.database()
        self.servers = self.servers_list()
        self.other = self.other_list()

    def database(self):
        db = client["Users"]
        col = db[str(self.id)]
        output = col.find()
        output = list(output)
        return output

    def return_server(self,id):
        for server in self.servers:
            if server.id == id:
                return server

    def servers_list(self):
        servers = []
        for i in self.obj:
            if i["type"] == "server":
                db = client[str(i["id"])]
                col = db["info"]
                output = col.find()
                output = list(output)
                output = output[0]
                server = Server(output["id"],output["name"],output["members"],output["text"],output["voice"],output["image"],output["created"],output["date"])
                servers.append(server)
        return servers

    def other_list(self):
        other = []
        for i in self.obj:
            if i["type"] != "server":
                db = client[str(i["master"])]
                col = db["members"]
                output = col.find({"id": i["id"]})
                output = list(output)
                output = output[0]
                if i["type"] == "member":
                    obj = Member(output["id"],output["name"],output["nick"],output["image"],output["created"],output["join"],self.return_server(i["master"]))
                    other.append(obj)
                elif i["type"] == "voice":
                    obj = Text(output["id"], output["name"], output["image"], output["created"], self.return_server(i["master"]))
                    other.append(obj)
                elif i["type"] == "text":
                    obj = Voice(output["id"], output["name"], output["image"], output["created"],self.return_server(i["master"]))
                    other.append(obj)
        return other

class Base:
    def __init__(self, id: int,name: str, image: str):
        self.id = id
        self.name = name
        self.image = image

class Server(Base):
    def __init__(self,id: int,name: str,members: int,text: int,voice: int, image: str, created: datetime.datetime, join: datetime.datetime):
        super().__init__(id,name,image)
        self.members = members
        self.text = text
        self.voice = voice
        self.created = created
        self.join = join

    def return_all_members(self):
        db = client[str(self.id)]
        col = db["members"]
        output = col.find()
        output = list(output)
        return output

    def return_member(self, id):
        db = client[str(self.id)]
        col = db["members"]
        output = col.find_one({"id":int(id)})
        return output

    def return_all_texts(self):
        db = client[str(self.id)]
        col = db["texts"]
        output = col.find()
        output = list(output)
        return output

    def return_text(self, id):
        db = client[str(self.id)]
        col = db["texts"]
        output = col.find_one({"id":int(id)})
        return output

    def return_all_voices(self):
        db = client[str(self.id)]
        col = db["voices"]
        output = col.find()
        output = list(output)
        return output

    def return_voice(self, id):
        db = client[str(self.id)]
        col = db["voices"]
        output = col.find_one({"id":int(id)})
        return output

    def return_members_log_sum(self, greater, less):
        db = client[str(self.id)]
        col = db["members_log"]
        output = col.find({"date": {"$gt":greater, "$lt":less}})
        output = list(output)
        temp = {}
        test_time = time_list(greater, less)
        for item in output:
            date = datetime_convert(item["date"])
            if date not in temp.keys():
                temp[date] = {"join": 0, "left": 0, "ban": 0, "unban": 0}
            temp[date][item["tag"]] += 1
        for i in test_time:
            if i not in temp.keys():
                temp[i] = {"join": 0, "left": 0, "ban": 0, "unban": 0}
        return temp

    def return_text_channel_message(self, id, greater, less):
        db = client[str(self.id)]
        col = db[str(id)]
        output = col.find({"date": {"$gt":greater, "$lt":less}})
        output = list(output)
         
        temp = {}
        test_time = time_list(greater, less)
        for item in output:
            date = datetime_convert(item["date"])
            if date not in temp.keys():
                temp[date] = {"send": 0, "del": 0, "mod": 0}
            temp[date][item["tag"]] += 1
        for i in test_time:
            if i not in temp.keys():
                temp[i] = {"send": 0, "del": 0, "mod": 0}
        data = temp
        dataKeys = list(data.keys())
        dataKeys.sort()
        newdata = {i: data[i] for i in dataKeys}
        return newdata

    def return_all_text_channel_message(self, greater, less):
        arr1 = {}
        for text in self.return_all_texts():
            arr1[str(text["id"])] = self.return_text_channel_message(text["id"], greater, less)
        return arr1

    def return_sum_text_channel_message(self, greater, less):
        arr = {}
        temp = self.return_all_text_channel_message(greater, less)
        for v in temp.values():
            for kv, vv in v.items():
                if kv not in arr.keys():
                    arr[kv] = {"send":0,"del":0,"mod":0}
                arr[kv]["send"] += vv["send"]
                arr[kv]["del"] += vv["del"]
                arr[kv]["mod"] += vv["mod"]
        return arr

    def return_member_text_channel_message(self, id, greater, less):
        db = client[str(self.id)]
        col = db[str(id)]
        output = col.find({"date": {"$gt":greater, "$lt":less}})
        output = list(output)
         
        test_time = time_list(greater, less)
        temp = {}
        for item in output:
            member = str(item["member"])
            if member not in temp.keys():
                temp[member] = {}
            date = datetime_convert(item["date"])
            if date not in temp[member].keys():
                temp[member][date] = {"send": 0, "del": 0, "mod": 0}
            temp[member][date][item["tag"]] += 1
        for i in test_time:
            for u, j in temp.items():
                if i not in j.keys():
                    temp[u][i] = {"send": 0, "del": 0, "mod": 0}
        data = temp
        dataKeys = list(data.keys())
        dataKeys.sort()
        newdata = {i: data[i] for i in dataKeys}
        return newdata

    def return_all_member_text_channel_message(self, greater, less):
        arr1 = {}
        for text in self.return_all_texts():
            arr1[str(text["id"])] = self.return_member_text_channel_message(text["id"], greater, less)
        return arr1

    def return_sum_member_text_message(self, greater, less):
        arr = {}
        temp = self.return_all_member_text_channel_message(greater, less)
        for v in temp.values():
            for member, vv in v.items():
                if member not in arr.keys():
                    arr[member] = {}
                for date, vvv in vv.items():
                    if date not in arr[member].keys():
                        arr[member][date] = {"send": 0, "del": 0, "mod": 0}
                    arr[member][date]["send"] += vvv["send"]
                    arr[member][date]["del"] += vvv["del"]
                    arr[member][date]["mod"] += vvv["mod"]
        return arr

    def return_member_voice_channel_hours(self, id, greater, less):
        db = client[str(self.id)]
        col = db[str(id)]
        output = col.find({"date": {"$gt":greater, "$lt":less}})
        output = list(output)
         
        temp = {}
        temp2 = {}
        test_time = time_list(greater, less)
        for item in output:
            member = item["member"]
            if member not in temp.keys():
                temp[member] = {"join":[],"exit":[]}

            if item["tag"] == "join":
                temp[member]["join"].append(item)
            elif item["tag"] == "exit":
                temp[member]["exit"].append(item)

        for memb,item in temp.items():
            if memb not in temp2.keys():
                temp2[memb] = {}
            # if item["join"][0] > item["exit"][0]:
            #     item["exit"].pop(0)
            # if item["join"][-1] < item["exit"][-1]:
            #     item["join"].pop(-1)
            for i,j in zip(item["join"],item["exit"]):
                x = datetime_convert(i["date"])
                y = datetime_convert(j["date"])
                x1 = i["date"]
                y1 = j["date"]
                if x not in temp2[memb].keys():
                    temp2[memb][x] = 0
                if y not in temp2[memb].keys():
                    temp2[memb][y] = 0
                if x == y:
                    temp2[memb][x] += (((y1-x1).total_seconds()) /60)/60
                else:
                    if (((y1-x1).total_seconds()) /60)/60 < 24:
                        z1 = datetime.datetime(y1.year,y1.month,y1.day)
                        temp2[memb][x] += (((z1 - x1).total_seconds()) / 60) / 60
                        temp2[memb][y] += (((y1 - z1).total_seconds()) / 60) / 60
                    else:
                        z1 = datetime.datetime(x1.year, x1.month, x1.day+1)
                        z2 = datetime.datetime(y1.year, y1.month, y1.day)
                        temp2[memb][x] += (((z1 - x1).total_seconds()) / 60) / 60
                        temp2[memb][y] += (((y1 - z2).total_seconds()) / 60) / 60
                        for i in time_list(i["date"],j["date"]):
                            if i not in [x,y]:
                                temp2[memb][i] = 24.0

        for i in test_time:
            for k,ite in temp2.items():
                if i not in ite.keys():
                    temp2[k][i] = 0
        data = temp2
        newtemp = {}
        for d,v in data.items():
            dataKeys = list(v.keys())
            dataKeys.sort()
            newdata = {i: v[i] for i in dataKeys}
            newtemp[d] = newdata
        return newtemp

    def return_all_member_voice_channel_hours(self, greater, less):
        arr1 = {}
        for voice in self.return_all_voices():
            arr1[str(voice["id"])] = self.return_member_voice_channel_hours(voice["id"], greater, less)
        return arr1

    def return_sum_member_voice_channel_hours(self, greater, less):
        arr = {}
        temp = self.return_all_member_voice_channel_hours(greater, less)
        for v in temp.values():
            for member, vv in v.items():
                if member not in arr.keys():
                    arr[member] = {}
                for date, vvv in vv.items():
                    if date not in arr[member].keys():
                        arr[member][date] = 0
                    arr[member][date] += vvv
        return arr

class MembersServer:
    def __init__(self,id, server: Server):
        self.server = server
        self.id = id
        self.members = []
        for i in self.server.return_all_members():
            nick = i["nick"]
            if nick is None:
                nick = i["name"]
            self.members.append(Member(i["id"],i["name"],nick,i["image"],i["join"],i["created"],self.server))

class ChannelServer:
    def __init__(self, server: Server):
        self.server = server
        self.text = self.text_()
        self.voice = self.voice_()

    def text_(self):
        lista = []
        for i in self.server.return_all_texts():
            lista.append(Text(i["id"],i["name"],i["image"],i["created"],self.server))

    def voice_(self):
        lista = []
        for i in self.server.return_all_voices():
            lista.append(Voice(i["id"],i["name"],i["image"],i["created"],self.server))

class Member(Base):
    def __init__(self, id: int, member: str, username: str, image: str, join: datetime.datetime, created: datetime.datetime, server: Server):
        super().__init__(id, username, image)
        self.member = member
        self.created = created
        self.join = join
        self.server = server

    def return_messages(self,greater,less):
        temp = {}
        data = self.server.return_all_member_text_channel_message(greater,less)
        for key,values in data.items():
            for v in values:
                if v == self.id:
                    temp[key] = values[v]
        return temp

    def return_voice(self,greater,less):
        temp = {}
        data = self.server.return_all_member_voice_channel_hours(greater, less)
        for key, values in data.items():
            if key == self.id:
                temp[key] = values
        return temp

class Text(Base):
    def __init__(self,id: int,name: str, image: str,created: datetime.datetime, server: Server):
        super().__init__(id,name,image)
        self.server = server
        self.created = created
        self.server = server

    def retun_messages(self,greater,less):
        data = self.server.return_member_text_channel_message(self.id,greater, less)
        return data

    def retun_members(self):
        return self.server.return_all_members()


class Voice(Base):
    def __init__(self,id: int,name: str, image: str, created: datetime.datetime, server: Server):
        super().__init__(id,name,image)
        self.server = server
        self.created = created
        self.server = server

    def retun_hours(self,greater,less):
        data = self.server.return_member_voice_channel_hours(self.id,greater, less)
        return data

    def retun_members(self):
        return self.server.return_all_members()