import json
from enum import Enum
import re

EPSILON = -1e-9

MAX_FLOOR = 11
MIN_FLOOR = 1
MIN_ELEVATOR_ID = 1
MAX_ELEVATOR_ID = 6
PATH = '.'


class ElevatorState(Enum):
    PARKING = 1
    OPENED = 2
    RESETTING = 3


class BehaviorType(Enum):
    ARRIVE = 1
    OPEN = 2
    CLOSE = 3
    IN = 4
    OUT = 5
    RECEIVE = 6
    RESET = 7


class CustomError(Exception):
    pass


class Elevator:
    def __init__(self, elevator_id):
        self.reset_accept_time = 0
        self.passengers = set()
        self.cur_floor = 1
        self.last_behavior_time = 0
        self.elevator_id = elevator_id
        self.state = ElevatorState.PARKING
        self.capacity = 6
        self.move_time = 0.4
        self.expect_capacity = 6
        self.expect_move_time = 0.4
        self.passenger_list = []
        self.arrive_count = 0
        self.reset_ready = False

    def check(self, behavior_type, time, floor, passenger, capacity, move_time):
        if time < self.last_behavior_time:
            raise CustomError(f"时空倒流 From {self.last_behavior_time} To {time}")
        if behavior_type == 'OPEN':
            self.open(floor, time)
        elif behavior_type == 'OUT':
            self.exit(floor, passenger)
        elif behavior_type == 'IN':
            self.enter(floor, passenger)
        elif behavior_type == 'CLOSE':
            self.close(floor, time)
        elif behavior_type == 'ARRIVE':
            self.arrive(floor, time)
        elif behavior_type == 'RESET_ACCEPT':
            self.reset_accept(time, capacity, move_time)
        elif behavior_type == 'RESET_BEGIN':
            self.reset_begin(time)
        elif behavior_type == 'RESET_END':
            self.reset_end(time)
        elif behavior_type == 'RECEIVE':
            self.receive(passenger)
        print(self.elevator_id, behavior_type,
              f"passenger_num:{len(self.passengers)}", f"state:{self.state}")

    def arrive(self, floor, time):
        if floor == self.cur_floor:
            raise CustomError(f"还没动呢怎么就到了 At{self.cur_floor} id:{self.elevator_id}")
        if abs(floor - self.cur_floor) > 1:
            raise CustomError(f"跑了多层 From{self.cur_floor} To{floor} id:{self.elevator_id}")
        if floor < MIN_FLOOR or floor > MAX_FLOOR:
            raise CustomError(f"幽灵楼层 From{self.cur_floor} To {floor} id:{self.elevator_id}")
        if not (time - self.last_behavior_time >= self.move_time + EPSILON):
            raise CustomError(f"超速 From{self.cur_floor} To {floor} id:{self.elevator_id}")
        if self.state != ElevatorState.PARKING:
            raise CustomError(f"没关门 Elevator:{self.elevator_id} From{self.cur_floor} To {floor}")
        if len(self.passenger_list) == 0:
            raise CustomError(f"没有receive就动 id:{self.elevator_id}")
        if self.state == ElevatorState.RESETTING:
            raise CustomError(f"resetting时候乱动 id:{self.elevator_id}")
        if self.reset_ready:
            self.arrive_count += 1
        if self.arrive_count > 2:
            raise CustomError(f"未及时响应reset id:{self.elevator_id}")
        self.cur_floor = floor

    def close(self, floor, time):
        if floor != self.cur_floor:
            raise CustomError(f"电梯怎么飞到这层的？ At {self.cur_floor} OPEN:{floor} id:{self.elevator_id}")
        if not (time - self.last_behavior_time >= 0.4 + EPSILON):
            raise CustomError(f"关门太快 begin_open:{self.last_behavior_time} end_close:{time}\
            elevator_id:{self.elevator_id}")
        if self.state == ElevatorState.PARKING:
            raise CustomError(f"关过了 At{self.cur_floor} id{self.elevator_id}")
        if self.state == ElevatorState.RESETTING:
            raise CustomError(f"resetting时候乱动 id:{self.elevator_id}")
        self.state = ElevatorState.PARKING
        self.last_behavior_time = time

    def enter(self, floor, passenger):
        if floor != self.cur_floor:
            raise CustomError(f"电梯怎么飞到这层的？ At {self.cur_floor} OPEN:{floor} id:{self.elevator_id}")
        if self.state == ElevatorState.PARKING:
            raise CustomError(f"没开门！floor:{self.cur_floor} \
            Elevator_id:{self.elevator_id}\
                              id:{passenger.passenger_id}")
        if len(self.passengers) + 1 > self.capacity:
            raise CustomError(f"超载 id:{self.elevator_id}")
        if self.state == ElevatorState.RESETTING:
            raise CustomError(f"resetting时候乱动 id:{self.elevator_id}")
        if passenger not in self.passenger_list:
            print(self.passenger_list)
            raise CustomError(f"没分配到这个电梯 passenger{passenger.id} elevator_id:{self.elevator_id}")
        passenger.enter(floor, self.elevator_id)
        self.passengers.add(passenger)

    def open(self, floor, time):
        if floor != self.cur_floor:
            raise CustomError(f"电梯怎么飞到这层的？ At {self.cur_floor} OPEN:{floor} id:{self.elevator_id}")
        if self.state == ElevatorState.OPENED:
            raise CustomError(f"开过了！floor:{self.cur_floor} id:{self.elevator_id}")
        if self.state == ElevatorState.RESETTING:
            raise CustomError(f"resetting时候乱动 id:{self.elevator_id}")
        self.state = ElevatorState.OPENED
        self.last_behavior_time = time

    def exit(self, floor, passenger):
        if floor != self.cur_floor:
            raise CustomError(f"人怎么飞到这层的？ \
            At:{self.cur_floor} Exit:{floor} id:{self.elevator_id} \
                              Elevator_id:{passenger.passenger_id}")
        if self.state != ElevatorState.OPENED:
            raise CustomError(f"门没开！ \
                        At:{self.cur_floor} Exit:{floor} id:{self.elevator_id} \
                                          Elevator_id:{passenger.passenger_id}")
        if self.state == ElevatorState.RESETTING:
            raise CustomError(f"resetting时候乱动 id:{self.elevator_id}")
        for passengerInEle in self.passengers:
            if passengerInEle.id == passenger.id:
                self.passengers.remove(passenger)
                self.passenger_list.remove(passenger)
                passenger.exit(floor, self.elevator_id)
                return
        raise CustomError(f"电梯生人 \
            At:{self.cur_floor} id:{self.elevator_id} \
                              Person_id:{passenger.passenger_id}")

    def reset_accept(self, time, capacity, move_time):
        self.reset_accept_time = time
        self.expect_capacity = capacity
        self.expect_move_time = move_time
        self.reset_ready = True

    def reset_begin(self, time):
        if self.state == ElevatorState.RESETTING:
            raise CustomError(f"reset没有结束重新reset id:{self.elevator_id}")
        if self.state == ElevatorState.OPENED:
            raise CustomError(f"没关门就reset id:{self.elevator_id}")
        if len(self.passengers) != 0:
            raise CustomError(f"电梯有人就reset id：{self.elevator_id}")
        self.state = ElevatorState.RESETTING
        self.capacity = self.expect_capacity
        self.move_time = self.expect_move_time
        self.last_behavior_time = time
        self.passenger_list = []

    def reset_end(self, time):
        if not (time - self.last_behavior_time >= 1.2 + EPSILON):
            raise CustomError(f"reset太快 id:{self.elevator_id}")
        if not (time - self.reset_accept_time <= 5.0 + EPSILON):
            raise CustomError(f"reset响应太慢 id:{self.elevator_id}")
        self.state = ElevatorState.PARKING
        self.reset_ready = False
        self.arrive_count = 0

    def receive(self, passenger):
        if self.state == ElevatorState.RESETTING:
            raise CustomError(f"reset不能receive id:{self.elevator_id}")
        self.passenger_list.append(passenger)


