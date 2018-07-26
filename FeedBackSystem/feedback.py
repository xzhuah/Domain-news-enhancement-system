import re
from filelock import Timeout, FileLock
basewordScoreFile = "../basewordScore.txt"
stopwordFile = "../stopwords.txt"
from stemming.porter2 import stem
with open(stopwordFile) as ff:
    stopwordset = set(ff.read().split("\n"))
def updateBasewordScore(updater):
    baseScore = 5.0
    lock = FileLock(basewordScoreFile+".lock", timeout=1)
    with lock:
        lock.acquire()

        f = open(basewordScoreFile,"r")
        content = f.read().split("\n")
        f.close()
        score_table = {}
        for c in content:
            if(c!=""):
                head=c.split(" ")
                score_table[head[0]]=float(head[1])
        for word in updater:
            try:
                score_table[word]+=updater[word]
            except:
                score_table[word]=baseScore+updater[word]

        ff=open(basewordScoreFile,"w")
        for key in score_table:
            ff.write(key+" "+str(score_table[key])+"\n")
        ff.close()
        lock.release()


def news2keywordList(news):
    result = set()
    content = news["title"] + "," + news["content"]
    content=content.lower()
    content = set(re.sub(r'[^a-zA-Z_ ]+', ' ', content).split(" "))
    for c in content:

        if(c!="" and c not in stopwordset):
            result.add(stem(c))

    return result

def upgradeNews(news,confidence = 0.1):

    for new in news:

        keywords = news2keywordList(new)
        updater = {}
        for word in keywords:
            try:
                updater[word]+=confidence
            except:
                updater[word]=confidence
    return updater

def downgradeNews(news,confidence = 0.1):
    for new in news:

        keywords = news2keywordList(new)
        updater = {}
        for word in keywords:
            try:
                updater[word]-=confidence
            except:
                updater[word]=-confidence
    return updater

def combineUpdater(updater1,updater2):
    result={}
    for key in updater1:
        result[key]=updater1[key]
    for key in updater2:
        try:
            result[key]+=updater2[key]
        except:
            result[key]=updater2[key]
    return result

if __name__ == "__main__":
    pass
    #a = upgradeNews([{"time": "9:45  AM ET Thu, 17 Aug 2017", "title": "US jobless claims fall to near six-month low", "content": "The number of Americans filing for unemployment benefits fell to near a six-month low last week.", "url": "https://www.cnbc.com/2017/08/17/us-weekly-jobless-claims-aug-12-2017.html", "score": 2.962962962962963}])

    #updateBasewordScore(downgradeNews([{"time": "9:45  AM ET Thu, 17 Aug 2017", "title": "US jobless claims fall to near six-month low", "content": "The number of Americans filing for unemployment benefits fell to near a six-month low last week.", "url": "https://www.cnbc.com/2017/08/17/us-weekly-jobless-claims-aug-12-2017.html", "score": 2.962962962962963}]))    #print(a)