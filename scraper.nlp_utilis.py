import re
import spacy
from typing import Optional, Tuple

# Load small English model (download once: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

# Predefined species list
SPECIES_LIST = [
    "lion", "elephant", "leopard", "rhino", "buffalo", "giraffe", "zebra",
    "wildebeest", "hippo", "crocodile", "cheetah", "hyena", "wild dog"
]

def extract_species(text: str) -> Optional[str]:
    """Return first detected species in text."""
    text_lower = text.lower()
    for species in SPECIES_LIST:
        if species in text_lower:
            return species
    return None

def extract_location_from_text(text: str) -> Optional[str]:
    """Use spaCy NER to find GPE (geopolitical entity)."""
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            return ent.text
    return None

def compute_confidence(text: str, has_photo: bool, has_geo: bool) -> float:
    """Compute confidence score based on multiple signals."""
    score = 0.2 # base
    if has_photo:
        score += 0.3
    if has_geo:
        score += 0.3
    # boost if species name is exactly present
    if extract_species(text):
        score += 0.2
    return min(score, 1.0)
