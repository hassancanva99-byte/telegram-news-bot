import feedparser
import asyncio
import requests
import yt_dlp
from io import BytesIO
from telegram import Bot

TOKEN = "8790168869:AAE_FDokDqPB79HAQMlKCkbcPnj6KShBEnQ"
CHANNEL = "@rasd_alfaar"

bot = Bot(token=TOKEN)

feeds = [

# تويتر عربي
"https://rsshub.app/twitter/user/AlHadath",
"https://rsshub.app/twitter/user/AlArabiya_Brk",
"https://rsshub.app/twitter/user/AJABreaking",
"https://rsshub.app/twitter/user/AlMayadeenNews",
"https://rsshub.app/twitter/user/SkyNewsArabia_B",

# مواقع عربية
"https://www.aljazeera.net/aljazeera/rss",
"https://www.alarabiya.net/.mrss/ar.xml",
"https://www.skynewsarabia.com/web/rss",
"https://arabic.rt.com/rss/",
"https://www.alhurra.com/api/zmg/rss"
]

posted = set()


def download_video(url):

    ydl_opts = {
        "format": "mp4",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        video_url = info["url"]

        r = requests.get(video_url)

        return BytesIO(r.content)


def get_image(entry):

    if "media_content" in entry:
        return entry.media_content[0]["url"]

    if "enclosures" in entry and len(entry.enclosures) > 0:
        return entry.enclosures[0]["href"]

    return None


async def main():

    while True:

        for url in feeds:

            feed = feedparser.parse(url)

            for entry in feed.entries:

                if entry.link not in posted:

                    title = entry.title
                    text = entry.summary if "summary" in entry else ""

                    message = f"{title}\n\n{text}\n\n{entry.link}"

                    media = get_image(entry)

                    try:

                        # فيديو تويتر
                        if "twitter.com" in entry.link or "x.com" in entry.link:

                            video = download_video(entry.link)

                            await bot.send_video(
                                chat_id=CHANNEL,
                                video=video,
                                caption=message[:1000]
                            )

                        elif media:

                            img = requests.get(media)

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
                        print(e)

                    posted.add(entry.link)

        await asyncio.sleep(15)


asyncio.run(main())
