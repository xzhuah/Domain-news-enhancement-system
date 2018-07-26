# Domain news enhancement system


It helps domain experts to enhance their news by ranking them.

In this demo version, it sepcifically enhances the financial news from https://www.cnbc.com.


To run the program, you need to install all the dependence and run the following python program sequencially.

	python fin_news_crawler.py

start the news crawler, when the crawler finished crawling, a word cloud that summarized all the gathered news information will pop out. You will be able to find the news in news_store.csv. You can specify the number of news by changing the parameter in the main method.

	python LocalTextReader.py

Start the preprocessing script to extract all the keywords from the news and assign all these keyword an equal weight for latter scoring 

	python NewsRanker.py

This script will launch the java news scorer (FinNewsScorer) to assign each news a score according to its "information concentration", the result will be stored in sortedResult.txt

	python NewsReader.py

This script will lanuch the flask server through which, people can access the web interface and read the news. People will be able to give feedback on the ranking and a feedback collector will use these feedback to update the sortedResult.


The logic of this system is shown in the following diagram

![](https://i.imgur.com/RI8npeF.png)