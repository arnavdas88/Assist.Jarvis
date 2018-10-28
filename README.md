# Assist.Jarvis
A functional chatbot inspired from Google's DialogFlow
### Google's DialogFlow
[DialogFlow](https://dialogflow.com/) is a framework by google that allow developers to create their own goal oriented chatbot using Machine Learning and NLP.<br>
### About This Project
#### How it works
It primarily functions in 4 different phase:<br>

(1) It classifies the Intent using an LSTM Intent Classifier.<br>
(2) It parses all the Entities from the given text input.<br>
(3) The Entities are then passed to an Action(a function) associated with the Intent.<br>
(4) A Sequence-to-Sequence model is used to generate the final output response.<br>

Dataflow for the weather intent :
<div  align="center">
  <img src="https://pbs.twimg.com/media/DQj-DiUUIAAm3M9.png" height = "60%" width = "60%">

  <img src="https://raw.githubusercontent.com/arnavdas88/Assist.Jarvis/master/imgs/Example3.png" height = "60%" width = "60%"><br><br>
</div>

--------
## Intent Classifier
Our model uses a simple 3 Layered Intent Classifier.

<div align="left">
  <img src="https://raw.githubusercontent.com/arnavdas88/Assist.Jarvis/master/imgs/Intent.png" height = "20%" width = "20%">
</div>

The First layer is an LSTM followes by 2 Dense layers.

<div align="center">
  <img src="http://colah.github.io/posts/2015-08-Understanding-LSTMs/img/LSTM3-chain.png" height = "50%" width = "50%">
</div>

-------

## Entity Parser
The Entity Parser uses Spacy library to do NLP tasks

## Actions
Functions to parse weather, do a search, etc....

## Dialog Model
The Dialog Generation is done by a Sequence-to-Sequence Model.

<div align="center">
  <img src="https://cdn-images-1.medium.com/max/2000/1*sO-SP58T4brE9EHazHSeGA.png" height = "80%" width = "75%">
</div>

----------

# Usage

The python files are stored in the './src/' folder. A standalone jupyter notebook is saved inside the folder notebook.
The Folder imgs contain screenshots of the program.


Run the file 'main.py' inside the folder './src' to run the program.

<b><i><u>* Estimated time for the application to load : 36 seconds</u></i></b>
<div align="center">
  <img src="https://raw.githubusercontent.com/arnavdas88/Assist.Jarvis/master/imgs/console.png" height = "80%" width = "75%">
</div>

Try typing Hi or hello.....
<div align="center">
  <img src="https://raw.githubusercontent.com/arnavdas88/Assist.Jarvis/master/imgs/Example1.png" height = "80%" width = "75%">
</div>
First, it shows the intent of the text, then the entities, the generated dialog and at last, the reply from the bot...

------
Try asking about the weather.....
<div align="center">
  <img src="https://raw.githubusercontent.com/arnavdas88/Assist.Jarvis/master/imgs/Example2.png" height = "80%" width = "75%">
</div>
