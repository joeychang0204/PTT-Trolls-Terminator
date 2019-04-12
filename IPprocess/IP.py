import json
import statistics
from collections import defaultdict

class IPProcessor:
    def __init__(self):
        self.normals= set()
        self.trolls= set()
        self.normalIPs = defaultdict(set)
        self.trollIPs = defaultdict(set)
        self.IPusers= defaultdict(set)

    def AddToSet(self, author, ip):
        if author in self.normals:
            self.normalIPs[author].add(ip)
        elif author in self.trolls:
            self.trollIPs[author].add(ip)
        self.IPusers[ip].add(author)

    def printIPs(author):
        if author in self.normals:
            for key in self.normals:
                print(key, end = ' ')
                for IP in self.normalIPs[key]:
                    print(IP, end = ' ')
                print()
        if author in self.trolls:
            for key in self.trolls:
                print(key, end = ' ')
                for IP in self.trollIPs[key]:
                    print(IP, end = ' ')
                print()

    def loadfiles(self):
        # read troll and normal users from training sets
        with open("user_comments.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        for user_comment in data["user_comments"]:
            if user_comment["isTroll"] is True:
                self.trolls.add(user_comment["id"])
            else:
                self.normals.add(user_comment["id"])

        # read author, ip from raw data
        with open("Gossiping-20400-24800.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        for article in data["articles"]:
            # extract article IP 
            if article.get("author") and article.get("ip"):
                author= article["author"].split()[0]
                ip= article["ip"]
                self.AddToSet(author, ip)

            # extract comments IP 
            for comment in article["messages"]:
                if comment.get("push_userid") and comment.get("push_ipdatetime"):
                    author = comment["push_userid"]
                    ip = comment["push_ipdatetime"].split()[0]
                    self.AddToSet(author, ip)

    def domath(self):
        # numbers= []
        # for key in self.IPusers:
        #     if len(self.IPusers[key]) < 10000:
        #         numbers.append(len(self.IPusers[key]))
        numbers = [len(self.IPusers[key]) for key in self.IPusers if len(self.IPusers[key])< 10000]
        mean = statistics.mean(numbers)
        std= statistics.stdev(numbers)

        print("avg per IP used by %3f users\nstdev: %3f" % (mean, std))
        #weirdUserByIP= []
        for num in numbers:
            if num > 40:
                print(num)
                #weirdUserByIP.append()
                
        

    
if __name__=="__main__":
    cIP= IPProcessor()
    cIP.loadfiles()
    cIP.domath()