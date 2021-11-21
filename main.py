#!/usr/bin/env python
# coding=utf-8

import os
from datetime import date

import requests
import tweepy

def make_tweet(tweet):
    api_key = os.environ.get("TWITTER_API_KEY")
    secret_key = os.environ.get("TWITTER_SECRET_KEY")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    token_secret = os.environ.get("TWITTER_TOKEN_SECRET")
    
    auth = tweepy.OAuthHandler(api_key, secret_key)
    auth.set_access_token(access_token, token_secret)
    api = tweepy.API(auth)
    try:
        api.update_status(tweet)
    except Exception as identifier:
        print(identifier)

def get_data():
    response = requests.get("https://coronavirus-tracker-api.herokuapp.com/v2/locations/242?source=jhu&timelines=false").json()
    latest = response['location']['latest']
    return {
        'cases' : str(latest['confirmed']),
        'deaths' : str(latest['deaths'])
    }

def create_tweet():
    print("Starting job")
    myResponse = get_data()

    header = "Corona Virus Cases in Sweden"
    data = "📅 Date = %s" % (date.today())
    hashtags = "#Sweden #Sverige #COVIDー19 #Coronavirus"
    tweet = " %s \n\n %s \n %s \n %s" % (header , data , formatTwitterEnglish(myResponse), hashtags)
    post_tweet(tweet.replace(',', ''))

    header = "Corona Virus Cases i Sverige"
    data = "📅 Datum = %s" % (date.today())
    tweet = " %s \n\n %s \n %s \n %s" % (header , data , formatTwitterSwedish(myResponse), hashtags)
    post_tweet(tweet.replace(',', ''))
    print("Finished job")

def formatTwitterEnglish(object):
    confirmedCases = "🤒 Confirmed Cases = %s" % (object['cases'])
    #criticalCases = "😷 Critical Cases = %s" % (object['critical'])
    deaths = "😢 Deaths = %s"  % (object['deaths'])
    #recovered = "🥳 Recovered = %s" % (object['recovered'])
    return ('%s \n %s \n' % (confirmedCases, deaths))

def formatTwitterSwedish(object):
    confirmedCases = "🤒 Bekräftade fall = %s" % (object['cases'])
    #criticalCases = "😷 Kritiska fall = %s" % (object['critical'])
    deaths = "😢 Dödsfall = %s" % (object['deaths'])
    #recovered = "🥳 Krya på sig = %s" % (object['recovered'])
    return ('%s \n %s \n' % (confirmedCases, deaths))

def post_tweet(tweet):
    print(tweet)
    make_tweet(tweet)

create_tweet()
