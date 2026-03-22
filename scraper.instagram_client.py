import instaloader
import asyncio
import logging
from .config import INSTAGRAM_HASHTAGS
from .nlp_utils import extract_species, compute_confidence
from .geocode import geocode_location

logger = logging.getLogger(__name__)

class InstagramScraper:
    def __init__(self):
        self.loader = instaloader.Instaloader()

    async def fetch_hashtag_posts(self, hashtag):
        loop = asyncio.get_running_loop()
        posts = await loop.run_in_executor(None, self._get_posts, hashtag)
        return posts

    def _get_posts(self, hashtag):
        posts = []
        for post in instaloader.Hashtag.from_name(self.loader.context, hashtag).get_posts():
            if post.is_video:
                continue
            posts.append(post)
            if len(posts) >= 10:
                break
        return posts

    async def scrape(self):
        results = []
        for tag in INSTAGRAM_HASHTAGS:
            posts = await self.fetch_hashtag_posts(tag)
            for post in posts:
                text = post.caption or ""
                species = extract_species(text)
                if not species:
                    continue
                lat, lng = None, None
                if post.location:
                    lat = post.location.lat
                    lng = post.location.lng
                else:
                    loc_name = extract_location_from_text(text) or species
                    lat, lng = await geocode_location(loc_name)

                confidence = compute_confidence(text, has_photo=True, has_geo=(lat is not None))

                results.append({
                    "source": "instagram",
                    "source_url": f"https://www.instagram.com/p/{post.shortcode}/",
                    "content": text,
                    "author": post.owner_username,
                    "timestamp": post.date_utc,
                    "image_urls": [post.url],
                    "extracted_species": species,
                    "extracted_lat": lat,
                    "extracted_lng": lng,
                    "confidence_score": confidence,
                })
        return results
