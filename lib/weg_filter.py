import re

_initializedRE = False
_regexes       = {}

def _initRE():
    global _regexes, _initializedRE
    _regexes['find_hashtags'] = re.compile(r"#[A-Z0-9]+", re.IGNORECASE)
    _regexes['strip_punctuation'] = re.compile(r"[^a-zA-Z0-9\s]", re.IGNORECASE)
    _initializedRE = True

def filter_tweets(status):
    if len(status.user_mentions) == 0:
        if status.text.find('http') == -1:
            return status

def map_text(status):
    global _regexes, _initializedRE
    if not _initializedRE:
        _initRE()
    
    result = re.sub(_regexes['find_hashtags'], '', status.text)
    return result.strip()

def strip_punctuation(text):
    global _regexes, _initializedRE
    if not _initializedRE:
        _initRE()

    result = re.sub(_regexes['strip_punctuation'], '', text)
    return result.strip()

def to_key(word):
    return strip_punctuation(word).lower()
