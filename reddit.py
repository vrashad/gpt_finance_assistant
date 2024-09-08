import praw
import traceback
import string
import re
import json
from collections import Counter

from config import *
from utils import remove_emoji, remove_punctuation, contains_number


def get_reddit_tickers_and_comments(log):
    log.info('in get_reddit_tickers_and_comments')

    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )

        log.info(reddit)

        word_collection = []  # list of every word
        potential_stock_tickers = []
        list_of_comments = []  # list of every sentence

        log.info(f'looping through these subreddits: {SUBREDDITS_TO_QUERY}')
        for subreddit in SUBREDDITS_TO_QUERY:

            log.info(f"checking submissions in this subreddit: {subreddit}")
            for submission in reddit.subreddit(subreddit).hot(limit=REDDIT_COUNT):

                log.info(f"HERE IS THE SUBMISSION TITLE: {submission.title}")
                word_collection.extend(submission.title.split())
                list_of_comments.append(submission.title.strip())

                submission.comments.replace_more(limit=0)

                for comment in submission.comments:
                    log.info(f"HERE IS A COMMENT: {comment.body}")
                    word_collection.extend(comment.body.split())
                    list_of_comments.append(comment.body.strip())

        for word in word_collection:
            cleaned_word = remove_punctuation(word)
            cleaned_word = remove_emoji(cleaned_word)

            if cleaned_word.isupper() and not contains_number(cleaned_word) and cleaned_word not in KNOWN_NOT_STOCKS and len(cleaned_word) >= 3:
                potential_stock_tickers.append(cleaned_word)

        log.info(f"here are the potential stock tickers: {potential_stock_tickers}")

        cnt = Counter(potential_stock_tickers)
        log.info(f'potential stock tickers with counts: {cnt}')

        sorted_tickers = [key for key, value in cnt.items()]
        log.info(f'sorted_tickers: {sorted_tickers}')

        list_of_ticker_dicts = []

        for ticker in sorted_tickers:
            log.info(f'checking if ticker: {ticker} is in comments')
            comments_with_ticker = []

            pattern = r'\b(\$?{})\b'.format(re.escape(ticker))
            for comment in list_of_comments:
                if re.search(pattern, comment) is not None:
                    comments_with_ticker.append(comment.replace("\n", ""))

            if len(comments_with_ticker) > STOCK_COMMENT_MIN_COUNT:
                ticker_info = {
                    "ticker": ticker,
                    "comments": comments_with_ticker,
                    "comment_count": len(comments_with_ticker)
                }
                list_of_ticker_dicts.append(ticker_info)

        log.info(f"here is the list_of_ticker_dicts: {json.dumps(list_of_ticker_dicts, indent=4)}")

        final_sorted = sorted(list_of_ticker_dicts, key=lambda x: x["comment_count"], reverse=True)
        log.info(f"here is the final_sorted: {json.dumps(final_sorted, indent=4)}")

        return final_sorted

    except Exception as e:
        log.error(f"Error in get_tickers_and_comments: {e}")
        log.error(f"Traceback for get_tickers_and_comments error: {traceback.format_exc()}")
        return None