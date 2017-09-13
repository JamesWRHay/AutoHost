from json import loads
from urllib.request import urlopen
import urllib.request, socket, time, random, os

class auto(object):
    def __init__(self):
        #Add your query and channel name of the hosting channel
        query = ""
        host_chnl = ""
        oauth = ""
        
        live = False
        names = []
            
        data_chl = self.socket("https://api.twitch.tv/kraken/search/streams?query=" + query, oauth)
        _id = str(self.socket("https://api.twitch.tv/kraken/search/channels?query=" + host_chnl + "&type=suggest", oauth)["channels"][0]["_id"])
        check = self.socket("http://tmi.twitch.tv/hosts?include_logins=1&host=" + _id, oauth)

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

        #Checking for the person who is currently hosted if there is one and removing them from this host selection
        if check["hosts"][0]["host_display_name"] in names:
            names.remove(check["hosts"][0]["host_display_name"])
                            
        if live == True:
            self.random(names, query, oauth, host_chnl)
        else: 
            self.clr_print("No " + query + " streams currently online")
            self.loop(300.0)
    
    #"clr_print" clears the console output before printing a message just for easier reading
    def clr_print(self, msg):
        #os.system("clear") #Linux
        os.system("clr") #Windows
        print(msg)

    def log(self):
        #Add a log that puts the name and the time of when someone is hosted
        logged = open("Log", "w")
        logged.write("\n" + name)

    #The socket method requests information from APIs and returns information in a JSON format  
    def socket(self, url, oauth):
        try:
            req = urllib.request.Request(url)
            req.add_header("Client-ID", oauth)
            req.add_header("Accept", "application/vnd.twitchtv.v5+json")
            resp = urllib.request.urlopen(req)
            data = resp.read()
            data_chl = loads(data.decode("utf-8"))
            return data_chl
        except:
            self.clr_print("There was an error, trying again")
            self.__init__()

    #The random method takes the list of names and randomly selects a name to keep things fair
    def random(self, names, query, oauth, host_chnl):
        name = names[random.randint(0, len(names) - 1)]
        self.host(name, query, oauth, host_chnl)

    #The host method just uses opens an IRC session and hosts the randomly selected channel name
    def host(self, name, query, oauth, host_chnl):
        host = "irc.twitch.tv"
        port = 6667
        self.clr_print("Hosted: " + name)

        s = socket.socket()
        s.connect((host, port))
        s.send(bytes("PASS oauth:" + oauth + "\r\n", "UTF-8"))
        s.send(bytes("NICK "+ host_chnl.lower() +"\r\n", "UTF-8"))
        s.send(bytes("JOIN #"+ host_chnl.lower() +"\r\n", "UTF-8"))
        s.send(bytes("PRIVMSG #"+ host_chnl.lower() +" :/unhost\r\n", "UTF-8"))
        s.send(bytes("PRIVMSG #"+ host_chnl.lower() +" :/host " + name +"\r\n", "UTF-8"))
        self.loop(1860.0)

    #The loop method does what you'd think, it just loops the class after a set amount of time
    def loop(self, seconds):
        self.clr_print("Trying again in "+ str(seconds) + " seconds")
        time.sleep(seconds)
        self.__init__()
auto()
