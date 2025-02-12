
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# OpenAI Web Arayüzü URL'si
CHATGPT_URL = "https://chat.deepseek.com/"

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy(path):
   url = f"{CHATGPT_URL}/{path}"

   headers = {key: value for key, value in request.headers if key != "Host"}
   headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64;) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36"
   data = request.get_data() if request.method != "GET" else None

   response = requests.request(
       method=request.method,
       url=url,
       headers=headers,
       data=data,
       cookies=request.cookies if "cf_clearance" in request.cookies else None,
       allow_redirects=False
   )

   return response.content, response.status_code, response.headers.items()

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)

