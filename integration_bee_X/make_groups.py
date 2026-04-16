import random
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- AUTH (same as your setup) ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "path/to/your/service-account.json", scope
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

for i, size in enumerate(group_sizes):
    group = teams[idx:idx+size]
    groups.append(group)
    idx += size

# --- EXPORT CSV ---
with open("groups.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    for i, group in enumerate(groups, start=1):
        writer.writerow([f"Group {i}"])
        writer.writerow(["Team Name", "Member 1", "Member 2"])

        for team, m1, m2 in group:
            writer.writerow([team, m1, m2])

        writer.writerow([])  # blank line between groups

print("groups.csv generated")