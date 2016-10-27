from weg_filter import to_key
from weg_math import get_random_index

def build_table(tweet):
    result = {}
    words  = tweet.split()

    i = 0
    while i < (len(words) - 1):
        this_key  = to_key(words[i])
        next_word = words[i+1]
        
        try:
            result[this_key].append(next_word)
        except KeyError:
            result[this_key] = []
            result[this_key].append(next_word)
        
        i += 1
    
    return result

def combine_tables(tables):
    result = {}
    
    for table in tables:
        for key in table:
            if not key in result:
                result[key] = []
            for word in table[key]:
                result[key].append(word)
    
    print('DEBUG combined %d markov tables' % len(tables))
    return result

def pick_random_key(big_table, last_key=None):
    index  = get_random_index(big_table)
    result = big_table.keys()[index]
    
    if last_key == None:
        return result
    
    if result == last_key:
        return pick_random_key(big_table, last_key=last_key)
    
    return result

def pick_random_value(arr):
    index = get_random_index(arr)
    return arr[index]
