import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
class IntentClassifier(object):
  def __init__(self, classes, model, **kwargs):
    self.classes = classes
    self.classifier = model
    self.tokenizer = kwargs.get('tokenizer')
    self.label_encoder = kwargs.get('label_encoder')
    self.max_len = kwargs.get('max_len', 28)
  
  def __call__(self, text: str):
    sequence = self.tokenizer.texts_to_sequences([text])
    sequence = pad_sequences(sequence, maxlen=self.max_len, padding='post')
    pred = self.classifier(sequence)
    return self.label_encoder.inverse_transform(np.argmax(pred, 1))[0]

class EntityClassifier():
  def __init__(self, tags, model, **kwargs):
    self.__tags = tags
    self.__classifier = model
    self.__tokenizer = kwargs.get('tokenizer')
    self.__vocab = list(self.__tokenizer.word_index.keys())
    self.__max_len = kwargs.get('max_len', 28)
  
  def __call__(self, message):
    sequence = self.__tokenizer.texts_to_sequences([message])
    p = self.__classifier.predict(sequence)
    p = np.argmax(p, -1)
    entities = []
    for x, y in zip(sequence[0], p[0]):
      if x == 0: break
      pair = (self.__vocab[x-1], self.__tags[y])
      entities.append(pair)
    return entities

def load_intent_classifier(**kwargs):
    model_directory = kwargs.get('model', 'intent_classifier')
    classes_file = kwargs.get('classes', 'classes.pickle')
    tokenizer_file = kwargs.get('tokenizer', 'tokenizer_intent.pickle')
    label_encoder = kwargs.get('label_encoder', 'label_encoder.pickle')

    model = load_model(model_directory)

    with open(classes_file, 'rb') as _file:
        classes = pickle.load(_file)

    with open(tokenizer_file, 'rb') as _file:
        tokenizer = pickle.load(_file)
    
    with open(label_encoder, 'rb') as _file:
        label_encoder = pickle.load(_file)
    
    return IntentClassifier(
        classes,
        model,
        tokenizer=tokenizer,
        label_encoder=label_encoder
    )

def load_entity_classifier(**kwargs):
    model_directory = kwargs.get('model', 'entity_classifier')
    tags_file = kwargs.get('tags', 'tags.pickle')
    tokenizer_file = kwargs.get('tokenizer', 'tokenizer_entity.pickle')

    model = load_model(model_directory)

    with open(tags_file, 'rb') as _file:
        tags = pickle.load(_file)
    
    with open(tokenizer_file, 'rb') as _file:
        tokenizer = pickle.load(_file)
    
    return EntityClassifier(
        tags, model, tokenizer=tokenizer
    )