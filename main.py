#!/usr/bin/env python
# coding=utf-8

import os
from datetime import date

import requests
import tweepy
from bs4 import BeautifulSoup


def makeTweet(tweet):
    apiKey = os.environ.get("TWITTER_API_KEY")
    secretKey = os.environ.get("TWITTER_SECRET_KEY")
    accessToken = os.environ.get("TWITTER_ACCESS_TOKEN")
    tokenSecret = os.environ.get("TWITTER_TOKEN_SECRET")
    
    auth = tweepy.OAuthHandler(apiKey, secretKey)
    auth.set_access_token(accessToken, tokenSecret)
    api = tweepy.API(auth)
    try:
        api.update_status(tweet)
        #print(tweet)
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
            if(td.text == "Sweden"):
                parentTds = td.parent.find_all('td')
                return {
                'country' : parentTds[1].text,
                'cases' : parentTds[2].text,
                'critical' : parentTds[7].text, 
                'deaths' :  parentTds[4].text,
                'recovered' : parentTds[6].text
                }

def makeScrap():
    print("Starting job")
    myResponse = scrapPage()

    header = "Corona Virus Cases in Sweden"
    data = "📅  Date = %s" % (date.today())
    hashtags = "#COVIDー19 #CoronaSverige #Coronavirus #CoronaSweden #CoronaVirusSweden"
    tweet = " %s \n\n %s \n %s \n %s" % (header , data , formatTwitterEnglish(myResponse), hashtags)
    postTweet(tweet.replace(',', ''))

    header = "Corona Virus Cases i Sverige"
    data = "📅 Datum = %s" % (date.today())
    tweet = " %s \n\n %s \n %s \n %s" % (header , data , formatTwitterSwedish(myResponse), hashtags)
    postTweet(tweet.replace(',', ''))
    print("Finished job")

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

makeScrap()
