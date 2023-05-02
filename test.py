import random
from collections import deque

class Process:
    def __init__(self, arrival_time, complexity, model):
        self.arrival_time = arrival_time
        self.complexity = complexity
        self.model = model
        self.burst_time = self.calculate_bt()
        self.start_time = None
        self.finish_time = None

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

    current_time = 0
    total_processes = len(processes)
    completed_processes = 0

    while queue:
        current_process = queue.popleft()

        if current_process.start_time is None:
            current_process.start_time = current_time

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
            current_process.finish_time = current_time + time_quantum
            finished_processes.append(current_process)
            completed_processes += 1

            # Calculate WT, TT, NTT
            wt = current_process.start_time - current_process.arrival_time
            tt = current_process.finish_time - current_process.arrival_time
            ntt = tt / bt

            print(f"Completed process {completed_processes}/{total_processes}")
            print(f"Process Name: {model}, AT: {at}, BT: {bt}, WT: {wt}, TT: {tt}, NTT: {ntt}\n")
        else:
            current_process.burst_time = remaining_bt
            queue.append(current_process)

        current_time += time_quantum

    return finished_processes, current_time

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
    finished_processes, total_time = schedule_processes(processes, cores, time_quantum_table)

    total_power_p_cores = sum(core.power_usage * core.speed for core in cores[:3]) * total_time
    total_power_e_core = cores[3].power_usage * cores[3].speed * total_time
    total_power = total_power_p_cores + total_power_e_core
    average_response_time = sum((process.finish_time - process.arrival_time) for process in finished_processes) / len(processes)

    print(f"Total BT Time: {total_time}")
    print(f"Average Response Time: {average_response_time}")
    print(f"P-cores Total Power Usage: {total_power_p_cores}")
    print(f"E-core Total Power Usage: {total_power_e_core}")
    print(f"Total Power Usage: {total_power}")

if __name__ == "__main__":
    main()
