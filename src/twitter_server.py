import tweepy

import src.config.data as data
from bin.modules import TwitterListener
from src.config.local_config import *
from src.config.style import color


def print_tweets_with_query(query):
    search_results = api.search(q=query)
    print(f"{color.BLUE}Tweets that include keyword "
          f"{color.ITALIC}{query}{color.END}:\n")
    for i in range(len(search_results)):
        print(f"{getattr(search_results[i], 'text')}\n"
              + "_" * 100)


def print_top_trends(region: str):
    try:
        trends = api.trends_place(data.woeid[region])
    except KeyError:
        print(f"Invalid region. Aviable regions:\n{list(data.woeid.keys())}")
        return

    print(f"{color.BLUE}Top global trends:{color.END}\n")
    trends = trends[0]['trends']
    for i in range(len(trends)):
        print(f"#{i + 1}\t{trends[i]['name']}")


def live_stream():
    stream_listener = TwitterListener()
    stream = tweepy.Stream(api.auth, stream_listener)
    try:
        stream.sample()
    except Exception as e:
        print(e, e.__doc__)


if __name__ == "__main__":
    auth = tweepy.OAuthHandler(cons_key, cons_sec)
    auth.set_access_token(app_key, app_sec)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    print_tweets_with_query("travel")
    print_top_trends("Worldwide")

    live_stream()
