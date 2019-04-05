import os
import json

def load_dbs(path):
    search_db = load_search_db(os.path.join(path, 'search.json'))
    learn_db = load_learn_db(os.path.join(path, 'learn.json'))
    return search_db, learn_db

def save_dbs(path, search_db, learn_db):
    save_search_db(os.path.join(path, 'search.json'), search_db)
    save_learn_db(os.path.join(path, 'learn.json'), learn_db)


#LOAD BOTS
def load_learn_db(filename):
    with open(filename, 'r') as outfile:
        learn_db = json.load(outfile)
    return learn_db

def load_search_db(filename):
    with open(filename, 'r') as outfile:
        search_db = json.load(outfile)
    return search_db


#SAVE BOTS
def save_learn_db(filename, learn_db):
    with open(filename, 'w') as outfile:
        json.dump(learn_db, outfile, sort_keys=True, indent=4, separators=(',', ': '))


def save_search_db(filename, search_db):
    with open(filename, 'w') as outfile:
        json.dump(search_db, outfile, sort_keys=True, indent=4, separators=(',', ': '))

