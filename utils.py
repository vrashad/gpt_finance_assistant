import string
import re
import yfinance as yf
from openai import OpenAI
from config import *

def remove_punctuation(word):
    punc_remove_list = [
        char for char in word if char not in string.punctuation]
    punc_removed_word = ''.join(punc_remove_list)
    return punc_removed_word

def remove_emoji(word):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', word)

def contains_number(word):
    for char in word:
        if char.isdigit():
            return True
    return False

def validate_ticker(log, ticker):
    log.info(f'in validate_ticker for ticker: {ticker}')

    try:
        yahoo_data = yf.download(tickers=ticker, period="1d")

        if not yahoo_data.empty:
            current_price = round(yahoo_data['Close'].iloc[-1], 2)
            return True, current_price
        else:
            return False, None
    except Exception as e:
        log.error(f"Error validating ticker {ticker}: {e}")
        return False, None

def get_gpt_summary(log, prompt):
    log.info(f'in get_gpt_summary with prompt: {prompt}')

    client = OpenAI(api_key=GPT_API_KEY, base_url=GPT_BASE_URL)

    base_instruct = "You are a helpful AI assistant tasked with summarizing stock market sentiment. Provide a concise summary of the key points and overall sentiment based on the given comments about a specific stock."

    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": base_instruct},
                {"role": "user", "content": prompt},
            ],
            max_tokens=4000,
            stream=False
        )
        chat_answer = response.choices[0].message.content

        log.info(f'here is the gpt response: {chat_answer}')
        return chat_answer
    except Exception as e:
        log.error(f"Error in get_gpt_summary: {e}")
        return None