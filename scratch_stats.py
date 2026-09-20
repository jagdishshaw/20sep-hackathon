import csv
import sys
import json
from collections import Counter, defaultdict
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# 1. Detailed analysis of Daily Household Transactions
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

for r in daily:
    r['dt'] = parse_date(r['Date'])
    r['amt'] = float(r['Amount']) if r['Amount'] else 0.0

daily.sort(key=lambda x: x['dt'])

print(f"Total transactions: {len(daily)}")
print(f"First txn: {daily[0]['dt']} - {daily[0]['Note']} (₹{daily[0]['amt']})")
print(f"Last txn: {daily[-1]['dt']} - {daily[-1]['Note']} (₹{daily[-1]['amt']})")

# Aggregates by Type
totals_by_type = defaultdict(float)
counts_by_type = Counter()
for r in daily:
    totals_by_type[r['Income/Expense']] += r['amt']
    counts_by_type[r['Income/Expense']] += 1

print("\nIncome/Expense Totals:")
for t, total in totals_by_type.items():
    print(f"  {t}: ₹{total:,.2f} across {counts_by_type[t]} txns")

# Salary breakdown by year
salaries_by_year = defaultdict(list)
for r in daily:
    if r['Category'] == 'Salary':
        salaries_by_year[r['dt'].year].append(r['amt'])

print("\nSalaries by year:")
for y, sals in sorted(salaries_by_year.items()):
    print(f"  {y}: {len(sals)} months, total ₹{sum(sals):,.2f}, avg ₹{sum(sals)/len(sals):,.2f}, min ₹{min(sals):,.2f}, max ₹{max(sals):,.2f}")

# Yearly spending breakdown
spending_by_year = defaultdict(float)
for r in daily:
    if r['Income/Expense'] == 'Expense':
        spending_by_year[r['dt'].year] += r['amt']

print("\nExpense spending by year:")
for y, exp in sorted(spending_by_year.items()):
    print(f"  {y}: ₹{exp:,.2f}")

# Investments breakdown
inv_by_year = defaultdict(float)
for r in daily:
    if 'Mutual Fund' in r['Category'] or r['Category'] in ('Investment', 'Public Provident Fund', 'Recurring Deposit', 'Fixed Deposit', 'Small Cap fund 2', 'Small cap fund 1', 'Share Market'):
        inv_by_year[r['dt'].year] += r['amt']

print("\nInvestments by year:")
for y, amt in sorted(inv_by_year.items()):
    print(f"  {y}: ₹{amt:,.2f}")

# Top food items
food_items = Counter()
for r in daily:
    if r['Category'] == 'Food' and r['Note']:
        food_items[r['Note'].lower()] += 1

print("\nTop 15 Food notes:")
for item, cnt in food_items.most_common(15):
    print(f"  {item}: {cnt}")

# Transportation routes
routes = Counter()
for r in daily:
    if r['Category'] == 'Transportation' and r['Note']:
        routes[r['Note']] += 1

print("\nTop 15 Transportation routes:")
for rt, cnt in routes.most_common(15):
    print(f"  {rt}: {cnt}")

# Medical events
meds = [r for r in daily if r['Category'] == 'Health']
print(f"\nTotal Health transactions: {len(meds)}, Total spent: ₹{sum(r['amt'] for r in meds):,.2f}")
# Medical clusters:
med_months = Counter(r['dt'].strftime('%Y-%m') for r in meds)
print("Top medical months:")
for m, cnt in med_months.most_common(5):
    print(f"  {m}: {cnt} visits/medicines")
