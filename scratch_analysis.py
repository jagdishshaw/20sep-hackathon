import csv
import json
from collections import Counter, defaultdict
from datetime import datetime

print("==================================================")
print("EXPLORING ALL THREE DATASETS")
print("==================================================")

# 1. Augmented_IndiaTransactMultiFacet2024
with open('dataset/Augmented_IndiaTransactMultiFacet2024.csv', 'r', encoding='utf-8', errors='replace') as f:
    rows_aug = list(csv.DictReader(f))

print(f"\n[Augmented_IndiaTransactMultiFacet2024] Total rows: {len(rows_aug)}")
years_aug = Counter()
cats_aug = Counter()
cust_tx = Counter()
cust_info = defaultdict(dict)

for r in rows_aug:
    dt = r.get('trans_date_trans_time', '').strip()
    if dt and '/' in dt:
        parts = dt.split('/')
        if len(parts) >= 3:
            y = parts[2].split()[0]
            years_aug[y] += 1
    cats_aug[r.get('category', '')] += 1
    cid = r.get('customer_id')
    if cid:
        cust_tx[cid] += 1
        if 'name' not in cust_info[cid]:
            cust_info[cid]['name'] = f"{r.get('first', '')} {r.get('last', '')}".strip()
            cust_info[cid]['job'] = r.get('job', '')
            cust_info[cid]['city'] = r.get('city', '')
            cust_info[cid]['state'] = r.get('state', '')

print("Years in Augmented:", sorted(years_aug.items()))
print("Categories in Augmented:", cats_aug)
print("Top customers in Augmented:")
for cid, cnt in cust_tx.most_common(5):
    print(f"  {cid}: {cnt} txns | {cust_info[cid]}")

# Check if any customer has a large receipt life
print(f"Total unique customers: {len(cust_tx)}")
print(f"Max txns for single customer: {cust_tx.most_common(1)}")

# 2. Daily Household Transactions
with open('dataset/Daily Household Transactions.csv', 'r', encoding='utf-8', errors='replace') as f:
    rows_daily = list(csv.DictReader(f))

print(f"\n[Daily Household Transactions] Total rows: {len(rows_daily)}")
modes_daily = Counter(r['Mode'] for r in rows_daily)
types_daily = Counter(r['Income/Expense'] for r in rows_daily)
cats_daily = Counter(r['Category'] for r in rows_daily)
subcats_daily = Counter(r['Subcategory'] for r in rows_daily)
print("Modes:", modes_daily)
print("Types:", types_daily)
print("Top 15 Categories:", cats_daily.most_common(15))
print("Top 15 Subcategories:", subcats_daily.most_common(15))

# 3. Spotify History
with open('dataset/spotify_history.csv', 'r', encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    spotify_total = 0
    spotify_years = Counter()
    spotify_top_artists = Counter()
    for r in reader:
        spotify_total += 1
        ts = r.get('ts', '')
        if ts:
            spotify_years[ts[:4]] += 1
        art = r.get('artist_name')
        if art:
            spotify_top_artists[art] += 1

print(f"\n[Spotify History] Total rows: {spotify_total}")
print("Streams by year:", sorted(spotify_years.items()))
print("Top 15 Artists overall:", spotify_top_artists.most_common(15))
