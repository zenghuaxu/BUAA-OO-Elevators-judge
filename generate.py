import json
import random


MAX_FLOOR = 11
MIN_FLOOR = 1
CAPACITY = 6
MIN_ELEVATOR_ID = 1
MAX_ELEVATOR_ID = 6
PATH = '.'


class Generate:
    def __init__(self):
        self.IDset = set(range(1, 10001))
        self.numbers = 2000
        self.passengers = set()
        self.generate_passengers()

    def generate_passengers(self):
        for i in range(self.numbers):
            self.passengers.add(self.generate_one_passenger())
        self.passengers = sorted(list(self.passengers), key=lambda p: p.time)

    def generate_one_passenger(self):
        from_floor = random.randint(MIN_FLOOR, MAX_FLOOR)
        to_floor = random.randint(MIN_FLOOR, MAX_FLOOR)
        while to_floor == from_floor:
            to_floor = random.randint(MIN_FLOOR, MAX_FLOOR)
        passenger_id = random.choice(list(self.IDset))
        self.IDset.remove(passenger_id)
        elevator_id = random.randint(MIN_ELEVATOR_ID, MAX_ELEVATOR_ID)
        time = random.uniform(1, 10)
        return Passenger(from_floor, to_floor, passenger_id, elevator_id, time)


class Passenger:
    def __init__(self, from_floor, to_floor, passenger_id, elevator_id, time):
        self.from_floor = from_floor
        self.to_floor = to_floor
        self.passenger_id = passenger_id
        self.elevator_id = elevator_id
        self.time = time

    def get_request(self):
        return f"[{self.time:.1f}]{self.passenger_id}-FROM-{self.from_floor}-TO-{self.to_floor}-BY-{self.elevator_id}"

    def to_dict(self):
        passenger_dict = {'time': self.time, 'from_floor': self.from_floor, 'to_floor': self.to_floor,
                          'passenger_id': self.passenger_id, 'elevator_id': self.elevator_id}
        return passenger_dict


def main():
    generator = Generate()
    passengers = generator.passengers
    with open(PATH + '/stdin.txt', 'w') as file:
        for passenger in passengers:
            file.write(passenger.get_request())
            file.write('\n')
    with open(PATH + '/passengers.json', 'w') as file:
        passengers_list = []
        for passenger in passengers:
            passengers_list.append(passenger.to_dict())
        json.dump(passengers_list, file, indent=4)


main()
