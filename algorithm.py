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

class DynamicRoundRobinAlgorithm(SchedulingAlgorithm):
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
            print(f"     {process.pid}     |  {process.gpt_model}  |      {process.complexity}     |       {process.arrival_time}      |      {process.burst_time}     |      {process.waiting_time}      |        {process.turnaround_time}        |        {process.completed_time}        | {process.count}")
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
        
class FCFS(SchedulingAlgorithm):
    def __init__(self,processor_select_signal):    #p코어 e코어 갯수 입력 받음
        super().__init__(processor_select_signal)
        self.process_queue = [] #프로세스 큐
        self.ready_queue = []   #레디 큐
        self.completed_processes = []   #료된 프로세스들 보관하는 리스트

        self.processor0_queue = []
        self.processor1_queue = []
        self.processor2_queue = []
        self.processor3_queue = []
                                            
    def add_process(self, process):         #프로세스 할당
        self.process_queue.append(process)  #프로세스 큐에 프로세스 추가 
        
    def update_current_process(self,processor, current_time):
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
          
            #각 코어에 할당, 비선점 할당
            if not processor0.current_process and not processor0.core_type == None and self.ready_queue:                 #0번째 프로세서에 존재x, 레디큐에 존재    
                processor0.current_process = self.ready_queue.pop(0)
                    

            if not processor1.current_process and not processor1.core_type == None and self.ready_queue:                                  
                processor1.current_process = self.ready_queue.pop(0)
                    

            if not processor2.current_process and not processor2.core_type == None and self.ready_queue:
                processor2.current_process = self.ready_queue.pop(0)
                    

            if not processor3.current_process and not processor3.core_type == None and self.ready_queue:
                processor3.current_process = self.ready_queue.pop(0)
                
                    
            
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

            #한 주기 긑
            current_time += 1   

class RR(SchedulingAlgorithm):
    def __init__(self,processor_select_signal):    #p코어 e코어 갯수 입력 받음
        super().__init__(processor_select_signal)
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
            elif processor.core_type == "E":
                processor.current_process.remaining_time -= 1
            if processor.core_type == "P":
                processor.power_usage += 3
            elif processor.core_type == "E":
                processor.power_usage += 1
            if processor.current_process.remaining_time <= 0:
                processor.current_process.waiting_time = (current_time - processor.current_process.arrival_time - processor.current_process.count + 1)
                processor.current_process.turnaround_time = processor.current_process.waiting_time + processor.current_process.count
                processor.current_process.completed_time = current_time + 1
                self.completed_processes.append(processor.current_process)
                processor.current_process = None
            elif processor.current_process.remaining_time > 0:
                if (processor.current_process.burst_time - processor.current_process.remaining_time) % processor.current_process.time_quantum == 0:
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

class SPN(SchedulingAlgorithm):
    def __init__(self,processor_select_signal):    #p코어 e코어 갯수 입력 받음
        super().__init__(processor_select_signal)
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
            elif processor.core_type == "E":
                processor.current_process.remaining_time -= 1
            if processor.core_type == "P":
                processor.power_usage += 3
            elif processor.core_type == "E":
                processor.power_usage += 1
            if processor.current_process.remaining_time <= 0:
                processor.current_process.waiting_time = (current_time - processor.current_process.arrival_time - processor.current_process.count + 1)
                processor.current_process.turnaround_time = processor.current_process.waiting_time + processor.current_process.count
                processor.current_process.completed_time = current_time + 1
                self.completed_processes.append(processor.current_process)
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
            
class SRTN(SchedulingAlgorithm):
    def __init__(self,processor_select_signal):    #p코어 e코어 갯수 입력 받음
        super().__init__(processor_select_signal)
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
            elif processor.core_type == "E":
                processor.current_process.remaining_time -= 1
            if processor.core_type == "P":
                processor.power_usage += 3
            elif processor.core_type == "E":
                processor.power_usage += 1
            if processor.current_process.remaining_time <= 0:
                processor.current_process.waiting_time = (current_time - processor.current_process.arrival_time - processor.current_process.count + 1)
                processor.current_process.turnaround_time = (processor.current_process.waiting_time + processor.current_process.count)
                processor.current_process.completed_time = current_time + 1
                self.completed_processes.append(processor.current_process)
                processor.current_process = None
            elif processor.current_process.remaining_time > 0 and self.ready_queue: #시간 남아있고 레디큐에 존재하면
                    if processor.current_process.remaining_time > self.ready_queue[0].remaining_time:   #레디큐 0번째의 RT가 0프로세서의 프로세스의 RT보다 작으면
                        tmp = processor.current_process                                #둘이 교환
                        processor.current_process = self.ready_queue[0]
                        self.ready_queue[0]=tmp
                

        
                                            
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
        
