import json
import numpy as np

INVALID_INTENTS = ['confirmation', 'contentonly', 'outofdomain', 'rejection']
with open('answers.json') as _file:
    DIALOG_ANSWERS = json.loads(_file.read())

TOLERANCE = 3

class DialogManager(object):
    def __init__(self, user_name = '', current_intent = None, **kwargs):
        self.__user_name = user_name
        self.__current_intent = current_intent
        self.__entities = kwargs.get('entities', {})
        self.__patience = 0
    
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
                return np.random.choice(DIALOG_ANSWERS['invalid'])
            else:
                self.__start_dialog(intent, entities)
        return self.__handle_dialog(intent, entities)
    
    def __start_dialog(self, intent, entities):
        self.__current_intent = intent
        self.__entities = entities
    
    def __handle_dialog(self, intent, entities):
        pass
                