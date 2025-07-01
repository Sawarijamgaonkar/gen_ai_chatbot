import random
import json 
import pickle
import numpy as np
import tensorflow as tf
import nltk 
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer=WordNetLemmatizer()

intents=json.loads(open(r'D:\college\internships\nullclass\chatbot\serenity_chatbot\serenity.json').read())

#creating empty list:
words=[]
classes=[]
documents=[]
ignoreLetters=["?","!",".",","]

#nester for loop to iterate through each pattern in intent file:
for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        #tokenizing: (seprating sentences to words/ token)
        wordList=nltk.word_tokenize(pattern)
        # to add token from current pattern to words list
        words.extend(wordList)
        # to open a tuple containing tokenized pattern and its associated intent tag to the document list:
        documents.append((wordList,intent["tag"]))
        # to update the class list:
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

# lemmatizing every word present in words except the ignore letters
words=[lemmatizer.lemmatize(word) for word in words if word not in ignoreLetters]
# to remove duplicate word:
words=sorted(set(words))
classes=sorted(set(classes))

pickle.dump(words,open("serentiy_words.pkl","wb"))
pickle.dump(classes,open("serenity_class.pkl","wb"))

# to prepare training data, by creating empty training list and outputempty is list of 0 for one zero or each class and will be used as template for our data
training=[]
outputEmpty=[0]*len(classes)

# preprocessing:
for document in documents:
    bag = []
    wordPatterns = document[0]
    wordPatterns = [lemmatizer.lemmatize(word.lower()) for word in wordPatterns]
    # if word is in pattern then 1 or else 0
    for word in words:
        bag.append(1) if word in wordPatterns else bag.append(0)

    outputRow = list(outputEmpty)
    outputRow[classes.index(document[1])] = 1
    training.append(bag + outputRow)
# shuffle training dataset:
random.shuffle(training)
training=np.array(training)
# splitting data into features in numpy:
trainX = training[:, : len(words)]
trainY = training[:, len(words) :]


model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(128, input_shape=(len(trainX[0]),), activation="relu"))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(64, activation="relu"))
model.add(tf.keras.layers.Dropout(0.5))
# output layer, softmax returns probablity and is used for multiclass classification:
model.add(tf.keras.layers.Dense(len(trainY[0]), activation="softmax"))
# sgd is stochastic gradient descent an optimizinf algorithm that helps module learn
# momentum helps accelerating grading vector in the right directing
# the nestrov momentum is modification of standard momentum that helps in improve performance
sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

hist = model.fit(
    np.array(trainX), np.array(trainY), epochs=400, batch_size=5, verbose=1
)
model.save("serenity_chatbot_model.h5", hist)
print("Done")
