# This file provides function the score the news based on domain experts knowledge
import os
import re
from stemming.porter2 import stem
import TextProcessingTools.LocalTextReader as LocalTextReader
result_file_path = "../sortedResult.txt"
def getScoreTable(baseTextScoreFile):

    f = open(baseTextScoreFile)
    score_table = {}
    content = f.read().split("\n")
    for c in content:
        if(c!=""):
            head = c.split(" ")
            score_table[head[0]] = float(head[1])

    return score_table


def scoreNews(newscsvfile,baseTextScoreFile):
    system_weight = 10 #bias for system evaluation | one news
    expert_weight = 5# bias for expert keyword } one word

    score_table = getScoreTable(baseTextScoreFile)

    LocalTextReader.fileFormmater(newscsvfile)
    os.system('java -jar ../FinNewsScorer.jar ../newstext.txt')

    system_score_table=[]
    f = open("../newstext.txt_st")
    content = f.read().split("\n")
    for c in content:
        if(c!=""):
            system_score_table.append(float(c.split("|")[-1]))
    index=0
    final_score_list = []
    with open("../newstext.txt") as f:
        content = f.read().split("\n")
        for c in content:
            if(c!=""):
                auto_score = system_score_table[index] * system_weight
                sentence = re.sub(r'[^a-zA-Z_ ]+', ' ', c).split(" ")
                length = len(sentence)

                for word in sentence:
                    word=word.lower()
                    word = stem(word)
                    try:
                        auto_score+=score_table[word] * expert_weight
                    except:
                        pass
                final_score_list.append(auto_score/length)
                index+=1


    allnews = LocalTextReader.readLocalNews(newscsvfile)

    result_obj_list = []
    for i in range(len(allnews)):
        obj = {
            "time":allnews[i][0].replace('"',"'").replace("'","[##]"),
            "title":allnews[i][1].replace('"',"'").replace("'","[##]"),
            "content":allnews[i][2].replace('"',"'").replace("'","[##]"),
            "url":allnews[i][3].replace('"',"'").replace("'","[##]"),
            "score":final_score_list[i]
        }
        result_obj_list.append(obj)
    newlist = sorted(result_obj_list, key=lambda x: x["score"], reverse=True)
    f=open(result_file_path,"w")
    for obj in newlist:
        f.write(str(obj).replace("'",'"').replace("[##]","'")+"\n")

    f.close()

if __name__ == "__main__":
    scoreNews("../news_store.csv","../basewordScore.txt")

