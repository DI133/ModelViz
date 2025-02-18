# -*- coding: utf-8 -*-
"""Project_LogisticRegression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1R9TSKP4Y9CTRyddo4t9svCy4J_Te7Kz5
"""

# from google.colab import drive
# drive.mount('/content/drive')


# prompt: Read dataset from drive, 'Dataset_SDP.csv'

import pandas as pd
import io
import joblib
df = pd.read_csv(r'd:\ModelViz\backend\static\SpamTextCSV.csv')

# df = pd.read_csv('/content/drive/My Drive/ML SDP Project Items/SpamTextCSV.csv') # Assuming the file is in your MyDrive
print(df.head())

# Commented out IPython magic to ensure Python compatibility.
# import seaborn as sns
# import matplotlib.pyplot as plt
# # %matplotlib inline

# df.columns

# df.isnull().sum()
# df.info()

# #extra column indicating length of message
# df["Message Length"]=df["Message"].apply(len)

# #figure
# fig=plt.figure(figsize=(10,6))
# sns.histplot(
#     x=df["Message Length"],
#     hue=df["Category"]
# )
# plt.title("ham & spam messege length comparision")
# plt.show()

ham_desc = df[df["Category"]=="ham"]["Message Length"].describe()
spam_desc = df[df["Category"]=="spam"]["Message Length"].describe()
print("Ham Message Length Stats")
print(ham_desc)
print("Spam Message Length Stats")
print(spam_desc)

df["Category"].value_counts()
sns.countplot(
    data=df,
    x="Category"
)
plt.title("ham vs spam")
plt.show()

ham_count=df["Category"].value_counts()[0]
spam_count=df["Category"].value_counts()[1]

total_count=df.shape[0]

print("Ham contains:{:.2f}% of total data.".format(ham_count/total_count*100))
print("Spam contains:{:.2f}% of total data.".format(spam_count/total_count*100))

import numpy as np
#compute the length of majority & minority class
minority_len=len(df[df["Category"]=="spam"])
majority_len=len(df[df["Category"]=="ham"])

#store the indices of majority and minority class
minority_indices=df[df["Category"]=="spam"].index
majority_indices=df[df["Category"]=="ham"].index

#generate new majority indices from the total majority_indices
#with size equal to minority class length so we obtain equivalent number of indices length
random_majority_indices=np.random.choice(
    majority_indices,
    size=minority_len,
    replace=False
)
#concatenate the two indices to obtain indices of new dataframe
undersampled_indices=np.concatenate([minority_indices,random_majority_indices])

# print(undersampled_indices)
#create df using new indices
data=df.loc[undersampled_indices]

#shuffle the sample
data=data.sample(frac=1)

#reset the index as its all mixed
data=data.reset_index()

#drop the older index
data=data.drop(
    columns=["index"],
)

data.shape
data["Category"].value_counts()

data.head()

data.shape

import nltk

nltk.download('stopwords')
nltk.download('punkt_tab')

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

stemmer=PorterStemmer()
#declare empty list to store tokenized message
corpus=[]

#iterate through the data["Message"]
for message in data["Message"]:

    #replace every special characters, numbers etc.. with whitespace of message
    #It will help retain only letter/alphabets
    message=re.sub("[^a-zA-Z]"," ",message)

    #convert every letters to its lowercase
    message=message.lower()

    #split the word into individual word list
    message=message.split()

    #perform stemming using PorterStemmer for all non-english-stopwords
    message=[stemmer.stem(words)
            for words in message
             if words not in set(stopwords.words("english"))
            ]
    #join the word lists with the whitespace
    message=" ".join(message)

    #append the message in corpus list
    corpus.append(message)

corpus[0]

newdf = pd.DataFrame({"Message":corpus,"Label":data["Label"]})

newdf.head()

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)
X = vectorizer.fit_transform(data["Message"])
y = data["Label"]

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

LR_model = LogisticRegression()
LR_model.fit(X_train, y_train)

y_pred = LR_model.predict(X_test)
print(classification_report(y_test, y_pred))

# from sklearn.metrics import confusion_matrix
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Assuming y_test and y_pred are already defined from your previous code

# cm = confusion_matrix(y_test, y_pred)

# plt.figure(figsize=(8, 6))
# sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
#             xticklabels=['Ham', 'Spam'], yticklabels=['Ham', 'Spam'])
# plt.xlabel('Predicted')
# plt.ylabel('Actual')
# plt.title('Confusion Matrix')
# plt.show()

# from sklearn import metrics
# from sklearn.metrics import recall_score, precision_score

# accuracy = metrics.accuracy_score(y_test, y_pred)
# print("Accuracy:", accuracy)
# recall = recall_score(y_test, y_pred, pos_label=1)
# print("Recall:", recall)
# precision = precision_score(y_test, y_pred, pos_label=1)
# print("Precision:", precision)

# prompt: construct a function that takes the model and sentence and prints whether sentence is spam or not spam

def predict_spam(model, sentence):
    # Preprocess the input sentence
    stemmer = PorterStemmer()
    sentence = re.sub("[^a-zA-Z]", " ", sentence)
    sentence = sentence.lower()
    sentence = sentence.split()
    sentence = [stemmer.stem(word) for word in sentence if word not in set(stopwords.words("english"))]
    sentence = " ".join(sentence)

    # Vectorize the sentence
    vectorized_sentence = vectorizer.transform([sentence])

    # Make the prediction
    prediction = model.predict(vectorized_sentence)[0]

    # Print the result
    if prediction == 1:
        print("Spam")
    else:
        print("Not Spam")

# predict_spam(LR_model, "Going for shopping to buy dress")
# predict_spam(LR_model, "You won 200$!! Woahh!! email us your account number and you will get your prize money!!")
# predict_spam(LR_model, "select free consult financi advisor schedul")
# predict_spam(LR_model, "Had your mobile 11 months or more? U R entitled to Update to the latest colour mobiles with camera for Free! Call The Mobile Update Co FREE on 08002986030")
# predict_spam(LR_model, "good to see you there, thanks for coming.")

joblib.dump(LR_model, 'svm_joblib.pkl')