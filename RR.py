class Process:
    def __init__(self, pid, arrival_time, burst_time, completed_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completed_time = completed_time
        self.count = 0  #프로세스에서 돈 시간 카운트
        self.waiting_time = 0
        self.turnaround_time = 0


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

        #0 :프로세서 off, 1 : P코어 선택-, 2 : E코어 선택
        for i in range(len(processor_select_signal)):
            if processor_select_signal[i] == 0:
                self.processors.append(Processor(i, None))
            elif processor_select_signal[i] == 1:
                self.processors.append(Processor(i, "P"))
            elif processor_select_signal[i] == 2:
                self.processors.append(Processor(i, "E"))

    def schedule(self):
        raise NotImplementedError("sub클래스에서 구현")

                                            

#알고리즘
class RR(SchedulingAlgorithm):
    def __init__(self,processor_select_signal, time_quantum):    #p코어 e코어 갯수 입력 받음
        super().__init__(processor_select_signal)
        self.time_quantum = time_quantum
        self.process_queue = [] #프로세스 큐
        self.ready_queue = []   #레디 큐
        self.completed_processes = []   #료된 프로세스들 보관하는 리스트
        self.outed_process=[]           #컷팅 프로세스

        self.processor0_queue = []
        self.processor1_queue = []
        self.processor2_queue = []
        self.processor3_queue = []
                                            
    def add_process(self, process):         #프로세스 할당
        self.process_queue.append(process)  #프로세스 큐에 프로세스 추가
        
    def update_current_process(self,processor,current_time):
        if processor.current_process:
            processor.current_process.count += 1
            if processor.core_type == "P":
                processor.current_process.remaining_time -= 2
                processor.power_usage += 3
            elif processor.core_type == "E":
                processor.current_process.remaining_time -= 1
                processor.power_usage += 1
            if processor.current_process.remaining_time <= 0:
                processor.current_process.waiting_time = (current_time - processor.current_process.arrival_time - processor.current_process.count + 1)
                processor.current_process.turnaround_time = (processor.current_process.waiting_time + processor.current_process.count)
                processor.current_process.completed_time = current_time + 1
                self.completed_processes.append(processor.current_process)
                processor.current_process = None
            elif processor.current_process.remaining_time > 0:
                if (processor.current_process.burst_time - processor.current_process.remaining_time) % self.time_quantum == 0:
                    self.ready_queue.append(processor.current_process)
                    processor.current_process = None
        
                                            
    def schedule(self):                     #스케줄링 함수
        current_time = 0                    #현재 시간 0으로 지정
        processor0 = self.processors[0]     #0번째 프로세서
        processor1 = self.processors[1]     #1번째 프로세서
        processor2 = self.processors[2]     #2번째 프로세서
        processor3 = self.processors[3]     #3번째 프로세서


        while self.process_queue or self.ready_queue or processor0.current_process or processor1.current_process or processor2.current_process or processor3.current_process:
            #프로세스큐, 레디큐, 각 프로세스 별로 원소들이 존재하면 반복
            incoming_processes = [proc for proc in self.process_queue if proc.arrival_time == current_time]
            #현재시간과 도착시간이 같은 프로세스 큐안에있는 프로세스들을 모아논 리스트
            for process in incoming_processes:      #AT=CT인 프로세스들을 큐에서 제거하고 레디큐로 내려보냄
                self.process_queue.remove(process)  
                self.ready_queue.append(process)
           
            
                
            #각 코어에 할당
            if not processor0.current_process and not processor0.core_type == None and self.ready_queue:                 #0번째 프로세서에 존재x, 레디큐에 존재
                        processor0.current_process = self.ready_queue.pop(0)                                        #프로세서0에 프로세서 할당

            if not processor1.current_process and not processor1.core_type == None and self.ready_queue:                                  
                        processor1.current_process = self.ready_queue.pop(0)

            if not processor2.current_process and not processor2.core_type == None and self.ready_queue:
                        processor2.current_process = self.ready_queue.pop(0)

            if not processor3.current_process and not processor3.core_type == None and self.ready_queue:
                        processor3.current_process = self.ready_queue.pop(0)
            

            #프로세서 큐 할당
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

            #프로세서 별로 전력 계산
            processor0.update_power_status(processor0)
            processor1.update_power_status(processor1)
            processor2.update_power_status(processor2)
            processor3.update_power_status(processor3)


            #프로세스 처리 매 초마다
            self.update_current_process(processor0, current_time)
            self.update_current_process(processor1, current_time)
            self.update_current_process(processor2, current_time)
            self.update_current_process(processor3, current_time)            
            #프로세서0에 현재 프로세스가 있으면
            
            current_time += 1
            
    def print_results(self):
        
        print("Process ID  Arrival Time | Burst Time | Waiting Time | Turnaround Time | Completed Time")
        for process in self.completed_processes:
            print(f"{process.pid} | {process.arrival_time} | {process.burst_time} | {process.waiting_time} | {process.turnaround_time} | {process.completed_time}")
        P_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "P"])
        E_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "E"])
        print("P코어 총 전력 사용량:",P_cores_power_usage,"W")
        print("E코어 총 전력 사용량:",E_cores_power_usage,"W")
        print("총 전력 사용량:",round(P_cores_power_usage+E_cores_power_usage, 1),"W")
        print("프로세서 0에서 작업한 프로세스:", self.processor0_queue)
        print("프로세서 1에서 작업한 프로세스:", self.processor1_queue)
        print("프로세서 2에서 작업한 프로세스:", self.processor2_queue)
        print("프로세서 3에서 작업한 프로세스:", self.processor3_queue)


class Main:
    def __init__(self, process_select_signal, processor_select_signal, time_quantum):
        self.processes = []
        self.process_select_signal = process_select_signal
        self.rr_algorithm = RR(processor_select_signal, time_quantum)

    def create_process(self):
        for i in self.process_select_signal:
            pid = i[0]
            arrival_time = i[1]
            burst_time = i[2]
            completed_time = 0

            process = Process(pid, arrival_time, burst_time, completed_time)
            self.processes.append(process)

    def run_scheduler(self):
        for process in self.processes:
            self.rr_algorithm.add_process(process)
        self.rr_algorithm.schedule()

    def print_result(self):
        self.rr_algorithm.print_results()
            

def main():
    time_quantum = 2
    process_select_signal = [[1, 1, 6],
                             [2, 12, 20],
                             [3, 7, 3],
                             [4, 16, 16],
                             [5, 8 ,18],
                             [6, 2, 8],
                             [7, 15, 6],
                             [8, 7, 2],
                             [9, 3, 1],
                             [10, 0, 14],
                             [11, 1, 12],
                             [12, 13, 9],
                             [13, 5, 24],
                             [14, 4, 11],
                             [15, 11, 10]]

    processor_select_signal = [1, 1, 1, 2]

    main_program = Main(process_select_signal, processor_select_signal, time_quantum)
    main_program.create_process()
    main_program.run_scheduler()
    main_program.print_result()


if __name__ == "__main__":
    main()