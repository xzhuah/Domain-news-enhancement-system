#0~14
#14~19
import json
from flask import render_template
from flask import Flask,redirect
from flask import request
import feedback
import NewsRanker
app = Flask(__name__)
result_file_path = "../sortedResult.txt"
def loadNews(news_path):

    high_score_news_ = []
    mid_score_news_ = []
    low_score_news_ = []

    f=open(news_path)
    content = f.read().split("\n")
    for c in content:
        if c!="":

            obj=json.loads(c)

            if(obj["score"]>19):
                high_score_news_.append(obj)
            elif(obj["score"]>14):
                mid_score_news_.append(obj)
            else:
                low_score_news_.append(obj)



    return high_score_news_,mid_score_news_ ,low_score_news_
high_score_news,mid_score_news ,low_score_news = loadNews(result_file_path)
local_updater = {}

@app.route('/')
def redirectTo():
    global local_updater, high_score_news, mid_score_news, low_score_news
    return redirect("./highrank", code=302)

@app.route('/highrank')
def highrank():
    global local_updater, high_score_news, mid_score_news, low_score_news
    #return '<h1>'+str(high_score_news)+'</h1>'
    return render_template('./basicHtml.html', title='High Rank News', all_news=high_score_news,keywords=local_updater)

@app.route('/midrank')
def midrank():
    global local_updater, high_score_news, mid_score_news, low_score_news
    #return '<h1>'+str(high_score_news)+'</h1>'
    return render_template('./basicHtml.html', title='Mid Rank News', all_news=mid_score_news,keywords=local_updater)

@app.route('/lowrank')
def lowrank():
    global local_updater, high_score_news, mid_score_news, low_score_news
    #return '<h1>'+str(high_score_news)+'</h1>'
    return render_template('./basicHtml.html', title='Low Rank News', all_news=low_score_news,keywords=local_updater)

@app.route('/submit')
def submitAndRerank():
    global local_updater,high_score_news, mid_score_news, low_score_news
    #return '<h1>'+str(high_score_news)+'</h1>'
    feedback.updateBasewordScore(local_updater)

    NewsRanker.scoreNews("../news_store.csv","../basewordScore.txt")
    high_score_news, mid_score_news, low_score_news = loadNews(result_file_path)
    local_updater = {}
    return redirect("./highrank", code=302)



@app.route('/upgrade')
def upgradeNews():
    global local_updater
    title = request.args.get("title")
    content = request.args.get("content")
    #return title,content
    updater = feedback.upgradeNews([{"title":title,"content":content}])
    local_updater = feedback.combineUpdater(local_updater,updater)
    print(str(local_updater))
    return (''), 204

@app.route('/downgrade')
def downgradeNews():
    global local_updater
    title = request.args.get("title")
    content = request.args.get("content")
    #return title,content
    updater = feedback.downgradeNews([{"title":title,"content":content}])
    local_updater = feedback.combineUpdater(local_updater, updater)
    print(str(local_updater ))
    return (''), 204

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8081)


