import feedparser
import telegram
import time
import requests
from io import BytesIO

# --- إعدادات البوت ---
TOKEN = "8790168869:AAE_FDokDqPB79HAQMlKCkbcPnj6KShBEnQ"
CHANNEL = "@rasd_alfaar"

bot = telegram.Bot(token=TOKEN)

# --- قائمة RSS جاهزة لجميع الحسابات والمصادر ---
feeds = [
    # حسابات تويتر متخصصة بالحرب
    "https://rsshub.app/twitter/user/MiddleEast01",
    "https://rsshub.app/twitter/user/A_M_R_M1",
    "https://rsshub.app/twitter/user/followthenews36",
    "https://rsshub.app/twitter/user/IDF",
    "https://rsshub.app/twitter/user/IsraelWarRoom",
    "https://rsshub.app/twitter/user/IsraeliPM",

    # مصادر أخبار عالمية
    "http://feeds.bbci.co.uk/news/world/middle_east/rss.xml",
    "http://rss.cnn.com/rss/edition_world.rss",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www.reutersagency.com/feed/?best-topics=world-news",

    # تغطية الشرق الأوسط العامة
    "http://feeds.alarabiya.net/alarabiya/arabic",
    "https://www.middleeasteye.net/rss"
]

posted = set()

# --- وظيفة لجلب الصورة من RSS ---
def get_image(entry):
    # معظم RSS يحتوي على media_content أو enclosure
    if hasattr(entry, 'media_content'):
        return entry.media_content[0]['url']
    if hasattr(entry, 'enclosures') and len(entry.enclosures) > 0:
        return entry.enclosures[0]['href']
    return None

# --- الحلقة الرئيسية للبوت ---
while True:
    for rss_url in feeds:
        try:
            feed = feedparser.parse(rss_url)
        except Exception as e:
            print("Error parsing RSS:", e)
            continue

        for entry in feed.entries:
            if entry.link not in posted:
                msg = f"{entry.title}\n{entry.link}"

                # جلب الصورة إذا موجودة
                image_url = get_image(entry)

                try:
                    if image_url:
                        # تحميل الصورة
                        response = requests.get(image_url)
                        image_bytes = BytesIO(response.content)
                        bot.send_photo(chat_id=CHANNEL, photo=image_bytes, caption=msg)
                    else:
                        bot.send_message(chat_id=CHANNEL, text=msg)
                except Exception as e:
                    print("Error sending message:", e)

                posted.add(entry.link)

    # تحديث كل 15 ثانية
    time.sleep(15)