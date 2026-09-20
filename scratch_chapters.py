import csv
import sys
from collections import Counter, defaultdict
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

with open('dataset/Daily Household Transactions.csv', 'r', encoding='utf-8', errors='replace') as f:
    daily = list(csv.DictReader(f))

def parse_date(d_str):
    d_str = d_str.strip()
    for fmt in ('%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(d_str, fmt)
        except ValueError:
            pass
    return None

for i, r in enumerate(daily):
    r['id'] = i + 1
    r['dt'] = parse_date(r['Date'])
    r['amt'] = float(r['Amount']) if r['Amount'] else 0.0

daily.sort(key=lambda x: x['dt'])

print("=== CHAPTER 1: Finding Footing & The Root Canal Trial (Early 2015: Jan - Apr 2015) ===")
ch1 = [r for r in daily if datetime(2015, 1, 1) <= r['dt'] <= datetime(2015, 4, 30)]
print(f"Count: {len(ch1)}, Total spent: ₹{sum(r['amt'] for r in ch1 if r['Income/Expense']=='Expense'):,.2f}")
ch1_med = [r for r in ch1 if r['Category'] == 'Health']
print(f"Health events in Ch1: {len(ch1_med)} items, ₹{sum(r['amt'] for r in ch1_med):,.2f}")
for r in ch1_med:
    print(f"  {r['dt'].strftime('%Y-%m-%d')}: ₹{r['amt']} - {r['Note']}")

print("\n=== CHAPTER 2: The Commute & Independent Household (Mid-to-Late 2015: May - Dec 2015) ===")
ch2 = [r for r in daily if datetime(2015, 5, 1) <= r['dt'] <= datetime(2015, 12, 31)]
print(f"Count: {len(ch2)}, Total spent: ₹{sum(r['amt'] for r in ch2 if r['Income/Expense']=='Expense'):,.2f}")
ch2_transport = [r for r in ch2 if r['Category'] == 'Transportation']
print(f"Transport events in Ch2: {len(ch2_transport)} items")

print("\n=== CHAPTER 3: Family Duty, Exam Aspirations & Festivities (2016: Jan - Dec 2016) ===")
ch3 = [r for r in daily if datetime(2016, 1, 1) <= r['dt'] <= datetime(2016, 12, 31)]
print(f"Count: {len(ch3)}, Total spent: ₹{sum(r['amt'] for r in ch3 if r['Income/Expense']=='Expense'):,.2f}")
ch3_fam = [r for r in ch3 if r['Category'] in ('Family', 'Gift', 'Festivals')]
print(f"Family/Festivals/Gifts in Ch3: {len(ch3_fam)} items, ₹{sum(r['amt'] for r in ch3_fam):,.2f}")
for r in ch3_fam[:10]:
    print(f"  {r['dt'].strftime('%Y-%m-%d')}: ₹{r['amt']} [{r['Category']}] - {r['Note']}")

print("\n=== CHAPTER 4: Financial Ascendance & Serious Wealth Building (2017: Jan - Dec 2017) ===")
ch4 = [r for r in daily if datetime(2017, 1, 1) <= r['dt'] <= datetime(2017, 12, 31)]
print(f"Count: {len(ch4)}, Total spent: ₹{sum(r['amt'] for r in ch4 if r['Income/Expense']=='Expense'):,.2f}")
ch4_inv = [r for r in ch4 if 'Mutual Fund' in r['Category'] or r['Category'] in ('Investment', 'Public Provident Fund', 'Recurring Deposit', 'Fixed Deposit')]
print(f"Investments in Ch4: {len(ch4_inv)} txns, ₹{sum(r['amt'] for r in ch4_inv):,.2f}")

print("\n=== CHAPTER 5: Digital Maturity & The Modern Lifestyle (2018: Jan - Sep 2018) ===")
ch5 = [r for r in daily if datetime(2018, 1, 1) <= r['dt'] <= datetime(2018, 9, 30)]
print(f"Count: {len(ch5)}, Total spent: ₹{sum(r['amt'] for r in ch5 if r['Income/Expense']=='Expense'):,.2f}")
ch5_sub = [r for r in ch5 if r['Category'] == 'subscription' or r['Mode'] in ('Credit Card', 'Gpay Reward')]
print(f"Digital / Subscriptions / Cards in Ch5: {len(ch5_sub)} txns")
