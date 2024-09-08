# config.py

NEWSLETTER_LOG_PATH = 'stock_analysis_logs/'

REDDIT_CLIENT_ID = 'your_client_id'
REDDIT_CLIENT_SECRET = 'your_client_secret'
REDDIT_USER_AGENT = 'your_user_agent_name'
REDDIT_COUNT = 100
STOCK_COMMENT_MIN_COUNT = 0

SUBREDDITS_TO_QUERY = ['stocks', 'wallstreetbets']

KNOWN_NOT_STOCKS = ['UPVOTE', 'SUPPORT', 'YOLO', 'CLASS', 'ACTION', 'LAWSUIT', 'AGAINST', 'VALHALLA', 'MOON', 'PE', 'COVID', 'IMO', 'IPO', 'BTC', 'PUT', 'CALL','ROBINHOOD', 'GAIN', 'LOSS', 'PORN', 'WSB', 'I', 'STILL', "DIDN'T", 'HEAR', 'EBITDA', 'SQUEEZE', 'BS', 'VIX', 'FUD', 'HUT', 'ITM', 'OTM', 'NO', 'BELL', 'CEO', 'CFO', 'DD', 'MOASS', 'STONK', 'MEME', 'DICK', 'FOMO', 'EV', 'PIPE', 'HOLD', 'OTC', 'NOKPF', 'TTM', 'SPY', 'EVER', 'TO', 'A', 'THE', 'FUCK', 'US', 'FUCKING', 'ARE', 'DD', 'US', 'TLDR', 'EDIT', 'IV', 'SP500', 'SEC', 'GLOBE', 'NEWSWIRE', 'PT', 'NYSE', 'SPAC', 'FDA', 'DNA', 'HODL', 'USDA', 'PTSD', 'ETF', 'LLC', 'CSE', 'USA', 'EPS', 'BUY', 'B', 'AM', 'PM', 'SI', 'SP', 'TBA', 'TBD', 'TA', 'AI', 'LINK','CLICK', 'IRA', 'LIVE', 'NEXT', 'FID', 'UK', 'IP', 'FOMC', 'HOUR', 'API', 'SIP', 'FREE', 'NASDAQ', 'VOTE', 'NSFW', 'PGA','LIV', 'LOL', 'WEED', 'OP', 'AH', 'PL', 'VR', 'AR', 'FB', 'YTD', 'WSJ', 'NOT', 'ATH', 'CPI', 'CNBC', 'NBC', 'ADD', 'SERIOUS', 'FYI', 'GPT', 'DCA', 'FOR', 'BTFD', 'RIF']

TWITTER_LIST_ID = '1426231980518252551'
RAPIDAPI_KEY = 'your_rapidapi_key'
RAPIDAPI_HOST = 'twitter-api47.p.rapidapi.com'
TWEET_COUNT = 100
STOCK_TWEET_MIN_COUNT = 0

GPT_MIN_COMMENT_COUNT = 4
GPT_API_KEY = 'your_openai_api_key'
GPT_BASE_URL = 'https://api.openai.com/v1/chat/completions'
GPT_MODEL = 'gpt-4o'

OUTPUT_FILE_PATH = 'stock_analysis_report.md'