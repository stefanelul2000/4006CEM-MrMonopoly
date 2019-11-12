import nltk
nltk.download('punkt')

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np 
import tensorflow as tf
import random
import json
from tensorflow import keras
import tensorboard
import datetime
import os
import pandas as pd

with open("intents.json") as file:
    data=json.load(file)

#print(data)


#Tokenize each pattern 


list_of_labels = []

for intent in data["intents"]:
                list_of_labels.append(intent["tag"])

stemmed_encoded_pattern = [] # E.g hello is encoded to 2765
pattern_list = [] # All the different phrases that the user may ask
token_pattern = [] # ['hello','how','are','you']
labels = [] # Tags Eg greetings
one_hot_labels = []
#
for intent in data["intents"]:
    
    for pattern in intent["patterns"]:
            pattern_list.append(pattern.lower())
            #wrds = nltk.word_tokenize(pattern.lower())
            wrds = keras.preprocessing.text.text_to_word_sequence(pattern, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' ')
    
            token_pattern.extend(wrds)
            #token_pattern.extend(intent["tag"])
            labels.append(intent["tag"])
    
    if intent["tag"] not in labels:
        labels.append(intent["tag"])
        
        
token_pattern.extend(labels)       

stem_token_pattern = [stemmer.stem(w.lower()) for w in token_pattern]
        
remove_duplicate_words= pd.Series(stem_token_pattern).drop_duplicates().tolist()
        

#find vocab length

#vocab_len = len(list_of_labels) + len(remove_duplicate_words)
vocab_len_temp_list = []
def vocab_len():
        for i in range(len(remove_duplicate_words)):
                encoding = tf.keras.preprocessing.text.one_hot(
                remove_duplicate_words[i],
                10000,
                filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                lower=True,
                split=' '
                )
                vocab_len_temp_list.extend(encoding)
                temp_dic = dict(zip(vocab_len_temp_list,remove_duplicate_words))

        return len(temp_dic)






for i in range(len(remove_duplicate_words)):
        encoding = tf.keras.preprocessing.text.one_hot(
         remove_duplicate_words[i],
        vocab_len(),
        filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
        lower=True,
        split=' '
        )
        stemmed_encoded_pattern.extend(encoding)


#print(remove_duplicate_words)
#print(stemmed_encoded_pattern)






myMap_number_word = dict(zip(stemmed_encoded_pattern,remove_duplicate_words))
myMap_word_number = dict(zip(remove_duplicate_words,stemmed_encoded_pattern))
#print(myMap_number_word)
#print(myMap_word_number)



# https://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-whilst-preserving-order

#======================================================
#
########### Buddy encoded pattern and tag



#print('\n')
#print(pattern_list)
#print(labels)

#stem_patern_list = [stemmer.stem(w.lower()) for w in pattern_list]

token_stem_phrase = []

for w in pattern_list:
                   for_loop_stem = []
                   ind_words = keras.preprocessing.text.text_to_word_sequence(w, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' ')
                   for each_word in ind_words:
                           for_loop_stem.append(stemmer.stem(each_word.lower()))

                   token_stem_phrase.append(for_loop_stem)




#print(token_stem_phrase)
#print('tags')
#print(labels)
#encoded_pattern_list = 

#replace token stem phrases with dictionary value


encoded_token_stem_phrase = []

for i in range(len(token_stem_phrase)):
        temp_list=[]
        for k in range(len(token_stem_phrase[i])):
                if token_stem_phrase[i][k] in myMap_word_number:
                        word_in_list = token_stem_phrase[i][k]
                        temp_list.append(myMap_word_number[word_in_list])
        encoded_token_stem_phrase.append(temp_list)


#print('encoded phrases')
#print(encoded_token_stem_phrase)








#Encode tag

encoded_label = []

for i in range(len(labels)):
        if stemmer.stem(labels[i]) in myMap_word_number:
                tagWord = stemmer.stem(labels[i])
                encoded_label.append(myMap_word_number[tagWord])



#print('Encoded label values')
#print(encoded_label)
"""
list_of_labels = []

for intent in data["intents"]:
                list_of_labels.append(intent["tag"])

"""
#One hot encode tags

