#download và import thư viện
# !pip install tweepy
# !pip install stopwords
# !pip install nltk
# !pip install stylecloud
# !pip install IPython
 
import csv
import operator
import os
import re
 
import nltk
import stylecloud
import tweepy as tw
 
nltk.download('vader_lexicon')
nltk.download('stopwords')
from IPython.display import HTML, Image, display
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
 
# Go to https://developer.twitter.com/en/apps to create an app and get values
# for these credentials, which you'll need to provide in place of these
# empty string values that are defined as placeholders.
# See https://developer.twitter.com/en/docs/basics/authentication/overview/oauth
# for more information on Twitter's OAuth implementation.
 
#key API Twitter đã request
CONSUMER_KEY = 'PT3TjQFnQjwPq6UwWh0l9mVLA'
CONSUMER_SECRET = 'uHwkJ6qK5WKWwRYsKy5zjkyYG0U68MtBButh0WKhtenfAocMJJ'
OAUTH_TOKEN = '1656867841-JpwZ5MWT4jNHZsF8vxFjSkaEmcKfx1gHEk8lkVN'
OAUTH_TOKEN_SECRET = '95LXQGHGhXrWE8OsFB1sAhy2Efcx0TRInDxova9kzUsGF'
 
auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)
 
#export hình khi word cloud song và truyền icon hình
def exportWordClound(content, file_name):
    file_name = file_name + '.png'
    stylecloud.gen_stylecloud(text=content,
                              icon_name="fas fa-comment-dollar",
                              palette="cartocolors.diverging.TealRose_7",
                              output_name=file_name,
                              size=1080,
                              background_color="white")
    display(Image(filename=file_name))
# xác định search term và ngày lấy dữ liệu, dữ liệu giới hạn
search_words = ["#BNB"]
since_date = '2021-05-18'
until_date = '2021-05-25'
limit = 5000
sentiments = []
 
def collectTweets(key_search):
    results = ""
    # Collect tweets
    tweets = tw.Cursor(api.search, q=key_search, lang="en",
                       since=since_date, until=until_date).items(limit)
 
    # Iterate and print tweets
    for tweet in tweets:
        analyzer = SentimentIntensityAnalyzer()
        word = str(tweet.text).lower().replace('\n', '')
 
        polarity = analyzer.polarity_scores(word)
        score = polarity['compound']
 
        if word: #cài đặt cấu trúc khi xuất file excel
            sentiments.append({'CONTENT': word, 'SCORE': score, 'CREATED_AT': tweet.created_at})
 
        clean_str = ''.join([c for c in word if ord(c) < 128])
        clean_str = ' '.join([
            c for c in clean_str.split()
            if c not in (stopwords.words('english'))
            and not operator.contains(word, "https")
        ])
 
        clean_str = re.sub('[!@#$]', '', clean_str)
        clean_str = re.sub(r'\([^)]*\)', '', clean_str)
 
        results += clean_str.strip()
    return results
 
def main():
    #    contents = ""
 
    for key in search_words:
        contents = collectTweets(key)
        # print(contents)
        exportWordClound(contents, key)
    writeSentiment()
 
def writeSentiment():
    # now we will open a file for writing
    data_file = open(os.path.join('BNB.csv'),
                     'w',
                     encoding='UTF-8')
 
    # create the csv writer object
    csv_writer = csv.writer(data_file)
 
    # Counter variable used for writing
    # headers to the CSV file
    count = 0
 
    for emp in sentiments:
        if count == 0:
 
            # Writing headers of CSV file
            header = emp.keys()
            csv_writer.writerow(header)
            count += 1
 
        # Writing data of CSV file
        csv_writer.writerow(emp.values())
 
    data_file.close()
 
main()