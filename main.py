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

# NO NEED TO GO BENEATH THESE BOUNDARIES IF YOU'RE A NON DEV :)
##################################################################################################################

TWITTER_USERNAME = "" # your twitter username here
TWITTER_PASSWORD = "" # your twitter password here
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD') # your gmail password app here
TWITTER_EMAIL = "" # enter your twitter email address
CHROMEDRIVER_PATH = '' # path to your chrome driver. Your browser must be google chrome
EMAIL_SENDER='' # your email adress
prog = 0 # saves value of last sent email to prevent an email to be sent twice

####################################################################################################################


# Function to replace non-BMP characters with their Unicode escape sequences
def unicode_escape(text):
    return re.sub(r'[^\u0000-\uFFFF]', lambda x: '\\U{:08X}'.format(ord(x.group())), text)


# Setting driver options for chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True )


# Investigating latest progress through the list of quotes
with open('progress.txt', 'r') as progress:
    a = progress.read().strip()
    score = int(a)
# print(score)

# Getting hold of the quotes, author and emojis
for i in range(score,score+1):
    author = quotes[i]['author']
    emoji= quotes[i]['emoji']
    emoji_tweet = '✨'
    body = "\"" + quotes[i]['body']+ "\""
    emoji_tweet = unicode_escape(emoji_tweet)

    with open('finished.txt', 'w',encoding='utf-8') as file:
        with open('template.txt', 'r') as temp:
            content=temp.read()
            quote_replace=content.replace('[QUOTE GOES HERE]', body).replace('[AUTHOR NAME]', author).replace('[AUTHOR EMOJIS]', emoji)
        file.write(quote_replace)


# getting hold of final content to be sent via mail
with open('finished.txt', 'r', encoding='utf-8') as finished:
    content = finished.read()


# make sure the quote is different everyday by incrementing prog and saving in progress file
prog = score+1
with open('progress.txt', 'w') as progress:
    prog = str(prog)
    progress.write(prog)

# send an email to yourself
msg = MIMEText(content, 'plain', 'utf-8')
msg['Subject'] = "Motivational Quote"
with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=EMAIL_SENDER, password=GMAIL_APP_PASSWORD)
    connection.sendmail(from_addr=EMAIL_SENDER,
                        to_addrs=EMAIL_SENDER,
                        msg=msg.as_string(),
                        )


# make a tweet
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,options=chrome_options)
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
    user_name.send_keys(TWITTER_USERNAME)
    user_name.send_keys(Keys.ENTER)
    time.sleep(3)
password = driver.find_element(By.NAME,value="password")
password.send_keys(TWITTER_PASSWORD)
password.send_keys(Keys.ENTER)
time.sleep(1)
print(content)
time.sleep(10)
my_post = driver.find_element(By.XPATH,value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div')
time.sleep(3)
my_post.send_keys(f"{body}\n\n {author} {emoji_tweet}")
time.sleep(3)
post_button = driver.find_element(By.XPATH,value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button/div/span/span')
print('clicked')
post_button.click()
time.sleep(7)
driver.quit()

