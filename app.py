from flask import Flask, request, render_template, Response
import requests

app = Flask(__name__)

# ChatGPT URL'sini proxy üzerinden yönlendireceğiz
CHATGPT_URL = "https://chat.openai.com"

@app.route("/")
def home():
   return render_template("index.html")

@app.route("/proxy/<path:path>", methods=["GET", "POST"])
def proxy(path):
   url = f"{CHATGPT_URL}/{path}"

   headers = {key: value for key, value in request.headers.items() if key.lower() not in ["host", "referer", "origin"]}
   headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

   if request.method == "POST":
       response = requests.post(url, headers=headers, data=request.data, cookies=request.cookies)
   else:
       response = requests.get(url, headers=headers, cookies=request.cookies)

   return Response(response.content, response.status_code, response.headers.items())

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)

