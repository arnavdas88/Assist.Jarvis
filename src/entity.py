import spacy


class NER:
  def __init__(self, lang = 'en'):
    self.nlp = spacy.load('en')
    self.PropertyDiscription = {'GPE' : 'location', 'TIME' : 'time', 'DATE' : 'date'}
    self.replaceWords = {}
    return
  
  def GetFor(self, text = ''):
    doc = self.nlp(text)
    '''
    for ent in doc.ents:
        print(ent, ent.label_, [token.dep_ for token in ent])
    '''
    return doc.ents
  
  def AddCustomReplaceWords(self, words, _class):
    for word in words:
      self.replaceWords[word] = _class
    return

  def GetAllEntities(self, text = ''):
    doc = self.nlp(text)
    entities = {self.replaceWords[word] : word for word in text.split(' ') if word in self.replaceWords.keys()}
    for key, value in entities.items():
      r = key
      r = r.replace('_', ' ')
      r = "{" + r + "}"
      value = str(value)
      text = text.replace(r, value)
    entities.update({self.PropertyDiscription[ent.label_] : str(ent) for ent in doc.ents if ent.label_ in self.PropertyDiscription.keys()})
    for key, value in entities.items():
      r = key
      r = r.replace('_', ' ')
      r = "{" + r + "}"
      value = str(value)
      text = text.replace(r, value)
    return text, entities

  def train(self):
    return
