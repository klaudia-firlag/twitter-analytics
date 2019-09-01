from bin.modules import TwitterMain

if __name__ == "__main__":
    num_tweets_to_analyze = 100
    retweet_count = 10000
    twit = TwitterMain(num_tweets_to_analyze, retweet_count)

    twit.print_tweets_with_query("travel")

    twit.add_top_trends("Worldwide")
    twit.add_top_trends("Poland")
    twit.print_top_trends()

    twit.print_streaming_data()
