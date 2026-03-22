import os
from dotenv import load_dotenv

load_dotenv()

# Database
DB_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/ati")

# Twitter API v2
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_KEYWORDS = ["#safari", "#wildlifesighting", "lion sighting", "elephant herd", "rhino sighting", "leopard sighting", "giraffe", "zebra", "wildebeest", "buffalo", "cheetah", "hippo", "crocodile", "hyena"]

# Instagram
INSTAGRAM_HASHTAGS = ["safaridiaries", "wildlifesighting", "bigfive", "serengeti", "masaimara", "krugernationalpark", "lion", "elephant"]

# Geocoding
GEOCODING_TIMEOUT = 5 # seconds
