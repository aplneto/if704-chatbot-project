import json
import numpy as np

from intents.openinggreeting import OpeningGreeting
from collections import defaultdict
INVALID_INTENTS = ['confirmation', 'contentonly', 'outofdomain', 'rejection']
with open('answers.json') as _file:
    DIALOG_ANSWERS = json.loads(_file.read())
with open('dialogs.json') as _file:
    DIALOG_FLOW = json.loads(_file.read())

TOLERANCE = 3

class DialogManager(object):
    def __init__(self, user_name = '', current_intent = None, **kwargs):
        self.__user_name = user_name
        self.__current_intent = current_intent
        self.__entities = kwargs.get('entities', [])
        self.__patience = 0
        self.__possible_actions = []
        self.__current_action = ""
    
    @property
    def name(self):
        return self.__user_name
    
    @property
    def intent(self):
        return self.__current_intent
    
    def __call__(self, intent, entities = {}):
        if self.intent is None:
            if (intent in INVALID_INTENTS):
                print(self.__patience)
                self.__patience += 1
                if (self.__patience >= TOLERANCE):
                    return np.random.choice(DIALOG_ANSWERS['help'])
                return __evaluate_action('invalid', entities)
        return self.__start_dialog(intent, entities)
    
    def __start_dialog(self, intent, entities):
        if self.__current_intent is None:
            self.__current_intent = intent
        self.__entities += [(x, y) for x, y in entities if x != 'O']
        
        if self.__current_action and (intent in ("confirmation", "rejection")):
            if intent == "confirmation":
                action = current_action
            elif len(self.__possible_actions) > 0:
                action = "ask_for_confirmation"
                self.__current_action = self.__possible_actions
            else:
                self.__current_action = ''
                action = 'invalid'
        else:
            action = 'invalid'
            actions = DIALOG_FLOW[intent]["actions"]
            for action_name in actions:
                entities_needed = set(actions[action_name])
                print(entities_needed, action_name)
                if entities_needed <= set([x for x, y in self.__entities]):
                    action = action_name
        
        return self.__evaluate_action(action, self.__entities)
        

    
    def __evaluate_action(self, action, entities):
        
        if action == 'greet':
            name = [y for x, y in self.__entities if x == 'name']
            name = ' '.join(name)
            return np.random.choice(DIALOG_ANSWERS['greetings']) % name
        elif action == 'invalid':
            return np.random.choice(DIALOG_ANSWERS['invalid'])