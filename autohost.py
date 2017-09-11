from json import loads
from urllib.request import urlopen
import urllib.request, socket, time, random, os

class auto(object):
    def __init__(self):
        os.system("clear")
        live = False
        names = []
            
        data_chl = self.socket("https://api.twitch.tv/kraken/search/streams?query=")
        check = self.socket("http://tmi.twitch.tv/hosts?include_logins=1&host=")

        #Getting the list of names of people that are currently streaming with PrimRP in their title    
        for line in data_chl["streams"]:
            if "PrimRP" in line["channel"]["status"]:
                name = line["channel"]["name"]
                live = True
                names.append(name)

        convert = "".join(str(x) for x in names)
        if convert == str(check["hosts"][0]["host_display_name"]):
            print(convert + " was recently hosted looking for new host")
            self.loop(10.0)

        #Checking for the person who is currently hosted and removing them from this host selection
        if check["hosts"][0]["host_display_name"] in names:
            names.remove(check["hosts"][0]["host_display_name"])
                            
        if live == True:
            self.random(names)
        else: 
            print("No streams currently online")
            self.loop(10.0)
            

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
            print("There was an error, trying again")
            self.__init__()

    def random(self, names):
        name = names[random.randint(0, len(names) - 1)]
        self.host(name)

    def host(self, name):
        host = "irc.twitch.tv"
        port = 6667
        user_name = ""
        print("Hosted: " + name)

        s = socket.socket()
        s.connect((host, port))
        s.send(bytes("PASS \r\n", "UTF-8"))
        s.send(bytes("NICK "+ user_name +"\r\n", "UTF-8"))
        s.send(bytes("JOIN #"+ user_name +"\r\n", "UTF-8"))
        #s.send(bytes("PRIVMSG #"+ user_name +" :"+ name +"\r\n", "UTF-8"))
        s.send(bytes("PRIVMSG #"+ user_name +" :/host " + name +"\r\n", "UTF-8"))
        self.loop(1860.0)

    def loop(self, seconds):
        print("Trying again in "+ str(seconds) + " seconds")
        time.sleep(seconds)
        self.__init__()
auto()
