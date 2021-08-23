import numpy as np

def greet(name):
    possible_greets = [
        'Hi, %s' % name,
        "Hello, %s" % name,
        'Hi, %s. How may I help you?' % name,
        "Hello, %s. Can I help you with something?" % name,
    ]
    return np.random.choice(possible_greets)


class OpeningGreeting:
    ACTIONS = {
        "greet" : greet
    }