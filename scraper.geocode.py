import asyncio
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import logging

logger = logging.getLogger(__name__)

geolocator = Nominatim(user_agent="africa_wildlife_scraper", timeout=5)

async def geocode_location(location_name: str) -> Tuple[float, float]:
    """Return (lat, lng) for a location name; async wrapper."""
    loop = asyncio.get_running_loop()
    try:
        result = await loop.run_in_executor(None, geolocator.geocode, location_name)
        if result:
            return result.latitude, result.longitude
    except GeocoderTimedOut:
        logger.warning("Geocoding timed out for %s", location_name)
    return None, None
