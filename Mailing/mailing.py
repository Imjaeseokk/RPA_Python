import smtplib
from email.message import EmailMessage

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64

# import myPassword
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


# Simple Mail Transfer Protocol
# 사용하는 email 계정의 smtp 서버 도메인 이름 입력
# smtp_gmail = smtplib.SMTP('smtp.gmail.com',587)
smtp_gmail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

# 서버 연결 설정
# smtp_gmail.ehlo()

# 연결을 암호화
# smtp_gmail.starttls()

# 로그인
app_password = os.environ.get('MYAPPPW')
print("pw is",app_password)
smtp_gmail.login('kakaokokoa9971@gmail.com',app_password)

## fear and greed 가져오기
url = "https://edition.cnn.com/markets/fear-and-greed"
driver.get(url)

# 페이지가 완전히 로드될 때까지 잠시 대기
# time.sleep(15)  # 필요에 따라 대기 시간 조절 가능
# Fear & Greed Index 다이얼 이미지 요소 찾기
# wait = WebDriverWait(driver, 10)
# dial_element = driver.find_element(By.CLASS_NAME, 'market-fng-gauge__meter')
# dial_element = driver.find_element(By.XPATH, '/html/body/div[1]/section[4]/section[1]/section[1]/div/section/div[1]/div[2]')


# # gpt가 이렇게 해보라고 함 1
wait = WebDriverWait(driver, 10)
while driver.execute_script("return document.readyState;") != "complete":
    time.sleep(1)
print("loading complete")

# 값이 40인 모든 요소를 찾고 클래스 이름 출력
all_elements = driver.find_elements(By.XPATH, '//*')
if all_elements:
    print(all_elements)
# 각 요소의 class name과 HTML value를 출력
for element in all_elements:
    print(element)
    class_name = element.get_attribute('class')
    html_value = element.get_attribute('innerHTML').strip()
    if html_value == "40":
        print(f"Class: {class_name}, Value: {html_value}")
### end

value_element = driver.find_element(By.CLASS_NAME, 'market-fng-gauge__dial-number-value')
fear_and_greed_index = value_element.text

print(fear_and_greed_index)

# 다이얼 이미지 스크린샷 캡처
# screenshot_path = "FeadAndGreed.png"
# dial_element.screenshot(screenshot_path)
# print("다이얼 이미지를 성공적으로 캡처하여", screenshot_path, "에 저장했습니다.")

# msg = EmailMessage()
# image 추가용 code
msg = MIMEMultipart()
msg['From'] = 'kakaokokoa9971@gmail.com'
msg['To'] = 'jaeseokk@ajou.ac.kr'
# msg['To'] = 'june1012june@gmail.com,kakaokokoa9971@gmail.com,dw12.jeong@g.skku.edu'


msg['Subject'] = "Today's FGI is "+str(fear_and_greed_index)+"."

# text = MIMEText("Please refer to the attached image.:)")
# msg.attach(text)
#
# with open("FeadAndGreed.png", "rb") as attachment:
#     image_part = MIMEImage(attachment.read(), name="FeadAndGreed.png")
#     msg.attach(image_part)
#
# smtp_gmail.send_message(msg)
#
# smtp_gmail.quit()

# HTML 형식의 본문 생성
html_body = f"""
<html>
  <body>
    <p>Today's Fear and Greed Index: {fear_and_greed_index}</p>
    <img src="cid:image1" width="331" height="184">
  </body>
</html>
"""

# MIMEText 객체 생성 후 HTML 본문 추가
html_part = MIMEText(html_body, 'html')
msg.attach(html_part)

# 이미지를 base64로 인코딩하여 본문에 첨부
# with open(screenshot_path, 'rb') as img_file:
#     img_data = img_file.read()
#     img_base64 = base64.b64encode(img_data).decode('utf-8')

# msg_image = MIMEImage(img_data)
# msg_image.add_header('Content-ID', '<image1>')
# msg.attach(msg_image)

# 이메일 보내기
smtp_gmail.send_message(msg)

# 종료
smtp_gmail.quit()
