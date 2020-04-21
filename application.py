from flask import Flask, request, render_template
import json, requests
from bs4 import BeautifulSoup


app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("index.html")

    # money_have = get_amount_scrape()
    # count(request.remote_addr)
    # return f'Hello!\n {money_have}'


def count(ip_address):
    data = {}
    with open('visitors.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        if ip_address not in data["ips"]:
            data["total"] += 1
            data["uniques"] += 1
            data["ips"].append(ip_address)
        else:
            data["total"] += 1
    with open('visitors.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_amount_scrape():
    response = requests.get("https://www.nadejeprooliho.cz/")
    soup = BeautifulSoup(response.text, "html.parser")
    czk = soup.find(class_="wnd-font-size-160").get_text().replace(" ", "")
    euro = float(czk) / curency()
    formated_euro = float("{:.2f}".format(euro))
    return formated_euro


def curency():
    response = requests.get('https://prime.exchangerate-api.com/v5/7ea45fe6d84d2b815a3e313e/latest/EUR')
    data = response.json()
    return float(data["conversion_rates"]["CZK"])


if __name__ == "__main__":
    app.run(port=5000, debug=True)