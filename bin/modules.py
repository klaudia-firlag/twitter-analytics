import json
from collections import Counter

from tweepy import StreamListener

from src.config.data import langs
from src.config.style import color


class TwitterListener(StreamListener):

    def __init__(self, num_tweets_to_grab, retweet_count=50000):
        super().__init__()
        self.counter = 0
        self.num_tweets_to_grab = num_tweets_to_grab
        self.retweet_count = retweet_count
        self.languages = []
        self.top_languages = []

    def on_data(self, raw_data):
        if self.counter >= self.num_tweets_to_grab:
            print(f"\n{color.BLUE}Languages of the processed tweets:{color.END}")
            print(self.languages)
            print(Counter(self.languages))
            print(f"\n{color.BLUE}Languages of the processed tweets that "
                  f"have more than {self.retweet_count} number of retweets:{color.END}")
            print(self.top_languages)
            print(Counter(self.top_languages))
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
                    print(f"\nLanguage: {language}, "
                          f"Retweeted {retweet_count} times. Tweet:\n"
                          f"{json_data['text']}")
                    self.top_languages.append(language)

            self.languages.append(language)
            self.counter += 1
        return True

    def on_error(self, status_code):
        print(status_code)
