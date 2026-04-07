from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import os

# تۆکەنەکەی خۆت لێرە دابنێ لەناو کەوانەکان
TOKEN = os.environ.get("BOT_TOKEN", "8103815264:AAGFXJOpFoG8qIJLK7Ibdqe99s1tcElTe_c)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            update = json.loads(post_data.decode('utf-8'))
            
            if "message" in update and "text" in update["message"]:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"]["text"]
                
                # وەڵامی بۆتەکە
                if text == "/start":
                    reply_text = "سڵاو شێرەکەم! 🦁 من ئێستا لەسەر Vercel کاردەکەم و قەت نانووم!"
                else:
                    reply_text = f"تۆ وتت: {text} - منیش بەردەوام لە خەتەم!"
                
                # ناردنی نامەکە بۆ تیلیگرام
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                data = json.dumps({"chat_id": chat_id, "text": reply_text}).encode('utf-8')
                req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
                urllib.request.urlopen(req)
                
        except Exception as e:
            print("Error:", e)

        # پێدانی وەڵام بە تیلیگرام بۆ ئەوەی بزانێت ئیشەکەمان کرد
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Webhook is running!")
