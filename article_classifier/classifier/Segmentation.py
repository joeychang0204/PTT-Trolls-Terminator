import json
import jieba
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

if __name__ == "__main__":

#   setup stop word as a set
    stop_list = set()
    with open("stopwords.txt", "r", encoding = "utf-8") as stopwords:
        for stopword in stopwords:
            stop_list.add(stopword.strip('\n'))

#   load special word dictionary to jieba
    jieba.load_userdict("dict.txt")
    documents = []
    with open("determined.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
#   transform raw data to useable form and save to segmentation.txt
    counter = 0
    segmentation = open("segmentation.txt", "w", encoding = "utf-8")
    for article in data["articles"]:
        if article["political"] == 1:
            label = 1
        else:
            label = 0
        segmentation.write(str(label) + " ")
        words = []
        cut_list =  list(jieba.cut(article["content"], cut_all = False))
        for word in cut_list:
            if word not in stop_list:
                segmentation.write(word + " ")    
        segmentation.write("\n")
        counter = counter +1
    segmentation.close()
    