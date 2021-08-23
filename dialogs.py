import json
import numpy as np
import pandas as pd

from intents.openinggreeting import OpeningGreeting
from collections import defaultdict
INVALID_INTENTS = ['confirmation', 'contentonly', 'outofdomain', 'rejection']
with open('answers.json') as _file:
    DIALOG_ANSWERS = json.loads(_file.read())
with open('dialogs.json') as _file:
    DIALOG_FLOW = json.loads(_file.read())

TOLERANCE = 3

claim_database = pd.read_csv('claims.csv')
policy_database = pd.read_csv('policy.csv')

class DialogManager(object):
    def __init__(self, user_name = '', current_intent = None, **kwargs):
        self.__user_name = user_name
        self.__current_intent = current_intent
        self.__entities = kwargs.get('entities', [])
        self.__patience = 0
        self.__possible_actions = []
        self.__current_action = ""
        self.__waiting_for_variable = False
        self.__current_message = ""
    
    @property
    def name(self):
        return self.__user_name
    
    @property
    def intent(self):
        return self.__current_intent
    
    @property
    def message(self):
        return self.__current_message
    
    def __call__(self, message, intent, entities = {}):
        self.__current_message = message
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
            self.__patience = 0
            self.__current_intent = intent
            print("New intent: %s" % intent)
        self.__entities += [(x, y) for x, y in entities if x != 'O']

        if intent in ('outofdomain', 'contentonly') and self.__waiting_for_variable:
            actions = DIALOG_FLOW[self.__current_intent]["actions"]
            entity_needed = actions[self.__current_action][0]
            self.__entities.append((entity_needed, self.message))
        
        if self.__current_action and (intent in ("confirmation", "rejection")):
            if intent == "confirmation":
                action = "ask_for_entities"
                self.__waiting_for_variable = True
            elif len(self.__possible_actions) > 0:
                action = "ask_for_confirmation"
                self.__current_action = self.__possible_actions.pop()
            else:
                self.__current_action = ''
                action = 'invalid'

        else:
            action = ''
            actions = DIALOG_FLOW[self.__current_intent]["actions"]
            print(actions)
            for action_name in actions:
                entities_needed = set(actions[action_name])
                if entities_needed <= set([x for x, y in self.__entities]):
                    action = action_name
                    return self.__evaluate_action(action, self.__entities)
            if self.__current_intent in DIALOG_ANSWERS:
                return np.random.choice(DIALOG_ANSWERS[self.__current_intent])
            if len(action) == 0:
                self.__possible_actions = [x for x in actions]
                self.__current_action = self.__possible_actions.pop()
                action = 'ask_for_confirmation'
        
        return self.__evaluate_action(action, self.__entities)
        
    def __evaluate_action(self, action, entities):
        print(action)
        if action == 'greet':
            self.__current_intent = None
            name = [y for x, y in self.__entities if x == 'name']
            name = ' '.join(name)
            return np.random.choice(DIALOG_ANSWERS['greetings']) % name
        elif action == 'ask_for_entities':
            return self.__ask_for_entities()
        elif action == 'ask_for_confirmation':
            return self.__ask_for_confirmation()
        elif action == "open_claim":
            pass
        elif action == "search_claim_by_name":
            return "Your claim status is: [OK]"
        elif action == "search_claim_by_claimid":
            return "There is no claim by that id number"
        elif action == "search_claim_by_ssn":
            return "Your claim status is: [OK]"
        else:
            return np.random.choice(DIALOG_ANSWERS['invalid'])
    
    def __ask_for_entities(self):
        actions = DIALOG_FLOW[self.__current_intent]["actions"]
        entities_needed = actions[self.__current_action]
        aliases = DIALOG_FLOW[self.__current_intent]["entities_aliases"]
        names = []
        for x in entities_needed:
            names.append(aliases[x] if x in aliases else x)
        asking = ', '.join(names[:-1:])
        asking = [asking] if asking else []
        asking = ' and '.join(asking + names[-1:])
        return "Can you please tell me your %s?" % asking
    
    def __ask_for_confirmation(self):
        action_name = self.__current_action
        if action_name in DIALOG_FLOW[self.__current_intent]['alias']:
            action_name = DIALOG_FLOW[self.__current_intent]['alias'][action_name]
        return "Do you want me to %s?" % action_name