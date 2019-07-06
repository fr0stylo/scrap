import requests
from bs4 import BeautifulSoup
import smtplib
import os

EMAIL_ACCOUNT = os.environ.get("email_account")
EMAIL_PASSWORD = os.environ.get("email_password")
EMAIL_TO = os.environ.get("email_to")
SCRAPE_URL = os.environ.get("url")

print("Starting scraper...")

def send_mail(price):
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.ehlo()

    smtp.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)

    subject = 'Norima kaina'
    body = 'Dabartine kaina' + str(price)

    msg = f"Subject: {subject}\n\n{body}"

    smtp.sendmail(EMAIL_ACCOUNT, EMAIL_TO, msg)

    print("Sent")

    smtp.quit()


headers = {
    'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0"
}

response = requests.get(SCRAPE_URL, headers)

print("Getting resource")

page_content = BeautifulSoup(response.content, 'html.parser')

price_children = page_content.findChild('span', class_="price")

price_string = price_children.find_next('span').string

price = float(str.replace(price_string, ',', '.'))

print(f"Parsed price {str(price)}")

if price < 11.00:
    send_mail(price)
