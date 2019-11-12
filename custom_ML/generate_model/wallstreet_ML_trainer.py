import nltk#Natural language library
nltk.download('punkt')

from nltk.stem.lancaster import LancasterStemmer#Stemmer method to find root of word
stemmer = LancasterStemmer()

import numpy as np #Library to store data for machine learning
import tensorflow as tf #Powerful deep learning library developed by Google
import json #Method to import our JSON training data
from tensorflow import keras #ML API that sits ontop of Tensorflow 
import tensorboard# Realtime visualisation of training model
import datetime# Save logs of ML model corresponding to time
import os# Saving logs to a path
import pandas as pd # Powerdul data handling library

with open("intents.json") as file:# Load intens.JSON file
    data=json.load(file)






list_of_labels = [] #Tags Eg Stock,buy,sell,portfolio

for intent in data["intents"]:
                list_of_labels.append(intent["tag"])

stemmed_encoded_pattern = [] # E.g "hello how are you" is encoded to "[45,56,23,11]"
pattern_list = [] # All the different training phrases
token_pattern = [] # [['Show','me','my','portfolio'],[.....]]
labels = [] # Tags such as buy,sell,portfolio. Index in list corresponds to index in token_pattern

one_hot_labels = [] #Integer encoded labels



#Tokenise training phrases into words e.g "Show me my portfolio" is now ['Show','me','my','portfolio']
for intent in data["intents"]:
    
    for pattern in intent["patterns"]:
            pattern_list.append(pattern.lower())#Extract training phrase,lower case and add to list
            #wrds = nltk.word_tokenize(pattern.lower())
            text_to_word_token = keras.preprocessing.text.text_to_word_sequence(pattern, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' ') #Convert sentences to word tokens using Keras API
    
            token_pattern.extend(text_to_word_token)#Append tokenised sentence to list
            #token_pattern.extend(intent["tag"])
            labels.append(intent["tag"])# Add tag to list so tag retains index in sync with tokenised sentence
    
    if intent["tag"] not in labels:
        labels.append(intent["tag"])
        
        
token_pattern.extend(labels)#Adding labels to voacbulary list       

stem_token_pattern = [stemmer.stem(w.lower()) for w in token_pattern]# Dissolving words into its root and adding using list comprehension
        
remove_duplicate_words= pd.Series(stem_token_pattern).drop_duplicates().tolist()#Removing duplicate words and retain order of list
        



def vocab_len():# Work out length of vocabulary after it is integer encoded
        vocab_len_temp_list = []# 
        for i in range(len(remove_duplicate_words)):
                encoding = tf.keras.preprocessing.text.one_hot(
                remove_duplicate_words[i],
                10000,
                filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                lower=True,
                split=' '
                )
                vocab_len_temp_list.extend(encoding)
                temp_dic = dict(zip(vocab_len_temp_list,remove_duplicate_words))# Crreates a temporary dict to work out length

        return len(temp_dic)# Returns length of vocab after its been filtered and integer encoded






for i in range(len(remove_duplicate_words)):#Converts stemmed words into integer encoding
        encoding = tf.keras.preprocessing.text.one_hot(
        remove_duplicate_words[i],
        vocab_len(),
        filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
        lower=True,
        split=' '
        )
        stemmed_encoded_pattern.extend(encoding)#Attach to list







#Create a mapping to decode encoded pattern to words
myMap_number_word = dict(zip(stemmed_encoded_pattern,remove_duplicate_words))



#Create a mapping to encode word to integer 
myMap_word_number = dict(zip(remove_duplicate_words,stemmed_encoded_pattern))




# https://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-whilst-preserving-order



token_stem_phrase = []

#Generate list of stemmed training phrases
for w in pattern_list:
                   for_loop_stem = []
                   ind_words = keras.preprocessing.text.text_to_word_sequence(w, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' ')
                   for each_word in ind_words:
                           for_loop_stem.append(stemmer.stem(each_word.lower()))

                   token_stem_phrase.append(for_loop_stem)




encoded_token_stem_phrase = []


#Encode stemmed and tokenised phrases with integer encoding
for i in range(len(token_stem_phrase)):
        temp_list=[]
        for k in range(len(token_stem_phrase[i])):
                if token_stem_phrase[i][k] in myMap_word_number:
                        word_in_list = token_stem_phrase[i][k]
                        temp_list.append(myMap_word_number[word_in_list])
        encoded_token_stem_phrase.append(temp_list)









#Encode tag

encoded_label = []

