from flask import Flask
import threading
import requests
from bs4 import BeautifulSoup as bp
import time




app = Flask(__name__)

url = "https://jeemain.nta.nic.in/"
keywords = ["final","score","card","result","results"]  

def telegram_msg(message):
    token = '7938656924:AAExo-EbeKqJ7DSG3cPtolnqzN8DwiXg8Ak'
    chat_id = '-1002689870013'
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

def answer_key_checker():
    try:
        web_data = requests.get(url)
        soup = bp(web_data.text, "html.parser")
        first_div = soup.find("div", class_="vc_tta-panel-body")
        li = first_div.find_all("li")
        latest_li = li[0]
        text = latest_li.text.lower()

        if keywords[0] in text:
            print("keyword 0 found")
            telegram_msg("Jee main final answer key is released")
            return True
        
        else:
            print("Keyword Not Found")

    except Exception as e:
        print("An error occurred:", e)

def run_checker_loop():
    while True:
        if answer_key_checker():
            break
        else:
            print("Refreshing every 40 seconds")
        time.sleep(40)



def result_checker():
    try:
        web_data = requests.get(url)
        soup = bp(web_data.text, "html.parser")
        first_div = soup.find("div", class_="vc_tta-panel-body")
        li = first_div.find_all("li")
        latest_li = li[0]
        text = latest_li.text.lower()

        if any(k in text for k in keywords[1:]):
            print("keyword 1 to end found")
            telegram_msg("Jee main Result is released")
            return True
        
        else:
            print("Keyword Not Found")

    except Exception as e:
        print("An error occurred:", e)

def run_checker_loop1():
    while True:
        if result_checker():
            break
        else:
            print("Refreshing every 40 seconds")
        time.sleep(40)

# Start the checker loop in the background
threading.Thread(target=run_checker_loop, daemon=True).start()
threading.Thread(target=run_checker_loop1, daemon=True).start()

@app.route('/')
def home():
    return "Bot is running and checking for both Answer Key and Result every 40 seconds."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
