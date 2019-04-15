import json
import codecs
if __name__ == "__main__":
    with open("determined.json", "r", encoding="utf-8") as f1:
        data = json.load(f1)
    print ("pass")