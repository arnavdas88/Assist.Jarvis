import sys

class Actions:
  
  def __init__(self):
    self.Functions = {}
    self.NullFunctions = {}
    return
  
  def Add(self, Name, Function = None):
    if Function == None:
      self.NullFunctions[Name] = None
    self.Functions[Name] = Function
    #print(Name, ' : ', Function)
    return
  
  def Func(self):
    return self.Functions.items()
  
  def Print(self):
    for key, value in self.Functions.items():
      print('[', key , ' : ', value, ']')
    return
  
  def ExecuteAction(self, intent, entities):
    try:
      if not len(entities.items()) == 0:
        return self.Functions[intent](entities)
      return self.Functions[intent]()
    except:
      # Add Exception, Error => log For why.did.skil.fail
      return


  def Mix(self, Entities, dialog):
    for key, value in Entities.items():
      r = key
      r = r.replace('_', ' ')
      r = "{" + r + "}"
      dialog = dialog.replace(r, value)
    return dialog
  
  def GetFeedbackDialog(self, intent, entities, dialog):
    try:
      if intent in self.NullFunctions.keys():
        f = open('error.log', 'a')
        f.writelines('\n' + intent + '|actions.exceptions.NoActionFoundError')
        f.close()
        return ''.join(['Oops! looks like you are out of luck... ' , 
        'This project is just for educational purpose and is a demo,' ,
        ' not a production ready app. Thus some of the capabilities are',
        ' not yet added. Please add them manually or contact the' ,
        ' developer at GitHub : arnavdas88 '])

      if intent in self.Functions.keys():
        if len(entities.items()) == 0:
          entities = self.Functions[intent]()
        else:
          entities = self.Functions[intent](entities)
      else:
        return dialog
    except:
      # Add Exception, Error => log For why.did.skil.fail
      error = str(sys.exc_info()[0]).replace('<class \'','').replace('\'>', '')
      f = open('error.log', 'a')
      f.writelines('\n' + intent + '|' + error)
      f.close()
      return "Oops! " + error + " occured."
    '''
    print('\n\t', entities.items(), '\n')
    '''

    for key, value in entities.items():
      r = key
      r = r.replace('_', ' ')
      r = "{" + r + "}"
      value = str(value)
      #print('[', key, ': ', value, ']')
      dialog = dialog.replace(r, value)
    return dialog

