import csv
import sys
from collections import Counter, defaultdict
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

print("Connecting Spotify and Daily Household Transactions...")

# Load Daily Household Transactions
with open('dataset/Daily Household Transactions.csv', 'r', encoding='utf-8', errors='replace') as f:
    daily = list(csv.DictReader(f))

def parse_daily_date(d_str):
    d_str = d_str.strip()
    for fmt in ('%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(d_str, fmt)
        except ValueError:
            pass
    return None

daily_by_date = defaultdict(list)
for r in daily:
    dt = parse_daily_date(r['Date'])
    if dt:
        d_key = dt.strftime('%Y-%m-%d')
        daily_by_date[d_key].append({**r, 'dt': dt})

print(f"Daily transaction unique days: {len(daily_by_date)}")

# Let's inspect Spotify streams on those exact days
spotify_on_daily_days = defaultdict(list)
total_spotify_matched = 0

with open('dataset/spotify_history.csv', 'r', encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    for r in reader:
        ts = r.get('ts', '')
        if not ts:
            continue
        d_key = ts[:10]
        if d_key in daily_by_date:
            total_spotify_matched += 1
            if len(spotify_on_daily_days[d_key]) < 20: # keep sample
                spotify_on_daily_days[d_key].append(r)

print(f"Total Spotify streams on days with receipts: {total_spotify_matched}")
print(f"Number of receipt days that have Spotify listening: {len(spotify_on_daily_days)} / {len(daily_by_date)}")

# Check some special days:
special_dates = [
    ('2015-03-03', 'Dentist / Root Canal day'),
    ('2015-10-07', 'Kindle + gift wrap purchase'),
    ('2016-11-03', 'Birthday celebration day (cake + letters)'),
    ('2016-10-31', 'Bhaiduj / Mi band 5'),
    ('2017-08-05', 'Rakshabandhan purse shopping'),
    ('2018-09-16', 'Ganesh Pujan idol purchase'),
    ('2018-09-19', 'Netflix subscription renewed')
]

for d_key, desc in special_dates:
    receipts = daily_by_date.get(d_key, [])
    streams = spotify_on_daily_days.get(d_key, [])
    print(f"\n==================== {d_key}: {desc} ====================")
    print(f"Receipts ({len(receipts)}):")
    for rc in receipts:
        print(f"  - [{rc['Category']}/{rc['Subcategory']}] ₹{rc['Amount']} | {rc['Note']} (Mode: {rc['Mode']})")
    print(f"Spotify Streams ({len(streams)} recorded, showing up to 5):")
    for s in streams[:5]:
        print(f"  - {s['ts']} | {s['track_name']} by {s['artist_name']} ({s['platform']}, ms: {s['ms_played']})")
