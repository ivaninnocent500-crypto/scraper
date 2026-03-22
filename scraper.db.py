import asyncpg
import logging
from .config import DB_URL

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(DB_URL)

    async def insert_crowdsourced_report(self, report: dict):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO crowdsourced_reports (
                    source, source_url, content, author_handle,
                    image_urls, extracted_species,
                    extracted_location, extracted_timestamp,
                    confidence_score, status
                ) VALUES ($1, $2, $3, $4, $5, $6,
                          ST_SetSRID(ST_MakePoint($7, $8), 4326),
                          $9, $10, 'PENDING')
                ON CONFLICT (source_url) DO NOTHING
            """,
                report["source"],
                report["source_url"],
                report["content"],
                report["author"],
                report["image_urls"],
                report["extracted_species"],
                report["extracted_lng"] if report["extracted_lng"] is not None else 0.0,
                report["extracted_lat"] if report["extracted_lat"] is not None else 0.0,
                report["timestamp"],
                report["confidence_score"],
            )

    async def close(self):
        await self.pool.close()
