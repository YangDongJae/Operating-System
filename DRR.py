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

    def update_power_status(self,processor):
        if processor.current_process:
            if not processor.power_on:
                processor.power_on = True
                if processor.core_type == "P":
                    processor.power_usage += 0.5
                elif processor.core_type == "E":
                    processor.power_usage += 0.1
        else:
            if processor.power_on:
                processor.power_on = False     
                
class SchedulingAlgorithm:
    def __init__(self, processor_select_signal):
        self.processors = []

        for i in range(len(processor_select_signal)):
            if processor_select_signal[i] == 0:
                self.processors.append(Processor(i, None))
            elif processor_select_signal[i] == 1:
                self.processors.append(Processor(i, "P"))
            elif processor_select_signal[i] == 2:
                self.processors.append(Processor(i, "E"))


    def schedule(self):
        raise NotImplementedError("schedule method must be implemented by a subclass")

class DRR(SchedulingAlgorithm):
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

        self.processor0_queue = []
        self.processor1_queue = []
        self.processor2_queue = []
        self.processor3_queue = []

    def add_process(self, process):
        self.process_queue.append(process)
          
    def assign_process_to_processor(self, processor, processor_list, ready_queue):
        if not processor.current_process and ready_queue:
            if processor.core_type == "P":
                if ready_queue[0].remaining_time > 1 and ready_queue[0].complexity > 4:
                    processor.current_process = ready_queue.pop(0)
            elif processor.core_type == "E":
                if ready_queue[0].remaining_time == 1 or ready_queue[0].complexity <= 4:
                    processor.current_process = ready_queue.pop(0)
                elif all([p.current_process for p in processor_list]):
                    processor.current_process = ready_queue.pop(0)                
                
    def handle_outed_process(self, processor, scheduler, current_time):
        processor.current_process.waiting_time = (current_time - processor.current_process.arrival_time - processor.current_process.count + 1)
        processor.current_process.turnaround_time = (processor.current_process.waiting_time + processor.current_process.count)
        processor.current_process.completed_time = current_time + 1
        scheduler.outed_processes.append(processor.current_process)
        processor.current_process = None

    def handle_completed_process(self, processor, scheduler, current_time):
        processor.current_process.waiting_time = (current_time - processor.current_process.arrival_time - processor.current_process.count + 1)
        processor.current_process.turnaround_time = (processor.current_process.waiting_time + processor.current_process.count)
        processor.current_process.completed_time = current_time + 1
        scheduler.completed_processes.append(processor.current_process)
        processor.current_process = None

    def handle_preempted_process(self, processor, scheduler):
        scheduler.ready_queue.append(processor.current_process)
        processor.current_process = None
                
                
    def update_current_process(self,processor, scheduler, current_time):
        if processor.current_process:
            processor.current_process.count += 1
            if processor.core_type == "P":
                processor.current_process.remaining_time -= 2
                processor.power_usage += 3
            elif processor.core_type == "E":
                processor.current_process.remaining_time -= 1
                processor.power_usage += 1

            if processor.current_process.count >= 10:
                self.handle_outed_process(processor, scheduler, current_time)
            elif processor.current_process.remaining_time <= 0:
                self.handle_completed_process(processor, scheduler, current_time)
            elif processor.current_process.remaining_time > 0:
                if (processor.current_process.burst_time - processor.current_process.remaining_time) % processor.current_process.time_quantum == 0:
                    self.handle_preempted_process(processor, scheduler)
                    
                         

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

            self.assign_process_to_processor(processor0, self.processors, self.ready_queue)
            self.assign_process_to_processor(processor1, self.processors, self.ready_queue)
            self.assign_process_to_processor(processor2, self.processors, self.ready_queue)
            self.assign_process_to_processor(processor3, self.processors, self.ready_queue)

            if processor0.current_process:
                self.processor0_queue.append(processor0.current_process.pid)
            else:
                self.processor0_queue.append(0)

            if processor1.current_process:
                self.processor1_queue.append(processor1.current_process.pid)
            else:
                self.processor1_queue.append(0)

            if processor2.current_process:
                self.processor2_queue.append(processor2.current_process.pid)
            else:
                self.processor2_queue.append(0)

            if processor3.current_process:
                self.processor3_queue.append(processor3.current_process.pid)
            else:
                self.processor3_queue.append(0)


            processor0.update_power_status(processor0)
            processor1.update_power_status(processor1)
            processor2.update_power_status(processor2)
            processor3.update_power_status(processor3)

            

            self.update_current_process(processor0, self, current_time)
            self.update_current_process(processor1, self, current_time)
            self.update_current_process(processor2, self, current_time)
            self.update_current_process(processor3, self, current_time)


            current_time += 1

    def print_results(self):
        print("Process ID | GPT Model | Complexity | Arrival Time | Burst Time | Waiting Time | Turnaround Time | Completed Time | Working Time")
        for process in self.completed_processes:
            print(f"{process.pid} | {process.gpt_model} | {process.complexity} | {process.arrival_time} |  {process.burst_time} | {process.waiting_time} | {process.turnaround_time} | {process.completed_time} | {process.count}")
        print("<아웃된 프로세스>")
        for process in self.outed_processes:
            print(f"{process.pid} | {process.gpt_model} | {process.complexity} | {process.arrival_time} | {process.burst_time} | {process.waiting_time} | {process.turnaround_time} | {process.completed_time} | {process.count}")
        P_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "P"])
        E_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "E"])
        print("P코어 총 전력 사용량:",round(P_cores_power_usage, 1),"W")
        print("E코어 총 전력 사용량:",round(E_cores_power_usage, 1),"W")
        print("총 전력 사용량:",round(P_cores_power_usage+E_cores_power_usage, 1),"W")
        print("프로세서 0에서 작업한 프로세스:", self.processor0_queue)
        print("프로세서 1에서 작업한 프로세스:", self.processor1_queue)
        print("프로세서 2에서 작업한 프로세스:", self.processor2_queue)
        print("프로세서 3에서 작업한 프로세스:", self.processor3_queue)

