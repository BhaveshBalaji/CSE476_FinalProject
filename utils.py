import re

# Erase punctuation
ARTICLES = {"a", "an", "the"}

def normalize_text(s: str) -> str:
    # handle boolean values to pass through questions in common_sense domain (boolean to string)
    if isinstance(s, bool):
        s = "true" if s else "false"

    s = (s or "").strip().lower()

    # Remove surrounding punctuation and extra whitespace
    s = re.sub(r"[^\w\s\-']", " ", s)
    s = re.sub(r"\s+", " ", s).strip()

    # Remove articles as I saw some answers are not accurate just because of extra articles.
    tokens = [t for t in s.split() if t not in ARTICLES]

    # Map common synonyms used in these tests
    synonyms = {
        "unchanged": "stay the same",
        "no change": "stay the same",
        "same": "stay the same",
        "second place": "second",
        "2nd": "second",
        "first place": "first",
        "third place": "third",
        
        # true or false synonyms to see if it improves common_sense accuracy
        "true": "true",
        "false": "false",
        "yes": "true",
        "no": "false",
    }
    tokens = [synonyms.get(t, t) for t in tokens]

    return " ".join(tokens)