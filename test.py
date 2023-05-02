import random
from collections import deque

class Process:
    def __init__(self, arrival_time, complexity, model):
        self.arrival_time = arrival_time
        self.complexity = complexity
        self.model = model
        self.burst_time = self.calculate_bt()

    def calculate_bt(self):
        base_time = random.randint(1, 45)
        if self.model == "GPT4":
            return min(base_time + (self.complexity * 2), 45)
        else:
            return min(base_time + self.complexity, 45)

class Core:
    def __init__(self, speed, power_usage, startup_power):
        self.speed = speed
        self.power_usage = power_usage
        self.startup_power = startup_power

def create_time_quantum_table():
    table = {}
    for i in range(1, 46):
        if i <= 10:
            table[i] = 1
        elif i <= 20:
            table[i] = 2
        elif i <= 30:
            table[i] = 3
        else:
            table[i] = 4
    return table

def schedule_processes(processes, cores, time_quantum_table):
    p_cores = cores[:3]
    e_core = cores[3]
    queue = deque(processes)
    finished_processes = []

    while queue:
        current_process = queue.popleft()
        at, bt, complexity, model = current_process.arrival_time, current_process.burst_time, current_process.complexity, current_process.model

        if bt == 1 or complexity <= 5 or sum(core.speed for core in p_cores) == 3 and e_core.speed == 0:
            time_quantum = 1
            remaining_bt = bt - time_quantum
            e_core.speed += time_quantum
        else:
            time_quantum = min(time_quantum_table[bt], 2)
            remaining_bt = bt - time_quantum
            min_p_core = min(p_cores, key=lambda x: x.speed)
            min_p_core.speed += time_quantum

        if remaining_bt <= 0 or bt >= 30:
            finished_processes.append(current_process)
        else:
            current_process.burst_time = remaining_bt
            queue.append(current_process)

    return finished_processes

def main():
    processes = [
        Process(0, 5, "GPT4"),
        Process(1, 10, "Default GPT 3.5"),
        Process(2, 15, "Legacy GPT 3.5"),
        Process(3, 20, "GPT4"),
    ]

    cores = [
        Core(2, 3, 0.5),
        Core(2, 3, 0.5),
        Core(2, 3, 0.5),
        Core(1, 1, 0.1),
    ]

    time_quantum_table = create_time_quantum_table()
    finished_processes = schedule_processes(processes, cores, time_quantum_table)
    
    for process in finished_processes:
        print(f"Arrival Time: {process.arrival_time}, Burst Time: {process.burst_time}, Complexity: {process.complexity}, Model: {process.model}")

if __name__ == "__main__":
    main()
