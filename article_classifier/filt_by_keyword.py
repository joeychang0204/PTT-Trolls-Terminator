import json
import jieba
import codecs

if __name__ == "__main__":
    stop_list = set()
#   setup stop word as a set
    with open("stopwords.txt", "r", encoding = "utf-8") as stopwords:
        for stopword in stopwords:
            stop_list.add(stopword.strip('\n'))
#   load special word dictionary to jieba
    jieba.load_userdict("dict.txt")
    # Gossiping-20400-24800.json
    with open("Gossiping-20400-24800.json", "r", encoding="utf-8") as read_file:
            data = json.load(read_file)

    keywords = set()
    with open("politicians.txt", "r", encoding = "utf-8") as words:
        for keyword in words:
            keywords.add(keyword.strip('\n'))

    counter = 0
    counter_determined = 0
    counter_not_determined=0
    article_num = len(data["articles"]) - 4710
    end_num = len(data["articles"]) - 1690

    with codecs.open('determined.json', 'a', encoding='utf-8') as f1:
        f1.write('{"articles": [')
    with codecs.open('not_determined.json', 'a', encoding='utf-8') as f2:
        f2.write('{"articles": [')
        
    for i, article in enumerate(data["articles"]):
        if i < article_num:
            continue
        if i == end_num:
                break
        
        if article["message_count"]["boo"]<30 and article["message_count"]["push"]<30:
            continue

        cut_list = list(jieba.cut(article["content"], cut_all = False))
        cut_list.extend(list(jieba.cut(article["article_title"], cut_all = False)))
        for word in cut_list:
            if word in keywords:
                article["political"] = 1
                break
        if "political" not in article:
            article["political"] = 0

        d = json.dumps(article, sort_keys=False, ensure_ascii=False)
        if article["political"] == 1:
            if counter_determined !=0:
                d = ',\n' + d
            with codecs.open('determined.json', 'a', encoding='utf-8') as f1:
                f1.write(d)
            counter_determined = counter_determined +1
        else:
            if counter_not_determined !=0:
                d = ',\n' + d
            with codecs.open('not_determined.json', 'a', encoding='utf-8') as f2:
                f2.write(d)
            counter_not_determined = counter_not_determined+1
        counter = counter +1

    with codecs.open('determined.json', 'a', encoding='utf-8') as f1:
        f1.write(']}\n')
    with codecs.open('not_determined.json', 'a', encoding='utf-8') as f2:        
        f2.write(']}\n')
