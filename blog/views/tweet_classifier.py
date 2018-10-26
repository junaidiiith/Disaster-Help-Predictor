#!/usr/bin/env python
# coding: utf-8

import pickle,os,sys,re
import numpy as np
import pandas as pd

import pickle, re, csv, string, nltk
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import normalize

dir_path = os.path.dirname(os.path.realpath(__file__))

def stripPunc(wordList):
    """Strips punctuation from list of words"""
    puncList = [".",";",":","!","?","/","\\",",","$","&",")","(","\""]
    for punc in puncList:
        for word in wordList:
            wordList=[word.replace(punc,'') for word in wordList]
    return wordList

def hash_handler(word):
    if word[0] is not '#':
        return [word]
    word = word[1:]
    return [a for a in re.split('([A-Z][a-z]+)', word) if a]

def categorise(X):
    states,map_states = np.unique(X,return_inverse=True)
#     print states
#     print map_states.shape
    return states,map_states

def classifier(x_train,y_train,x_test,y_test,clf,name,text,mappings):
    clf.fit(x_train,y_train)

    # pred_t = clf.predict(x_train)
    pred = clf.predict(x_test)


    # cf = confusion_matrix(y_test,pred)
    return clf.predict_proba(x_test), accuracy_score(y_test,pred)


def preprocess(tweet):
    urls = []
    m=re.search(r"http\S+", tweet)
    if(m):    
        tweet = str(re.sub(r"http\S+", "", tweet))


    l = stripPunc(tweet.split(" "))
    tweet = ' '.join([x for x in l])

    with open(dir_path+'/OOV_Dict/OOV_Dictionary_V1.0.tsv', 'rt',encoding='latin-1') as f:
        oov = [row for row in csv.reader(f.read().splitlines())]

    out = list()
    rep = list()
    for line in oov:
        w1,w2 = line[0].split('\t')
        out.append(w1)
        rep.append(w2)

    sw = set(stopwords.words('english'))

    out_cnt = 0
    words = list()
    for word in tweet.split():
        word = hash_handler(word)
        for w in word:
            if w not in sw and w[0] is not '@' and w[0] not in string.punctuation:
                if w in out:
                    out_cnt += 1
                    w = rep[out.index(w)]
                words.append(w.lower())
    return words

def main(datafile,labelfile):
    text = []
    with open(dir_path+'/'+datafile) as f:
        for row in f:
            text.append((row.strip()))


    tag = []
    with open(dir_path+'/'+labelfile) as f:
        for row in f:
            tag.append((row.strip()))
    print("Corpus created!!")
    corpus = list()
    # out_cnt = 0
    for tweet in text:
        t = preprocess(tweet)
        corpus.append(t)


    size=100
    model = Word2Vec(corpus,min_count=1,size=size,window=5,sg=1)

    words = list(model.wv.vocab)

    with open(dir_path+'/Word2Vec.pkl','wb') as f:
        pickle.dump(model,f)

    embed_size = size
    embed_data = list()
    final_labels = list()
    final_text = list()

    for i,tweet in enumerate(corpus):
        temp = np.zeros(embed_size)
        cnt = 0
        for w in tweet:
            temp = np.add(temp,model.wv[w.lower()])
            cnt += 1
        if cnt:
            temp = np.divide(temp,cnt)
            embed_data.append(temp)
            final_labels.append(tag[i])
            final_text.append(text[i])


    # In[21]:


    embed_data = np.asarray(embed_data)
    final_labels = np.asarray(final_labels)
    final_text = np.asarray(final_text)

    mappings,mapped_labels = categorise(final_labels)

    x_train, x_test, y_train, y_test, train_text, test_text = train_test_split(
        embed_data,mapped_labels,final_text,test_size=0.2,random_state=15)
    gbdt = GradientBoostingClassifier(n_estimators=150,verbose=0)
    gbdt_prob, gbdt_acc = classifier(x_train,y_train,x_test,y_test,gbdt,'gbdt',test_text,mappings)

    knn = KNeighborsClassifier(n_neighbors=25)
    knn_prob, knn_acc = classifier(x_train,y_train,x_test,y_test,knn,'knn',test_text,mappings)

    lr = LogisticRegression(verbose=0,max_iter=100)
    lr_prob, lr_acc = classifier(x_train,y_train,x_test,y_test,lr,'lr',test_text,mappings)

    mlp = MLPClassifier(hidden_layer_sizes=(128, 64, 32),verbose=0,random_state=15)
    mlp_prob, mlp_acc = classifier(x_train,y_train,x_test,y_test,mlp,'mlp',test_text,mappings)
    fused_prob = np.add(gbdt_acc*normalize(gbdt_prob),knn_acc*normalize(knn_prob))
    fused_prob = np.add(fused_prob,lr_acc*normalize(lr_prob))
    fused_prob = np.add(fused_prob,mlp_acc*normalize(mlp_prob))

    fused_pred = np.argmax(fused_prob,axis=1)
    mapped_pred = mappings[fused_pred]
    return (gbdt,gbdt_acc,mlp,mlp_acc,lr,lr_acc,knn,knn_acc,model,mappings)
   