class Passenger:
    def __init__(self, passenger_dict):
        self.time = passenger_dict['time']
        self.cur_floor = passenger_dict['from_floor']
        self.to_floor = passenger_dict['to_floor']
        self.id = passenger_dict['passenger_id']
        self.is_in_elevator = False

    def exit(self, floor, elevator_id):
        self.is_in_elevator = False
        self.cur_floor = floor

    def enter(self, floor, elevator_id):
        if self.cur_floor != floor:
            raise CustomError(f"人怎么飞到这层的？ \
                            At:{self.cur_floor} Exit:{floor} id:{self.id} \
                                              Elevator_id:{elevator_id}")
        if self.is_in_elevator:
            raise CustomError(f"进过电梯了 id:{self.id} Enter {elevator_id}")
        self.is_in_elevator = True


class Behavior:
    def __init__(self, info):
        pattern = r'\[[ ]*(\d+\.\d+)\]([A-Z]+)-(\d+-)?(\d+)-(\d+)'
        match = re.match(pattern, info)
        if match:
            self.time = float(match.group(1))
            self.behavior = match.group(2)
            if self.behavior == 'RECEIVE':
                self.passenger_id = int(match.group(4))
                self.elevator_id = int (match.group(5))
                self.floor = 1
                return
            if self.behavior == 'IN' or self.behavior == 'OUT':
                self.passenger_id = int(match.group(3)[:-1])
            elif self.behavior == 'ARRIVE' or self.behavior == 'OPEN' or self.behavior == 'CLOSE':
                self.passenger_id = 0
            else:
                print(info)
                raise CustomError("格式错误")
            self.floor = int(match.group(4))
            self.elevator_id = int(match.group(5))
            return
        pattern = r'\[[ ]*(\d+\.\d+)\]([A-Z_]+)-(\d+)-(\d+)-(\d+\.\d+)'
        match = re.match(pattern, info)
        if match:
            self.time = float(match.group(1))
            self.behavior = match.group(2)
            self.elevator_id = int(match.group(3))
            self.capacity = int(match.group(4))
            self.move_time = float(match.group(5))
            self.floor = 1
            self.passenger_id = 1
            return
        pattern = r'\[[ ]*(\d+\.\d+)\]([A-Z_]+)-(\d+)'
        match = re.match(pattern, info)
        if match:
            self.time = float(match.group(1))
            self.behavior = match.group(2)
            self.elevator_id = int(match.group(3))
            self.floor = 1
            self.passenger_id = 1


