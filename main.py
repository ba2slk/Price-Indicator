import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
from email.mime.text import MIMEText

AMAZON_PRODUCT_URL = "https://www.amazon.com/Linksys-Dual-Band-Coverage-High-Speed-Streaming/dp/B08RXBDG8M/?_encoding=UTF8&pd_rd_w=zYBRh&content-id=amzn1.sym.1d393eda-2182-4936-ba64-8ccccc70d004&pf_rd_p=1d393eda-2182-4936-ba64-8ccccc70d004&pf_rd_r=MJHKDYQ99K5TDADB79G2&pd_rd_wg=xZEYu&pd_rd_r=2197fff9-d782-4ac2-9492-7e65e5b3d860&ref_=pd_gw_exports_top_sellers_unrec&th=1"
HOST = "smtp.naver.com"
SENDER = "SECRET@naver.com"
RECEIVER = SENDER
USER_ID = "USER_ID"
PASSWORD = "SECRET"
text = ""

WISHING_PRICE = 200

headers = {
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
}
response = requests.get(url=AMAZON_PRODUCT_URL, headers=headers)
print(response)
product_page = response.text

soup = BeautifulSoup(product_page, "lxml")
price_section = soup.find_all(name="span", attrs={"aria-hidden": "true"})[3]
price_without_currency = float(price_section.getText()[1:])
product_name = soup.select_one("#productTitle").getText().strip()
print(product_name)
print(price_without_currency)

if price_without_currency <= WISHING_PRICE:
    text = f"Product: {product_name}\n" \
           f"Price: ${price_without_currency}\n\n" \
           f"It's now under ${WISHING_PRICE}, your wishing price!\n" \
           f"Your product is waiting for you. Grab the Chance.\n\n" \
           f"URL: {AMAZON_PRODUCT_URL}" \

msg = MIMEText(text)
msg["Subject"] = f"Amazon Price Indicator: ${price_without_currency}!"
msg["From"] = SENDER
msg["To"] = RECEIVER

connection = smtplib.SMTP(HOST, 587)
connection.starttls()
connection.login(user=USER_ID, password=PASSWORD)
connection.sendmail(from_addr=SENDER, to_addrs=RECEIVER, msg=msg.as_string())

