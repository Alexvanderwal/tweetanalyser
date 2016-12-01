import re

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE)


def sanitize(tweet_text):
    # Method to clean the given tweet from unwanted charachters, this is so we don't end up with unwanted
    # charachters which could confuse our sentiment analysis

    #Make the text lowercase so its easier to handle
    tweet_text = tweet_text.lower()
    # change urls to URL
    tweet_text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http://[^\s]+))', 'URL', tweet_text)
    # change mentions to MENTION (for speed)
    tweet_text = re.sub('@[^\s]+', 'MENTION', tweet_text)
    # remove white space
    tweet_text = re.sub('[\s]+', ' ', tweet_text)
    # remove hashtags
    tweet_text = re.sub(r'#([^\s]+)', r'\1', tweet_text)
    # remove leestekens
    tweet_text = re.sub(r'[!:?.,-_]', '', tweet_text)
    # remove quotes
    tweet_text = re.sub("'", '', tweet_text)
    # strip the text
    tweet_text = tweet_text.strip('\'"')

    return tweet_text

def tokenize(tweet_text):
    return tokens_re.findall(sanitize(tweet_text))



