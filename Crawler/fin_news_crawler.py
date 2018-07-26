from bs4 import BeautifulSoup
import urllib.request
import threading
import WordCloudGen
import csv
baseUrl = "https://www.cnbc.com/"

def readDataFrom(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-agent',
         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36")]  # We must cheat the google
    html = opener.open(url)
    return str(html.read())

local_news_buffer = []

def extractNewsFromUrl(url,use_local_news_buffer=False):
    global local_news_buffer
    result = []
    raw_page = readDataFrom(url)
    soup = BeautifulSoup(raw_page, "html.parser")
    news_cards = soup.find("ul","stories_assetlist").find_all("li")
    for card in news_cards:
        try:
            news_title = card.find("div", "headline").text.replace("\\n","").replace("\\t","").replace("\\","").strip()
            news_url = baseUrl+card.find("a").get("href")[3:-2].strip()
            news_time = card.find("time").text.strip()
            news_detail = card.find("p","desc").text.replace("\\","").strip()
            news = {
                "title":news_title,
                "url":news_url,
                "time":news_time,
                "detail":news_detail
            }
            if use_local_news_buffer:
                local_news_buffer.append(news)
            else:
                result.append(news)
        except:
            pass
    return result


def listBreaker(the_list,max_element_per_list = 10):
    index = 0
    result = []
    while index+max_element_per_list<len(the_list):
        result.append(the_list[index:index+max_element_per_list])
        index += max_element_per_list
    result.append(the_list[index:])
    return result


def extractNewsOnPages(start_page = 1, end_page = 10):
    urls=[]
    for page in range(start_page,end_page+1):
        urls.append("https://www.cnbc.com/economy/?page="+str(page))
    url_batch = listBreaker(urls)
    for batch in url_batch:
        thrs = [threading.Thread(target=extractNewsFromUrl, args=[url,True]) for url in batch]
        [thr.start() for thr in thrs]
        [thr.join() for thr in thrs]
        print(len(batch))


if __name__ == "__main__":
    extractNewsOnPages(1,5)
    all_text = ""
    file = "../news_store.csv"
    f = open(file, "w",newline='')
    spamwriter = csv.writer(f, delimiter=',')
    spamwriter.writerow(["Time","Title","Content","URL"])
    for news in local_news_buffer:
        spamwriter.writerow([news["time"],news["title"],news["detail"],news["url"]])
        all_text+=news["title"]+" "+news["detail"]
    WordCloudGen.drawCloud(all_text, plot_or_show="show")

