import logging
import os
import datetime
import json

from config import *
from reddit import get_reddit_tickers_and_comments
from twitter import get_twitter_tickers_and_tweets
from utils import validate_ticker, get_gpt_summary
from report_generator import generate_report


log = logging.getLogger()


def logging_handler():
    print('in logging_handler()')
    log_directory = NEWSLETTER_LOG_PATH

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_format = '%(asctime)s %(levelname)s %(module)s:%(lineno)d %(message)s'

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(stream_handler)

    log_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f'{log_directory}log-{log_name}.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(file_handler)

    logging.getLogger().setLevel(logging.DEBUG)

    return log_file


def main():
    print('in main method')

    log_file = logging_handler()

    log.info(f"started script at {datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")

    reddit_tickers = get_reddit_tickers_and_comments(log)
    log.info(f"here is the reddit_tickers in main: {json.dumps(reddit_tickers, indent=4)}")

    twitter_tickers = get_twitter_tickers_and_tweets(log)
    if twitter_tickers:
        log.info(f"here is the twitter_tickers in main: {json.dumps(twitter_tickers, indent=4)}")
    else:
        log.warning("No Twitter data available or error occurred while fetching Twitter data")

    combined_ticker_dicts = []

    if reddit_tickers is not None:
        for reddit_ticker in reddit_tickers:
            combined_record = reddit_ticker.copy()
            combined_record['combined_comments_and_tweets'] = combined_record.pop('comments')
            combined_record['combined_comment_and_tweet_count'] = combined_record.pop('comment_count')

            if twitter_tickers is not None:
                for twitter_ticker in twitter_tickers:
                    if twitter_ticker['ticker'] == reddit_ticker['ticker']:
                        combined_record['combined_comments_and_tweets'].extend(twitter_ticker['tweets'])
                        combined_record['combined_comment_and_tweet_count'] += twitter_ticker['tweet_count']
                        break

            combined_ticker_dicts.append(combined_record)

    if twitter_tickers is not None:
        for twitter_ticker in twitter_tickers:
            if not any(twitter_ticker['ticker'] == combined_ticker['ticker'] for combined_ticker in combined_ticker_dicts):
                combined_record = twitter_ticker.copy()
                combined_record['combined_comments_and_tweets'] = combined_record.pop('tweets')
                combined_record['combined_comment_and_tweet_count'] = combined_record.pop('tweet_count')
                combined_ticker_dicts.append(combined_record)

    log.info(f'here is the combined_ticker_dicts: {combined_ticker_dicts}')

    combined_ticker_dicts = [
        item for item in combined_ticker_dicts if item['combined_comment_and_tweet_count'] >= GPT_MIN_COMMENT_COUNT
    ]

    summary_list = []

    for ticker_dict in combined_ticker_dicts:
        is_valid, current_price = validate_ticker(log, ticker_dict['ticker'])

        if is_valid:
            log.info(f"ticker {ticker_dict['ticker']} is valid, sending to GPT for summary")

            comment_sentence = " ,".join(ticker_dict['combined_comments_and_tweets'])
            prompt = f"Summarize the sentiment and key points about {ticker_dict['ticker']} based on these comments: '{comment_sentence}'. Include any notable trends, concerns, or predictions mentioned."

            gpt_response = get_gpt_summary(log, prompt)
            log.info(f'here is the gpt_response in main: {gpt_response}')

            if gpt_response is not None:
                summary_dict = {
                    'ticker': ticker_dict['ticker'],
                    'gpt_summary': gpt_response,
                    'current_price': current_price,
                    'mention_count': ticker_dict['combined_comment_and_tweet_count']
                }
                summary_list.append(summary_dict)

    log.info(f'here is the final summary list: {json.dumps(summary_list, indent=4)}')

    generate_report(log, summary_list)


if __name__ == '__main__':
    main()