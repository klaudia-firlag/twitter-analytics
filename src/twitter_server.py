import tweepy

import src.config.data as data
from bin.modules import TwitterListener, TwitterMain
from src.config.local_config import *
from src.config.style import FONT


if __name__ == "__main__":
    num_tweets_to_analyze = 100
    retweet_count = 10000
    twit = TwitterMain(num_tweets_to_analyze, retweet_count)

    twit.get_tweets_with_query("travel")
    twit.get_top_trends("Worldwide")
    twit.print_streaming_data()
