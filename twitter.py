import json
import http.client
from config import *
from utils import remove_emoji, remove_punctuation, contains_number


def get_twitter_tickers_and_tweets(log):
    log.info('in get_twitter_tickers_and_tweets')

    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)

    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    }

    try:
        conn.request("GET", f"/v2/latest-list-tweets?listId={TWITTER_LIST_ID}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        response_data = json.loads(data.decode("utf-8"))

        log.info(json.dumps(response_data, indent=4, sort_keys=True))

        if 'data' in response_data:
            twitter_tickers = get_tickers_from_tweets(log, response_data['data'])
            return twitter_tickers
        else:
            log.error("Unexpected response format from Twitter API")
            return None
    except Exception as e:
        log.error(f"Error fetching Twitter data: {e}")
        return None


def get_tickers_from_tweets(log, tweets):
    log.info('in get_tickers_from_tweets')

    ticker_list = []
    tickers_and_tweets = []

    for tweet in tweets:
        if 'text' in tweet:
            tweet_text = tweet['text']
            tweet_words = tweet_text.split()

            for word in tweet_words:
                if word.startswith('$') and len(word) > 1:
                    ticker = word[1:]  # Удаляем символ $
                    if ticker.isupper() and not contains_number(ticker):
                        ticker = remove_emoji(ticker)
                        ticker = remove_punctuation(ticker)

                        ticker_list.append(ticker)

                        ticker_tweet_dict = {
                            'ticker': ticker,
                            'tweet': tweet_text
                        }
                        tickers_and_tweets.append(ticker_tweet_dict)

    log.info(f'Twitter tickers_and_tweets: {json.dumps(tickers_and_tweets, indent=4)}')

    combined_list = combine_tweets_by_ticker(log, tickers_and_tweets)
    return combined_list


def combine_tweets_by_ticker(log, tickers_and_tweets):
    log.info('in combine_tweets_by_ticker')

    ticker_tweets = {}
    ticker_counts = {}

    for entry in tickers_and_tweets:
        ticker = entry['ticker']
        tweet = entry['tweet']

        if ticker in ticker_tweets:
            if tweet not in ticker_tweets[ticker]:
                ticker_tweets[ticker].append(tweet)
                ticker_counts[ticker] += 1
        else:
            ticker_tweets[ticker] = [tweet]
            ticker_counts[ticker] = 1

    combined_list = [{'ticker': ticker, 'tweets': tweets, 'tweet_count': ticker_counts[ticker]}
                     for ticker, tweets in ticker_tweets.items()]

    log.info(f'combined_list before sort: {json.dumps(combined_list, indent=4)}')

    combined_list.sort(key=lambda x: x['tweet_count'], reverse=True)
    log.info(f'combined_list after sort: {json.dumps(combined_list, indent=4)}')

    combined_list = [list_element for list_element in combined_list
                     if list_element['tweet_count'] > STOCK_TWEET_MIN_COUNT]
    log.info(f'combined_list after filter by minimum count: {json.dumps(combined_list, indent=4)}')

    return combined_list