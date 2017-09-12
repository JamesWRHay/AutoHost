from json import loads
from urllib.request import urlopen
import urllib.request, socket, time, random, os

class auto(object):
    def __init__(self):
        live = False
        names = []
        query = ""
        client_id = ""
            
        data_chl = self.socket("https://api.twitch.tv/kraken/search/streams?query=" + query)
        check = self.socket("http://tmi.twitch.tv/hosts?include_logins=1&host=" + client_id)

        #Getting the list of names of people that are currently streaming with query in their title    
        for line in data_chl["streams"]:
            if query in line["channel"]["status"]:
                name = line["channel"]["name"]
                live = True
                names.append(name)

        try:
            convert = "".join(str(x) for x in names)
            if convert == str(check["hosts"][0]["target_login"]):
                self.clr_print(convert + " was recently hosted looking for new host")
                self.loop(300.0)
        except:
            print("No one is hosted")

        #Checking for the person who is currently hosted and removing them from this host selection
        if check["hosts"][0]["host_display_name"] in names:
            names.remove(check["hosts"][0]["host_display_name"])
                            
        if live == True:
            self.random(names, query)
        else: 
            self.clr_print("No " + query + " streams curretly online")
            self.loop(300.0)
            
    def clr_print(self, msg):
        #os.system("clear") Linux
        os.system("cls") #Windows
        print(msg)

    def socket(self, url):
        try:
            req = urllib.request.Request(url)
            req.add_header("Client-ID", "")
            req.add_header("Accept", "application/vnd.twitchtv.v5+json")
            resp = urllib.request.urlopen(req)
            data = resp.read()
            data_chl = loads(data.decode("utf-8"))
            return data_chl
        except:
            self.clr_print("There was an error, trying again")
            self.__init__()

    def random(self, names, query):
        name = names[random.randint(0, len(names) - 1)]
        self.host(name, query)

    def host(self, name, query):
        host = "irc.twitch.tv"
        port = 6667
        user_name = ""
        self.clr_print("Hosted: " + name)

        s = socket.socket()
        s.connect((host, port))
        s.send(bytes("PASS oauth:\r\n", "UTF-8"))
        s.send(bytes("NICK "+ user_name +"\r\n", "UTF-8"))
        s.send(bytes("JOIN #"+ user_name +"\r\n", "UTF-8"))
        s.send(bytes("PRIVMSG #"+ user_name +" :/unhost\r\n", "UTF-8"))
        s.send(bytes("PRIVMSG #"+ user_name +" :/host " + name +"\r\n", "UTF-8"))
        self.loop(1860.0)

    def loop(self, seconds):
        self.clr_print("Trying again in "+ str(seconds) + " seconds")
        time.sleep(seconds)
        self.__init__()
auto()
