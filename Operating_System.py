class Process:
    def __init__(self, pid, arrival_time, burst_time, complexity, time_quantum):
        self.pid = pid
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.remaining_time = burst_time
        self.count = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.complexity = complexity
        self.time_quantum = time_quantum

class Processor:
    def __init__(self, processor_id, core_type: str):
        self.processor_id = processor_id
        self.core_type = core_type
        self.current_process = None
        self.power_on = False
        self.power_usage = 0

class SchedulingAlgorithm:
    def schedule(self):
        raise NotImplementedError("schedule method must be implemented by a subclass")

class RoundRobinAlgorithm(SchedulingAlgorithm):
    def __init__(self):
        self.processors = [Processor(0,"P"),Processor(1,"P"),Processor(2,"P"),Processor(3,"E")]
        self.process_queue = []
        self.ready_queue = []
        self.completed_processes = []
        self.time_quantum_table = {
            (1, 10):  2,
            (11, 20): 4,
            (21, 30): 6,
            (31, 45): 8,
        }

    def add_process(self, process):
        self.process_queue.append(process)

    def schedule(self):
        current_time = 0
        processor0 = self.processors[0]
        processor1 = self.processors[1]
        processor2 = self.processors[2]
        processor3 = self.processors[3]


        while self.process_queue or self.ready_queue or processor0.current_process or processor1.current_process or processor2.current_process or processor3.current_process:
            incoming_processes = [proc for proc in self.process_queue if proc.arrival_time == current_time]
            for process in incoming_processes:
                self.process_queue.remove(process)
                self.ready_queue.append(process)

            if self.ready_queue:
                for(lower, upper), quantum in self.time_quantum_table.items():
                    for process in self.ready_queue:
                        if lower <= process.remaining_time <= upper:
                            process.time_quantum = quantum

            if not processor0.current_process and self.ready_queue:
                if processor0.core_type == "P":
                    if self.ready_queue[0].remaining_time > 1 and self.ready_queue[0].complexity > 4:
                        processor0.current_process = self.ready_queue.pop(0)
                elif processor0.core_type == "E":
                    if self.ready_queue[0].remaining_time == 1 or self.ready_queue[0].complexity <= 4:
                        processor0.current_process = self.ready_queue.pop(0)
                    elif processor1.current_process and processor2.current_process and processor3.current_process:
                        processor0.current_process = self.ready_queue.pop(0)

            if not processor1.current_process and self.ready_queue:
                if processor1.core_type == "P":
                    if self.ready_queue[0].remaining_time > 1 and self.ready_queue[0].complexity > 4:
                        processor1.current_process = self.ready_queue.pop(0)
                elif processor1.core_type == "E":
                    if self.ready_queue[0].remaining_time == 1 or self.ready_queue[0].complexity <= 4:
                        processor1.current_process = self.ready_queue.pop(0)
                    elif processor0.current_process and processor2.current_process and processor3.current_process:
                        processor1.current_process = self.ready_queue.pop(0)

            if not processor2.current_process and self.ready_queue:
                if processor2.core_type == "P":
                    if self.ready_queue[0].remaining_time > 1 and self.ready_queue[0].complexity > 4:
                        processor2.current_process = self.ready_queue.pop(0)
                elif processor2.core_type == "E":
                    if self.ready_queue[0].remaining_time == 1 or self.ready_queue[0].complexity <= 4:
                        processor2.current_process = self.ready_queue.pop(0)
                    elif processor0.current_process and processor1.current_process and processor3.current_process:
                        processor2.current_process = self.ready_queue.pop(0)

            if not processor3.current_process and self.ready_queue:
                if processor3.core_type == "P":
                    if self.ready_queue[0].remaining_time > 1 and self.ready_queue[0].complexity > 4:
                        processor3.current_process = self.ready_queue.pop(0)
                elif processor3.core_type == "E":
                    if self.ready_queue[0].remaining_time == 1 or self.ready_queue[0].complexity <= 4:
                        processor3.current_process = self.ready_queue.pop(0)
                    elif processor0.current_process and processor1.current_process and processor2.current_process:
                        processor3.current_process = self.ready_queue.pop(0)

            if processor0.current_process:
                if processor0.power_on == False:
                    processor0.power_on = True
                    if processor0.core_type == "P":
                        processor0.power_usage += 0.5
                    elif processor0.core_type == "E":
                        processor0.power_usage += 0.1
            elif not processor0.current_process:
                if processor0.power_on == True:
                    processor0.power_on = False

            if processor1.current_process:
                if processor1.power_on == False:
                    processor1.power_on = True
                    if processor1.core_type == "P":
                        processor1.power_usage += 0.5
                    elif processor1.core_type == "E":
                        processor1.power_usage += 0.1
            elif not processor1.current_process:
                if processor1.power_on == True:
                    processor1.power_on = False

            if processor2.current_process:
                if processor2.power_on == False:
                    processor2.power_on = True
                    if processor2.core_type == "P":
                        processor2.power_usage += 0.5
                    elif processor2.core_type == "E":
                        processor2.power_usage += 0.1
            elif not processor2.current_process:
                if processor2.power_on == True:
                    processor2.power_on = False

            if processor3.current_process:
                if processor3.power_on == False:
                    processor3.power_on = True
                    if processor3.core_type == "P":
                        processor3.power_usage += 0.5
                    elif processor3.core_type == "E":
                        processor3.power_usage += 0.1
            elif not processor3.current_process:
                if processor3.power_on == True:
                    processor3.power_on = False

            if processor0.current_process:
                processor0.current_process.count += 1
                if processor0.core_type == "P":
                    processor0.current_process.remaining_time -= 2
                elif processor0.core_type == "E":
                    processor0.current_process.remaining_time -= 1
                if processor0.core_type == "P":
                    processor0.power_usage += 3
                elif processor0.core_type == "E":
                    processor0.power_usage += 1
                if processor0.current_process.remaining_time <= 0:
                    processor0.current_process.waiting_time = (current_time - processor0.current_process.arrival_time - processor0.current_process.count + 1)
                    processor0.current_process.turnaround_time = (processor0.current_process.waiting_time + processor0.current_process.count)
                    self.completed_processes.append(processor0.current_process)
                    processor0.current_process = None
                elif processor0.current_process.remaining_time > 0:
                    if (processor0.current_process.burst_time - processor0.current_process.remaining_time) % processor0.current_process.time_quantum == 0:
                        self.ready_queue.append(processor0.current_process)
                        processor0.current_process = None


            if processor1.current_process:
                processor1.current_process.count += 1
                if processor1.core_type == "P":
                    processor1.current_process.remaining_time -= 2
                elif processor1.core_type == "E":
                    processor1.current_process.remaining_time -= 1
                if processor1.core_type == "P":
                    processor1.power_usage += 3
                elif processor1.core_type == "E":
                    processor1.power_usage += 1
                if processor1.current_process.remaining_time <= 0:
                    processor1.current_process.waiting_time = (current_time - processor1.current_process.arrival_time - processor1.current_process.count + 1)
                    processor1.current_process.turnaround_time = processor1.current_process.waiting_time + processor1.current_process.count
                    self.completed_processes.append(processor1.current_process)
                    processor1.current_process = None
                elif processor1.current_process.remaining_time > 0:
                    if (processor1.current_process.burst_time - processor1.current_process.remaining_time) % processor1.current_process.time_quantum == 0:
                        self.ready_queue.append(processor1.current_process)
                        processor1.current_process = None


            if processor2.current_process:
                processor2.current_process.count += 1
                if processor2.core_type == "P":
                    processor2.current_process.remaining_time -= 2
                elif processor2.core_type == "E":
                    processor2.current_process.remaining_time -= 1
                if processor2.core_type == "P":
                    processor2.power_usage += 3
                elif processor2.core_type == "E":
                    processor2.power_usage += 1
                if processor2.current_process.remaining_time <= 0:
                    processor2.current_process.waiting_time = (current_time - processor2.current_process.arrival_time - processor2.current_process.count + 1)
                    processor2.current_process.turnaround_time = (processor2.current_process.waiting_time + processor2.current_process.count)
                    self.completed_processes.append(processor2.current_process)
                    processor2.current_process = None
                elif processor2.current_process.remaining_time > 0:
                    if (processor2.current_process.burst_time - processor2.current_process.remaining_time) % processor2.current_process.time_quantum == 0:
                        self.ready_queue.append(processor2.current_process)
                        processor2.current_process = None


            if processor3.current_process:
                if processor3.core_type == "P":
                    processor3.current_process.remaining_time -= 2
                elif processor3.core_type == "E":
                    processor3.current_process.remaining_time -= 1
                if processor3.core_type == "P":
                    processor3.power_usage += 3
                elif processor3.core_type == "E":
                    processor3.power_usage += 1
                    processor3.current_process.count += 1
                if processor3.current_process.remaining_time <= 0:
                    processor3.current_process.waiting_time = (current_time - processor3.current_process.arrival_time - processor3.current_process.count + 1)
                    processor3.current_process.turnaround_time = (processor3.current_process.waiting_time + processor3.current_process.count)
                    self.completed_processes.append(processor3.current_process)
                    processor3.current_process = None
                elif processor3.current_process.remaining_time > 0:
                    if (processor3.current_process.burst_time - processor3.current_process.remaining_time) % processor3.current_process.time_quantum == 0:
                        self.ready_queue.append(processor3.current_process)
                        processor3.current_process = None


            current_time += 1

    def print_results(self):
        print("Process ID | Arrival Time | Burst Time  | Waiting Time | Turnaround Time")
        for process in self.completed_processes:
            print(f"{process.pid} | {process.arrival_time} | {process.burst_time} | {process.waiting_time} | {process.turnaround_time}")
        P_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "P"])
        E_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "E"])
        print("P코어 총 전력 사용량:",P_cores_power_usage,"W")
        print("E코어 총 전력 사용량:",E_cores_power_usage,"W")


def main():
    processes = [Process(1, 0, 15, 5, 0)]
    rr_algorithm = RoundRobinAlgorithm()
    for process in processes:
        rr_algorithm.add_process(process)

    rr_algorithm.schedule()
    rr_algorithm.print_results()

if __name__ == "__main__":
    main()
