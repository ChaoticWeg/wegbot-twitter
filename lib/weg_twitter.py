import twitter

from weg_filter import filter_tweets, map_text

_config = None
_api    = None

def init(config):
    global _config, _api

    if not _config == None and not _api == None:
        return

    _config = config
    
    api_config = config['TwitterAPI']

    _api = twitter.Api(
        consumer_key        =       api_config['consumerkey'],
        consumer_secret     =    api_config['consumersecret'],
        access_token_key    =    api_config['accesstokenkey'],
        access_token_secret = api_config['accesstokensecret'],
        sleep_on_rate_limit = True
    )


def get_tweets():
    global _config, _api

    if _config == None or _api == None:
        print('FATAL called get_tweets() before initializing config and/or API')
        raise RuntimeError

    twitter_config    = _config['Twitter']
    hive_mind_members = _api.GetListMembers(
        slug              = twitter_config['listslug'],
        owner_screen_name = twitter_config['username'],
        skip_status       = True
    )

    print('DEBUG pulling tweets from %d members\n' % len(hive_mind_members))

    raw_tweets = _api.GetListTimeline(
        slug = twitter_config['listslug'],
        owner_screen_name = twitter_config['username'],
        count = twitter_config['tweetcount'],
        include_rts = False,
    )
    
    result = filter(filter_tweets, raw_tweets)
    result = map(map_text, result)
    
    return result

def post_tweet(text):
    global _config, _api
    
    if _config == None or _api == None:
        print('FATAL called post_tweet() before initializing config and/or API')
        raise RuntimeError

    return _api.PostUpdate(text)

