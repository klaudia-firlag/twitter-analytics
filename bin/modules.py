import json
import re

import tweepy
from tweepy import StreamListener

from src.config import data
from src.config.data import langs
from src.config.local_config import *
from src.config.style import FONT


class TwitterStats:

    def __init__(self):
        self.languages = []
        self.top_languages = []
        self.top_tweets = []

    def add_language(self, language):
        if language not in self.languages:
            self.languages.append(language)

    def add_top_language(self, language):
        if language not in self.top_languages:
            self.top_languages.append(language)

    def add_top_tweet(self, tweet):
        self.top_tweets.append(tweet)

    def get_stats(self):
        return self.languages, self.top_languages, self.top_tweets


class TwitterMain:

    def __init__(self, num_tweets_to_analyze, retweet_count=10000):
        self.auth = tweepy.OAuthHandler(cons_key, cons_sec)
        self.auth.set_access_token(app_key, app_sec)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True)

        self.num_tweets_to_analyze = num_tweets_to_analyze
        self.retweet_count = retweet_count
        self.stats = TwitterStats()

        self.trends = {}
        self.search_results = None

    def add_top_trends(self, region: str):
        try:
            region_id = data.woeid[region]
        except KeyError:
            print(f"Invalid region. Available regions:\n{list(data.woeid.keys())}")
            return

        trends = self.api.trends_place(region_id)
        self.trends[region] = trends[0]['trends']

    def print_top_trends(self):
        print(f"\n{FONT.BOLD}Top trends:{FONT.END}")
        for region_key in self.trends:
            print(f"\t* {region_key}: {str([trend['name'] for trend in self.trends[region_key]])[1:-1]}")

    def _get_tweets_with_query(self, query: str):
        self.search_results = self.api.search(q=query)

    @staticmethod
    def _print_with_indent(text: str):
        newline_idxs = [0] + [m.start() for m in re.finditer('\n', text)] + [-1]
        for i in range(len(newline_idxs) - 1):
            line = text[newline_idxs[i]:newline_idxs[i + 1]]
            if i == 0:
                print('\t* ' + str(line[1:] if line[:1] == '\n' else line))
            else:
                print('\t  ' + str(line[1:] if line[:1] == '\n' else line))

    def print_tweets_with_query(self, query: str):
        self._get_tweets_with_query(query)
        print(f"\n{FONT.BOLD}Tweets that include keyword "
              f"{FONT.ITALIC}{query}{FONT.END}:")
        for tweet in self.search_results:
            self._print_with_indent(tweet.text)

    def _get_streaming_data(self):
        stream_listener = TwitterListener(num_tweets_to_grab=self.num_tweets_to_analyze,
                                          stats=self.stats, retweet_count=self.retweet_count)
        stream = tweepy.Stream(self.api.auth, stream_listener)
        try:
            stream.sample()
        except Exception as e:
            print(e, e.__doc__)

        return self.stats.get_stats()

    def print_streaming_data(self):
        languages, top_languages, top_tweets = self._get_streaming_data()
        print(f"\n{FONT.BOLD}Languages of the analyzed tweets:"
              f"{FONT.END}\n{str(languages)[1:-1]}")
        print(f"\n{FONT.BOLD}Tweets with more than {self.retweet_count} "
              f"retweets: {FONT.END}")
        print(f"\t* languages:\t\t{str(top_languages)[1:-1]}")
        print(f"\t* tweets:\t\t\t{str([tweet.text for tweet in top_tweets])[1:-1]}")
        print(f"\t* tweets' htmls:\t{str([tweet.html for tweet in top_tweets])[1:-1]}")


class TwitterListener(StreamListener):

    def __init__(self, num_tweets_to_grab, stats, retweet_count):
        super().__init__()
        self.counter = 0
        self.num_tweets_to_grab = num_tweets_to_grab
        self.retweet_count = retweet_count
        self.stats = stats

    def on_data(self, raw_data):
        if self.counter >= self.num_tweets_to_grab:
            return False

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
                    tweet = Tweet(self.api, language, retweet_count, json_data['text'], json_data['id'])
                    self.stats.add_top_tweet(tweet)
                    self.stats.add_top_language(language)

            self.stats.add_language(language)
            self.counter += 1
        return True

    def on_error(self, status_code):
        print(status_code)

    def get_top_tweets(self):
        return self.top_tweets


class Tweet:

    def __init__(self, api, language, retweet_count, text, id):
        self.language = language
        self.retweet_count = retweet_count
        self.text = text
        self.html = self._get_html(api, id)

    @staticmethod
    def _get_html(api, id):
        oembed = api.get_oembed(id=id, hide_media=True, hide_thread=True)
        html_info = oembed['html'].strip('\n')
        idx = [html_info.find('a href=\"', 1) + 8]
        idx.append(idx[0] + html_info[idx[0]:].find('\"'))
        return html_info[idx[0]:idx[1]]
