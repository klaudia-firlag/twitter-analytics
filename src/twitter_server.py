import tweepy

import src.config.data as data
from bin.modules import TwitterListener, TwitterMain
from src.config.local_config import *
from src.config.style import color


if __name__ == "__main__":
    num_tweets_to_analyze = 100
    retweet_count = 10000
    twit = TwitterMain(num_tweets_to_analyze, retweet_count)
    twit.get_tweets_with_query(query="travel")
    twit.get_top_trends(region="Worldwide")
    twit.get_streaming_data()

    # print_tweets_with_query("travel")
    # print_top_trends("Worldwide")

    # top_tweets = live_stream(num_tweets_to_analyze=100)
    # print([top_tweets[i].text for i in range(len(top_tweets))])
