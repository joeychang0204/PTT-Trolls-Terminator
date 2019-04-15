import json
import codecs
from shutil import copyfile
if __name__ == "__main__":
    with open("determined.json", "r", encoding="utf-8") as read_file:
        determined = json.load(read_file)
    copyfile("determined.json", "determined_backup.json")
    with codecs.open('determined.json', 'w', encoding='utf-8') as f1:
        f1.write('{"articles": [')
    counter_determined = 0
    for article in determined["articles"]:
        d = json.dumps(article, sort_keys=False, ensure_ascii=False)
        if counter_determined!=0:
            d = ',\n' + d
        with codecs.open('determined.json', 'a', encoding='utf-8') as f1:
            f1.write(d)
        counter_determined = counter_determined +1

    with open("not_determined.json", "r", encoding="utf-8") as read_file:
        not_determined = json.load(read_file)
    copyfile("not_determined.json", "not_determined_backup.json")
    with codecs.open('not_determined.json', 'w', encoding='utf-8') as f1:
        f1.write('{"articles": [')

    stop_flag = 0
    counter_not_determined = 0
    counter = 0
    for article in not_determined["articles"]:
        if stop_flag == 1:
            d = ',\n' + json.dumps(article, sort_keys=False, ensure_ascii=False)
            with codecs.open('not_determined.json', 'a', encoding='utf-8') as f2:
                f2.write(d)
            counter_not_determined = counter_not_determined+1
            continue

        print (article["article_title"])
        print (article["content"])
        response = input("Is this article political related? Yes : y, No : any other input. quit to stop.\n")
        
        if response == "quit":
            stop_flag = 1
            d = json.dumps(article, sort_keys=False, ensure_ascii=False)
            with codecs.open('not_determined.json', 'a', encoding='utf-8') as f2:
                f2.write(d)
            counter_not_determined = counter_not_determined+1
            continue
        
        if response == "y":
            article["political"] = 1
        d = json.dumps(article, sort_keys=False, ensure_ascii=False)
        d = ',\n' + d
        with codecs.open('determined.json', 'a', encoding='utf-8') as f1:
            f1.write(d)
        counter_determined = counter_determined +1
        counter = counter + 1

    with codecs.open('determined.json', 'a', encoding='utf-8') as f1:
        f1.write(']}\n')
    with codecs.open('not_determined.json', 'a', encoding='utf-8') as f2:        
        f2.write(']}\n')
    print ("Classified ", counter, "articles this time.")
    print (counter_determined, "articles classified, ", counter_not_determined, "wait to be classified.")