class HRRN(SchedulingAlgorithm):
    def __init__(self,processor_select_signal):    #p코어 e코어 갯수 입력 받음
        super().__init__(processor_select_signal)
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
            elif processor.core_type == "E":
                processor.current_process.remaining_time -= 1
            if processor.core_type == "P":
                processor.power_usage += 3
            elif processor.core_type == "E":
                processor.power_usage += 1
            if processor.current_process.remaining_time <= 0:
                processor.current_process.waiting_time = (current_time - processor.current_process.arrival_time - processor.current_process.count + 1)
                processor.current_process.turnaround_time = processor.current_process.waiting_time + processor.current_process.count
                processor.current_process.completed_time = current_time + 1
                self.completed_processes.append(processor.current_process)
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
#메인
class Main:
    def __init__(self, processor_select_signal, N):
        self.N = N  #프로세스 갯수
        self.processes = []
        
        self.fcfs_algorithm = FCFS(processor_select_signal)
        self.spn_algorithm = SPN(processor_select_signal)
        self.rr_algorithm = RR(processor_select_signal)
        self.srtn_algorithm = SRTN(processor_select_signal)
        self.hrrn_algorithm = HRRN(processor_select_signal)
        self.drr_algorithm = DynamicRoundRobinAlgorithm(processor_select_signal)


    def create_process(self, version, TQ=0):
        for i in range(self.N):
            pid = i + 1 #ID
            arrival_time = random.randint(0,3) #0~15
            gpt_model = random.choice(["GPT 4","GPT 3.5"])  #둘중에 하나
            complexity = random.randint(1,12)               #1~12

            if gpt_model == "GPT 4":
                gpt_multiplier = 2                          
            elif gpt_model == "GPT 3.5":
                gpt_multiplier = 1
            if version=="RRRTN":
                burst_time = complexity * gpt_multiplier        #3*gpt4 = 6
            else : 
                burst_time= random.randint(5,11)
            time_quantum = TQ                              
            completed_time = 0

            process = Process(pid, arrival_time, burst_time, completed_time, gpt_model, complexity, time_quantum)
            self.processes.append(process)  #프로세스 리스트에 추가

    def run_scheduler(self, version):          

        if version=="RR":
            for process in self.processes:
                self.rr_algorithm.add_process(process)  #프로세스 하나씩 rr알고리즘에 추가
            self.rr_algorithm.schedule()                #rr알고리즘 실행

        elif version =="FCFS":
            for process in self.processes:
                self.fcfs_algorithm.add_process(process)  #프로세스 하나씩 rr알고리즘에 추가
            self.fcfs_algorithm.schedule()                #rr알고리즘 실행

        elif version=="SPN":
            for process in self.processes:
                self.spn_algorithm.add_process(process)  #프로세스 하나씩 rr알고리즘에 추가
            self.spn_algorithm.schedule()                #rr알고리즘 실행   #미구현

        elif version=="SRTN":
            for process in self.processes:
                self.srtn_algorithm.add_process(process)  #프로세스 하나씩 rr알고리즘에 추가
            self.srtn_algorithm.schedule()                #rr알고리즘 실행

        elif version=="HRRN":
            for process in self.processes:
                self.hrrn_algorithm.add_process(process)  #프로세스 하나씩 rr알고리즘에 추가
            self.hrrn_algorithm.schedule()                #rr알고리즘 실행

        elif version =="DRR":
            for process in self.processes:
                self.drr_algorithm.add_process(process)  #프로세스 하나씩 rr알고리즘에 추가
            self.drr_algorithm.schedule()                #rr알고리즘 실행            

    def print_result(self, version):                         #출력
        
        if version== "FCFS":
            super(FCFS,self.fcfs_algorithm).print_results()
        elif version== "SPN":
            super(SPN,self.spn_algorithm).print_results()
        elif version== "RR":
            super(RR,self.rr_algorithm).print_results()
        elif version=="SRTN":
            super(SRTN,self.srtn_algorithm).print_results()
        elif version=="HRRN":
            super(HRRN,self.hrrn_algorithm).print_results()
        elif version=="DRR":
            self.drr_algorithm.print_results()            


            

def main(version, TQ=0):
        processor_select_signal = [1, 1, 1, 2]         #프로세서 p코어3개, e코어 1개 ,순서대로
        N = 5
        main_program = Main(processor_select_signal, N)

        if TQ==0:
            main_program.create_process(version)                   #프로세스 생성, 
            main_program.run_scheduler(version)                    #스케줄링
            main_program.print_result(version)                     #출력
        else:
            main_program.create_process(version,TQ)                   #프로세스 생성, 
            main_program.run_scheduler(version)                    #스케줄링
            main_program.print_result(version)                     #출력

if __name__ == "__main__":
    main("DRR")        #RR빼고 그냥 "FCFS", "SPN", "SRTN"
                        #RR은 Time Quantum값 지정 ex) main("RR",3)