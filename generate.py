import json
import random

# Passenger numbers:
'''
request max num, max time and min time
if want to generate random numbers of requests, set true(default: request_num = max_num)
'''
RANDOM_NUM = False
MAX_NUM = 64
MIN_TIME = 5.0
MAX_TIME = 5.0
RANDOM_FLOOR = False
FROM_FLOOR = 11
TO_FLOOR = 1

# reset
'''
reset min time, normal reset times and intervals between two requests in ONE elevator
'''
RESET_MIN_TIME = 2.0
RESET_TIMES = 0
INTERVAL_MAX = 8.0
INTERVAL_MIN = 4.0
RANDOM_CHANGE_FLOOR = True
CHANGE_FLOOR = [9, 9, 9, 9, 9, 9]

MAX_FLOOR = 11
MIN_FLOOR = 1
CAPACITY = 6
MIN_ELEVATOR_ID = 1
MAX_ELEVATOR_ID = 1

PATH = '.'


class Generate:
    def __init__(self):
        self.IDset = set(range(1, 10001))
        self.numbers = random.randint(1, MAX_NUM) if RANDOM_NUM else MAX_NUM
        self.capacity_list = [3, 4, 5, 6, 7, 8]
        self.move_time_list = [0.2, 0.3, 0.4, 0.5, 0.6]
        self.passengers = set()
        self.resets = set()
        self.generate_passengers()
        self.generate_resets()
        self.items = []
        self.merge()

    def generate_passengers(self):
        for i in range(self.numbers):
            self.passengers.add(self.generate_one_passenger())
        self.passengers = list(self.passengers)

    def generate_one_passenger(self):
        # from_floor = random.randint(1, 3)
        # to_floor = random.randint(9, 11)
        from_floor = random.randint(MIN_FLOOR, MAX_FLOOR) if RANDOM_FLOOR else FROM_FLOOR
        to_floor = random.randint(MIN_FLOOR, MAX_FLOOR) if RANDOM_FLOOR else TO_FLOOR
        while to_floor == from_floor:
            to_floor = random.randint(MIN_FLOOR, MAX_FLOOR)
        passenger_id = random.choice(list(self.IDset))
        self.IDset.remove(passenger_id)
        time = random.uniform(MIN_TIME, MAX_TIME)
        return Passenger(from_floor, to_floor, passenger_id, time)

    def generate_resets(self):
        for i in range(1, 7):
            time = RESET_MIN_TIME - random.uniform(INTERVAL_MIN, INTERVAL_MIN + 1)
            for j in range(RESET_TIMES):
                time = time + random.uniform(INTERVAL_MIN, INTERVAL_MAX)
                capacity = random.choice(self.capacity_list)
                move_time = random.choice(self.move_time_list)
                reset = Reset(time, i, capacity, move_time)
                self.resets.add(reset)
            time = time + random.uniform(INTERVAL_MIN, INTERVAL_MAX)
            capacity = random.choice(self.capacity_list)
            move_time = random.choice(self.move_time_list)
            floor = CHANGE_FLOOR[i - 1] if RANDOM_CHANGE_FLOOR else random.randint(3, 9)
            self.resets.add(DCReset(time, i, capacity, move_time, floor))
        self.resets = list(self.resets)

    def merge(self):
        self.items = self.passengers + self.resets
        self.items = sorted(self.items, key=lambda p: p.time)


class Passenger:
    def __init__(self, from_floor, to_floor, passenger_id, time):
        self.from_floor = from_floor
        self.to_floor = to_floor
        self.passenger_id = passenger_id
        self.time = time

    def get_request(self):
        return f"[{self.time:.1f}]{self.passenger_id}-FROM-{self.from_floor}-TO-{self.to_floor}"

    def to_dict(self):
        passenger_dict = {'time': self.time, 'from_floor': self.from_floor, 'to_floor': self.to_floor,
                          'passenger_id': self.passenger_id}
        return passenger_dict


class Reset:
    def __init__(self, time, elevator_id, capacity, move_time):
        self.time = time
        self.elevator_id = elevator_id
        self.capacity = capacity
        self.move_time = move_time

    def get_request(self):
        return (f"[{self.time:.1f}]RESET-Elevator-{self.elevator_id}-"
                f"{self.capacity}-{self.move_time}")


class DCReset:
    def __init__(self, time, elevator_id, capacity, move_time, floor):
        self.time = time
        self.elevator_id = elevator_id
        self.capacity = capacity
        self.move_time = move_time
        self.floor = floor

    def get_request(self):
        return (f"[{self.time:.1f}]RESET-DCElevator-{self.elevator_id}-{self.floor}-"
                f"{self.capacity}-{self.move_time}")


def main():
    generator = Generate()
    items = generator.items
    with open(PATH + '/stdin.txt', 'w') as file:
        for item in items:
            file.write(item.get_request())
            file.write('\n')
    with open(PATH + '/passengers.json', 'w') as file:
        passengers_list = []
        for item in items:
            if isinstance(item, Passenger):
                passenger = item
                passengers_list.append(passenger.to_dict())
        json.dump(passengers_list, file, indent=4)


main()

