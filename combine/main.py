from IP import IPProcessor
import pickle
from sklearn.svm import SVC
import json
import jieba
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

if __name__ == "__main__":
    with open("user_comment_len.json", "r", encoding="utf-8") as read_file:
        push_data = json.load(read_file)
    cIP = IPProcessor()
    cIP.loadIPJson()
    cIP.loadStat()
#   load the models
    word_vectors = Doc2Vec.load("trained_model_word2vector")
    with open('trained_model_SVM.pickle', 'rb') as f:
        svclassifier = pickle.load(f)
#   setup stop word as a set
    stop_list = set()
    with open("stopwords.txt", "r", encoding = "utf-8") as stopwords:
        for stopword in stopwords:
            stop_list.add(stopword.strip('\n'))
#   load special word dictionary to jieba
    jieba.load_userdict("dict.txt")
    documents = []

    with open("test_set.json", "r", encoding="utf-8") as read_file:
        data = json.load(read_file)

    true_positive = 0
    false_negative = 0
    false_positive = 0
    true_negative = 0
    counter = 0
    push_dict={}
    for user in push_data["user_comment_len"]:
        push_dict[user["id"]] = float(user["average_len"])
    for user_comment in data["user_comments"]:
        IP_predict, push_predict = 0,0

        label = user_comment["isTroll"]
        if user_comment["isTroll"] is True:
            label = 1
        else:
            label = 0
        if cIP.chkUser(user_comment["id"]) is True:
            IP_predict = 1
        else:
            IP_predict = 0
        if push_dict[user_comment["id"]]<=7:
            print ()
            push_predict = 1
        else:
            push_predict = 0
        
        cut_list =  list(jieba.cut(user_comment["comments"], cut_all = False))
        words = []
        for word in cut_list:
            if word not in stop_list:
                words.append(word)
        vector = word_vectors.infer_vector(words)
        predict = svclassifier.predict([vector])

        # if IP_predict == 1 or push_predict == 1:
        #     predict = 1

        if label == 1 and predict == 1:
            true_positive = true_positive + 1
        elif label == 1 and predict == 0:
            false_negative = false_negative + 1
        elif label == 0 and predict == 1:
            false_positive = false_positive + 1
        elif label == 0 and predict == 0:
            true_negative = true_negative +1
        counter = counter + 1
    precision = true_positive/(true_positive+false_positive)
    recall = true_positive/(true_positive+false_negative)
    F1_score = 2*(precision*recall/(precision+recall))
    accuracy = (true_positive + true_negative)/(true_positive +true_negative + false_negative +false_positive)
    print ("Total ", counter, "accounts in test set.")
    print ("Precision:", precision)
    print ("Recall:", recall)
    print ("F1 score:", F1_score)
    print ("accuracy:", accuracy)