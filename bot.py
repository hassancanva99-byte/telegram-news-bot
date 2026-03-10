import asyncio
from io import BytesIO
import requests
import tweepy
from telegram import Bot

# -----------------------------
# إعداد التليجرام
# -----------------------------
TOKEN = "8790168869:AAE_FDokDqPB79HAQMlKCkbcPnj6KShBEnQ"
CHANNEL = "@rasd_alfaar"
bot = Bot(token=TOKEN)

# -----------------------------
# إعداد Twitter API v2
# -----------------------------
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAACql8AEAAAAA5LWVg3W2GIdGVYFKjESE44%2FKERI%3DM16DVAKlOLUI0DMaRjIauI27GxxWhCpzPmnYwyqUZxGD48I7nm"
client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

# -----------------------------
# قائمة 120 حساب عربي معروف بالأخبار العسكرية والحروب
# -----------------------------
twitter_accounts = [
    "AJABreaking", "AlHadath", "AlArabiya_Brk", "SkyNewsArabia_B", "AlMayadeenNews",
    "AlMasdarNews", "AlArabiya", "AlHadathNews", "AlmanarNews", "AlJazeeraArabic",
    "AlBaghdadiaNews", "RTArabic", "SputnikArabia", "PressTVArabic", "AlArabiyaLive",
    # أكمل باقي الحسابات حتى 120...
]

posted = set()

# -----------------------------
# جلب التغريدات من الحساب
# -----------------------------
async def fetch_tweets(username):
    try:
        user = client.get_user(username=username)
        tweets = client.get_users_tweets(
            id=user.data.id,
            tweet_fields=["attachments","created_at","entities","text"],
            expansions=["attachments.media_keys"],
            media_fields=["url","preview_image_url"]
        )

        if not tweets.data:
            return []

        results = []
        media_map = {}
        if tweets.includes and "media" in tweets.includes:
            for m in tweets.includes["media"]:
                media_map[m.media_key] = m

        for tweet in tweets.data:
            if tweet.id in posted:
                continue
            text = tweet.text
            images = []
            videos = []

            if "attachments" in tweet.data:
                for key in tweet.data["attachments"]["media_keys"]:
                    media = media_map.get(key)
                    if not media:
                        continue
                    if media.type == "photo":
                        images.append(media.url)
                    elif media.type in ["video","animated_gif"]:
                        videos.append(media.preview_image_url or media.url)

            results.append((tweet.id, text, images, videos))
        return results
    except Exception as e:
        print(f"fetch_tweets error for {username}: {e}")
        return []

# -----------------------------
# إرسال الرسائل للتليجرام
# -----------------------------
async def send_to_telegram(tweet_id, text, images, videos):
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
        print(f"send_to_telegram error: {e}")
    posted.add(tweet_id)

# -----------------------------
# فحص كل الحسابات
# -----------------------------
async def check_accounts():
    for username in twitter_accounts:
        tweets = await fetch_tweets(username)
        for tweet_id, text, images, videos in tweets:
            await send_to_telegram(tweet_id, text, images, videos)
            await asyncio.sleep(0.5)
        await asyncio.sleep(1)

# -----------------------------
# التشغيل الرئيسي
# -----------------------------
async def main():
    while True:
        try:
            await check_accounts()
        except Exception as e:
            print(f"main loop error: {e}")
        await asyncio.sleep(10)  # تحديث كل 10 ثواني

asyncio.run(main())
