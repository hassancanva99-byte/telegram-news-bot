import asyncio
import feedparser
from telegram import Bot

TOKEN = "8790168869:AAE_FDokDqPB79HAQMlKCkbcPnj6KShBEnQ"
CHANNEL = "@rasd_alfaar"

bot = Bot(token=TOKEN)

# مصادر تويتر عبر RSS
twitter_rss = [

"https://nitter.net/AJABreaking/rss",
"https://nitter.net/AlHadath/rss",
"https://nitter.net/AlArabiya_Brk/rss",
"https://nitter.net/SkyNewsArabia_B/rss",
"https://nitter.net/AlMayadeenNews/rss",
"https://nitter.net/RTarabic/rss",
"https://nitter.net/trtarabi/rss"

]

# مواقع اخبار عربية
news_rss = [

"https://www.aljazeera.net/aljazeera/rss",
"https://www.alarabiya.net/.mrss/ar.xml",
"https://www.skynewsarabia.com/web/rss",
"https://arabic.rt.com/rss/",
"https://www.alhurra.com/api/zmg/rss"

]

posted_links = set()

# فلترة اخبار الحرب
keywords = [

"إيران",
"اسرائيل",
"إسرائيل",
"قصف",
"صاروخ",
"هجوم",
"حرب",
"المقاومة",
"الدفاع الجوي"

]

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

                message = f"{entry.title}\n\n{entry.link}"

                try:

                    await bot.send_message(
                        chat_id=CHANNEL,
                        text=message
                    )

                except Exception as e:
                    print("Send error:", e)

                posted_links.add(entry.link)

        except Exception as e:
            print("RSS error:", e)


async def main():

    while True:

        await check_rss_sources()

        await asyncio.sleep(30)


asyncio.run(main())
