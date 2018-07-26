# A very cool file allow you to produce word cloud picture using raw text


import pymongo


import operator
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import textrank
import textrazor
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import six
default_config=[4,3,1] # [the minimum word length in result, the maximum word number in phrase, minimum keyword frequency]


def entities_text(text):
    """Detects entities in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
    result = set()
    for entity in entities:
        result.add(entity_type[entity.type])

    return result

def extractEvents(text):

    """Detects entities in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
    result = set()
    for entity in entities:
        if(entity_type[entity.type]=="EVENT"):

            result.add(entity.name)

    return result

# def extractEvent(text):
#     result = []
#     text = preprocessText(text)
#     all_phrase = extractPhrase(text)
#     for phrase in all_phrase:
#         print(phrase)
#         possible_type = entities_text(phrase)
#         print(possible_type)
#         if('EVENT' in possible_type):
#             result.append(phrase)
#     return result



def extractPhrase(text,config=default_config,method=-1):
    #method 0 requires network access and is more time consuming
    #method -1 requires network access not very time-consuming
    #method 1 not require netword time-consuming
    all_phrase = set()

    if(method<=0):
        textrazor.api_key = "46c31d1c45022d174816fd10f5531ccc1e5af24a86d2a0576cd629fe"

        client = textrazor.TextRazor(extractors=["entities"])
        response = client.analyze(text)
        all_phrase1=set()
        for entity in response.entities():
            all_phrase1.add(entity.id)
        for entity in all_phrase1:
            word = preprocessText(entity)
            word = re.sub(r'[^a-zA-Z\s]','',word)
            leng = word.count(" ")+1
            if(len(word)>=config[0] and leng<=config[1]):
                all_phrase.add(word)
    if(method>=0):
        all_phrase2 = textrank.extractKeyphrases(text)
        for word in all_phrase2:
            leng = word.count(" ") + 1
            if (len(word) >= config[0] and leng <= config[1]):
                all_phrase.add(word)

    return list(all_phrase)


def phraseFreq(text,maxi_phrase_length=default_config[1],mini_word_length=default_config[0]):
    preprocess = text
    #all_phrase = textrank.extractKeyphrases(preprocess)
    all_phrase = extractPhrase(preprocess) #use advanced method
    print(all_phrase)
    result={}
    for phrase in all_phrase:
        length = phrase.count(" ")+1
        if(length<=maxi_phrase_length and len(phrase)>=maxi_phrase_length):

            preprocess=" "+preprocess+" "
            preprocess = re.sub(r'[^a-zA-Z\s]',' ',preprocess)
            weight = preprocess.count(" "+phrase+" ") * length + preprocess.count(" "+phrase+"s ") * length + preprocess.count(" "+phrase+"ed ") * length# for phrase, the score should be in Proportional to its length
            if(weight>0):
                result[phrase]=weight # for phrase, the score should be in Proportional to its length

    return result


def preprocessText(text):
    text = text.lower()
    text = text.replace("...", ",").replace("-", " ").replace("–", " ").replace("—"," ").replace("/"," ").replace("%", "").replace('"',"").replace("'","")
    text = re.sub(' +', ' ', text)
    return text


def WordCloudFreq(text,config=default_config):
    # keep other punctuation to break the phrase
    text = preprocessText(text)

    print(text)

    # #method 1 not very good algorithm used here
    # r = rake.Rake(SmartStopList.words())
    # keywords = r.run(re.sub(r'[^a-zA-Z\s]','',text),config[0],config[1],config[2])
    # result = {}
    # for item in keywords:
    #     result[item[0]]=item[1]
    # print(result)
    # return result

    # #method 2, maybe reveal some meaning less low frequent but insteresting word phrase
    # r = Rake()
    # #r.extract_keywords_from_text(re.sub(r'[^\w\s]','',text))
    # r.extract_keywords_from_text(text)
    # result = r.get_ranked_phrases_with_scores()
    # result2 = {}
    # for item in result:
    #     length = item[1].count(" ")+1
    #     if(length<=config[1]):
    #         result2[item[1]]=item[0]
    # return result2

    #method 3
    return phraseFreq(text,config[1])





