import random
from fuzzywuzzy import process, fuzz
from text_normalization import clean


continuity = ["what else", "oh wow", "really?", "and?", "go on", "yeah", "yea", "ok", "yep", "great"]


class SimpleSearch(object):
    def __init__(self, db_search, db_learn):
        self._db_search = db_search
        self._db_learn = db_learn

    def get_response(self, text, past_intent=None, current_context=None):
        next_i = []
        if past_intent:
            next_i = self._db_learn[past_intent]['context_set']
        # check if 'what else'
        match, rate = self.fuzzy_matching(text, continuity, 70)
        if match != '':
            if next_i != []:
                if next_i[0] in self._db_learn:
                    response = random.choice(self._db_learn[next_i[0]]["responses"])
                    return response, next_i[0], self._db_learn[next_i[0]]['context'] # aargh!
        # check exact match
        match, confidence = self.fuzzy_matching(text, self._db_search.keys(), 65)

        #check if match found
        if match != '':
            intent = random.choice(self._db_search[match]["intents"])
            response = random.choice(self._db_learn[intent]["responses"])
            new_context = self._db_learn[intent]["context"]
            return response, intent, new_context
        else:
            if current_context:
                i = 'fallback_' + str(current_context)
                if i in self._db_learn:
                    return random.choice(self._db_learn[i]["responses"]), i, current_context

        # select global fallback
        return random.choice(self._db_learn['fallback_global']['responses']), 'fallback_global', ''  # returning random from fallbacks, no intent/topic match

    def fuzzy_matching(self, sentence, choices, confidence):
        query = clean(sentence)
        # TODO : more stuff for multiple matching sentences
        # Get a list of matches ordered by score, default limit to 5
        # process.extract(query, choices)
        match = process.extractOne(query, choices, scorer=fuzz.token_set_ratio)
        if match[1] > confidence:
            return match[0], match[1]
        else:
            return '', 0