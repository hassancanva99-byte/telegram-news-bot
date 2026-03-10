import asyncio
import feedparser
import requests
from io import BytesIO
from telegram import Bot, InputMediaPhoto, InputMediaVideo

TOKEN = "PUT_TOKEN_HERE"
CHANNEL = "@your_channel"

bot = Bot(token=TOKEN)

# 100 حساب تويتر عربي عبر Nitter RSS (أمثلة)
twitter_rss = [
    "https://nitter.net/AJABreaking/rss",
    "https://nitter.net/AlHadath/rss",
    "https://nitter.net/AlArabiya_Brk/rss",
    "https://nitter.net/SkyNewsArabia_B/rss",
    "https://nitter.net/AlMayadeenNews/rss",
    "https://nitter.net/RTarabic/rss",
    "https://nitter.net/trtarabi/rss",
    "https://nitter.net/AlghadeerTV/rss",
    "https://nitter.net/France24_ar/rss",
    "https://nitter.net/Alhurra/rss"
    # أضف بقية الحسابات حسب الحاجة حتى 100
]

# RSS مواقع عربية
news_rss = [
    "https://www.aljazeera.net/aljazeera/rss",
    "https://www.alarabiya.net/.mrss/ar.xml",
    "https://www.skynewsarabia.com/web/rss",
    "https://arabic.rt.com/rss/",
    "https://www.alhurra.com/api/zmg/rss"
]

posted_links = set()

# كلمات فلترة الأخبار
keywords = [
    "إيران", "اسرائيل", "إسرائيل", "قصف",
    "صاروخ", "هجوم", "حرب", "المقاومة", "الدفاع الجوي"
]

async def send_media(entry):
    media_urls = []

    # الصور والفيديو من RSS
    if "media_content" in entry:
        for m in entry.media_content:
            media_urls.append(m.get("url"))

    if "enclosures" in entry:
        for e in entry.enclosures:
            media_urls.append(e.get("href"))

    media_group = []
    for url in media_urls[:10]:  # الحد الأقصى 10 وسائط
        try:
            r = requests.get(url, timeout=10)
            content_type = r.headers.get("content-type", "")
            if "video" in content_type:
                media_group.append(InputMediaVideo(BytesIO(r.content)))
            else:
                media_group.append(InputMediaPhoto(BytesIO(r.content)))
        except:
            continue

    if media_group:
        await bot.send_media_group(chat_id=CHANNEL, media=media_group)
        return True

    return False

async def check_rss_sources():
    sources = twitter_rss + news_rss

    for url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                if entry.link in posted_links:
                    continue

                text = entry.title
                if not any(word in text for word in keywords):
                    continue

                # إرسال الصور والفيديو أولاً
                sent_media = await send_media(entry)

                # إرسال النص فقط إذا لم تُرسل وسائط أو النص طويل
                if not sent_media or len(text) > 50:
                    await bot.send_message(chat_id=CHANNEL, text=text)

                posted_links.add(entry.link)
        except Exception as e:
            print("RSS error:", e)

async def main():
    while True:
        await check_rss_sources()
        await asyncio.sleep(10)  # تحديث كل 10 ثواني

asyncio.run(main())
