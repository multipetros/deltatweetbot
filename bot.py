#! /usr/bin/env python
# -*- coding: utf-8 -*-

# DeltaTweetBot - deltaHacker Magazine - v.1.0
# Copyright (c) 2016, Petros Kyladitis
#
# A demonstration twitter bot, which post, using tweepy library, a time based greeting, an image 
# from a web camera, and the CPU temperature of the RPi from where running at scheduled times.
#
# This is free software, distributed under the GNU GPL 3

from datetime import datetime
import tweepy
import os
#download image without auth
import urllib
#download image with auth
import urllib2
import base64

consumer_key = ""  #Your key
consumer_secret = "" #Your secret
access_token = ""  #Your token
access_token_secret = "" #Your token secret
cam_url = "" #Webcam's snapshot url
cam_usr = "" #Webcam's user name
cam_pwd = "" #Webcam's user password

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

cpu_temp = os.popen('vcgencmd measure_temp').readline()
cpu_temp = cpu_temp.replace('temp=','').replace('\n','')
img_path = "/home/pi/live-cam.jpg" #Image storage path

now_hour = datetime.now().hour
greetings = {7 : "Good morning", 12 : "Good afternoon", 21 : "Good evening", 23 : "Good night"}
if now_hour in greetings.keys():
    tweet_text = greetings[now_hour]
    tweet_text = tweet_text + " with a picture from beautiful Chios. My RPi's CPU temp right now is about " + cpu_temp
    download_img() #if no need auth
    #download_img_auth() #if need auth
    api.update_with_media(img_path, tweet_text)

def download_img():
    urllib.urlretrieve(cam_url, img_path)

def download_img_auth():
    request = urllib2.Request(cam_url)
    base64string = base64.encodestring('%s:%s' % (cam_usr, cam_pwd)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    result = urllib2.urlopen(request)
    if result.headers.maintype == "image":
        open(img_path, "wb").write(result.read())
    
