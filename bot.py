import feedparser
import asyncio
import requests
from io import BytesIO
from telegram import Bot

TOKEN = "8790168869:AAE_FDokDqPB79HAQMlKCkbcPnj6KShBEnQ"
CHANNEL = "@rasd_alfaar"

bot = Bot(token=TOKEN)

feeds = [
    "https://rsshub.app/twitter/user/MiddleEast01",
    "https://rsshub.app/twitter/user/IDF",
    "http://feeds.bbci.co.uk/news/world/middle_east/rss.xml",
    "http://rss.cnn.com/rss/edition_world.rss",
    "https://www.aljazeera.com/xml/rss/all.xml"
]

posted = set()


def get_image(entry):
    if hasattr(entry, 'media_content'):
        return entry.media_content[0]['url']
    if hasattr(entry, 'enclosures') and len(entry.enclosures) > 0:
        return entry.enclosures[0]['href']
    return None


async def main():

    while True:

        for rss_url in feeds:

            feed = feedparser.parse(rss_url)

            for entry in feed.entries:

                if entry.link not in posted:

                    text = f"{entry.title}\n{entry.link}"

                    image_url = get_image(entry)

                    try:

                        if image_url:
                            response = requests.get(image_url)
                            image_bytes = BytesIO(response.content)

                            await bot.send_photo(
                                chat_id=CHANNEL,
                                photo=image_bytes,
                                caption=text
                            )

                        else:

                            await bot.send_message(
                                chat_id=CHANNEL,
                                text=text
                            )

                    except Exception as e:
                        print("Send error:", e)

                    posted.add(entry.link)

        await asyncio.sleep(15)


asyncio.run(main())
