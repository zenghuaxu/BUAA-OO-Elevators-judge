import json
import re

PATH = '.'


with open(PATH + '/stdin.txt', 'r') as file:
    pattern = r'\[(\d+\.\d+)\](\d+)-FROM-(\d+)-TO-(\d+)'
    passengers = []
    for line in file:
        match = re.match(pattern, line)
        if match:
            time = float(match.group(1))
            passenger_id = int(match.group(2))
            from_floor = int(match.group(3))
            to_floor = int(match.group(4))
            passenger = {"time": time,
                         "from_floor": from_floor,
                         "to_floor": to_floor,
                         "passenger_id": passenger_id
                         }
            passengers.append(passenger)

with open(PATH + '/passengers.json', 'w') as file:
    json.dump(passengers, file, indent=4)