#Integer encode tags
for i in range(len(labels)):
        if stemmer.stem(labels[i]) in myMap_word_number:
                tagWord = stemmer.stem(labels[i])
                encoded_label.append(myMap_word_number[tagWord])




#One hot encode tags



#Convert labels into integers based on index [0,1,2,3,4]
indices_labels = []
correct_indices_labels = []
for i in range(len(list_of_labels)):
        indices_labels.append(i)


for i in range(len(labels)):
        for k in range(len(list_of_labels)):
                if labels[i] == list_of_labels[k]:
                        correct_indices_labels.append(k)



# Work on indices encoding

#####################################################################################
#Legacy code for when one hot encoding was being tested 

indices_label_depth = len(indices_labels)

one_hot_labels.append( tf.one_hot(indices_labels,indices_label_depth,on_value=1,
    off_value= 0))



correct_order_one_hot_labels = []


#print(len(one_hot_labels[]),'range of 1hot labels')
for i in range(len(labels)):
        if labels[i] in list_of_labels:
                get_index = list_of_labels.index(labels[i])
                correct_order_one_hot_labels.append(one_hot_labels[0][get_index])



#convert tensor to numpy array
numpy_order_one_hot_labels = []
for i in range(len(correct_order_one_hot_labels)):
        a = (correct_order_one_hot_labels[i].numpy())
             
        numpy_order_one_hot_labels.append(a.tolist())

####################################################################################

#Padding senences in equal size for word embedding layer

encoded_token_stem_phrase= keras.preprocessing.sequence.pad_sequences(encoded_token_stem_phrase, maxlen=10, dtype='int32', padding='post', truncating='post', value=0)


training_data = np.array(encoded_token_stem_phrase)#Convert training data list to numpy array

training_labels = np.array(correct_indices_labels)#convert to numpy array


#Deep learning neural network model
model = keras.Sequential([
                        keras.layers.Embedding(len(myMap_word_number)+1,64),
                        keras.layers.GlobalAveragePooling1D(),
                        keras.layers.Flatten(),
                        keras.layers.Dense(8, activation = "relu"),
                        keras.layers.Dense(len(list_of_labels), activation = "softmax")
                        ])




#Defining algorithms to use for calculating and reducing loss
model.compile(optimizer="Adam", loss="sparse_categorical_crossentropy",metrics=["accuracy"]) 




training_comment = "_NA"#Custom comment for logs files

#directory to save log files
log_dir = os.path.join(
    "logs",
    "fit",
    datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")+training_comment,
)

# Extremely powerful realtime visualisation tool for ML models
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1, update_freq = "epoch", profile_batch=0)

print(model.summary())


#Defining what to feed into the ML model and for how many epochs to train
model.fit(training_data,training_labels, epochs=1000, callbacks=[tensorboard_callback], shuffle = True)



##tensorboard --logdir logs/fit







#========================Saving and testing ML model after training==========================
save_it = input("Do you want to save(y/n)")

if save_it == "y":
        model.save("wallstreetModelv2.h5")

        f= open("word_to_numb_dict.json","w+")
        json.dump(myMap_word_number, f, indent=4)

        f.close()

        f= open("numb_to_word_dict.json","w+")
        json.dump(myMap_number_word, f, indent=4)
        f.close()



def translateInput(userInput):
        tokeniseInput = []
        stemInput = []
        number_output=[]


        tokeniseInput.extend( keras.preprocessing.text.text_to_word_sequence(userInput, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' '))
        stemInput = [stemmer.stem(b.lower()) for b in tokeniseInput]

        for i in range(len(stemInput)):
                if stemInput[i] in myMap_word_number:
                        number_output.append(myMap_word_number.get(stemInput[i]))
                
                else:
                        number_output.append(0)
        

        number_output = keras.preprocessing.sequence.pad_sequences([number_output], maxlen=15, dtype='int32', padding='post', truncating='post', value=0)        
      #  print(number_output)
        return number_output



        



#Evaluate model



while True:
        print('Evaluating model\n')
        eval_input = input("Enter eval data\n")

        if eval_input == "quit":
                save_it = input("Do you want to save(y/n)")

                if save_it == "y":
                        model.save("stockmodel",datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S"))

        translated_eval_input = np.array( translateInput(eval_input))



        modelsPrediction = model.predict(translated_eval_input)
     #   print(modelsPrediction)
      #  print('tag_index:',np.argmax(modelsPrediction))
        print('----------')
        print("Classification: ",list_of_labels[np.argmax(modelsPrediction)])