# use default method in wordcloud
def drawCloudFromText(text,plot_or_show="plot"):
    text = preprocessText(text)


    #print(text)


    wordcloud = WordCloud(width=1900, height=1000, background_color="white").generate(re.sub(r'[^a-zA-Z\s]','',text))
    if (plot_or_show == "plot"):
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
    elif (plot_or_show == "show"):

        img = wordcloud.to_image()
        img.show()
    else:
        return wordcloud

def drawCloud(text,config=default_config,plot_or_show="plot"):
    word_freq = WordCloudFreq(text,config)

    print(word_freq)
    wordcloud= WordCloud(width=1900,height=1000,background_color="white").fit_words(word_freq)

    if(plot_or_show == "plot"):
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
    elif(plot_or_show=="show"):

        img = wordcloud.to_image()
        img.show()
    else:
        return wordcloud






def getNewsVector(client, year, month, date,config=default_config):
    if not isinstance(client, pymongo.MongoClient):
        raise ValueError("The input parameter type is wrong")
    #r = rake.Rake(SmartStopList.words())
    collection = client["Bitcoin_news"]["bitcoin_news"]
    query = collection.find({"date":year+"-"+month+"-"+date})
    result = []
    for q in query:

        text = q["heading"]+", "+q["content"]

        res = WordCloudFreq(text)


        for key in res:

            result.append((key,res[key]))
    return result


def writeFile(file_name,name_value):
    f = open(file_name,"w")
    f.write("name,value\n")
    sorted_x = sorted(name_value.items(), key=operator.itemgetter(1))
    sorted_x.reverse()
    for i in range(len(sorted_x)):

        try:
            f.write(sorted_x[i][0]+","+str(sorted_x[i][1])+"\n")
        except:
            print(sorted_x[i][0]+","+str(sorted_x[i][1]))

    f.close()



if __name__=="__main__":
    #nltk.download()
    #textrankText()
    # a =phraseFreq("Frames completes produced water treatment system for Kraken FPSO Offshore Oil and Gas Magazine- WOERDEN, the Netherlands – Frames has completed manufacturing of a produced water treatment package (PWT) for the Bumi Armada Kraken FPSO project. The PWT system is designed to process 460,000 b/d of reservoir water with heavy oil and solids It consists of a total of four skids, including cyclonic desanding and ...")
    # print(a)
    # #WordCloudFreq("Frames completes produced water treatment system for Kraken FPSO Offshore Oil and Gas Magazine- WOERDEN, the Netherlands – Frames has completed manufacturing of a produced water treatment package (PWT) for the Bumi Armada Kraken FPSO project. The PWT system is designed to process 460,000 b/d of reservoir water with heavy oil and solids It consists of a total of four skids, including cyclonic desanding and ...")

    all_text=open("words.txt",encoding='UTF-8').read()
    all_text=preprocessText(all_text)
    #all_text = re.sub(r'[^a-zA-Z\s]', ' ', all_text)
    import time

    start = time.time()
    #drawCloud(all_text, plot_or_show="show")

    #extractEvent(all_text)
    print(extractEvents(all_text))
    print("advanced word cloud", time.time() - start)

    # with SSHDBConnector() as connector:
    #     client = connector.getClient()
    #     all_text = getRawNewsIntervalFromDB(client)
    #     start = time.time()
    #     drawCloudFromText(all_text, plot_or_show="show")
    #     print("naive word cloud", time.time() - start)
    #     drawCloud(all_text, plot_or_show="show")
    #     print("advanced word cloud", time.time() - start)

    #bitcoinWordCould()
    #drawCloud("Frames completes produced water treatment system for Kraken FPSO Offshore Oil and Gas Magazine- WOERDEN, the Netherlands – Frames has completed manufacturing of a produced water treatment package (PWT) for the Bumi Armada Kraken FPSO project. The PWT system is designed to process 460,000 b/d of reservoir water with heavy oil and solids It consists of a total of four skids, including cyclonic desanding and ...")
    # pass

        #print(getNewsVector(client,"2013","01","03"))

