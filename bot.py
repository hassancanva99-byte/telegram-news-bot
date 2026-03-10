import asyncio
import feedparser
import requests
import snscrape.modules.twitter as sntwitter
from io import BytesIO
from telegram import Bot

TOKEN = "8790168869:AAE_FDokDqPB79HAQMlKCkbcPnj6KShBEnQ"
CHANNEL = "@rasd_alfaar"

bot = Bot(token=TOKEN)

# حسابات تويتر عربية
twitter_accounts = [
"AJABreaking",
"AlHadath",
"AlArabiya_Brk",
"SkyNewsArabia_B",
"AlMayadeenNews",
"RTarabic",
"trtarabi",
"France24_ar",
"Alhurra"
]

# كلمات الحرب
keywords = [
"إيران",
"اسرائيل",
"إسرائيل",
"قصف",
"صاروخ",
"مسيرة",
"حرب",
"هجوم",
"الدفاع الجوي"
]

# RSS المواقع العربية
rss_feeds = [

"https://www.aljazeera.net/aljazeera/rss",
"https://www.alarabiya.net/.mrss/ar.xml",
"https://www.skynewsarabia.com/web/rss",
"https://arabic.rt.com/rss/",
"https://www.alhurra.com/api/zmg/rss"

]

posted_tweets = set()
posted_news = set()


# ---------------------------
# فحص تويتر
# ---------------------------

async def check_twitter():

    for account in twitter_accounts:

        try:

            for tweet in sntwitter.TwitterUserScraper(account).get_items():

                if tweet.id in posted_tweets:
                    break

                text = tweet.content

                if not any(word in text for word in keywords):
                    continue

                message = f"{text}\n\n{tweet.url}"

                try:

                    if tweet.media:

                        media = tweet.media[0]

                        if hasattr(media, "fullUrl"):

                            img = requests.get(media.fullUrl)

                            await bot.send_photo(
                                chat_id=CHANNEL,
                                photo=BytesIO(img.content),
                                caption=message[:1000]
                            )

                    else:

                        await bot.send_message(
                            chat_id=CHANNEL,
                            text=message[:4000]
                        )

                except Exception as e:
                    print("Twitter send error:", e)

                posted_tweets.add(tweet.id)

                break

        except Exception as e:
            print("Twitter scrape error:", e)


# ---------------------------
# فحص RSS المواقع
# ---------------------------

async def check_rss():

    for url in rss_feeds:

        try:

            feed = feedparser.parse(url)

            for entry in feed.entries:

                if entry.link in posted_news:
                    continue

                title = entry.title
                summary = entry.summary if "summary" in entry else ""

                text = f"{title}\n\n{summary}\n\n{entry.link}"

                try:

                    if "media_content" in entry:

                        img = requests.get(entry.media_content[0]["url"])

                        await bot.send_photo(
                            chat_id=CHANNEL,
                            photo=BytesIO(img.content),
                            caption=text[:1000]
                        )

                    else:

                        await bot.send_message(
                            chat_id=CHANNEL,
                            text=text[:4000]
                        )

                except Exception as e:
                    print("RSS send error:", e)

                posted_news.add(entry.link)

        except Exception as e:
            print("RSS error:", e)


# ---------------------------
# التشغيل الرئيسي
# ---------------------------

async def main():

    while True:

        await check_twitter()

        await check_rss()

        await asyncio.sleep(20)


asyncio.run(main())
