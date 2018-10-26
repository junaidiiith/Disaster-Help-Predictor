import os
from blog.models.post import Post
from blog.models.comment import Comment
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener 
from tweepy import OAuthHandler
from blog.views import tweet_classifier
import numpy as np
import json
consumer_key = "3AhkJjBtIiFmvmZ06h8os31Eu"
consumer_secret = "OVxNFm3ipmr37d1FICWSHp62krc0xP4JWlQEUt5bfggTm7DXm8"
access_token = "365353775-CihmSQIIgjdB0MmKxmfPfAC0mpwsBM9xoulqbi69"
access_secret = "i4soDY2hqDIcKwGJq1ajjlDjJUL8rQJXfYUzyQxCHBAqD"
dir_path = os.path.dirname(os.path.realpath(__file__))
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status
 
# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse

import json
THRESHOLD = 5
modThresh = 30


def clean_tweet(tweet):
    tweet = json.loads(tweet)
    text = tweet['text']
    coordinates = None
    try:
        coordinates = tweet['coordinates']
    except:
        coordinates = None
    return text,coordinates

import datetime
global classifier

def predict(tweet,classifier):
    tweet = tweet_classifier.preprocess(tweet)
    cnt = 0
    temp = np.zeros(100,1)
    print(tweet)
    for w in tweet:
        if w in list(classifier[8].wv.vocab):
            temp = np.add(temp,classifier[8].wv[w.lower()])
            cnt += 1
    if cnt:
        embed_data = np.divide(temp,cnt)

    print(embed_data)
    clfs = [0,2,4,6]
    pred = np.zeros(8)
    for i in clfs:
        pred += classifier[i+1]*classifier[i].predict_proba(embed_data)
    print(pred)
    pred_label = np.argmax(pred)
    return classifier[9][pred_label]


def addToDatabase(tweet,classifier):
    cl = predict(tweet[0],classifier)
    print("printing class ",cl)
    text = tweet[0]
    location = tweet[1]
    if not location:
        location = "None"
    try:
        post.Post(clss=cl,location=location,body=text).save()
        p = post.Post.objects.all()
    except BaseException as e:
        print("Error while saving: ", str(e))


def reclassify():
    tweets = Post.objects.all()
    tweet_and_class = list()
    for tweet in tweets:
        votes = [comment.vote for comment in Comment.objects.filter(post=tweet)]
        if len(votes):
            votes = max(votes)
            if votes >= THRESHOLD:
                tweet.clss = votes
                tweet.save()
                tweet_and_class.append((tweet.body,tweet.clss))
    if len(tweet_and_class) > modThresh:
        newdata = [tweet for tweet,label in tweet_and_class]
        newlabels = [label for tweet,label in tweet_and_class]
        with open("text.txt",'rb') as f:
            for row in f:
                newdata.append(row)
        with open("tag.txt",'rb') as f:
            for row in f:
                newlabels.append(row)

        with open("text.txt",'wb') as f:
            for tweet in newdata:
                f.write(tweet)

        with open("tag.txt",'wb') as f:
            for tag in newlabels:
                f.write(tag)

        classifier = tweet_classfier()
        return classifier
classifier = tweet_classifier.main('text.txt','tag.txt')
class MyListener(StreamListener):
    def __init__(self,classifier):
        self.count =  0
        self.classifier = classifier     
    def on_data(self, data):
        try:
            data = clean_tweet(data)
            print(data)
            addToDatabase(data,self.classifier)
            print("Added tweet!")
            self.count += 1
            if self.count%100 == 0:
                self.classifier = reclassify()
            return True
        except BaseException as e:
            print("Error on_data: ",str(e))
        return True
 
    def on_error(self, status):
        print("Error mila number ",status)
        return True
 
#Set the hashtag to be searched
twitter_stream = Stream(auth, MyListener(classifier))
twitter_stream.filter(track=['#Disaster','#Floods',"#Hurricane","#BiharFloods"])