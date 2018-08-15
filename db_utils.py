import os
import json

def load_dbs(path):
    search_db = load_search_db(os.path.join(path, 'search.json'))
    learn_db = load_learn_db(os.path.join(path, 'learn.json'))
    context_db = load_context_db(os.path.join(path, 'context.json'))
    return search_db, learn_db, context_db

def save_dbs(path, search_db, learn_db, context_db):
    save_search_db(os.path.join(path, 'search.json'), search_db)
    save_learn_db(os.path.join(path, 'learn.json'), learn_db)
    save_context_db(os.path.join(path, 'context.json'), context_db)

#def merge_dbs(bot1, bot2, new_bot):
#    save_dbs(new_bot, merge_search(bot1, bot2), merge_learn(bot1, bot2), merge_context(bot1, bot2))

#LOAD BOTS
def load_learn_db(filename):
    with open(filename, 'r') as outfile:
        learn_db = json.load(outfile)
    return learn_db

def load_search_db(filename):
    with open(filename, 'r') as outfile:
        search_db = json.load(outfile)
    return search_db

def load_context_db(filename):
    with open(filename, 'r') as outfile:
        context_db = json.load(outfile)
    return context_db

#SAVE BOTS
def save_learn_db(filename, learn_db):
    with open(filename, 'w') as outfile:
        json.dump(learn_db, outfile, sort_keys=True, indent=4, separators=(',', ': '))


def save_search_db(filename, search_db):
    with open(filename, 'w') as outfile:
        json.dump(search_db, outfile, sort_keys=True, indent=4, separators=(',', ': '))

def save_context_db(filename, context_db):
    with open(filename, 'w') as outfile:
        json.dump(context_db, outfile, sort_keys=True, indent=4, separators=(',', ': '))


# MERGE BOTS
'''
def merge_learn(bot1, bot2):
    with open('learn_' + bot1 + '.json', 'r') as outfile:
        bot1_learn = json.load(outfile)
    with open('learn_' + bot2 + '.json', 'r') as outfile:
        bot2_learn = json.load(outfile)
    return {**bot1_learn, **bot2_learn}

def merge_search(bot1, bot2):
    with open('search_' + bot1 + '.json', 'r') as outfile:
        bot1_search = json.load(outfile)
    with open('search_' + bot2 + '.json', 'r') as outfile:
        bot2_search = json.load(outfile)
    return {**bot1_search, **bot2_search}

def merge_context(bot1, bot2):
    with open('context_' + bot1 + '.json', 'r') as outfile:
        bot1_context = json.load(outfile)
    with open('context_' + bot2 + '.json', 'r') as outfile:
        bot2_context = json.load(outfile)
    return merge_dicts(bot1_context, bot2_context)

def merge_dicts(d1, d2):
    both = d1.keys() & d2.keys()
    d3 = {**d1, **d2}
    for k in both:
        d3[k] = list(set(d3[k]).union(set(d1[k])))
    return d3
'''
