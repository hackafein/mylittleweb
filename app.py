from flask import Flask, request, render_template, Response
import requests
from flask import Flask, request, Response, redirect
app = Flask(__name__)

# ChatGPT URL'sini proxy üzerinden yönlendireceğiz
CHATGPT_URL = "https://chat.openai.com"

@app.route("/")
def home():
   return render_template("index.html")
@app.route("/proxy/<path:path>", methods=["GET", "POST"])
def proxy(path):
   url = f"{CHATGPT_URL}/{path}"

   # OpenAI'nin engellemesini aşmak için tarayıcıdan gelen header'ları proxy'ye geçiriyoruz
   headers = {
       "User-Agent": request.headers.get("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
       "Referer": "https://chat.openai.com",
       "Origin": "https://chat.openai.com",
       "Accept-Language": request.headers.get("Accept-Language", "en-US,en;q=0.9"),
       "Cache-Control": "no-cache",
       "Connection": "keep-alive"
   }

   # Cloudflare güvenlik doğrulaması için "cf_clearance" ve OpenAI'nin tokenlarını proxy'ye geçiriyoruz
   cookies = {key: value for key, value in request.cookies.items() if "cf_clearance" in key or "openai" in key}

   # HTTP metoduna göre isteği proxy üzerinden OpenAI'ye yönlendiriyoruz
   if request.method == "POST":
       response = requests.post(url, headers=headers, data=request.data, cookies=cookies)
   else:
       response = requests.get(url, headers=headers, cookies=cookies)

   # Eğer OpenAI bir yönlendirme (redirect) yaparsa, proxy de yönlendirme yapsın
   if response.status_code in [301, 302, 303, 307, 308]:
       return redirect(response.headers["Location"], code=response.status_code)

   return Response(response.content, response.status_code, response.headers.items())


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)

