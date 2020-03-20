#!/usr/bin/env python
# coding=utf-8

import requests
import json
from datetime import date
import time
import os
import tweepy

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

def makeTweet(tweet):
    apiKey = os.environ.get("TWITTER_API_KEY")
    secretKey = os.environ.get("TWITTER_SECRET_KEY")
    accessToken = os.environ.get("TWITTER_ACCESS_TOKEN")
    tokenSecret = os.environ.get("TWITTER_TOKEN_SECRET")
    
    auth = tweepy.OAuthHandler(apiKey, secretKey)
    auth.set_access_token(accessToken, tokenSecret)
    api = tweepy.API(auth)

    api.update_status(tweet)
    
def makeApiRequest():
    print("Starting job")
    posted = False
    while (not posted):
        response = requests.get("https://coronavirus-19-api.herokuapp.com/countries")
        try:
            for object in json.loads(response.content):
                if object['country'] == 'Sweden':
                    header = "Corona Virus Cases in Sweden"
                    data = "📅  Date = %s" % (date.today())
                    hashtags = "#COVID19 #CoronaSverige #Coronavirus #CoronaSweden"
                    tweet = " %s \n\n %s \n %s \n %s" % (header , data , formatTwitterEnglish(object), hashtags)
                    postTweet(tweet)

                    header = "Corona Virus Cases i Sverige"
                    data = "📅 Datum = %s" % (date.today())
                    hashtags = "#COVID19 #CoronaSverige #Coronavirus #CoronaSweden"
                    tweet = " %s \n\n %s \n %s \n %s" % (header , data , formatTwitterSwedish(object), hashtags)
                    postTweet(tweet)
                    posted = True
                    print("Finished job")
                    print("Finished job")
        except Exception as identifier:
            time.sleep(5)
            print(identifier)
            posted = True
    
    
    

def formatTwitterEnglish(object):
    confirmedCases = "🤒 Confirmed Cases = %s" % (object['cases'])
    criticalCases = "😷 Critical Cases = %s" % (object['critical'])
    deaths = "😢 Deaths = %s" % (object['deaths'])
    recovered = "🥳 Recovered = %s" % (object['recovered'])
    return ('%s \n %s \n %s \n %s \n ' % (confirmedCases, criticalCases, deaths, recovered))

def formatTwitterSwedish(object):
    confirmedCases = "🤒 Bekräftade fall = %s" % (object['cases'])
    criticalCases = "😷 Kritiska fall = %s" % (object['critical'])
    deaths = "😢 Dödsfall = %s" % (object['deaths'])
    recovered = "🥳 Krya på sig = %s" % (object['recovered'])
    return ('%s \n %s \n %s \n %s \n' % (confirmedCases, criticalCases, deaths, recovered))

def postTweet(tweet):
        makeTweet(tweet)

makeApiRequest()
