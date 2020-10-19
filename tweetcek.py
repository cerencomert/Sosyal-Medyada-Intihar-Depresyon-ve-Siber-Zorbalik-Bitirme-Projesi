import tweepy
import csv
import time
import pandas as pd

class Bot:
    def __init__(self):
        self.CONSUMER_KEY = "***"
        self.CONSUMER_KEY_SECRET = '***'
        self.ACCESS_TOKEN = '***'
        self.ACCESS_TOKEN_SECRET = '***'
        self.api = self.authenticate()
        self.user_list = []

    def authenticate(self):
        auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_KEY_SECRET)
        auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        try:
            api.verify_credentials()
        except:
            print('Bot baglanamadi, key ve tokenları kontrol ediniz')
        else:
            print("Bot basarılı bir sekilde baglandı")
            return api

    def search_tweets(self, user, max_tweets):
        searched_tweets = []
        last_id = -1
        max_tweets = max_tweets

        while len(searched_tweets) < max_tweets:
            count = max_tweets - len(searched_tweets)
            try:
                new_tweets = self.api.search(q=word, count=count, lang="tr", max_id=str(last_id - 1))
                if not new_tweets:
                    break
                searched_tweets.extend(new_tweets)
                last_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                print('Error', str(e))
                break
        with open('{}_tweets.csv'.format(word), 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            #writer.writerow(["user name", "name", "created_at", "text"])
            for tweet in searched_tweets:
                user = tweet.author.screen_name.encode('utf8')
                name = tweet.author.name
                writer.writerow([user, name, tweet.created_at, tweet.text])
                print(user, ' ', name,' ', tweet.created_at, ' ', tweet.text)
        return len(searched_tweets)


bot = Bot()
bot.search_tweets("ARANACAK KELİME", 500)

