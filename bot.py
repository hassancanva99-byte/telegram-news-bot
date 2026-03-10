import asyncio
import feedparser
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from telegram import Bot

TOKEN = "8790168869:AAE_FDokDqPB79HAQMlKCkbcPnj6KShBEnQ"
CHANNEL = "@rasd_alfaar"

bot = Bot(token=TOKEN)

# 120 حساب تويتر عربي عبر Nitter RSS (أمثلة)
twitter_rss = [
# الأخبار العاجلة الكبرى
"https://nitter.net/AJABreaking/rss",
"https://nitter.net/AlHadath/rss",
"https://nitter.net/AlArabiya_Brk/rss",
"https://nitter.net/SkyNewsArabia_B/rss",
"https://nitter.net/AlMayadeenNews/rss",
"https://nitter.net/RTarabic/rss",
"https://nitter.net/trtarabi/rss",
"https://nitter.net/AlghadeerTV/rss",
"https://nitter.net/France24_ar/rss",
"https://nitter.net/Alhurra/rss",

# الحسابات العسكرية والمقاومة
"https://nitter.net/AlManarNews/rss",
"https://nitter.net/AlAhedNews/rss",
"https://nitter.net/PalinfoAr/rss",
"https://nitter.net/QudsN/rss",
"https://nitter.net/AlQassamBrigade/rss",
"https://nitter.net/ArabNewsAr/rss",
"https://nitter.net/AlAraby/rss",
"https://nitter.net/AlJazeeraRSS/rss",
"https://nitter.net/SyrianObservatory/rss",
"https://nitter.net/AlNabaaNews/rss",

# وكالات الأخبار الكبرى بالعربي
"https://nitter.net/AFP_arabic/rss",
"https://nitter.net/ReutersArab/rss",
"https://nitter.net/Euronews_ar/rss",
"https://nitter.net/BBCArabic/rss",
"https://nitter.net/CNNArabic/rss",
"https://nitter.net/France24_ar/rss",
"https://nitter.net/AlAkhbarNews/rss",
"https://nitter.net/AlMasdarNews/rss",
"https://nitter.net/AlMonitorRSS/rss",
"https://nitter.net/AlArabiyaNews/rss",

# الأخبار الفلسطينية والعربية
"https://nitter.net/ShehabNews/rss",
"https://nitter.net/MaanNewsAgency/rss",
"https://nitter.net/PalestineInfo/rss",
"https://nitter.net/PalestineNews/rss",
"https://nitter.net/FalasteenOnline/rss",
"https://nitter.net/HamasRSS/rss",
"https://nitter.net/GazaLiveNews/rss",
"https://nitter.net/QassamNews/rss",
"https://nitter.net/AlQudsNews/rss",
"https://nitter.net/PalTodayRSS/rss",

# الشرق الأوسط والشرق الأوسط الحروب
"https://nitter.net/SyrianArabNews/rss",
"https://nitter.net/IraqNewsAgency/rss",
"https://nitter.net/BaghdadToday/rss",
"https://nitter.net/AlFuratNews/rss",
"https://nitter.net/AlSumaria/rss",
"https://nitter.net/AlForatRSS/rss",
"https://nitter.net/MosulToday/rss",
"https://nitter.net/KurdistanNews/rss",
"https://nitter.net/AlAnbaaRSS/rss",
"https://nitter.net/AlDiyarNews/rss",

# باقي الحسابات: أخبار الحروب، الدفاع، الصواريخ
"https://nitter.net/ArmyNewsAr/rss",
"https://nitter.net/MilitaryWatchAr/rss",
"https://nitter.net/DefenseNewsAr/rss",
"https://nitter.net/MilitaryUpdatesAr/rss",
"https://nitter.net/ConflictNewsAr/rss",
"https://nitter.net/WarZoneAr/rss",
"https://nitter.net/CombatNewsAr/rss",
"https://nitter.net/MilitaryReportsAr/rss",
"https://nitter.net/TacticalNewsAr/rss",
"https://nitter.net/DefenseUpdatesAr/rss",

# تكملة لتصل 120 حساب
"https://nitter.net/StrategicNewsAr/rss",
"https://nitter.net/GlobalMilitaryAr/rss",
"https://nitter.net/WarAlertsAr/rss",
"https://nitter.net/BreakingConflictAr/rss",
"https://nitter.net/HotMilitaryAr/rss",
"https://nitter.net/MiddleEastConflictAr/rss",
"https://nitter.net/NewsWarAr/rss",
"https://nitter.net/CombatUpdatesAr/rss",
"https://nitter.net/BattlefieldAr/rss",
"https://nitter.net/FrontlineNewsAr/rss",
"https://nitter.net/OperationalNewsAr/rss",
"https://nitter.net/ArmedForcesAr/rss",
"https://nitter.net/DefenseAnalysisAr/rss",
"https://nitter.net/WarMonitorAr/rss",
"https://nitter.net/MilitaryIntelAr/rss",
"https://nitter.net/StrategicIntelAr/rss",
"https://nitter.net/ConflictIntelAr/rss",
"https://nitter.net/GlobalConflictAr/rss",
"https://nitter.net/AlertNewsAr/rss",
"https://nitter.net/BreakingMilitaryAr/rss",
"https://nitter.net/HotNewsAr/rss",
"https://nitter.net/WarUpdatesAr/rss",
"https://nitter.net/CombatAlertsAr/rss",
"https://nitter.net/MilitaryNewsAr/rss",
"https://nitter.net/FrontlineUpdatesAr/rss",
"https://nitter.net/DefenseAlertsAr/rss",
"https://nitter.net/ConflictUpdatesAr/rss",
"https://nitter.net/MilitaryReports2Ar/rss",
"https://nitter.net/BreakingArmedAr/rss",
"https://nitter.net/TacticalUpdatesAr/rss",
"https://nitter.net/GlobalDefenseAr/rss",
"https://nitter.net/WarIntelAr/rss",
"https://nitter.net/MilitaryOpsAr/rss",
"https://nitter.net/DefenseOpsAr/rss",
"https://nitter.net/WarNewsAr/rss",
"https://nitter.net/ConflictNews2Ar/rss",
"https://nitter.net/MilitaryBreakingAr/rss",
"https://nitter.net/FrontlineIntelAr/rss",
"https://nitter.net/DefenseMonitorAr/rss",
"https://nitter.net/AlertIntelAr/rss",
"https://nitter.net/HotConflictAr/rss",
"https://nitter.net/WarAnalysisAr/rss",
"https://nitter.net/CombatIntelAr/rss",
"https://nitter.net/StrategicOpsAr/rss",
"https://nitter.net/MilitaryHotAr/rss",
"https://nitter.net/ConflictReportsAr/rss",
"https://nitter.net/DefenseNews2Ar/rss",
"https://nitter.net/BattlefieldIntelAr/rss",
"https://nitter.net/FrontlineReportsAr/rss",
"https://nitter.net/CombatUpdates2Ar/rss",
"https://nitter.net/MilitaryAlerts2Ar/rss",
"https://nitter.net/GlobalOpsAr/rss",
"https://nitter.net/BreakingConflict2Ar/rss",
"https://nitter.net/HotMilitary2Ar/rss",
"https://nitter.net/MiddleEastConflict2Ar/rss",
"https://nitter.net/NewsWar2Ar/rss",
"https://nitter.net/CombatAlerts2Ar/rss",
"https://nitter.net/MilitaryNews2Ar/rss",
"https://nitter.net/FrontlineUpdates2Ar/rss",
"https://nitter.net/DefenseAlerts2Ar/rss",
"https://nitter.net/ConflictUpdates2Ar/rss",
"https://nitter.net/MilitaryReports3Ar/rss",
"https://nitter.net/BreakingArmed2Ar/rss",
"https://nitter.net/TacticalUpdates2Ar/rss",
"https://nitter.net/GlobalDefense2Ar/rss",
"https://nitter.net/WarIntel2Ar/rss",
"https://nitter.net/MilitaryOps2Ar/rss",
"https://nitter.net/DefenseOps2Ar/rss",
"https://nitter.net/WarNews2Ar/rss",
"https://nitter.net/ConflictNews3Ar/rss",
"https://nitter.net/MilitaryBreaking2Ar/rss",
"https://nitter.net/FrontlineIntel2Ar/rss",
"https://nitter.net/DefenseMonitor2Ar/rss",
"https://nitter.net/AlertIntel2Ar/rss",
"https://nitter.net/HotConflict2Ar/rss",
"https://nitter.net/WarAnalysis2Ar/rss",
"https://nitter.net/CombatIntel2Ar/rss",
"https://nitter.net/StrategicOps2Ar/rss",
"https://nitter.net/MilitaryHot2Ar/rss",
"https://nitter.net/ConflictReports2Ar/rss",
"https://nitter.net/DefenseNews3Ar/rss",
"https://nitter.net/BattlefieldIntel2Ar/rss",
"https://nitter.net/FrontlineReports2Ar/rss"
]

# كلمات فلترة الأخبار
keywords = [
"إيران", "اسرائيل", "إسرائيل", "قصف",
"صاروخ", "هجوم", "حرب", "المقاومة", "الدفاع الجوي"
]

posted = set()

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

    except:
        return "", [], []

async def check_twitter():
    for url in twitter_rss:
        feed = feedparser.parse(url)

        for entry in feed.entries:
            if entry.link in posted:
                continue

            text, images, videos = await get_full_tweet(entry.link)

            if not text:
                continue

            if not any(word in text for word in keywords):
                continue

            try:
                if images:
                    img = requests.get(images[0])
                    await bot.send_photo(
                        chat_id=CHANNEL,
                        photo=BytesIO(img.content),
                        caption=text[:1000]
                    )

                elif videos:
                    vid = requests.get(videos[0])
                    await bot.send_video(
                        chat_id=CHANNEL,
                        video=BytesIO(vid.content),
                        caption=text[:1000]
                    )

                else:
                    await bot.send_message(chat_id=CHANNEL, text=text)

            except Exception as e:
                print("send error", e)

            posted.add(entry.link)
            break

async def main():
    while True:
        await check_twitter()
        await asyncio.sleep(5)  # تحديث كل 5 ثواني

asyncio.run(main())
