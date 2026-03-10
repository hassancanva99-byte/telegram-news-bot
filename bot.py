import asyncio
import feedparser
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from telegram import Bot

TOKEN = "8790168869:AAE_FDokDqPB79HAQMlKCkbcPnj6KShBEnQ"
CHANNEL = "@rasd_alfaar"

bot = Bot(token=TOKEN)

# 10 حسابات للتجربة (يمكن توسيعها لاحقًا)
twitter_accounts = [
    "AJABreaking", "AlHadath", "AlArabiya_Brk", "SkyNewsArabia_B", "AlMayadeenNews"
]

# قائمة سيرفرات Nitter بديلة
nitter_servers = [
    "https://nitter.net",
    "https://nitter.42l.fr",
    "https://nitter.it"
]

posted = set()

# ------------------------------
# دالة لجلب RSS مع سيرفر بديل
# ------------------------------
def safe_parse(account):
    for server in nitter_servers:
        url = f"{server}/{account}/rss"
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            feed = feedparser.parse(resp.content)
            return feed
        except Exception as e:
            print(f"RSS fetch failed for {account} at {server}: {e}")
    return None

# ------------------------------
# جلب التغريدة كاملة + الصور + الفيديو
# ------------------------------
async def get_full_tweet(link):
    try:
        html = requests.get(link, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        tweet_text = soup.find("div", {"class": "tweet-content"})
        text = tweet_text.text.strip() if tweet_text else ""

        images = []
        for img in soup.find_all("img"):
            src = img.get("src")
            if "/pic/" in src:
                images.append("https://nitter.net" + src)

        videos = []
        for video in soup.find_all("video"):
            src = video.get("src")
            if src:
                videos.append("https://nitter.net" + src)

        return text, images, videos
    except Exception as e:
        print("get_full_tweet error:", e)
        return "", [], []

# ------------------------------
# فحص جميع الحسابات
# ------------------------------
async def check_twitter():
    for account in twitter_accounts:
        feed = safe_parse(account)
        if not feed:
            continue

        for entry in feed.entries:
            if entry.link in posted:
                continue

            text, images, videos = await get_full_tweet(entry.link)

            # طباعة التحذيرات لمراقبة التغريدة
            if not text:
                print(f"No text found for {entry.link}")
            if not images and not videos:
                print(f"No images/videos for {entry.link}")

            try:
                if images:
                    img = requests.get(images[0], timeout=10)
                    await bot.send_photo(
                        chat_id=CHANNEL,
                        photo=BytesIO(img.content),
                        caption=text[:1000]
                    )
                elif videos:
                    vid = requests.get(videos[0], timeout=10)
                    await bot.send_video(
                        chat_id=CHANNEL,
                        video=BytesIO(vid.content),
                        caption=text[:1000]
                    )
                else:
                    await bot.send_message(chat_id=CHANNEL, text=text)
            except Exception as e:
                print("send error:", e)

            posted.add(entry.link)
            await asyncio.sleep(0.5)

        await asyncio.sleep(1)

# ------------------------------
# التشغيل الرئيسي
# ------------------------------
async def main():
    while True:
        try:
            await check_twitter()
        except Exception as e:
            print("check_twitter error:", e)
        await asyncio.sleep(5)

asyncio.run(main())
