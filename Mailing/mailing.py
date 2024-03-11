import smtplib
from email.message import EmailMessage

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import myPassword
import time


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


# Simple Mail Transfer Protocol
# 사용하는 email 계정의 smtp 서버 도메인 이름 입력
smtp_gmail = smtplib.SMTP('smtp.gmail.com',587)

# 서버 연결 설정
smtp_gmail.ehlo()

# 연결을 암호화
smtp_gmail.starttls()

# 로그인
smtp_gmail.login('kakaokokoa9971@gmail.com',myPassword.getPW())

## fear and greed 가져오기
url = "https://edition.cnn.com/markets/fear-and-greed"
driver.get(url)

# 페이지가 완전히 로드될 때까지 잠시 대기
time.sleep(5)  # 필요에 따라 대기 시간 조절 가능
# Fear & Greed Index 다이얼 이미지 요소 찾기
# wait = WebDriverWait(driver, 10)
# dial_element = driver.find_element(By.CLASS_NAME, 'market-fng-gauge__meter')
dial_element = driver.find_element(By.XPATH, '/html/body/div[1]/section[4]/section[1]/section[1]/div/section/div[1]/div[2]')
value_element = driver.find_element(By.XPATH, '/html/body/div[1]/section[4]/section[1]/section[1]/div/section/div[1]/div[2]/div[1]/div/div[1]/div[1]/div/div[4]/span')

fear_and_greed_index = value_element.text

print(fear_and_greed_index)

# 다이얼 이미지 스크린샷 캡처
screenshot_path = "FeadAndGreed.png"
dial_element.screenshot(screenshot_path)
print("다이얼 이미지를 성공적으로 캡처하여", screenshot_path, "에 저장했습니다.")

# msg = EmailMessage()
# image 추가용 code
msg = MIMEMultipart()

msg['Subject'] = "Today's FGI is "+str(fear_and_greed_index)+"."

# msg.set_content("Nice 2 meet U :)")
# image 추가용 code
text = MIMEText("Please refer to the attached image.:)")
msg.attach(text)

msg['From'] = 'kakaokokoa9971@gmail.com'
# msg['To'] = 'jaeseokk@ajou.ac.kr'
msg['To'] = 'june1012june@gmail.com'

with open("FeadAndGreed.png", "rb") as attachment:
    image_part = MIMEImage(attachment.read(), name="FeadAndGreed.png")
    msg.attach(image_part)

smtp_gmail.send_message(msg)

smtp_gmail.quit()