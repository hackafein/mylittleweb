from flask import Flask, request, render_template, Response
import asyncio
from playwright.async_api import async_playwright

app = Flask(__name__)

async def get_chatgpt_page():
   async with async_playwright() as p:
       browser = await p.chromium.launch(headless=True)
       page = await browser.new_page()
       await page.goto("https://chat.openai.com")

       # OpenAI'nin sayfasını al
       content = await page.content()
       await browser.close()
       return content

@app.route("/")
def home():
   return render_template("index.html")

@app.route("/proxy")
async def proxy():
   content = await get_chatgpt_page()
   return Response(content, mimetype="text/html")

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)


