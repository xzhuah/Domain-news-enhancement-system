
import csv
import re
from stemming.porter2 import stem
import WordCloudGen
def readLocalNews(filepath):
    allnews = []
    with open(filepath, 'r') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:

            allnews.append(row)
    return allnews

def fileFormmater(originalCSVFile):

    allnews = readLocalNews(originalCSVFile)
    f = open("../newstext.txt", "w")
    for new in allnews:
        line = new[1]+","+new[2]+"\n"
        f.write(line)
    f.close()
def keywordExtract(textfile,stopwordfile):
    with open(textfile) as f:
        with open(stopwordfile) as ff:
            content = f.read()
            content = set(re.sub(r'[^a-zA-Z_ ]+', ' ', content).split(" "))
            stopwordlist = set(ff.read().split("\n"))
            keywordSet = set()
            for word in content:
                word= stem(word.lower())
                if word not in stopwordlist and word!="":
                    keywordSet.add(word)

    return keywordSet

            #content=content.replace("\n"," ").replace(","," ").replace("."," ").replace('"'," ")v
if __name__ == "__main__":
    # se = keywordExtract("newstext.txt","../stopwords.txt")
    # f=open("basewordScore.txt","w")
    # for word in se:
    #     f.write(word+" 5"+"\n")

    fileFormmater("../news_store.csv")
    se = keywordExtract("../newstext.txt","../stopwords.txt")
    f=open("../basewordScore.txt","w")
    for word in se:
        f.write(word+" 5"+"\n")