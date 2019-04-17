import json
import statistics
from collections import defaultdict
import re
import geoip2.database


class User:
    def __init__(self):
        self.author= ""
        self.IPs= set()
        self.IPcount= defaultdict(int)
        self.mainlyIP = ""
        self.isTroll = False
        self.region= ""
        
    def addIP(self, ip):
        self.IPs.add(ip)
        self.IPcount[ip] += 1
    
    def checkMainlyUse(self):
        mainly= 0
        for ip in self.IPcount:
            mainly = max(mainly, self.IPcount[ip])
            if mainly == self.IPcount[ip]:
                self.mainlyIP= ip

class IPProcessor:
    def __init__(self):
        self.DBreader = geoip2.database.Reader('GeoLite2-City.mmdb')
        self.allUser= {}
        self.normals= set() # all normal users
        self.trolls= set() 
        self.normalIPs = defaultdict(set) # normal author -> IPs
        self.trollIPs = defaultdict(set)
        self.otherIPs= defaultdict(set)
        self.IPusers = defaultdict(set)  # IP -> authors use this IP
        self.region= defaultdict(int)
        population_mean= 0.0 # calculate the mean of how many IP used per user in the population
        population_stdev= 0.0 # standard deviation
        normal_mean= 0.0
        normal_stdev= 0.0
        troll_mean= 0.0
        troll_stdev= 0.0

    def AddToSet(self, author, ip):
        if "." not in ip:
            #print(author, ip)
            return

        if author in self.normals:
            self.normalIPs[author].add(ip)
        elif author in self.trolls:
            self.trollIPs[author].add(ip)
        else:
            self.otherIPs[author].add(ip)
            if author not in self.allUser:
                newuser = User()
                newuser.author = author
                self.allUser[newuser.author] = newuser
            #else:
            #    print("this author exist in database")
                
        self.allUser[author].addIP(str(ip))
        self.IPusers[ip].add(author)
        
        # unit test 
        #if author == "q13461346" or author == "Carrarese":
        #    self.testAddToSet(author, ip)
        

    def testAddToSet(self, author, ip):
        print("TestAdd %s, %s " %(author, ip), end=' ')
        print(self.allUser[author].IPcount[ip])

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

    def testinit(self):
        print("len of normal users: %d" % (len(self.normals)))
        for normaluser in self.normals:
            print("ID is %s, %s, %r" % (normaluser, self.allUser[normaluser].author, self.allUser[normaluser].isTroll))
        print("len of troll users: %d" % (len(self.trolls)))
        for trolluser in self.trolls:
            print("ID is %s, %s, %r" % (trolluser, self.allUser[trolluser].author, self.allUser[trolluser].isTroll))
    
    def initUsers(self):
        for normaluser in self.normals:
            newuser = User()
            newuser.author = normaluser
            self.allUser[newuser.author]= newuser
        
        for trolluser in self.trolls:
            newuser = User()
            newuser.author = trolluser
            newuser.isTroll = True
            self.allUser[newuser.author]= newuser

    def loadfiles(self):
        # read troll and normal users from training sets
        with open("user_comments.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        for user_comment in data["user_comments"]:
            if user_comment["isTroll"] is True:
                self.trolls.add(user_comment["id"])
            else:
                self.normals.add(user_comment["id"])

        # construct trolls and normal user instance
        self.initUsers() 
        #self.testinit()

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

        for author in self.allUser:
            self.allUser[author].checkMainlyUse()
            self.allUser[author].region = self.IPRegion(self.allUser[author].mainlyIP)
            self.region[self.allUser[author].region] += 1
        #print test log
        #for author in self.allUser:
        #    print("%s mainly use ip: %s"% (author, self.allUser[author].mainlyIP))

    def domath(self):
        numbers = [len(self.IPusers[key]) for key in self.IPusers] #if len(self.IPusers[key])< 10000]
        self.population_mean = statistics.mean(numbers)
        self.population_stdev= statistics.stdev(numbers)
        print("avg per IP used by %3f users\nstdev: %3f" % (self.population_mean, self.population_stdev))

        numbers = [len(self.normalIPs[key]) for key in self.normalIPs]
        self.normal_mean = statistics.mean(numbers)
        self.normal_stdev= statistics.stdev(numbers)
        print("avg normal user use %3f IP\nstdev: %3f" % (self.normal_mean, self.normal_stdev))

        numbers = [len(self.trollIPs[key]) for key in self.trollIPs]
        self.troll_mean = statistics.mean(numbers)
        self.troll_stdev= statistics.stdev(numbers)
        print("avg troll user use %3f IP\nstdev: %3f" % (self.troll_mean, self.troll_stdev))
    
    def compIP(self, author):
        if author in normals:
            numIP= normalIPs[author]
            if numIP > self.normal_mean+ 2* self.normal_stdev or numIP < self.normal_mean-self.normal_stdev:
                print("this ID in normal is outlier, can be consider as trolls")
        elif author in trolls:
            numIP= trollIPs[author]
            # might need to discuss
            if numIP > self.normal_mean+ 2* self.normal_stdev or numIP < self.normal_mean-self.normal_stdev:
                print("this ID in trolls is outlier, can be consider as trolls")
        
    def NumOfIPweird(self, author):
        #given id, compare the count of IP used by this author with mean of normal user 
        if author not in normals or trolls:
            print("the ID is not in the set")
        compIP(author)
    
    def IPRegion(self, ip):
        response = self.DBreader.city(ip)
        return response.country.name
    
    def SummarizeRegion(self):
        for key in self.region:
            print(key, self.region[key])
    
    
if __name__=="__main__":
    cIP = IPProcessor()
    cIP.loadfiles()
    #cIP.SummarizeRegion()
    #cIP.domath()