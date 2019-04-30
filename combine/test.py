from IP import IPProcessor
import pickle
from sklearn.svm import SVC
import json
import jieba
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

if __name__ == "__main__":
    with open("test_set.json", "r", encoding="utf-8") as read_file:
        data = json.load(read_file)
    cIP = IPProcessor()
    cIP.loadIPJson()
    cIP.loadStat()
    counter = 0
    with open("user_comment_len.json", "r", encoding="utf-8") as read_file:
        push_data = json.load(read_file)
    push_dict={}
    troll_count = 0
    normal_count = 0
    true_positive = 0
    false_negative = 0
    false_positive = 0
    true_negative = 0
    for user in push_data["user_comment_len"]:

        push_dict[user["id"]] = float(user["average_len"])
    for user_comment in data["user_comments"]:
        if cIP.chkUser(user_comment["id"]) ==True:
            predict = 1
        else:
            predict = 0
        