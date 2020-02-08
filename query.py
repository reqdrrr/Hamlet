import nltk
import numpy as np
import random
import string

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#read corpus
f = open('hamlet.txt','r',errors='ignore')
raw = f.read()
raw = raw.lower()

nltk.download('punkt')
nltk.download('wordnet')

sent_tokens = nltk.sent_tokenize(raw)   #convert to list of sentences
word_tokens = nltk.word_tokenize(raw)   #convert to list of words

#pre-process raw text
lemmer = nltk.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

#keyword matching

GREETING_INPUTS = ("hello", "hi", "sup", "yo", "hey", "what's up",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "What seems to be the problem officer?"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, max_df=0.7)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

# --CLI-----
# flag=True
# print("GAUD: I am Gaud. Choose your questions carefully or I will pee your pants.")
# while(flag==True):
#     user_response = input("YOU: ")
#     user_response=user_response.lower()
#     if(user_response!='bye'):
#         if(user_response=='thanks' or user_response=='thank you' ):
#             flag=False
#             print("GAUD: You are welcome..")
#         else:
#             if(greeting(user_response)!=None):
#                 print("GAUD: "+greeting(user_response))
#             else:
#                 print("GAUD: ",end="")
#                 print(response(user_response))
#                 sent_tokens.remove(user_response)
#     else:
#         flag=False
#         print("GAUD: Bye! take care..")

# --Server-----
def chat(query):
    result = ''
    if(greeting(query)!=None):
        result = greeting(query)
    else:
        result = response(query)
        sent_tokens.remove(query)

    return result
