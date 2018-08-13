from nltk import stem, tokenize, metrics

def process_input(io_text):
    commands = io_text.split('$')
    d = {'text':'','gesture': '', 'emotion':'', 'bml':''}
    for command in commands:
        if command.startswith('<gesture>'):
            d['gesture'] = clean_whitespace(command.strip('<gesture>'))
        elif command.startswith('<emotion>'):
            d['emotion'] = clean_whitespace(command.strip('<emotion>'))
        elif command.startswith('<bml>'):
            d['bml'] = clean_whitespace(command.strip('<bml>'))
        else:
            d['text'] = clean(command)
    return d

def dict_to_raw(d):
    raw = d['text'] + '$<gesture>' +clean_whitespace(d['gesture']) + '$<emotion>' + clean_whitespace(d['emotion']) + '$<bml>' + d['bml']
    return raw


#def fuzzy_match( s1, s2, max_dist=3):
#    return metrics.edit_distance(NLTK_normalize(s1), NLTK_normalize(s2)) <= max_dist


def clean_whitespace(text):
    """
    Remove any extra whitespace and line breaks as needed.
    """
    import re

    # Replace linebreaks with spaces
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

    # Remove any leeding or trailing whitespace
    text = text.strip()

    # Replace any whitespaces with single space
    text = re.sub('\s+', text, ' ')

    return text


def clean(text):
    text= text.lower()
    # text = expand_contractions(text)
    text = clean_whitespace(text)
    return text


def expand_contractions(text):  # TODO do the same for Abbreviations!!
    import re

    contractions = {
        "ain't": "am not",
        "aren't": "are not",
        "can't": "cannot",
        "can't've": "cannot have",
        "'cause": "because",
        "could've": "could have",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hadn't've": "had not have",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'd've": "he would have",
        "he'll": "he will",
        "he'll've": "he will have",
        "he's": "he is",
        "how'd": "how did",
        "how'd'y": "how do you",
        "how'll": "how will",
        "how's": "how is",
        "I'd": "I would",
        "I'd've": "I would have",
        "I'll": "I will",
        "I'll've": "I will have",
        "I'm": "I am",
        "I've": "I have",
        "isn't": "is not",
        "it'd": "it would",
        "it'd've": "it would have",
        "it'll": "it will",
        "it'll've": "it will have",
        "it's": "it is",
        "let's": "let us",
        "ma'am": "madam",
        "mayn't": "may not",
        "might've": "might have",
        "mightn't": "might not",
        "mightn't've": "might not have",
        "must've": "must have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "needn't": "need not",
        "needn't've": "need not have",
        "o'clock": "of the clock",
        "oughtn't": "ought not",
        "oughtn't've": "ought not have",
        "shan't": "shall not",
        "sha'n't": "shall not",
        "shan't've": "shall not have",
        "she'd": "she would",
        "she'd've": "she would have",
        "she'll": "she will",
        "she'll've": "she will have",
        "she's": "she is",
        "should've": "should have",
        "shouldn't": "should not",
        "shouldn't've": "should not have",
        "so've": "so have",
        "so's": "so is",
        "that'd": "that had",
        "that'd've": "that would have",
        "that's": "that is",
        "there'd": "there would",
        "there'd've": "there would have",
        "there's": "there is",
        "they'd": "they would",
        "they'd've": "they would have",
        "they'll": "they will",
        "they'll've": "they will have",
        "they're": "they are",
        "they've": "they have",
        "to've": "to have",
        "wasn't": "was not",
        "we'd": "we would",
        "we'd've": "we would have",
        "we'll": "we will",
        "we'll've": "we will have",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what will",
        "what'll've": "what will have",
        "what're": "what are",
        "what's": " what is",
        "what've": "what have",
        "when's": "when is",
        "when've": "when have",
        "where'd": "where did",
        "where's": "where is",
        "where've": "where have",
        "who'll": "who will",
        "who'll've": "who will have",
        "who's": "who is",
        "who've": "who have",
        "why's": " why is",
        "why've": "why have",
        "will've": "will have",
        "won't": "will not",
        "won't've": "will not have",
        "would've": "would have",
        "wouldn't": "would not",
        "wouldn't've": "would not have",
        "y'all": "you all",
        "y'all'd": "you all would",
        "y'all'd've": "you all would have",
        "y'all're": "you all are",
        "y'all've": "you all have",
        "you'd": "you would",
        "you'd've": "you would have",
        "you'll": "you will",
        "you'll've": " you will have",
        "you're": "you are",
        "you've": "you have"
    }
    contractions_re = re.compile('(%s)' % '|'.join(contractions.keys()))

    def replace(match):
        return contractions[match.group(0)]

    return contractions_re.sub(replace, text)


def remove_stopwords(tokens, language):
    """
    Takes a language (i.e. 'english'), and a set of word tokens.
    Returns the tokenized text with any stopwords removed.
    Stop words are words like "is, the, a, ..."
    """
    from nltk.corpus import stopwords

    # Get the stopwords for the specified language
    stop_words = stopwords.words(language)

    # Remove the stop words from the set of word tokens
    tokens = set(tokens) - set(stop_words)

    return tokens

