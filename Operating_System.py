import random

class Process:
    def __init__(self, pid, arrival_time, burst_time, completed_time, gpt_model, complexity, time_quantum):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completed_time = completed_time
        self.count = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.gpt_model = gpt_model
        self.complexity = complexity
        self.time_quantum = time_quantum

class Processor:
    def __init__(self, processor_id, core_type: str):
        self.processor_id = processor_id
        self.core_type = core_type
        self.current_process = None
        self.power_on = False
        self.power_usage = 0.0

class SchedulingAlgorithm:
    def __init__(self, processor_select_signal):
        self.processors = []

        for signal in processor_select_signal:
            if signal == 0:
                self.processors.append(Processor(signal, None))
            elif signal == 1:
                self.processors.append(Processor(signal, "P"))
            elif signal == 2:
                self.processors.append(Processor(signal, "E"))


    def schedule(self):
        raise NotImplementedError("schedule method must be implemented by a subclass")

class RoundRobinAlgorithm(SchedulingAlgorithm):
    def __init__(self, processor_select_signal):
        super().__init__(processor_select_signal)
        self.process_queue = []
        self.ready_queue = []
        self.completed_processes = []
        self.outed_processes = []
        self.time_quantum_table = {
            (1, 10):  2,
            (11, 20): 4,
            (21, 30): 6,
            (31, float('inf')): 8
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
                if processor0.current_process.count >= 10:
                    processor0.current_process.waiting_time = (current_time - processor0.current_process.arrival_time - processor0.current_process.count + 1)
                    processor0.current_process.turnaround_time = (processor0.current_process.waiting_time + processor0.current_process.count)
                    processor0.current_process.completed_time = current_time + 1
                    self.outed_processes.append(processor0.current_process)
                    processor0.current_process = None
                elif processor0.current_process.remaining_time <= 0:
                    processor0.current_process.waiting_time = (current_time - processor0.current_process.arrival_time - processor0.current_process.count + 1)
                    processor0.current_process.turnaround_time = (processor0.current_process.waiting_time + processor0.current_process.count)
                    processor0.current_process.completed_time = current_time + 1
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
                if processor1.current_process.count >= 10:
                    processor1.current_process.waiting_time = (current_time - processor1.current_process.arrival_time - processor1.current_process.count + 1)
                    processor1.current_process.turnaround_time = processor1.current_process.waiting_time + processor1.current_process.count
                    processor1.current_process.completed_time = current_time + 1
                    self.outed_processes.append(processor1.current_process)
                    processor1.current_process = None
                elif processor1.current_process.remaining_time <= 0:
                    processor1.current_process.waiting_time = (current_time - processor1.current_process.arrival_time - processor1.current_process.count + 1)
                    processor1.current_process.turnaround_time = processor1.current_process.waiting_time + processor1.current_process.count
                    processor1.current_process.completed_time = current_time + 1
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
                if processor2.current_process.count >= 10:
                    processor2.current_process.waiting_time = (current_time - processor2.current_process.arrival_time - processor2.current_process.count + 1)
                    processor2.current_process.turnaround_time = (processor2.current_process.waiting_time + processor2.current_process.count)
                    processor2.current_process.completed_time = current_time + 1
                    self.outed_processes.append(processor2.current_process)
                    processor2.current_process = None
                elif processor2.current_process.remaining_time <= 0:
                    processor2.current_process.waiting_time = (current_time - processor2.current_process.arrival_time - processor2.current_process.count + 1)
                    processor2.current_process.turnaround_time = (processor2.current_process.waiting_time + processor2.current_process.count)
                    processor2.current_process.completed_time = current_time + 1
                    self.completed_processes.append(processor2.current_process)
                    processor2.current_process = None
                elif processor2.current_process.remaining_time > 0:
                    if (processor2.current_process.burst_time - processor2.current_process.remaining_time) % processor2.current_process.time_quantum == 0:
                        self.ready_queue.append(processor2.current_process)
                        processor2.current_process = None

            if processor3.current_process:
                processor3.current_process.count += 1
                if processor3.core_type == "P":
                    processor3.current_process.remaining_time -= 2
                elif processor3.core_type == "E":
                    processor3.current_process.remaining_time -= 1
                if processor3.core_type == "P":
                    processor3.power_usage += 3
                elif processor3.core_type == "E":
                    processor3.power_usage += 1
                if processor3.current_process.count >= 10:
                    processor3.current_process.waiting_time = (current_time - processor3.current_process.arrival_time - processor3.current_process.count + 1)
                    processor3.current_process.turnaround_time = (processor3.current_process.waiting_time + processor3.current_process.count)
                    processor3.current_process.completed_time = current_time + 1
                    self.outed_processes.append(processor3.current_process)
                    processor3.current_process = None
                elif processor3.current_process.remaining_time <= 0:
                    processor3.current_process.waiting_time = (current_time - processor3.current_process.arrival_time - processor3.current_process.count + 1)
                    processor3.current_process.turnaround_time = (processor3.current_process.waiting_time + processor3.current_process.count)
                    processor3.current_process.completed_time = current_time + 1
                    self.completed_processes.append(processor3.current_process)
                    processor3.current_process = None
                elif processor3.current_process.remaining_time > 0:
                    if (processor3.current_process.burst_time - processor3.current_process.remaining_time) % processor3.current_process.time_quantum == 0:
                        self.ready_queue.append(processor3.current_process)
                        processor3.current_process = None


            current_time += 1

    def print_results(self):
        print("Process ID | GPT Model | Complexity | Arrival Time | Burst Time | Waiting Time | Turnaround Time | Completed Time | Working Time")
        for process in self.completed_processes:
            print(f"{process.pid} | {process.gpt_model} | {process.complexity} | {process.arrival_time} | {process.burst_time} | {process.waiting_time} | {process.turnaround_time} | {process.completed_time} | {process.count}")
        print("<아웃된 프로세스>")
        for process in self.outed_processes:
            print(f"{process.pid} | {process.gpt_model} | {process.complexity} | {process.arrival_time} | {process.burst_time} | {process.waiting_time} | {process.turnaround_time} | {process.completed_time} | {process.count}")
        P_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "P"])
        E_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "E"])
        print("P코어 총 전력 사용량:",P_cores_power_usage,"W")
        print("E코어 총 전력 사용량:",E_cores_power_usage,"W")

class Main:
    def __init__(self,processor_select_signal, N):
        self.N = N
        self.processes = []
        self.rr_algorithm = RoundRobinAlgorithm(processor_select_signal)

    def create_process(self):
        for i in range(self.N):
            pid = i + 1
            arrival_time = random.randint(0,15)
            gpt_model = random.choice(["GPT 4","GPT 3.5"])
            complexity = random.randint(1,15)

            if gpt_model == "GPT 4":
                gpt_multiplier = 2
            elif gpt_model == "GPT 3.5":
                gpt_multiplier = 1

            burst_time = complexity * gpt_multiplier
            time_quantum = 0
            completed_time = 0

            process = Process(pid, arrival_time, burst_time, completed_time, gpt_model, complexity, time_quantum)
            self.processes.append(process)

    def run_scheduler(self):
        for process in self.processes:
            self.rr_algorithm.add_process(process)
        self.rr_algorithm.schedule()

    def print_result(self):
        self.rr_algorithm.print_results()
            

def main():
    processor_select_signal = [1, 1, 1, 2]
    N = 20
    main_program = Main(processor_select_signal, N)
    main_program.create_process()
    main_program.run_scheduler()
    main_program.print_result()


if __name__ == "__main__":
    main()
