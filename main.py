#!/usr/bin/env python
# coding=utf-8

import os
from datetime import date

import requests
import tweepy
from bs4 import BeautifulSoup


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

def scrapPage():
    response = requests.get("https://www.worldometers.info/coronavirus/")
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find(id="main_table_countries_today")
    rows = table.find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        for td in tds:
            if td.text == "Sweden":
                parentTds = td.parent.find_all('td')
                return {
                'country' : parentTds[1].text,
                'cases' : parentTds[2].text,
                'casesDiff': parentTds[3].text,
                'critical' : parentTds[7].text,
                'deaths' :  parentTds[4].text,
                'deathsDiff': parentTds[5].text,
                'recovered' : parentTds[6].text
                }

def makeScrap():
    print("Starting job")
    myResponse = scrapPage()

    header = "Corona Virus Cases in Sweden"
    data = "📅  Date = %s" % (date.today())
    hashtags = "#COVIDー19 #CoronaSverige #Coronavirus #CoronaSweden #CoronaVirusSweden #COVID19sverige"
    tweet = " %s \n\n %s \n %s \n %s" % (header , data , formatTwitterEnglish(myResponse), hashtags)
    postTweet(tweet.replace(',', ''))

    header = "Corona Virus Cases i Sverige"
    data = "📅 Datum = %s" % (date.today())
    tweet = " %s \n\n %s \n %s \n %s" % (header , data , formatTwitterSwedish(myResponse), hashtags)
    postTweet(tweet.replace(',', ''))
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

def postTweet(tweet):
    print(tweet)
    make_tweet(tweet)

makeScrap()
