import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pytz

# for chat gpt api
import openai
import os
import pandas as pd
import time

# for mailing
import smtplib
from email.message import EmailMessage

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64


import myPassword
openai.api_key = ''

smtp_gmail = smtplib.SMTP('smtp.gmail.com',587)

# 서버 연결 설정
smtp_gmail.ehlo()

# 연결을 암호화
smtp_gmail.starttls()

# 로그인
smtp_gmail.login('kakaokokoa9971@gmail.com',myPassword.mypassword())


def get_completion(prompt, model="gpt-4"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

korea_tz = pytz.timezone('Asia/Seoul')
now_in_korea = datetime.now(korea_tz)

# 웹 페이지 URL
url = 'https://www.bloomberg.co.kr/blog/category/news/'

# requests를 사용하여 웹 페이지의 HTML 가져오기
response = requests.get(url)

# BeautifulSoup 객체 생성
soup = BeautifulSoup(response.text, 'html.parser')

# data-element-position이 1인 모든 <a> 태그 찾기
target_links = soup.find_all('a', {'data-description': 'title'})

rescently_news = target_links[0].get('href')
print(rescently_news)

rescently_url = rescently_news
rescently_response = requests.get(rescently_url)
soup = BeautifulSoup(rescently_response.text,'html.parser')
date = soup.find_all(string=re.compile(r'\d{4}\.\d{2}\.\d{2}'))[0].strip()
print(date)
today = now_in_korea.strftime('%Y.%m.%d')

if date == today:
    div = soup.find('div',class_='wpb_wrapper')
    div_html = str(div)
    cleaned_news = re.sub('<.*?>',"",div_html).replace('\t', '').replace('\n', '')

    prompt = cleaned_news+"는 오늘 자 Bloomberg 뉴스야, 요약 정리해줄 수 있어?"
    response = get_completion(prompt)
    print(response)

    msg = MIMEMultipart()
    msg['From'] = 'kakaokokoa9971@gmail.com'
    msg['To'] = 'jaeseokk@ajou.ac.kr,june1012june@gmail.com'
    msg['Subject'] = "Today's Bloomberg News Summary."
    msg_body = MIMEText(response)
    msg.attach(msg_body)
    smtp_gmail.send_message(msg)
    smtp_gmail.quit()
