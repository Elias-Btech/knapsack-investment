"""
Dataset Generator – 0/1 Knapsack Investment Portfolio Optimization
Produces investments.csv (120 items) with unique, real-world investment names.
Each name appears exactly once – no repetition.
"""

import csv
import random

# ── Configuration ────────────────────────────────────────────────────────────
OUTPUT_FILE = "investments.csv"
RANDOM_SEED = 7
# ──────────────────────────────────────────────────────────────────────────────

# 120 globally known, simple investment names – no codes, no jargon, no repeats
INVESTMENT_NAMES = [
    # Famous Company Stocks – brands everyone knows worldwide (40)
    "Apple",          "Microsoft",      "Amazon",         "Tesla",
    "Google",         "Meta",           "Netflix",        "Nike",
    "Coca-Cola",      "McDonald's",     "Disney",         "Samsung",
    "Toyota",         "BMW",            "Mercedes-Benz",  "Adidas",
    "Starbucks",      "Walmart",        "IKEA",           "Zara",
    "Spotify",        "Uber",           "Airbnb",         "PayPal",
    "Intel",          "IBM",            "Sony",           "Panasonic",
    "Ferrari",        "Rolex",          "Louis Vuitton",  "Gucci",
    "Chanel",         "Prada",          "Hermes",         "Nestle",
    "Pfizer",         "Johnson & Johnson", "Visa",        "MasterCard",

    # Government & Corporate Bonds – simple country/company names (20)
    "USA Government Bond",    "UK Government Bond",
    "Germany Government Bond","Japan Government Bond",
    "China Government Bond",  "France Government Bond",
    "Apple Bond",             "Microsoft Bond",
    "Amazon Bond",            "Toyota Bond",
    "Coca-Cola Bond",         "Disney Bond",
    "Nike Bond",              "Samsung Bond",
    "McDonald's Bond",        "Walmart Bond",
    "BMW Bond",               "Sony Bond",
    "Netflix Bond",           "Google Bond",

    # Real Estate – famous cities everyone knows (15)
    "New York Apartment",     "Dubai Apartment",
    "London Apartment",       "Paris Apartment",
    "Tokyo Apartment",        "Sydney House",
    "Singapore Condo",        "Berlin Apartment",
    "Miami Villa",            "Los Angeles House",
    "Chicago Office",         "Toronto Condo",
    "Hong Kong Flat",         "Shanghai Office",
    "Mumbai Office",

    # Investment Funds – plain English names (15)
    "S&P 500 Fund",           "Nasdaq Fund",
    "Dow Jones Fund",         "World Stock Fund",
    "Asia Stock Fund",        "Europe Stock Fund",
    "Tech Growth Fund",       "Healthcare Fund",
    "Clean Energy Fund",      "Real Estate Fund",
    "Gold Fund",              "Oil and Gas Fund",
    "Dividend Fund",          "Balanced Fund",
    "Emerging Markets Fund",

    # Commodities – one word, universally understood (10)
    "Gold",           "Silver",
    "Oil",            "Natural Gas",
    "Copper",         "Wheat",
    "Coffee",         "Sugar",
    "Cotton",         "Platinum",

    # Cryptocurrencies – globally famous names (10)
    "Bitcoin",        "Ethereum",
    "BNB",            "Solana",
    "Cardano",        "Ripple",
    "Dogecoin",       "Litecoin",
    "Polkadot",       "Avalanche",

    # Famous Banks & Finance Firms (10)
    "Goldman Sachs",  "JPMorgan",
    "Citibank",       "HSBC",
    "Barclays",       "Deutsche Bank",
    "Morgan Stanley", "BlackRock",
    "Vanguard",       "Fidelity",
]


def generate_dataset(seed: int = RANDOM_SEED) -> list[dict]:
    """
    Build 120 investment items in three tiers using unique names.

    Tier A – 'Greedy Bait' (40 items):  low cost, moderate return, high ratio
    Tier B – 'DP Sweet Spot' (40 items): medium cost, high absolute return
    Tier C – 'Noise' (40 items):         random cost and return
    """
    random.seed(seed)

    # Shuffle names so tier assignment is not predictable
    names = INVESTMENT_NAMES[:]
    random.shuffle(names)

    items = []

    for i, name in enumerate(names):
        idx = i + 1

        if i < 40:          # Tier A – greedy bait
            cost = random.randint(5, 15)
            ret = round(random.uniform(30, 60), 2)
        elif i < 80:        # Tier B – DP sweet spot
            cost = random.randint(20, 50)
            ret = round(random.uniform(80, 140), 2)
        else:               # Tier C – noise
            cost = random.randint(10, 90)
            ret = round(random.uniform(5, 100), 2)

        items.append({
            "Investment_ID": f"INV_{idx:03d}",
            "Name":          name,
            "Cost":          cost,
            "Return":        ret,
        })

    random.shuffle(items)
    # Reassign IDs after shuffle
    for i, item in enumerate(items, 1):
        item["Investment_ID"] = f"INV_{i:03d}"

    return items


def write_csv(items: list[dict], filename: str) -> None:
    fieldnames = ["Investment_ID", "Name", "Cost", "Return"]
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(items)
    print(f"[✓] Dataset saved → '{filename}' "
          f"({len(items)} items, seed={RANDOM_SEED})")


if __name__ == "__main__":
    items = generate_dataset()
    write_csv(items, OUTPUT_FILE)

    print(f"\n{'Investment_ID':<10} {'Name':<28} {'Cost':>6} {'Return':>8} "
          f"{'Ratio':>7}")
    print("-" * 65)
    for item in items[:10]:
        ratio = item["Return"] / item["Cost"]
        print(f"{item['Investment_ID']:<10} {item['Name']:<28} "
              f"{item['Cost']:>6} {item['Return']:>8}  {ratio:>7.2f}")
    print("  ... (showing first 10 of 120)")
