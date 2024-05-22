import os
import smtplib
from data import quotes
from datetime import datetime
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
import re
import unicodedata

TWITTER_PASSWORD = "@2Gether"

def unicode_escape(text):
    # Replace non-BMP characters with their Unicode escape sequences
    return re.sub(r'[^\u0000-\uFFFF]', lambda x: '\\U{:08X}'.format(ord(x.group())), text)
# def normalize_unicode(text):
#     return unicodedata.normalize('NFKD', text)



TWITTER_EMAIL = "dany.guimefack@centrale-casablanca.ma"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True )
email_sender='danyanderson2222@gmail.com'
prog = 0
with open('progress.txt', 'r') as progress:
    a = progress.read().strip()
    score = int(a)
# print(score)
for i in range(score,score+1):
    author = quotes[i]['author']
    emoji= quotes[i]['emoji']
    emoji_tweet = '✨'
    body = "\"" + quotes[i]['body']+ "\""
    emoji_tweet = unicode_escape(emoji_tweet)

    # print(author,"\n",emoji,"\n",containt)

    with open('finished.txt', 'w',encoding='utf-8') as file:
        with open('template.txt', 'r') as temp:
            content=temp.read()
            quote_replace=content.replace('[QUOTE GOES HERE]', body).replace('[AUTHOR NAME]', author).replace('[AUTHOR EMOJIS]', emoji)
        file.write(quote_replace)


# Send mail
with open('finished.txt', 'r', encoding='utf-8') as finished:
    content = finished.read()
msg = MIMEText(content, 'plain', 'utf-8')
msg['Subject'] = "Motivational"


# content = unicode_escape(content)
# with smtplib.SMTP("smtp.gmail.com") as connection:
#     connection.starttls()
#     connection.login(user=email_sender, password=os.environ.get('GMAIL_APP_PASSWORD'))
#     connection.sendmail(from_addr=email_sender,
#                         to_addrs='dany.guimefack@centrale-casablanca.ma',
#                         msg=msg.as_string(),
#
#                        )


# make a tweet
driver = webdriver.Chrome(executable_path=r'D:\Python Extra\webdrivers\chrome\version 125.0.6422\chromedriver.exe',options=chrome_options)
driver.get("https://twitter.com/i/flow/login")
time.sleep(5)
email=driver.find_element(By.NAME,value="text")
time.sleep(2)
email.send_keys(TWITTER_EMAIL)
time.sleep(1)
email.send_keys(Keys.ENTER)
time.sleep(2)
try:
    user_name=driver.find_element(By.NAME,value="text")
except NoSuchElementException:
    print("Unhandled Exception")
else:
    user_name.send_keys("@IAmDanyAnderson")
    user_name.send_keys(Keys.ENTER)
    time.sleep(3)
password = driver.find_element(By.NAME,value="password")
password.send_keys(TWITTER_PASSWORD)
password.send_keys(Keys.ENTER)
time.sleep(1)
print(content)
time.sleep(5)
# post_button = driver.find_element(By.XPATH,value='//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a')
# time.sleep(2)
# post_button.click()
time.sleep(10)
my_post = driver.find_element(By.XPATH,value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div')
time.sleep(3)
my_post.send_keys(f"{body}\n\n {author} {emoji_tweet}")
# script = f"arguments[0].value = '{content}';"
# driver.execute_script(script, my_post)
time.sleep(3)
post_button = driver.find_element(By.XPATH,value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button/div/span/span')
print('clicked')
# post_button.click()
# time.sleep(5)
# driver.quit()


# make sure the quote is different everyday
prog = score+1
with open('progress.txt', 'w') as progress:
    prog = str(prog)
    progress.write(prog)
#
#
