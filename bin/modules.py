import json
from collections import Counter

import tweepy
from tweepy import StreamListener

from src.config import data
from src.config.data import langs
from src.config.local_config import *
from src.config.style import color


class TwitterMain:

    def __init__(self, num_tweets_to_analyze, retweet_count=10000):
        self.auth = tweepy.OAuthHandler(cons_key, cons_sec)
        self.auth.set_access_token(app_key, app_sec)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True)

        self.num_tweets_to_analyze = num_tweets_to_analyze
        self.retweet_count = retweet_count

    def get_top_trends(self, region: str):
        try:
            region_id = data.woeid[region]
        except KeyError:
            print(f"Invalid region. Aviable regions:\n{list(data.woeid.keys())}")
            return

        trends = self.api.trends_place(region_id)
        # print(f"\n{color.BLUE}Top trends in region "
        #       f"{color.ITALIC}{region}:{color.END}\n")
        trends = trends[0]['trends']
        # for i in range(len(trends)):
        #     print(f"#{i + 1}\t{trends[i]['name']}")

    def get_tweets_with_query(self, query: str):
        search_results = self.api.search(q=query)
        # print(f"\n{color.BLUE}Tweets that include keyword "
        #       f"{color.ITALIC}{query}{color.END}:\n")
        # for i in range(len(search_results)):
        #     print(f"{getattr(search_results[i], 'text')}\n"
        #           + "_" * 100)

    def get_streaming_data(self):
        stream_listener = TwitterListener(num_tweets_to_grab=self.num_tweets_to_analyze,
                                          retweet_count=self.retweet_count)
        stream = tweepy.Stream(self.api.auth, stream_listener)
        try:
            stream.sample()
            # return stream_listener.get_top_tweets()
        except Exception as e:
            print(e, e.__doc__)


class TwitterListener(StreamListener):

    def __init__(self, num_tweets_to_grab, retweet_count):
        super().__init__()
        self.start_listener = True
        self.counter = 0
        self.num_tweets_to_grab = num_tweets_to_grab
        self.retweet_count = retweet_count
        self.languages = []
        self.top_languages = []
        self.top_tweets = []

    def on_data(self, raw_data):
        if self.counter >= self.num_tweets_to_grab:
            # print(f"\n{color.BLUE}Languages of the processed tweets:{color.END}")
            # print(self.languages)
            # print(Counter(self.languages))
            # print(f"\n{color.BLUE}Languages of the processed tweets that "
            #       f"have more than {self.retweet_count} number of retweets:{color.END}")
            # print(self.top_languages)
            # print(Counter(self.top_languages))
            return False

        # if self.start_listener:
        #     print(f"\n{color.BLUE}Tweets that were retweeted "
        #           f"at least {self.retweet_count} times:{color.END}")
        #     self.start_listener = False
        json_data = json.loads(raw_data)
        if 'text' in json_data:
            if json_data['lang'] in langs:
                language = langs[json_data['lang']]
            else:
                language = 'other'
            retweet_data = json_data.get('retweeted_status')
            if retweet_data:
                retweet_count = retweet_data['retweet_count']
                if retweet_count >= self.retweet_count:
                    # print(f"\nLanguage: {language}, "
                    #       f"Retweeted {retweet_count} times. Tweet:\n"
                    #       f"{json_data['text']}")
                    tweet = Tweet(language, retweet_count, json_data['text'])
                    self.top_tweets.append(tweet)
                    self.top_languages.append(language)

            self.languages.append(language)
            self.counter += 1
        return True

    def on_error(self, status_code):
        print(status_code)

    def get_top_tweets(self):
        return self.top_tweets


class Tweet:

    def __init__(self, language, retweet_count, text):
        self.language = language
        self.retweet_count = retweet_count
        self.text = text
