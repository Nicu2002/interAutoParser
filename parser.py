import requests
from bs4 import BeautifulSoup
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

filter_ = "Mercedes"
order_ = "by-price-asc"
URL = f'https://www.interauto.md/ro/cars/filter-marca-{filter_}/order-{order_}/page-10'
hostName = "localhost"
serverPort = 8080

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

cards = soup.find_all("div", class_="car_block")

result = []

for card in cards:
    link = card.find("div", class_="fader").find("a")["href"]
    img = card.find("div", class_="fader").find("a").find_all("img")[0]['src']
    title = card.find("h2", class_="car_block_title").text
    details = {
        "year": card.find_all("div", class_="car_other_detail")[0].find("strong").text,
        "cylinders": card.find_all("div", class_="car_other_detail")[1].find("strong").text,
        "fuel": card.find_all("div", class_="car_other_detail")[2].find("strong").text,
        "cutie": card.find_all("div", class_="car_other_detail")[3].find("strong").text,
    }
    price = card.find("div", class_="car_block_price")

    if card.find("div", class_="car_block_price_sale"):
        price = card.find("div", class_="car_block_price_sale").find("s").next_element.next_element
    elif card.find("div", class_="car_block_price_sold"):
        continue
    else:
        price = price.get_text()

    result.append({
        "link": link,
        "img": img,
        "title": title,
        "price": price,
        "details": details
    })


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(result), "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

