import re
import random
import configparser
from flask import Flask, request, abort
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import os
import  json
import csv
import requests
import getpass



from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)


line_bot_api = LineBotApi("nCa+Xtf8NEZEzmo/PVbgg4nYDcn9poYLZaVKqUpvpex/bkvre9n0k1GEeTEbXQ+EuVCNFhTFiv3XeQqGo7XxXaQxSp2Ki3mDG1HzXxe0QAr79tLvxFSuRBc2w87L2dL3WRfWnV88GeUHvh5AXsv29gdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("7402a448e8ef19c862d23e2d813a9846")




@app.route('/')
def index():
	return 'Welcome to tsbot!'


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'




@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)

    if event.message.text[0] == "@":
        questions = event.message.text[1:]
        url = 'https://www.evi.com/q/' + questions
        response = requests.get(url)
        bsObj = BeautifulSoup(response.text,'html.parser')
        try:
            str = (bsObj.find("div", {"class":"tk_common"})).get_text()
            content = str[98:len(str)-39]
        except:
            content = "Sorry, I don't yet have an answer to that question."
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))



    if event.message.text[0] == ">":
        account_input = event.message.text[1:9]
        print (account_input)
        password_input = event.message.text[9:]
        print (password_input)
        driver = webdriver.PhantomJS()
        driver.get("https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx")


        elem = driver.find_element_by_name("Txt_UserID")
        elem.clear()
        elem.send_keys(account_input)


        password = driver.find_element_by_name("Txt_Password")
        password.clear()
        password.send_keys(password_input)


        btn = driver.find_element_by_name("ibnSubmit")
        btn.click()

        wait = WebDriverWait(driver, 2)
        wait.until(lambda driver: driver.current_url != "https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx")


        aTagsInLi = driver.find_elements_by_css_selector('div')

        content = ""
        
        try:
            for a in aTagsInLi:
                if "待辦提醒" in a.text:
                    content += a.text
        
        except:
            content = "Can't login,please check your imformation"


        print(content)

        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
        return 0


    if event.message.text == "查作業~":
        content = "請輸入你的帳號和密碼(以>開頭ex:>s1041501a12345678)帳號密碼需連在一起~\n輸入後需要等待一分鐘登入時間..."
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        isQuestion = 1
        return 0

    if event.message.text.find('Y<<') != -1:
        data = []
        data.append(["", "", "", "", ""])
        data.append(["", "", "", "", ""])
        youtube_search(event.message.text, data)
        
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(
                text=data[0][0],
                actions=[ URITemplateAction(label = 'Watch it !!', uri = data[1][0]) ]
            ),
            CarouselColumn(
                text=data[0][1],
                actions=[ URITemplateAction(label = 'Watch it !!', uri = data[1][1]) ]
            ),
            CarouselColumn(
                text=data[0][2],
                actions=[ URITemplateAction(label = 'Watch it !!', uri = data[1][2]) ]
            ),
            CarouselColumn(
                text=data[0][3],
                actions=[ URITemplateAction(label = 'Watch it !!', uri = data[1][3]) ]
            ),
            CarouselColumn(
                text=data[0][4],
                actions=[ URITemplateAction(label = 'Watch it !!', uri = data[1][4]) ]
            ),            
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        return 0

 # input search query ----> return string

    


    if event.message.text == "查作業~":
        content = ptt_beauty()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0


    if event.message.text == "你問我答":
        content = "請輸入你的問題(In English，以@開頭)\n我只會英文，哈哈"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        isQuestion = 1
        return 0

    if event.message.text == "我們是誰":
        content = "我們是邱佳震、李泳誼、張皓儒"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "我想在youtube查音樂~~~!!!":
        content = "請輸入想搜尋的歌名並以Y<<作為開頭 ex: Y<<周杰倫"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    
    
    


    buttons_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ButtonsTemplate(
            title='選擇服務',
            text='請選擇',
            thumbnail_image_url='https://1.bp.blogspot.com/-0E4u9O1GPvY/WDuheSWu7xI/AAAAAAALjNc/oD5FVffdIRQGcIj5e0I8mHsnJDdVu3xCACLcB/s1600/AS001452_14.gif',
            actions=[
                MessageTemplateAction(
                    label='查作業~',
                    text='查作業~'
                ),
                MessageTemplateAction(
                    label='我們是誰',
                    text='我們是誰'
                ),
                MessageTemplateAction(
                    label='你問我答',
                    text='你問我答'
                ),
                MessageTemplateAction(
                    label='我想在youtube查音樂~~~!!!',
                    text='我想在youtube查音樂~~~!!!'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, buttons_template)


def youtube_search(text, redata): 
    search_query = text
    url = "https://www.youtube.com/results?search_query=" + search_query
    req = requests.get(url)
    content = req.content
    soup = BeautifulSoup(content, "html.parser")    

    out_times = 0

    for all_mv in soup.select(".yt-lockup-video"):      
        # 抓取 Title & Link
        data = all_mv.select("a[rel='spf-prefetch']")
        if len(data[0].get("href")) < 150:
            redata[0][out_times] = ("{}".format(data[0].get("title"))) # 影片名
            redata[1][out_times] = ("https://www.youtube.com{}".format(data[0].get("href"))) # 網址
            out_times += 1
            if out_times == 5:
                break
    return redata


if __name__ == '__main__':
    app.run()
