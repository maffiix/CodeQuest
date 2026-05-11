import json
import sys
from datetime import datetime

data = {}
lines = [line.strip() for line in sys.stdin if line.strip()]

for line in lines:
    if ':' not in line:
        continue
    # Разделяем по первому двоеточию
    parts = line.split(':', 1)
    key = parts[0].strip()
    value = parts[1].strip()
    
    if key == 'ABBR':
        data['ABBR'] = value
    elif key == 'Name':
        data['Name'] = value
    elif key == 'CrDat':
        try:
            datetime.strptime(value, '%Y/%m/%d')
            data['CrDat'] = value
        except ValueError:
            print('WARING: INCORRECT DATE INPUT')
            data['CrDat'] = 'N/A'
    elif key == 'Type':
        data['Type'] = value
    else:
        data[key] = value

for key in ['ABBR', 'Name', 'CrDat', 'Type']:
    if key not in data:
        data[key] = 'N/A'

if data['Name'] == 'N/A':
    filename = "unnamed.json"
else:
    filename = f"{data['Name']}.json"

with open(filename, 'w') as f:
    json.dump(data, f, indent=2)

print(f"> {filename}")