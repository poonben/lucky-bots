#-*-coding: utf-8 -*-
##from __future__ import absolute_import
###
from flask import Flask, jsonify, render_template, request
import json
import numpy as np
import pandas as pd
import xlsxwriter
import requests
import geopy.distance as ps
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ImageSendMessage, StickerSendMessage, AudioSendMessage, FlexSendMessage
)
from linebot.models.template import *
from linebot import (
    LineBotApi, WebhookHandler
)

app = Flask(__name__)

lineaccesstoken = '8HCqjQydLDgxFpTpctxyTI866HGSBWuoqUILyLgF0hfwbdZFmNSMYCdGIV151M4tQ7SABUzH/J6G7ReeCFlgM0xQG388iOrY4e5WKZ6m2rO01BCgKFzrmXM7z06MzyaGNQGE89+XHtzUq6yjijP3sAdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(lineaccesstoken)

casedata = pd.read_excel('bot.xlsx')

####################### new ########################
@app.route('/')
def index():
    return "ben bot line auto"


@app.route('/webhook', methods=['POST'])
def callback():
    json_line = request.get_json(force=False,cache=False)
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    no_event = len(decoded['events'])
    for i in range(no_event):
        event = decoded['events'][i]
        event_handle(event)
    return '',200


def event_handle(event):
    print(event)
    try:
        userId = event['source']['userId']
    except:
        print('error cannot get userId')
        return ''

    try:
        rtoken = event['replyToken']
    except:
        print('error cannot get rtoken')
        return ''
    if 'message' in event.keys():
        try:
            msgType = event["message"]["type"]
            msgId = event["message"]["id"]
        except:
            print('error cannot get msgID, and msgType')
            sk_id = np.random.randint(1,17)
            replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
            line_bot_api.reply_message(rtoken, replyObj)
            return ''
    if 'postback' in event.keys():
        msgType = 'postback'

    if msgType == "text":
        msg = str(event["message"]["text"])
        replyObj = handle_text(msg)
        line_bot_api.reply_message(rtoken, replyObj)

    if msgType == "postback":
        msg = str(event["postback"]["data"])
        replyObj = handle_postback(msg)
        line_bot_api.reply_message(rtoken, replyObj)

    if msgType == "location":
        lat = event["message"]["latitude"]
        lng = event["message"]["longitude"]
        #txtresult = handle_location(lat,lng,casedata,3)
        result = getcaseflex(lat,lng)
        replyObj = FlexSendMessage(alt_text='Flex Message alt text', contents=result)
        line_bot_api.reply_message(rtoken, replyObj)
    else:
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
    return ''
       
dat = pd.read_excel('bot.xlsx')
def getdata(query):
    res = dat[dat['QueryWord']==query]
    if len(res)==0:
        return ''
    else:
        ImgUrl1 = res['ImgUrl1'].values[0]
        Link1 = res['Link1'].values[0]
        Linkbt1 = res['Linkbt1'].values[0]
        Lineid1 = res['Lineid1'].values[0]
        ImgUrl2 = res['ImgUrl2'].values[0]
        Link2 = res['Link2'].values[0]
        Linkbt2 = res['Linkbt2'].values[0]
        Lineid2 = res['Lineid2'].values[0]        
        ImgUrl3 = res['ImgUrl3'].values[0]
        Link3 = res['Link3'].values[0]
        Linkbt3 = res['Linkbt3'].values[0]
        Lineid3 = res['Lineid3'].values[0]
        return ImgUrl1,Link1,Linkbt1,Lineid1,ImgUrl2,Link2,Linkbt2,Lineid2,ImgUrl3,Link3,Linkbt3,Lineid3

