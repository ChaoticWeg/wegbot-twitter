from weg_markov import pick_random_value
import re

_initializedRE = False
_regexes       = {}

def _initRE():
    global _initializedRE, _regexes

    if _initializedRE: return
    
    _regexes['is_lower_alpha']  = re.compile(r"[a-z]")
    _regexes['is_not_alpha']    = re.compile(r"[^a-zA-Z]")
    _regexes['find_quotes']     = re.compile(r"\"")
    _regexes['not_a_quote']     = re.compile(r"[^\"]")
    _regexes['is_sentence_end'] = re.compile(r"^.*[\!\?\.]+\"?$")
    _regexes['is_weirdness']    = re.compile(r"\&gt;")
    _regexes['is_punctuation']  = re.compile(r"[\!\?\.]+")
    
    _initializedRE = True


def sentence_case(text):
    _initRE()
    global _regexes

    words = text.split()
    
    i = 0
    cap_next_word = False
    while i < len(words):
        word = words[i]
        
        if i == 0:
            words[i] = capitalize_word(word)

        if cap_next_word:
            words[i] = capitalize_word(word)
            cap_next_word = False
        
        if re.match(_regexes['is_sentence_end'], word):
            cap_next_word = True
        
        i += 1

    return ' '.join(words).strip()

def capitalize_word(word):
    if (word[0].isupper()): return word

    _initRE()
    global _regexes

    i = 0
    capitalized = False

    while i < len(word):
        if re.match(_regexes['is_lower_alpha'], word[i]):
            word = replace_char_at_index(word, word[i].upper(), index=i)
            break
        i += 1
    
    return word.strip()

def replace_char_at_index(word, replacement, index=0):
    return word[0:index] + replacement + word[index+1:]

def remove_extra_quotes(text):
    _initRE()
    global _regexes

    quotes_count = len(re.sub(_regexes['not_a_quote'], '', text))
    print('DEBUG we have %d quotes in this tweet' % quotes_count)

    if not quotes_count % 2 == 0:
        index_of_last_quote = text.rfind('"')
        text = text[0:index_of_last_quote] + text[index_of_last_quote+1:]

    return text.strip()

def realign_quotes(text):
    _initRE()
    global _regexes

    quote_open = False
    
    words = text.split()
    i     = 0

    while i < len(words):
        word = words[i]
        word_no_punc = re.sub(_regexes['is_punctuation'], '', word)

        if word_no_punc.startswith('"'):
            if quote_open:
                # if open quote, but quote is already open, move quote to last word
                print('DEBUG open quote, but quote is already open: %s' % word)
                words[i-1] = words[i-1] + '"'
                words[i]   = words[i][1:]
                print('DEBUG == %s --> %s' % (word, words[i]))
                quote_open = False
            else:
                print('DEBUG opening new quote: %s' % word)
                quote_open = True

        if word_no_punc.endswith('"'):
            if not quote_open:
                # if close quote, but quote is not open, remove close quote
                print('DEBUG close quote, but quote not open: %s' % word)
                words[i] = re.sub(_regexes['find_quotes'], '', word)
                print('DEBUG == %s --> %s' % (word, words[i]))
            else:
                print('DEBUG closing quote: %s' % word)
                quote_open = False
            

        i += 1
    
    text = ' '.join(words)
    
    # if we leave a hanging quote open, close it
    if quote_open:
        print('DEBUG left quote open')
        if len(text) < 140:
            text = text + '"'
            print('DEBUG closed quote')
        else:
            text = text[0:len(text)-1] + '"'
            print('DEBUG replaced last character with close-quote')

        quote_open = False
        
    return text.strip()

def punctuate_end(text):
    _initRE()
    global _regexes

    words = text.split()

    last_word = words[len(words) - 1]

    if not re.match(_regexes['is_sentence_end'], re.sub(_regexes['find_quotes'], '', last_word)):
        if re.match(_regexes['is_not_alpha'], last_word[len(last_word) - 1]):
            print('DEBUG does not need to be punctuated: %s' % last_word)
            print('DEBUG last character in last word is: %s' % last_word[len(last_word) - 1])
        elif len(text) < 140:
            print('DEBUG properly punctuating last word: %s' % last_word)
            text = text + pick_random_value(['.', '?', '!'])
        else:
            print('DEBUG not properly punctuated but tweet is too long to fix: %s' % last_word)
    else:
        print('DEBUG properly punctuated: %s' % last_word)
    
    return text.strip()
   
def remove_weirdness(text):
    _initRE()
    global _regexes
    
    text = re.sub(_regexes['is_weirdness'], '', text)
    
    return text.strip()
