import json
import random

# Passenger numbers:
RANDOM_NUM = True
MAX_NUM = 200
MIN_TIME = 1.0
MAX_TIME = 5.0

# reset
RESET_MIN_TIME = 1.0
RESET_MAX_TIME = 50.0
RESET_TIMES = 12

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
        # from_floor = 1
        # to_floor = random.randint(MIN_FLOOR, MAX_FLOOR)
        from_floor = random.randint(MIN_FLOOR, MAX_FLOOR)
        to_floor = random.randint(MIN_FLOOR, MAX_FLOOR)
        while to_floor == from_floor:
            to_floor = random.randint(MIN_FLOOR, MAX_FLOOR)
        passenger_id = random.choice(list(self.IDset))
        self.IDset.remove(passenger_id)
        time = random.uniform(MIN_TIME, MAX_TIME)
        return Passenger(from_floor, to_floor, passenger_id, time)

    def generate_resets(self):
        for i in range(1, 7):
            capacity = random.choice(self.capacity_list)
            move_time = random.choice(self.move_time_list)
            times = RESET_TIMES
            interval = (RESET_MAX_TIME - RESET_MIN_TIME) // times
            times = (RESET_MAX_TIME - RESET_MIN_TIME) // 0.4 if interval < 0.4 else times
            interval = (RESET_MAX_TIME - RESET_MIN_TIME) // times
            for j in range(times):
                reset = Reset(RESET_MIN_TIME + interval * j, i, capacity, move_time)
                self.resets.add(reset)
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


def main():
    generator = Generate()
    items = generator.items
    for item in items:
        print(item.get_request())
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

