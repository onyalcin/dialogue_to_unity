import os
import time
import logging
import json
from nltk import TweetTokenizer
import random
import re

from agent import Agent
from text_normalization import *
from db_utils import *
from unity_body import UnityBody
from simple_search import SimpleSearch
from bml.gesture import Gesture
from bml.speech import Speech, Mark


def return_response(question, prev_intent=None, prev_context=None):
    db_search, db_learn, db_context = load_dbs('joey1')
    dial = SimpleSearch(db_search=db_search, db_learn=db_learn)

    resp, intent, context = dial.get_response(question, prev_intent, prev_context)
    return resp, intent, context


g_db = open('bml/unity_gestures.json')
gesture_db = json.load(g_db)
print(gesture_db)
tokenizer = TweetTokenizer()

g_c = open('bml/gesture_categoriesSD.json')
gesture_categories = json.load(g_c)

def random_gesture():
    if random.random() < 0.2:
        return random.choice(gesture_db)
    else:
        return None

def gesture_on_word(word):
        for k, v in gesture_categories.items():
            if word in v["keywords"]:
                return random.choice(v["gestures"])[0]
            else:
                return random_gesture()


def to_bml(str_message):
    sentences = []
    markings = []
    #sent_count = 0
    for sent in re.split('[?.!]', str_message):
        if sent != '':
            speech_id = 'myspeech0'  # + str(sent_count)
            text = []
            gesture = []
            count = 0
            #text.append(Mark('T' + str(count)))
            #text.append('.')
            count += 1
            for word in tokenizer.tokenize(sent):
                text.append(Mark('T' + str(count)))
                text.append(word)
                #timing = speech_id + ':T' + str(count)
                timing = 'T' + str(count)
                new_gesture = gesture_on_word(word)
                if new_gesture is not None:
                    gesture += [Gesture(name=new_gesture, start=timing)]
                count += 1
            text.append(Mark('T' + str(count)))  # marking the ending of a message
            #markings.append([Speech(id=speech_id, text=text)] + gesture)
            markings.append([Speech(text=text)] + gesture)
            #sent_count += 1
            sentences.append(markings)
        return sentences

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('unity').setLevel(logging.WARN)

    with UnityBody() as unity_body, Agent(unity_body) as agent:
        time.sleep(2)

        while True:
            # agent.transition_listening()

            query = input('Ask me anything: ')
            if not query.strip():
                continue
            '''
            # remove quotes if you want to have real response
            clean_query = clean(query)
            query, intent, context = return_response(clean_query)
            print('response: ', query)
            '''

            bml_response = to_bml(query)
            for bml in bml_response:
                print('bml_response: ', bml)
                agent.transition_speaking(bml)