class Main:
    def __init__(self, process_select_signal, processor_select_signal):
        self.processes = []
        self.process_select_signal = process_select_signal
        self.drr_algorithm = DRR(processor_select_signal)

    def create_process(self):
        for i in self.process_select_signal:
            pid = i[0]
            arrival_time = i[1]
            burst_time = i[2]

            gpt_model = i[3]
            complexity = i[4]

            time_quantum = 0
            completed_time = 0

            process = Process(pid, arrival_time, burst_time, completed_time, gpt_model, complexity, time_quantum)
            self.processes.append(process)

    def run_scheduler(self):
        for process in self.processes:
            self.drr_algorithm.add_process(process)
        self.drr_algorithm.schedule()

    def print_result(self):
        self.drr_algorithm.print_results()
            

def main():
    process_select_signal = [[1, 1, 6, "GPT 3.5", 6],
                             [2, 12, 20, "GPT 4", 10],
                             [3, 7, 3, "GPT 3.5", 3],
                             [4, 16, 16, "GPT 4", 8],
                             [5, 8 ,18, "GPT 4", 9],
                             [6, 2, 8, "GPT 3.5", 8],
                             [7, 15, 6, "GPT 4", 3],
                             [8, 7, 2, "GPT 3.5", 2],
                             [9, 3, 1, "GPT 3.5", 1],
                             [10, 0, 14, "GPT 4", 7],
                             [11, 1, 12, "GPT 4", 6],
                             [12, 13, 9, "GPT 3.5", 9],
                             [13, 5, 24, "GPT 4", 12],
                             [14, 4, 11, "GPT 3.5", 11],
                             [15, 11, 10, "GPT 4", 5]]

    processor_select_signal = [1, 1, 1, 2]

    main_program = Main(process_select_signal, processor_select_signal)
    main_program.create_process()
    main_program.run_scheduler()
    main_program.print_result()


if __name__ == "__main__":
    main()