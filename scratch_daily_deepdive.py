import csv
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

print("==================================================")
print("DEEP DIVE: Daily Household Transactions")
print("==================================================")

with open('dataset/Daily Household Transactions.csv', 'r', encoding='utf-8', errors='replace') as f:
    daily_rows = list(csv.DictReader(f))

# Let's inspect all fields, missing values, formats
print(f"Total rows: {len(daily_rows)}")
columns = list(daily_rows[0].keys())
print("Columns:", columns)

missing_counts = {col: 0 for col in columns}
for r in daily_rows:
    for col in columns:
        if not r[col].strip():
            missing_counts[col] += 1
print("Missing counts by column:", missing_counts)

# Let's look at all Categories & their Income/Expense breakdown
cat_summary = defaultdict(lambda: {'count': 0, 'total_amt': 0.0, 'subcats': Counter()})
for r in daily_rows:
    cat = r['Category'].strip()
    amt = float(r['Amount']) if r['Amount'] else 0.0
    sub = r['Subcategory'].strip()
    cat_summary[cat]['count'] += 1
    cat_summary[cat]['total_amt'] += amt
    if sub:
        cat_summary[cat]['subcats'][sub] += 1

print("\n--- CATEGORY BREAKDOWN ---")
for cat, data in sorted(cat_summary.items(), key=lambda x: x[1]['total_amt'], reverse=True):
    sub_top = ", ".join([f"{s}({c})" for s, c in data['subcats'].most_common(3)])
    print(f"[{cat}] {data['count']} txns | Total: ₹{data['total_amt']:,.2f} | Subcats: {sub_top or 'None'}")

# Chronological sorting & timeline analysis
def parse_date(d_str):
    d_str = d_str.strip()
    for fmt in ('%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(d_str, fmt)
        except ValueError:
            pass
    return None

daily_rows_parsed = []
for r in daily_rows:
    dt = parse_date(r['Date'])
    amt = float(r['Amount']) if r['Amount'] else 0.0
    daily_rows_parsed.append({**r, 'parsed_dt': dt, 'amt_float': amt})

# Sort ascending by date
daily_rows_parsed.sort(key=lambda x: x['parsed_dt'] if x['parsed_dt'] else datetime.min)

print(f"\nEarliest: {daily_rows_parsed[0]['parsed_dt']} | Note: {daily_rows_parsed[0]['Note']} | Amt: {daily_rows_parsed[0]['Amount']}")
print(f"Latest: {daily_rows_parsed[-1]['parsed_dt']} | Note: {daily_rows_parsed[-1]['Note']} | Amt: {daily_rows_parsed[-1]['Amount']}")

# Let's see life milestones:
# 1. Salary history (dates, amounts)
salaries = [r for r in daily_rows_parsed if r['Category'] == 'Salary']
print(f"\n--- SALARY MILESTONES ({len(salaries)} records) ---")
for s in salaries[:10]:
    print(f"  {s['parsed_dt'].strftime('%Y-%m-%d')}: ₹{s['amt_float']:,.0f} | Note: {s['Note']} | Mode: {s['Mode']}")
if len(salaries) > 10:
    print("  ...")
    for s in salaries[-5:]:
        print(f"  {s['parsed_dt'].strftime('%Y-%m-%d')}: ₹{s['amt_float']:,.0f} | Note: {s['Note']} | Mode: {s['Mode']}")

# 2. Rent history (dates, amounts)
rents = [r for r in daily_rows_parsed if r['Category'] == 'Rent']
print(f"\n--- RENT HISTORY ({len(rents)} records) ---")
for r in rents:
    print(f"  {r['parsed_dt'].strftime('%Y-%m-%d')}: ₹{r['amt_float']:,.0f} | Note: {r['Note']}")

# 3. Places and Commutes
place_mentions = defaultdict(list)
for r in daily_rows_parsed:
    note = r['Note']
    found_places = re.findall(r'Place\s*\d+|Permanent Residence', note, re.IGNORECASE)
    for p in set(found_places):
        place_mentions[p.title()].append(r)

print(f"\n--- PLACES MENTIONED ---")
for p, txns in sorted(place_mentions.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"  {p}: {len(txns)} transactions (e.g., {[t['Note'] for t in txns[:3]]})")

# 4. Family & People mentions
print("\n--- PEOPLE / FAMILY MENTIONS ---")
family_txns = [r for r in daily_rows_parsed if r['Category'] in ('Family', 'Gift') or any(w in r['Note'].lower() for w in ['mother', 'mom', 'father', 'dad', 'brother', 'sister', 'aunt', 'uncle', 'friend', 'bhai', 'didi', 'bhabhi'])]
print(f"Total family/people related txns: {len(family_txns)}")
for r in family_txns[:15]:
    print(f"  {r['parsed_dt'].strftime('%Y-%m-%d')}: ₹{r['amt_float']:,.0f} | Cat: {r['Category']}/{r['Subcategory']} | Note: {r['Note']}")

# 5. Festivals & Celebrations
festivals = [r for r in daily_rows_parsed if r['Category'] == 'Festivals' or any(w in r['Note'].lower() for w in ['diwali', 'ganesh', 'holi', 'eid', 'rakhi', 'raksha', 'navratri', 'puja', 'pujan', 'celebration', 'birthday'])]
print(f"\n--- FESTIVALS & CELEBRATIONS ({len(festivals)} records) ---")
for r in festivals:
    print(f"  {r['parsed_dt'].strftime('%Y-%m-%d')}: ₹{r['amt_float']:,.0f} | Note: {r['Note']}")

# 6. Medical / Health
health_txns = [r for r in daily_rows_parsed if r['Category'] == 'Health' or any(w in r['Note'].lower() for w in ['hospital', 'doctor', 'medicine', 'dr.', 'clinic', 'dentist', 'blood', 'test', 'fever'])]
print(f"\n--- HEALTH / MEDICAL ({len(health_txns)} records) ---")
for r in health_txns[:15]:
    print(f"  {r['parsed_dt'].strftime('%Y-%m-%d')}: ₹{r['amt_float']:,.0f} | Note: {r['Note']}")

# 7. Subscriptions & Tech / Lifestyle
subs = [r for r in daily_rows_parsed if r['Category'] == 'subscription' or any(w in r['Note'].lower() for w in ['netflix', 'spotify', 'hbr', 'amazon', 'prime', 'tata play', 'tata sky', 'recharge', 'data', 'broadband', 'internet'])]
print(f"\n--- SUBSCRIPTIONS & TECH ({len(subs)} records) ---")
for r in subs[:15]:
    print(f"  {r['parsed_dt'].strftime('%Y-%m-%d')}: ₹{r['amt_float']:,.0f} | Note: {r['Note']}")
