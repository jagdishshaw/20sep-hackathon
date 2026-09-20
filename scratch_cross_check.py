import csv
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

print("Checking cross-dataset links...")

with open('dataset/Daily Household Transactions.csv', 'r', encoding='utf-8', errors='replace') as f:
    daily = list(csv.DictReader(f))

with open('dataset/Augmented_IndiaTransactMultiFacet2024.csv', 'r', encoding='utf-8', errors='replace') as f:
    aug = list(csv.DictReader(f))

print(f"Daily rows: {len(daily)}, Augmented rows: {len(aug)}")

# Check dates overlap
daily_dates = [r['Date'].split()[0] for r in daily if r['Date']]
aug_dates = [r['trans_date_trans_time'].split()[0] for r in aug if r['trans_date_trans_time']]

print(f"Daily dates sample: {daily_dates[:3]} to {daily_dates[-3:]}")
print(f"Augmented dates sample: {aug_dates[:3]} to {aug_dates[-3:]}")

# Check if any text/merchant/note matches
aug_merchants = set(r['merchant'] for r in aug if r['merchant'])
print(f"Unique aug merchants: {len(aug_merchants)}")
sample_merchants = list(aug_merchants)[:10]
print("Sample aug merchants:", sample_merchants)

# Check if 'fraud_' prefix is on all merchants in aug
fraud_merch = [m for m in aug_merchants if m.startswith('fraud_')]
print(f"Merchants starting with fraud_: {len(fraud_merch)} / {len(aug_merchants)}")

# Check customer profiles in aug
print("\nAugmented dataset profile:")
jobs = Counter(r['job'] for r in aug if r['job'])
print("Top jobs in aug:", jobs.most_common(5))
cities = Counter(r['city'] for r in aug if r['city'])
print("Top cities in aug:", cities.most_common(5))
