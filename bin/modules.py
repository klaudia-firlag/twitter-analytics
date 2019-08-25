import json

from tweepy import StreamListener


class TwitterListener(StreamListener):

    def __init__(self, num_tweets_to_grab):
        super().__init__()
        self.counter = 0
        self.num_tweets_to_grab = num_tweets_to_grab

    def on_data(self, raw_data):
        if self.counter >= self.num_tweets_to_grab:
            return False
        json_data = json.loads(raw_data)
        if 'text' in json_data:
            print(json_data['text'])
            self.counter += 1
        return True

    def on_error(self, status_code):
        print(status_code)
