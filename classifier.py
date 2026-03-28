"""
classifier.py
-------------
Rule-based expense classification system.
Demonstrates AI/ML concept: keyword-based classification (a form of rule-based AI).
"""

import re

# ─────────────────────────────────────────────
#  CATEGORY KEYWORD MAP
#  Each category has a set of keywords.
#  The classifier scans the description and
#  votes for the best matching category.
# ─────────────────────────────────────────────
CATEGORY_KEYWORDS = {
    "Food": [
        "swiggy", "zomato", "restaurant", "cafe", "coffee", "lunch", "dinner",
        "breakfast", "pizza", "burger", "biryani", "chai", "tea", "snack",
        "grocery", "vegetables", "fruit", "milk", "bread", "eggs", "dal",
        "rice", "maggi", "dominos", "kfc", "mcdonalds", "subway", "hotel",
        "mess", "canteen", "tiffin", "food", "eat", "meal", "drink", "juice",
    ],
    "Transport": [
        "uber", "ola", "auto", "rickshaw", "bus", "metro", "train", "cab",
        "taxi", "petrol", "diesel", "fuel", "bike", "car", "travel", "flight",
        "airport", "parking", "toll", "rapido", "bluesmart", "irctc",
        "ticket", "transport", "commute", "ferry", "boat",
    ],
    "Entertainment": [
        "netflix", "amazon prime", "hotstar", "spotify", "youtube", "movie",
        "cinema", "pvr", "inox", "concert", "event", "game", "gaming", "steam",
        "playstation", "xbox", "party", "club", "bar", "pub", "outing",
        "fun", "show", "theatre", "magic", "comedy", "music", "subscription",
    ],
    "Essentials": [
        "rent", "electricity", "water", "gas", "wifi", "internet", "mobile",
        "phone", "recharge", "insurance", "emi", "loan", "medicine", "medical",
        "hospital", "doctor", "pharmacy", "health", "gym", "school", "college",
        "fee", "tuition", "book", "stationery", "utilities", "maintenance",
    ],
    "Shopping": [
        "amazon", "flipkart", "myntra", "meesho", "ajio", "nykaa", "clothes",
        "shoes", "shirt", "jeans", "dress", "watch", "bag", "jewellery",
        "cosmetics", "beauty", "skincare", "haircut", "salon", "spa",
        "furniture", "electronics", "appliance", "gadget", "laptop", "mobile",
    ],
}

# Default if nothing matches
DEFAULT_CATEGORY = "Other"


def parse_expense(raw_input: str) -> dict | None:
    """
    Parse a natural-language expense string like '250 swiggy lunch'.

    Extracts:
      - amount  : float
      - description : str
      - category : str

    Returns None if the input is invalid.
    """
    raw_input = raw_input.strip()
    if not raw_input:
        return None

    # Find the first number (int or float) anywhere in the string
    amount_match = re.search(r"\d+(\.\d+)?", raw_input)
    if not amount_match:
        return None

    amount = float(amount_match.group())
    if amount <= 0:
        return None

    # Description = everything except the matched number
    description = re.sub(r"\d+(\.\d+)?", "", raw_input, count=1).strip()
    description = description if description else "Unnamed"

    category = classify(description)

    return {
        "amount": amount,
        "description": description.title(),
        "category": category,
    }


def classify(description: str) -> str:
    """
    Rule-based classifier.
    Scans description keywords against CATEGORY_KEYWORDS.
    Returns the category with the highest keyword match count.

    AI/ML concept: This mirrors a Bag-of-Words Naive Bayes approach
    but uses explicit rules instead of learned probabilities.
    """
    desc_lower = description.lower()
    scores = {cat: 0 for cat in CATEGORY_KEYWORDS}

    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in desc_lower:
                scores[category] += 1

    best_category = max(scores, key=scores.get)

    # Only assign if at least one keyword matched
    if scores[best_category] == 0:
        return DEFAULT_CATEGORY

    return best_category
