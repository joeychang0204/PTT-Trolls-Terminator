import json
import codecs
class dataProcessor:
    def __init__(self):
        self.user_content = {}
        self.user_comment = {}
    def loadFromJson(self):
        with open("Gossiping-20400-24800.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        articles = data["articles"]
        print("number of articles :", len(articles))
        
        # start from one week before election: Nov 17th
        article_num = len(articles) - 4710
        # end at one day after election
        end_num = len(articles) - 1690      
        for i, article in enumerate(articles):
            # handling the start / end article
            if i < article_num:
                continue
            if i == end_num:
                break
            
            # ignore articles with invalid format
            if not article["author"]:
                continue
            else:
                post_id = article["author"].split()[0]
            self.user_content[post_id] = self.user_content.get(post_id, []) + [article["content"]]

            comments = article["messages"]
            for comment in comments:
                comment_id = comment["push_userid"]
                self.user_comment[comment_id] = self.user_comment.get(comment_id, []) + [comment["push_content"]]
        valid_users = 0
        """
        known_troll_list = ["Sattar","diaogaro","rorobus","oweno","joy2001billy","ginoweng","soisoi","breaki","ninstagram00","worked","Bouchard",
                      "sg2361610","chatterati","tonycool0309","GDloveSM","rave16","JeonMinJu","ryan970784","cup18",
                      "mariez","Chakrit","winwinnow","Liebig","croy89","love90619","koala0919","csicrime",
                      "chhoher","Birken","t30113011","werock","zxc03211130","kiemets","matthew0129","raymondabcd",
                      "ps45689","papanot","gefroren","targoo","b8350580","cothade","catchy","livewild0327","asush97","richardjian",
                      "ashotwa47","stonetiger","paorei","yooze","remem","suihun","l314520","pojoke","qickly",
                      "sun41102","momom","deityfire","henryK","fowemo","yeees","SUNDAVE","d790929","kimeaharu",
                      "fowemo","vacuumboy","ji3sie"]
        """
        print("Successfully load data")
    def handsomeYuanClassify(self):
        print("start classifying")
        with codecs.open('user_comments.json', 'a', encoding='utf-8') as f:
            f.write('{"user_comments":[\n')
        classified_count = 0
        classified_target = 5
        for k, v in self.user_comment.items():
            # ignore users with a few comments
            if len(v) < 50:
                continue
            classified_count += 1
            print("comment :", v)
            print("remain ids :", classified_target - classified_count + 1)
            print("user id :", k)

            response = input("Is this a troll? Not troll : space, troll : any other input.\n")
            # not troll - space, troll : any other input
            isTroll = (response != ' ')
            classified_data = {'id' : k,
                               'isTroll' : isTroll,
                               'comment' : ' , '.join(v),
                               }
            d = json.dumps(classified_data, sort_keys=False, ensure_ascii=False)

            # last one don't add ','
            if classified_count != classified_target:
                d = d + ',\n'
            else:
                d = d + '\n'
            with codecs.open('user_comments.json', 'a', encoding='utf-8') as f:
                f.write(d)
            if classified_count == classified_target:
                break
        with codecs.open('user_comments.json', 'a', encoding='utf-8') as f:
            f.write(']}\n')
    def handsomeYuanCheck(self):
        with open("user_comments.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        print("good! valid json output!")
    def getAverageCommentLength(self):
        with open("user_comments_all.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        raw_data = data["user_comments"]
        with codecs.open('user_comment_len.json', 'a', encoding='utf-8') as f:
            f.write('{"user_comment_len":[\n')
        for i, cur in enumerate(raw_data):
            user_id, user_comments = cur["id"],  cur["comments"]
            comments = user_comments.split(" , ")
            total_len = 0
            for comment in comments:
                total_len += len(comment)
            towrite = {'id': user_id, 'average_len': '%.3f' %(total_len/len(comments))}
            d = json.dumps(towrite, sort_keys=False, ensure_ascii=False)
            # last one don't add ','
            if i != len(raw_data)-1:
                d = d + ',\n'
            else:
                d = d + '\n'
            with codecs.open('user_comment_len.json', 'a', encoding='utf-8') as f:
                f.write(d)
        with codecs.open('user_comment_len.json', 'a', encoding='utf-8') as f:
            f.write(']}\n')
d = dataProcessor()
#d.loadFromJson()
#d.handsomeYuanClassify()
#d.handsomeYuanCheck()
d.getAverageCommentLength()
