from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request

# لێرە تۆکەنەکەت ڕاستەوخۆ دابنێ یان لە Environment Variable بیخوێنەوە
TOKEN = os.environ.get("BOT_TOKEN", "8103815264:AAGFXJOpFoG8qIJLK7Ibdqe99s1tcElTe_c")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": text}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print("Error sending message:", e)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # خوێندنەوەی ئەو نامەیەی تیلیگرام بۆمانی دەنێرێت
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            update = json.loads(post_data.decode('utf-8'))
            
            # ئەگەر نامە بوو
            if "message" in update and "text" in update["message"]:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"]["text"]
                
                # وەڵامەکان لێرە ڕێکبخە
                if text == "/start":
                    send_message(chat_id, "سڵاو شێرەکەم! 🦁 من ئێستا لەسەر Vercel بە سیستەمی Webhook کاردەکەم و هەرگیز نانووم!")
                else:
                    send_message(chat_id, f"تۆ وتت: {text}")
                    
        except Exception as e:
            pass

        # پێدانی وەڵامی 200 بە تیلیگرام بۆ ئەوەی بزانێت نامەکەمان پێ گەیشت
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
        
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Webhook is Active!")