def main():
    with open(PATH + '/passengers.json', 'r') as file:
        passenger_dicts = json.load(file)
    passengers = {}
    for passenger_dict in passenger_dicts:
        passengers[passenger_dict['passenger_id']] = Passenger(passenger_dict)

    elevators = {}
    for i in range(MIN_ELEVATOR_ID, MAX_ELEVATOR_ID + 1):
        elevators[i] = Elevator(i)

    with open(PATH + '/stdout.txt', 'r', encoding='utf-8') as file:
        for info in file:
            behavior = Behavior(info)
            floor = behavior.floor
            time = behavior.time
            passenger_id = behavior.passenger_id
            elevator_id = behavior.elevator_id
            behavior_type = behavior.behavior
            passenger = 0
            capacity = 6
            move_time = 0.4
            if behavior_type == 'IN' or behavior_type == "OUT" or behavior_type == 'RECEIVE':
                passenger = passengers[passenger_id]
                if passenger_id not in passengers.keys():
                    raise CustomError(f"没这人 id{passenger_id}")
            if behavior_type == 'RESET_ACCEPT':
                capacity = behavior.capacity
                move_time = behavior.move_time
            elevators[elevator_id].check(behavior_type, time, floor, passenger, capacity, move_time)

    for key, passenger in passengers.items():
        if passenger.cur_floor != passenger.to_floor:
            raise CustomError(f"没送到 id:{passenger.id} At {passenger.cur_floor}\
                              To {passenger.to_floor}")

    for key, elevator in elevators.items():
        if elevator.state != ElevatorState.PARKING:
            raise CustomError(f"最后没关上门/没结束RESET id:{elevator.elevator_id}")
        if len(elevator.passengers) != 0:
            raise CustomError(f"困在里面{elevator.passengers}")
    print("pass!")


main()
