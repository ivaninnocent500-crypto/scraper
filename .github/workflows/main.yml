import asyncio
import logging
import schedule
import time
from .config import DB_URL
from .twitter_client import TwitterScraper
from .instagram_client import InstagramScraper
from .db import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def scrape_and_store():
    logger.info("Starting scraping cycle")
    db = Database()
    await db.connect()

    twitter = TwitterScraper()
    instagram = InstagramScraper()

    # Fetch from Twitter
    twitter_reports = await twitter.fetch_recent_tweets()
    for report in twitter_reports:
        await db.insert_crowdsourced_report(report)

    # Fetch from Instagram
    insta_reports = await instagram.scrape()
    for report in insta_reports:
        await db.insert_crowdsourced_report(report)

    logger.info("Scraped %d Twitter + %d Instagram reports", len(twitter_reports), len(insta_reports))
    await db.close()

def run_async():
    asyncio.run(scrape_and_store())

if __name__ == "__main__":
    # Run once immediately
    run_async()
    # Schedule every 30 minutes
    schedule.every(30).minutes.do(run_async)
    while True:
        schedule.run_pending()
        time.sleep(1)
