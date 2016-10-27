import os, twitter
import lib.weg_config as Config

from lib.weg_filter  import filter_tweets, map_text, to_key
from lib.weg_markov  import build_table, combine_tables, pick_random_value
from lib.weg_strings import sentence_case, remove_extra_quotes, realign_quotes, punctuate_end, remove_weirdness
from lib.weg_twitter import init as init_twitter, get_tweets, post_tweet


# Read config from wegbot.ini
config = Config.read(os.path.join(os.path.realpath('.'), 'wegbot.ini'))


# run below

def run():
    init_twitter(config)
    
    tweets = get_tweets()
    
    first_words = []
    for tweet in tweets:
        if len(tweet.split()) > 1:
            first_words.append(tweet.split()[0])
    
    first_word  = pick_random_value(first_words)
    
    tables = []
    for tweet in tweets:
        table = build_table(tweet)
        tables.append(table)
    
    big_table = combine_tables(tables)
    
    created_tweet = ''
    last_word = first_word
    
    while True:
        next_word = pick_random_value(big_table[to_key(last_word)])
    
        if (len(created_tweet) + len(next_word) + 1) >= 140:
            break
    
        created_tweet += next_word + ' '
        last_word = next_word
        
        try:
            next_word = pick_random_value(big_table[to_key(last_word)])
        except KeyError:
            break
    
    print('DEBUG unadulterated tweet: %s' % created_tweet)
    
    created_tweet = remove_weirdness(created_tweet)
    created_tweet = sentence_case(created_tweet)
    created_tweet = realign_quotes(created_tweet)
    created_tweet = punctuate_end(created_tweet)
    
    print('\n%d characters:\n%s' % (len(created_tweet), created_tweet))
    
    posted_update = post_tweet(created_tweet)
    print('\nDEBUG posted:\n%s' % posted_update.text)


if __name__ == "__main__":
    import time, sys

    running = True
    
    try:
        while running:
            run()

            sleep_delay = int(config['Wegbot']['delay'])
            print('\nDEBUG sleeping for %d seconds' % sleep_delay)
            time.sleep(sleep_delay)

            print('\n---\n')
    except KeyboardInterrupt:
        running = False
        print('FATAL KeyboardInterrupt\n')
        sys.exit(running)
    except TwitterError as e:
        running = False
        print('FATAL TwitterError\n')
        print(e)
        sys.exit(69)
