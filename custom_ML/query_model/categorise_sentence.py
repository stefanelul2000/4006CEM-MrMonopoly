import nltk
nltk.download('punkt')

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np 
import tensorflow as tf
import json
from tensorflow import keras





"""
========
Read me:
=========
Dependicies to install:

pip install nltk

pip install numpy

pip install tensorflow

================

METHOD
----------
evaluate_model(userInput)

-Pass string datatype

- Returns the classification of the user sentence

- E.g 
>>>>>>>evaluate_model('Buy 500 shares in Apple")

>>>>>>> "buy"

>>>>>>>evaluate_model('show me the stock price of Apple")

>>>>>>> "stock"




"""









#Load dictionary which translates words to text for model
with open("custom_ML/query_model/word_to_numb_dict.json") as file:
    mapWordToNumb=json.load(file)


#Load model V1
model = keras.models.load_model("custom_ML/query_model/wallstreetModelv1.h5")


#list of categories that can classify 
list_of_labels = ["stock","buy","sell","portfolio"]


#Converts string to tokenised and stem words, then converts to integers
def translateInput(userInput):
        tokeniseInput = []
        stemInput = []
        number_output=[]


        tokeniseInput.extend( keras.preprocessing.text.text_to_word_sequence(userInput, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' '))
        stemInput = [stemmer.stem(b.lower()) for b in tokeniseInput]

        for i in range(len(stemInput)):
                if stemInput[i] in mapWordToNumb:
                        number_output.append(mapWordToNumb.get(stemInput[i]))
                
                else:
                        number_output.append(0)
        

        number_output = keras.preprocessing.sequence.pad_sequences([number_output], maxlen=15, dtype='int32', padding='post', truncating='post', value=0)        
    
        number_output = np.array(number_output)

        return number_output



        

#Evaluate model, give string to get category

def evaluate_model(userInput):
        userInput = str(userInput)
        print(userInput)
        print(translateInput(userInput))
        modelsPrediction = model.predict(translateInput(userInput))
        print(modelsPrediction)
        
        return list_of_labels[np.argmax(modelsPrediction)]


       







