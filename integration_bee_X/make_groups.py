import random
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import io
import requests

# --- AUTH (same as your setup) ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "C:/Users/raula/Downloads/vocal-unfolding-472611-k1-aa03d0f758cf.json", scope
)
client = gspread.authorize(creds)

# --- LOAD SHEET ---
SPREADSHEET_ID = "1e1S-HuM-6Dy0nxopEc7be8SIsMK-GedcoqHmfu1pyLQ"
sheet = client.open_by_key(SPREADSHEET_ID).get_worksheet_by_id(438147461)

data = sheet.get_all_records()

# --- EXTRACT TEAMS ---
teams = []

for row in data:
    team = row.get("Team Name", "").strip()
    m1 = row.get("Member 1 Name", "").strip()
    m2 = row.get("Member 2 Name", "").strip()

    # skip completely empty rows
    if team or m1 or m2:
        teams.append((team, m1, m2))

# --- SHUFFLE ---
random.shuffle(teams)

# --- GROUPING FUNCTION ---
def split_groups(teams):
    n = len(teams)

    # Try combinations of group sizes 3–5 to minimize imbalance
    best = None

    for g5 in range(n // 5 + 1):
        for g4 in range(n // 4 + 1):
            for g3 in range(n // 3 + 1):
                total = 5*g5 + 4*g4 + 3*g3
                if total == n:
                    groups = [5]*g5 + [4]*g4 + [3]*g3
                    imbalance = max(groups) - min(groups) if groups else 0

                    if best is None or imbalance < best[0]:
                        best = (imbalance, groups)

    # fallback: all groups of 4 if no exact match
    if best is None:
        size = 4
        groups = [size] * (n // size)
        if n % size:
            groups.append(n % size)
    else:
        groups = best[1]

    return groups

group_sizes = split_groups(teams)

# --- BUILD GROUPS ---
groups = []
idx = 0

for size in group_sizes:
    group = teams[idx:idx+size]
    groups.append(group)
    idx += size

# --- EXPORT JSON (optional, can remove later) ---
groups_data = []
for i, group in enumerate(groups, start=1):
    group_dict = {
        "group_id": i,
        "teams": [
            {"team_name": team, "member1": m1, "member2": m2}
            for team, m1, m2 in group
        ]
    }
    groups_data.append(group_dict)

with open("groups.json", "w", encoding="utf-8") as f:
    json.dump(groups_data, f, indent=4)

print("groups.json generated")

# --- PREPARE DATA FOR GOOGLE SHEET ---
rows = []

for group_id, group in enumerate(groups, start=1):
    for team, m1, m2 in group:
        rows.append([group_id, team, m1, m2, 0])  # score starts at 0

# --- UPLOAD TO GOOGLE SHEET ---
SCORE_SHEET_ID = "1pyNcvwS60H6ixJGHHkiwTbyfR4Fy1jONKxUmaZjfeZ0"
score_sheet = client.open_by_key(SCORE_SHEET_ID).worksheet("Sheet1")

score_sheet.clear()

# header
score_sheet.append_row(["group", "team", "member1", "member2", "score"])

# bulk upload (FASTER than loop)
score_sheet.append_rows(rows)

print("Google Sheet updated")

# --- OPTIONAL: EXPORT LOCAL CSV ---
with open("absolute_scores.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["group", "team", "member1", "member2", "score"])
    writer.writerows(rows)

print("absolute_scores.csv generated")