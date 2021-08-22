import json
import uuid
import requests
from dialogs import DialogManager
from classifiers import EntityClassifier, IntentClassifier, \
    load_entity_classifier, load_intent_classifier
from flask import Flask, request, session
from threading import Thread


intent_classifier = None
entity_classifier = None

server = Flask('Chatbot')
server.secret_key = "senha super segura"

dialogs = dict()

@server.before_request
def handle_sessions():
    if not 'user_id' in session:
        user_id = str(uuid.uuid4())
        user_dialog_manager = DialogManager('guest')
        dialogs[user_id] = user_dialog_manager
        session['user_id'] = user_id

@server.route('/message', methods=['POST'])
def _parse_sentence():
    message = request.json['message']
    if message:
        intent = intent_classifier(message)
        entities = intent_classifier(message)
        user_id = session['user_id']
        user_dialog_manager = dialogs[user_id]
        response = user_dialog_manager(intent, entities)
        return json.dumps(
            {'response' : response}
        )

if __name__ == '__main__':
    intent_classifier = load_intent_classifier()
    entity_classifier = load_entity_classifier()
    server.run(host='0.0.0.0', port=9000)