indices_labels = []
correct_indices_labels = []
for i in range(len(list_of_labels)):
        indices_labels.append(i)


for i in range(len(labels)):
        for k in range(len(list_of_labels)):
                if labels[i] == list_of_labels[k]:
                        correct_indices_labels.append(k)


print(labels)
print(list_of_labels)

print(correct_indices_labels)

# Work on indices encoding


indices_label_depth = len(indices_labels)

one_hot_labels.append( tf.one_hot(indices_labels,indices_label_depth,on_value=1,
    off_value= 0))

#print(list_of_labels)
#print(one_hot_labels)


#get_order_of labels

correct_order_one_hot_labels = []


#print(len(one_hot_labels[]),'range of 1hot labels')
for i in range(len(labels)):
        if labels[i] in list_of_labels:
                get_index = list_of_labels.index(labels[i])
                correct_order_one_hot_labels.append(one_hot_labels[0][get_index])

#print(labels)
#print(correct_order_one_hot_labels)


#for intent in data["intents"]:
#        for pattern in intent["pattern"]:


#print(list_of_labels)

#print(correct_order_one_hot_labels)

#convert tensor to numpy
numpy_order_one_hot_labels = []
for i in range(len(correct_order_one_hot_labels)):
        a = (correct_order_one_hot_labels[i].numpy())
        
      #  x = [list(i) for i in a]        
        numpy_order_one_hot_labels.append(a.tolist())

"""
print('---------------------------------')
#print(correct_order_one_hot_labels[0].numpy())
print(correct_order_one_hot_labels)
print(len(numpy_order_one_hot_labels))
print('----------------------------------')
#numpy_order_one_hot_labels = numpy_order_one_hot_labels.astype(int)
print(numpy_order_one_hot_labels)
"""
#Padding senences in equal size

encoded_token_stem_phrase= keras.preprocessing.sequence.pad_sequences(encoded_token_stem_phrase, maxlen=10, dtype='int32', padding='post', truncating='post', value=0)

#print(encoded_token_stem_phrase)

training_data = np.array(encoded_token_stem_phrase)
#print(training_data)
#print(training_data)


#training_labels = np.array(numpy_order_one_hot_labels)
training_labels = np.array(correct_indices_labels)



#print(training_data)

#print(training_labels)





model = keras.Sequential([
                        keras.layers.Embedding(len(myMap_word_number)+1,64),
                        keras.layers.GlobalAveragePooling1D(),
                        keras.layers.Flatten(),
                        keras.layers.Dense(8, activation = "relu"),
                        keras.layers.Dense(len(list_of_labels), activation = "softmax")
                        ])




#Adagrad working wells
#Adadelta is better
#Adamax failed
#Nadam



model.compile(optimizer="Adam", loss="sparse_categorical_crossentropy",metrics=["accuracy"]) #changed sparse
#logs_dir="logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

training_comment = "_NA"

log_dir = os.path.join(
    "logs",
    "fit",
    datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")+training_comment,
)
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1, update_freq = "epoch", profile_batch=0)

print(model.summary())
model.fit(training_data,training_labels, epochs=1000, callbacks=[tensorboard_callback], shuffle = True)

#validation_data=(test_images,test_label

##tensorboard --logdir logs/fit

#TODO Numpyarry, output i.e tag sould be 2D array and tags should be classified as [0,0,0,1] tf.hots
#TODO work on indices label

#TODO 


save_it = input("Do you want to save(y/n)")

if save_it == "y":
        model.save("wallstreetModelv2.h5")

        f= open("word_to_numb_dict.json","w+")
        json.dump(myMap_word_number, f, indent=4)

        f.close()

        f= open("numb_to_word_dict.json","w+")
        json.dump(myMap_number_word, f, indent=4)
        f.close()


      #  f= open("labels_list","w+")
       # f.write(list_of_labels)
        #f.close()


        #Save tag list

        #Tag index




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



#TODO buy, sell View stock , view portfolio, (compare with index e.g FTSE 100, other stocks, own performance, each year), leaderboards, compare with someone