import json
import codecs
import statistics

## numpy is used for creating fake data
import numpy as np 
import matplotlib as mpl 

## agg backend is used to create plot as a .png file
mpl.use('agg')
import matplotlib.pyplot as plt

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
    def getAverageResponseTime(self):

        with open("determined.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        articles = data["articles"]
        
        print('article_len ==', len(articles))
        error_num = 0
        less_num = 0
        user_response_time = {}
        bad_articles = set()
        political, nonPolitical = 0, 0
        for article in articles:

            # ignore articles with invalid format
            # convert post time to format date/hour/min/sec
            # all in Nov, don't consider month
            if not article["author"]:
                continue
            elif article["political"] == 0:
                nonPolitical += 1
                # ignore non-political articles
                continue
            else:
                post_time = article["date"].split()[2:4]
                political += 1
            post_time = ' '.join(post_time)
            post_time = post_time.replace(':', ' ')
            #print(post_time)
            
            comments = article["messages"]
            for comment in comments:
                #if not comment["push_ipdatetime"] or comment['push_ipdatetime']=='誤':
                    #continue
                #print(comment["push_ipdatetime"], comment["push_ipdatetime"].split('/'))
                try:
                    comment_id = comment["push_userid"]
                    comment_time = comment["push_ipdatetime"].split('/')[1]
                    comment_time = comment_time.replace(':', ' ')
                    comment_time = comment_time + ' 59'
                    dif = self.calculateTimeDifference(post_time, comment_time)
                    if dif < 0:
                        less_num += 1
                        bad_articles.add(article["article_id"])
                        continue
                    user_response_time[comment_id] = user_response_time.get(comment_id, []) + [dif]
                except Exception as e:
                    print(str(e))
                    error_num += 1
                    #print("error :post_time :", post_time,"push time:" ,comment["push_ipdatetime"])
        '''
        with codecs.open('user_average_response_time.json', 'a', encoding='utf-8') as f:
            f.write('{"user_response_time":[\n')
        for key,value in user_response_time.items():
            towrite = {'id': key, 'average_time': '%.3f' %(sum(value) / len(value))}
            d = json.dumps(towrite, sort_keys=False, ensure_ascii=False) + ',\n'
            with codecs.open('user_average_response_time.json', 'a', encoding='utf-8') as f:
                f.write(d)
        
        with codecs.open('user_average_response_time.json', 'a', encoding='utf-8') as f:
            f.write(']}\n')
        '''
        print('political :', political, 'nonPolitical :', nonPolitical)
            
    def calculateTimeDifference(self, time1, time2):
        diff = 0
        time1, time2 = time1.split(), time2.split()
        ith_minute = [24 * 60, 60, 1, 1/60]
        for i in range(len(time1)):
            diff += (int(time2[i]) - int(time1[i])) * ith_minute[i]
        return diff
    def troll_average_time(self):
        with open("user_comments_all.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        # build troll dictionary
        user_isTroll = {}
        for comment in data["user_comments"]:
            user_isTroll[comment['id']] = comment['isTroll']
        with open("user_average_response_time.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        troll, nonTroll = [], []
        thresholds = [3, 4, 5, 6, 7, 8, 9, 10]
        for threshold in thresholds:
            quick_troll, quick_nonTroll = 0, 0
            for d in data["user_response_time"]:
                user, time = d['id'], d['average_time']
                if user not in user_isTroll:
                    continue
                if user_isTroll[user]:
                    if float(time) < threshold:
                        #print('quick troll : ',user)
                        quick_troll += 1
                    troll.append(float(time))
                else:
                    if float(time) < threshold:
                        #print('quick non-troll : ',user)
                        quick_nonTroll += 1
                    nonTroll.append(float(time))
            print('threshold', threshold, 'quick troll ', quick_troll, 'quick nonTroll', quick_nonTroll)
        print('time :')
        print('troll min :', min(troll), 'troll max :', max(troll))
        print('troll average = ', sum(troll)/len(troll))
        print('troll standard deviation = ', statistics.pstdev(troll))
        print('non-troll min :', min(nonTroll), 'non-troll max :', max(nonTroll))
        print('non-troll average =', sum(nonTroll)/len(nonTroll))
        print('non-troll standard deviation = ', statistics.pstdev(nonTroll))
    def troll_average_len(self):
        with open("user_comments_all.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        # build troll dictionary
        user_isTroll = {}
        for comment in data["user_comments"]:
            user_isTroll[comment['id']] = comment['isTroll']
        with open("user_comment_len.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        troll, nonTroll = [], []
        thresholds = [6]
        for threshold in thresholds:
            short_troll, short_nonTroll = 0, 0
            for d in data["user_comment_len"]:
                user, time = d['id'], d['average_len']
                if user not in user_isTroll:
                    continue
                if user_isTroll[user]:
                    if float(time) < threshold:
                        short_troll += 1
                        #print('short troll :', user)
                    troll.append(float(time))
                else:
                    if float(time) < threshold:
                        short_nonTroll += 1
                        #print('quick nontroll id :', user)
                        #print('short non-troll :', user)
                    nonTroll.append(float(time))
            print('threshold', threshold, 'short troll ', short_troll, 'short nonTroll', short_nonTroll)
        print(' ')
        print('len :')
        print('short troll ', short_troll, 'short nonTroll', short_nonTroll)
        #print('troll min :', min(troll), 'troll max :', max(troll))
        #print('troll average = ', sum(troll)/len(troll))
        #print('troll standard deviation = ', statistics.pstdev(troll))
        #print('non-troll min :', min(nonTroll), 'non-troll max :', max(nonTroll))
        #print('non-troll average =', sum(nonTroll)/len(nonTroll))
        #print('non-troll standard deviation = ', statistics.pstdev(nonTroll))
        print('troll users :', len(troll), 'non-trolls :', len(nonTroll))

        all_user = troll + nonTroll
        print('total average :', sum(all_user) / len(all_user))
        print('total standard deviation =', statistics.pstdev(all_user))
        
    def getPrecisionRecall(self):
        with open("test_set.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        user_isTroll = {}
        for comment in data["user_comments"]:
            user_isTroll[comment['id']] = comment['isTroll']
        with open("user_comment_len.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        tp, fp, tn, fn = 0, 0, 0, 0
        for d in data["user_comment_len"]:
            user, l = d['id'], d['average_len']
            if user not in user_isTroll:
                continue
            if user_isTroll[user]:
                if float(l) < 6:
                    tp += 1
                    #print('short troll :', user)
                else:
                    fn += 1
            else:
                if float(l) < 6:
                    fp += 1
                else:
                    tn += 1
        print('troll :', tp+fn)
        recall, precision = tp/(tp+fn), tp/(tp+fp)
        accuracy, F1 = (tp+tn)/(tp+tn+fp+fn), 2*recall*precision/(precision+recall)
        print('recall :', recall, 'precision :', precision)
        print('accuracy :', accuracy, 'F1 :', F1)
    def getBoxPlot(self):
        with open("user_comments_all.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        user_isTroll = {}
        for comment in data["user_comments"]:
            user_isTroll[comment['id']] = comment['isTroll']
        #with open("user_comment_len.json", "r", encoding="utf-8") as read_file:
        with open("user_average_response_time.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        trollLen, nonTrollLen, allLen = [], [], [] 
        for d in data["user_response_time"]:
            user, l = d['id'], d['average_time']
            if user not in user_isTroll:
                continue
            if user_isTroll[user]:
                trollLen.append(float(l))
            else:
                nonTrollLen.append(float(l))
            allLen.append(float(l))
        #print('stats for all users:')
        allLen.sort()
        nonTrollLen.sort()
        trollLen.sort()

        plotData = [allLen, trollLen, nonTrollLen]
        # Create a figure instance
        fig = plt.figure(1, figsize=(9, 6))

        # Create an axes instance
        ax = fig.add_subplot(111)

        # Create the boxplot
        #bp = ax.boxplot(allLen)
        bp = ax.boxplot(plotData)
        ax.set_xticklabels(['All Users', 'Trolls', 'Normal Users'])

        # Save the figure
        # fig.savefig('boxplotTime.png', bbox_inches='tight')
        
        
        
    
    
        
        
d = dataProcessor()
#d.loadFromJson()
#d.handsomeYuanClassify()
#d.handsomeYuanCheck()
#d.getAverageCommentLength()
#d.getAverageResponseTime()
#d.troll_average_time()
d.troll_average_len()
#d.getPrecisionRecall()
d.getBoxPlot()