def flexmessage(query):
    res = getdata(query)
    if res == 'nodata':
        return ''
    else:
        ImgUrl1,Link1,Linkbt1,Lineid1,ImgUrl2,Link2,Linkbt2,Lineid2,ImgUrl3,Link3,Linkbt3,Lineid3 = res 
    flex = '''
    {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "mega",
      "hero": {
        "type": "image",
        "url": "%s",
        "size": "full",
        "aspectRatio": "10:12.2",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "%s"
        },
        "align": "center"
      },
      "footer": {
        "type": "box",
        "layout": "horizontal",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
              "type": "uri",
              "label": "สมัครสมาชิก",
              "uri": "%s"
            },
            "color": "#00000022",
            "adjustMode": "shrink-to-fit"
          },
          {
            "type": "button",
            "style": "primary",
            "action": {
              "type": "uri",
              "label": "ติดต่อโฆษา",
              "uri": "%s"
            },
            "color": "#ffffff22",
            "height": "sm"
          }
        ],
        "flex": 0,
        "background": {
          "type": "linearGradient",
          "angle": "70deg",
          "startColor": "#ffdd0030",
          "endColor": "#ffdd0020",
          "centerColor": "#ff0000"
        },
        "backgroundColor": "#000000"
      }
    },
    {
      "type": "bubble",
      "size": "mega",
      "hero": {
        "type": "image",
        "url": "%s",
        "size": "full",
        "aspectRatio": "10:12.2",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "%s"
        },
        "align": "center"
      },
      "footer": {
        "type": "box",
        "layout": "horizontal",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
              "type": "uri",
              "label": "สมัครสมาชิก",
              "uri": "%s"
            },
            "color": "#00000022",
            "adjustMode": "shrink-to-fit"
          },
          {
            "type": "button",
            "style": "primary",
            "action": {
              "type": "uri",
              "label": "ติดต่อโฆษา",
              "uri": "%s"
            },
            "color": "#ffffff22",
            "height": "sm"
          }
        ],
        "flex": 0,
        "background": {
          "type": "linearGradient",
          "angle": "70deg",
          "startColor": "#ffdd0030",
          "endColor": "#ffdd0020",
          "centerColor": "#000000"
        },
        "backgroundColor": "#000000"
      }
    },
    {
      "type": "bubble",
      "size": "mega",
      "hero": {
        "type": "image",
        "url": "%s",
        "size": "full",
        "aspectRatio": "10:12.2",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "%s"
        },
        "align": "center"
      },
      "footer": {
        "type": "box",
        "layout": "horizontal",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
              "type": "uri",
              "label": "สมัครสมาชิก",
              "uri": "%s"
            },
            "color": "#00000022",
            "adjustMode": "shrink-to-fit"
          },
          {
            "type": "button",
            "style": "primary",
            "action": {
              "type": "uri",
              "label": "ติดต่อโฆษา",
              "uri": "%s"
            },
            "color": "#ffffff22",
            "height": "sm"
          }
        ],
        "flex": 0,
        "background": {
          "type": "linearGradient",
          "angle": "70deg",
          "startColor": "#ffdd0030",
          "endColor": "#ffdd0020",
          "centerColor": "#ffff00"
        },
        "backgroundColor": "#000000"
      }
    }
  ]
}
    '''%(ImgUrl1,Link1,Linkbt1,Lineid1,ImgUrl2,Link2,Linkbt2,Lineid2,ImgUrl3,Link3,Linkbt3,Lineid3)
    return flex

from linebot.models import (TextSendMessage,FlexSendMessage)
import json

def handle_text(inpmessage):
    flex = flexmessage(inpmessage)
    if flex == 'nodata':
        replyObj = TextSendMessage(text=inpmessage)
    else:
        flex = json.loads(flex)
        replyObj = FlexSendMessage(alt_text='Flex Message alt text', contents=flex)
    return replyObj

def handle_postback(inpmessage):
    replyObj = TextSendMessage(text=inpmessage)
    return replyObj


def handle_location(lat,lng,cdat,topK):
    result = getdistace(lat, lng,cdat)
    result = result.sort_values(by='km')
    result = result.iloc[0:topK]
    txtResult = ''
    for i in range(len(result)):
        kmdistance = '%.1f'%(result.iloc[i]['km'])
        newssource = str(result.iloc[i]['News_Soruce'])
        txtResult = txtResult + 'ห่าง %s กิโลเมตร\n%s\n\n'%(kmdistance,newssource)
    return txtResult[0:-2]


def getcaseflex(lat,lng):
    url = 'http://botnoiflexapi.herokuapp.com/getnearcase?lat=%s&long=%s'%(lat,lng)
    res = requests.get(url).json()
    return res

def getdistace(latitude, longitude,cdat):
  coords_1 = (float(latitude), float(longitude))
  ## create list of all reference locations from a pandas DataFrame
  latlngList = cdat[['Latitude','Longitude']].values
  ## loop and calculate distance in KM using geopy.distance library and append to distance list
  kmsumList = []
  for latlng in latlngList:
    coords_2 = (float(latlng[0]),float(latlng[1]))
    kmsumList.append(ps.vincenty(coords_1, coords_2).km)
  cdat['km'] = kmsumList
  return cdat

if __name__ == '__main__':
    app.run(debug=True)
