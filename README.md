# 🚀 BotRunner — Telegram Bot Hosting Panel

یەک وێبسایتی ناوازەی iOS 17 dark کە بەرێوەبردنی بۆتی تیلیگرامت ئاسان دەکات.

---

## 📁 Structure

```
botrunner/
├── api/
│   └── run.py          ← Vercel Python serverless API
├── public/
│   └── index.html      ← Dashboard UI (iOS 17 dark)
├── vercel.json         ← Vercel config
├── requirements.txt    ← (empty — packages installed at runtime)
└── README.md
```

---

## 🐙 STEP 1 — Upload to GitHub

### ناوی پڕۆژە لە GitHub
```
botrunner
```
یان هەر ناوێکی تر وەک:
```
telegram-bot-panel
my-bot-host
```

### چۆنیەتی:
1. بچۆ **github.com** → چەپ سەرەوە **"New"** کلیک بکە
2. **Repository name:** `botrunner`
3. **Description:** `Telegram Bot Hosting Panel — iOS 17 UI`
4. **Public** یاخود **Private** — هەردووک کار دەکات
5. **"Create repository"** کلیک بکە
6. پاشان ئەم فایلەکانت بۆ ئەپلۆد بکە:
   - لوپتۆپەوە: `git clone` → کۆپی فایلەکان → `git push`
   - یاخود ڕاستەوخۆ لە GitHub: **"uploading an existing file"** کلیک بکە

---

## ▲ STEP 2 — Deploy to Vercel

1. بچۆ **vercel.com** → چوونەژوورەوە با GitHub حسابت
2. **"Add New Project"** کلیک بکە
3. **"Import Git Repository"** — `botrunner` هەڵبژێرە
4. **Framework Preset:** Other
5. **"Deploy"** کلیک بکە

⏳ ئامادەبوون نزیکەی 1-2 خولەک دەخایەنێت.

---

## 🔐 STEP 3 — Environment Variables

> لە Vercel Dashboard → سەلێنە پڕۆژەکەت → **Settings** → **Environment Variables**

### ئایا پێویستی بە Environment Variablesە؟

بۆ ئەم وێبسایتە **پێویست نییە** Environment Variable دابنێی.

بۆتەکەت خۆی بە خۆی دەیخوێنێتەوە لە ئەپلۆدەکەت.

### ئەگەر بۆتەکەت لە داخڵی خۆیدا `BOT_TOKEN` ئاگادارییەکەی پێویستە:
| Name | Value |
|------|-------|
| `BOT_TOKEN` | `123456789:ABCdef...` (تۆکەنی بۆتت) |

> **ئەمە چۆنە؟**
> - **Name** = ناوی گۆڕاوەکە — ئەمەیە کاری لەگەڵی دەکات: بزاوتی چەپ
> - **Value** = نرخی گۆڕاوەکە — ئەمەیە کاری لەگەڵی دەکات: بزاوتی ڕاست
> - "Add" کلیک بکە → "Save" کلیک بکە

---

## ✅ STEP 4 — Use the Panel

1. **وێبسایتەکەت** بکەرەوە (Vercel لینکەکەت دەدات)
2. **Upload** — فایلی `bot.py`ت بکەرە
3. **Packages** — پاکێجەکانت بنووسە (یەک لە هەر ڕیزێک)
4. **Run Bot** — کلیک بکە

---

## ⚠️ تێبینیی گرنگ

### Vercel Serverless Timeout
Vercel بە سەرخۆیی **فانکشنەکانی** دەوەستێنێت دوای **10 چرکە** (Free plan).

**چارەسەر:** بۆتەکەت لە **Background Thread** ڕادەکات — بۆتەکە زیندوو دەمێنێتەوە تا کاتێک Vercel container دا بکوژێت.

### Bot Token
دڵنیابە بۆتەکەت تۆکەن لە `os.environ.get("BOT_TOKEN")` دەخوێنێتەوە:
```python
import os
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
```

### ئەگەر ئارەزووی هۆستکردنی بەردەوام هەیتە:
- **Railway.app** — زیاتر مناسبە بۆ بۆتی تیلیگرام
- **Render.com** — Free tier باشی هەیە
- **VPS** — کۆنتڕۆلی تەواو

---

## 🎨 Design Notes

- iOS 17 dark aesthetic
- Animated gradient orb background
- Glassmorphism cards
- Real-time progress bar
- Live console terminal
- Smooth step indicator
- Zero external dependencies
