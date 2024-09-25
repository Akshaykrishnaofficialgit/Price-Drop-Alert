from bs4 import BeautifulSoup
import requests,re
import smtplib
import os
import lxml
from dotenv import load_dotenv
load_dotenv()

url = "https://www.amazon.in/Daikin-Fixed-Copper-Filter-FTL28U/dp/B09R4SF5SP/ref=sr_1_4?_encoding=UTF8&rps=1&s=kitchen&sr=1-4"
headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/112.0.0.0 Safari/537.36"
    ),
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}


response = requests.get(url=url, headers=headers)
data = response.text

soup = BeautifulSoup(data, "lxml")
# Check the actual class name for price in the HTML structure
price_data = soup.find("span", class_="a-price-whole")  # update the class based on inspection
price = price_data.getText().strip().split('.')[0]
float_price=price
target_price="30,000"
product_title = soup.find(id="productTitle").get_text()
cleaned_product_title = re.sub(r'\s+', ' ', product_title).strip()

if float_price<target_price:
    message=f"🎉🎉🎉Hey here's is today's offer!!🎈\n\n{cleaned_product_title} is on sale for Rs.{float_price}"
    with smtplib.SMTP(os.environ["SMTP_ADDRESS"],port=587) as connection:
        connection.starttls()
        result=connection.login(os.environ["EMAIL_ADD"],os.environ["PWD"])
        connection.sendmail(
            from_addr=os.environ["EMAIL_ADD"],
            to_addrs=os.environ["EMAIL_ADD2"],
            msg=f"subject:Amazon Price Alert\n\n{message}\nbuy now:\n{url}".encode("utf-8")
        )

