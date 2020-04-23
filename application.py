from flask import Flask, request, render_template
import json, requests
from bs4 import BeautifulSoup


app = Flask(__name__)


@app.route('/')
def index():
    try:
        if request.headers.getlist("X-Forwarded-For"):
           ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr
        count(ip)      
    except Exception:
        count("0.0")
    try:
        amount = get_amount_scrape()
    except Exception as e:
        print(e)
        amount = "1 607 270"
    return render_template("index.html", amount=amount)


@app.route('/help')
def help():
    try:
        amount = get_amount_scrape()
    except Exception as e:
        print(e)
        amount = "1 607 270"
    return render_template("help.html", amount=amount)


@app.route('/story')
def story():
    try:
        amount = get_amount_scrape()
    except Exception as e:
        print(e)
        amount = "1 607 270"
    return render_template("story.html", amount=amount)


@app.route('/developer/y8Nasd651zgd5s6g4sm0fKocdadx')
def development():
    with open('visitors.json', 'r', encoding='utf-8') as file:
        return json.load(file)


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
    spans = soup.find_all("span")
    czk = spans[22].get_text().replace("VYBRÁNO:", "").replace("Kč", "").replace("\xa0", "").replace(" ", "")
    euro = float(czk) / curency()
    formated_euro = str(float("{:.2f}".format(euro)))
    amount = formated_euro.split(".")[0]
    result = f"{amount[0]} {amount[1]}{amount[2]}{amount[3]} {amount[4]}{amount[5]}{amount[6]}"
    return result

def curency():
    response = requests.get('https://prime.exchangerate-api.com/v5/7ea45fe6d84d2b815a3e313e/latest/EUR')
    data = response.json()
    return float(data["conversion_rates"]["CZK"])


if __name__ == "__main__":
    pass
    # app.run(port=5000, debug=True)