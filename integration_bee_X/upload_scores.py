import sys
import csv

if len(sys.argv) < 3:
    print("Usage: python upload_scores.py <add> <team_name>")
    sys.exit(1)

try:
    add = float(sys.argv[1])
except ValueError:
    print("Error: <add> must be a number")
    sys.exit(1)

team_name = ' '.join(sys.argv[2:])

# Read the CSV file
rows = []
found = False
try:
    with open('absolute_scores.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[0] == team_name:
                row[1] = str(float(row[1]) + add)
                found = True
            rows.append(row)
except FileNotFoundError:
    print("Error: absolute_scores.csv not found")
    sys.exit(1)

if not found:
    print(f"Error: Team '{team_name}' not found in absolute_scores.csv")
    sys.exit(1)

# Write back to the CSV file
with open('absolute_scores.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

print(f"Updated score for team '{team_name}' by adding {add}")