import random

class Process:
    def __init__(self, pid, arrival_time, burst_time, completed_time, gpt_model, complexity, time_quantum):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completed_time = completed_time
        self.count = 0  #프로세스에서 돈 시간 카운트
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
    def __init__(self, p_core, e_core):
        self.p_core = p_core
        self.e_core = e_core
        self.processors = [Processor(i,"P") for i in range(p_core)] + [Processor(i,"E") for i in range(p_core,p_core+e_core)]
        #processors list에 Processorp코어 e코어 할당
    def schedule(self):
        raise NotImplementedError("sub클래스에서 구현")
class FCFS(SchedulingAlgorithm):
    def __init__(self,P, E):    #p코어 e코어 갯수 입력 받음
        super().__init__(P, E)
        self.process_queue = [] #프로세스 큐
        self.ready_queue = []   #레디 큐
        self.completed_processes = []   #완료된 프로세스들 보관하는 리스트

    def add_process(self, process):         #프로세스 할당
        self.process_queue.append(process)  #프로세스 큐에 프로세스 추가
                                            
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
            if not processor0.current_process and self.ready_queue:                 #0번째 프로세서에 존재x, 레디큐에 존재
                if processor0.core_type == "P":                                     #p코어면
                    if self.ready_queue[0].remaining_time > 1 and self.ready_queue[0].complexity > 4:   #복잡도 4초과, 남은시간 1초과
                        processor0.current_process = self.ready_queue.pop(0)                            #p코어(1)에 할당
                elif processor0.core_type == "E":                                                       #E코어
                    if self.ready_queue[0].remaining_time == 1 or self.ready_queue[0].complexity <= 4:  #복잡도 4이하, 남은시간1이면 e코어 할당
                        processor0.current_process = self.ready_queue.pop(0)
                    elif processor1.current_process and processor2.current_process and processor3.current_process:  #나머지 프로세서에 프로세스가 존재하면
                        processor0.current_process = self.ready_queue.pop(0)                                        #프로세서0에 프로세서 할당

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

            #프로세서 별로 전력 계산

            if processor0.current_process:              #0프로세서에 프로세스 있으면
                if processor0.power_on == False:        #꺼져있으면
                    processor0.power_on = True          #키고
                    if processor0.core_type == "P":     #p면
                        processor0.power_usage += 0.5   #시동전력 0.5
                    elif processor0.core_type == "E":   #e면
                        processor0.power_usage += 0.1   #시동전력 0.1
            elif not processor0.current_process:        #프로세서가 없으면
                if processor0.power_on == True:         #켜지있는거
                    processor0.power_on = False         #끄기

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



            #프로세스 처리 매 초마다

            #프로세서0
            if processor0.current_process:
                processor0.current_process.count += 1   #현재 프로세스 카운트+1
                if processor0.core_type == "P":         #p코어이면
                    processor0.current_process.remaining_time -= 2  #남은시간 -2
                elif processor0.core_type == "E":       #e코어면
                    processor0.current_process.remaining_time -= 1  #남은시간 -2
                if processor0.core_type == "P":                     #전력계산
                    processor0.power_usage += 3
                elif processor0.core_type == "E":
                    processor0.power_usage += 1
                
                
                #RT(Remaining Time)가 1이면 레디큐로 0번째로 올리기
                

                elif processor0.current_process.remaining_time <= 0:  #남은시간이 0보다 작으면 완료니까 WT TT 계산 후 Cp에 올리기
                    #WT 계산 CT - AT - Count
                    processor0.current_process.waiting_time = (current_time - processor0.current_process.arrival_time - processor0.current_process.count + 1)
                    #TT 계산 = WT + Count
                    processor0.current_process.turnaround_time = (processor0.current_process.waiting_time + processor0.current_process.count)
                    #프로세스가 완료된 시간
                    processor0.current_process.completed_time = current_time + 1
                    #완성된 프로세스 리스트에 넣기
                    self.completed_processes.append(processor0.current_process)
                    #프로세서0의 현재 프로세스 비우기
                    processor0.current_process = None

            
            #프로세서1 
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
                    processor1.current_process.completed_time = current_time + 1
                    self.completed_processes.append(processor1.current_process)
                    processor1.current_process = None
                

            #프로세서2
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
                    processor2.current_process.completed_time = current_time + 1
                    self.completed_processes.append(processor2.current_process)
                    processor2.current_process = None
               

            #프로세서3
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

                

                elif processor3.current_process.remaining_time <= 0:
                    processor3.current_process.waiting_time = (current_time - processor3.current_process.arrival_time - processor3.current_process.count + 1)
                    processor3.current_process.turnaround_time = (processor3.current_process.waiting_time + processor3.current_process.count)
                    processor3.current_process.completed_time = current_time + 1
                    self.completed_processes.append(processor3.current_process)
                    processor3.current_process = None
            

            #한 주기 긑
            current_time += 1
    #출력
    def print_results(self):
        print("FCFS")
        print("Process ID | GPT Model | Complexity | Arrival Time | Burst Time | Waiting Time | Turnaround Time | Completed Time")
        for process in self.completed_processes:
            print(f"{process.pid} | {process.gpt_model} | {process.complexity} | {process.arrival_time} | {process.burst_time} | {process.waiting_time} | {process.turnaround_time} | {process.completed_time}")
        P_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "P"])
        E_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "E"])
        print("P코어 총 전력 사용량:",P_cores_power_usage,"W")
        print("E코어 총 전력 사용량:",E_cores_power_usage,"W")
    
                  

class SPN():
    def __init__(self,P, E):    #p코어 e코어 갯수 입력 받음
        super().__init__(P, E)
        self.process_queue = [] #프로세스 큐
        self.ready_queue = []   #레디 큐
        self.completed_processes = []   #완료된 프로세스들 보관하는 리스트

    def add_process(self, process):         #프로세스 할당
        self.process_queue.append(process)  #프로세스 큐에 프로세스 추가
                                            
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
            if not processor0.current_process and self.ready_queue:                 #0번째 프로세서에 존재x, 레디큐에 존재
                if processor0.core_type == "P":                                     #p코어면
                    if self.ready_queue[0].remaining_time > 1 and self.ready_queue[0].complexity > 4:   #복잡도 4초과, 남은시간 1초과
                        processor0.current_process = self.ready_queue.pop(0)                            #p코어(1)에 할당
                elif processor0.core_type == "E":                                                       #E코어
                    if self.ready_queue[0].remaining_time == 1 or self.ready_queue[0].complexity <= 4:  #복잡도 4이하, 남은시간1이면 e코어 할당
                        processor0.current_process = self.ready_queue.pop(0)
                    elif processor1.current_process and processor2.current_process and processor3.current_process:  #나머지 프로세서에 프로세스가 존재하면
                        processor0.current_process = self.ready_queue.pop(0)                                        #프로세서0에 프로세서 할당

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

            #프로세서 별로 전력 계산

            if processor0.current_process:              #0프로세서에 프로세스 있으면
                if processor0.power_on == False:        #꺼져있으면
                    processor0.power_on = True          #키고
                    if processor0.core_type == "P":     #p면
                        processor0.power_usage += 0.5   #시동전력 0.5
                    elif processor0.core_type == "E":   #e면
                        processor0.power_usage += 0.1   #시동전력 0.1
            elif not processor0.current_process:        #프로세서가 없으면
                if processor0.power_on == True:         #켜지있는거
                    processor0.power_on = False         #끄기

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



            #프로세스 처리 매 초마다

            #프로세서0
            if processor0.current_process:
                processor0.current_process.count += 1   #현재 프로세스 카운트+1
                if processor0.core_type == "P":         #p코어이면
                    processor0.current_process.remaining_time -= 2  #남은시간 -2
                elif processor0.core_type == "E":       #e코어면
                    processor0.current_process.remaining_time -= 1  #남은시간 -2
                if processor0.core_type == "P":                     #전력계산
                    processor0.power_usage += 3
                elif processor0.core_type == "E":
                    processor0.power_usage += 1
                
                
                #RT(Remaining Time)가 1이면 레디큐로 0번째로 올리기
                if processor0.current_process.remaining_time == 1: 
                    self.ready_queue.insert(0,processor0.current_process)
                    processor0.current_process=None

                elif processor0.current_process.remaining_time <= 0:  #남은시간이 0보다 작으면 완료니까 WT TT 계산 후 Cp에 올리기
                    #WT 계산 CT - AT - Count
                    processor0.current_process.waiting_time = (current_time - processor0.current_process.arrival_time - processor0.current_process.count + 1)
                    #TT 계산 = WT + Count
                    processor0.current_process.turnaround_time = (processor0.current_process.waiting_time + processor0.current_process.count)
                    #프로세스가 완료된 시간
                    processor0.current_process.completed_time = current_time + 1
                    #완성된 프로세스 리스트에 넣기
                    self.completed_processes.append(processor0.current_process)
                    #프로세서0의 현재 프로세스 비우기
                    processor0.current_process = None

            
            #프로세서1 
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
                    
                   
                elif processor1.current_process.remaining_time == 1: 
                    self.ready_queue.insert(0,processor1.current_process)
                    processor1.current_process=None

                if processor1.current_process.remaining_time <= 0:
                    processor1.current_process.waiting_time = (current_time - processor1.current_process.arrival_time - processor1.current_process.count + 1)
                    processor1.current_process.turnaround_time = processor1.current_process.waiting_time + processor1.current_process.count
                    processor1.current_process.completed_time = current_time + 1
                    self.completed_processes.append(processor1.current_process)
                    processor1.current_process = None
                

            #프로세서2
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
                    
                elif processor2.current_process.remaining_time == 1: 
                    self.ready_queue.insert(0,processor2.current_process)
                    processor2.current_process=None

                if processor2.current_process.remaining_time <= 0:
                    processor2.current_process.waiting_time = (current_time - processor2.current_process.arrival_time - processor2.current_process.count + 1)
                    processor2.current_process.turnaround_time = (processor2.current_process.waiting_time + processor2.current_process.count)
                    processor2.current_process.completed_time = current_time + 1
                    self.completed_processes.append(processor2.current_process)
                    processor2.current_process = None
               

            #프로세서3
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

                if processor3.current_process.remaining_time == 1: 
                    self.ready_queue.insert(0,processor3.current_process)
                    processor3.current_process=None

                elif processor3.current_process.remaining_time <= 0:
                    processor3.current_process.waiting_time = (current_time - processor3.current_process.arrival_time - processor3.current_process.count + 1)
                    processor3.current_process.turnaround_time = (processor3.current_process.waiting_time + processor3.current_process.count)
                    processor3.current_process.completed_time = current_time + 1
                    self.completed_processes.append(processor3.current_process)
                    processor3.current_process = None
            

            #한 주기 긑
            current_time += 1
    #출력
    def print_results(self):
        print("FCFS")
        print("Process ID | GPT Model | Complexity | Arrival Time | Burst Time | Waiting Time | Turnaround Time | Completed Time")
        for process in self.completed_processes:
            print(f"{process.pid} | {process.gpt_model} | {process.complexity} | {process.arrival_time} | {process.burst_time} | {process.waiting_time} | {process.turnaround_time} | {process.completed_time}")
        P_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "P"])
        E_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "E"])
        print("P코어 총 전력 사용량:",P_cores_power_usage,"W")
        print("E코어 총 전력 사용량:",E_cores_power_usage,"W")
class SRTN():
    pass
class HRRN():
    pass
class RoundRobinAlgorithm(SchedulingAlgorithm):
    def __init__(self,P, E):    #p코어 e코어 갯수 입력 받음
        super().__init__(P, E)
        self.process_queue = [] #프로세스 큐
        self.ready_queue = []   #레디 큐
        self.completed_processes = []   #료된 프로세스들 보관하는 리스트
        self.outed_process=[]           #컷팅 프로세스
        self.time_quantum_table = {     #타임 퀀텀 테이블
            (1, 10):  2,
            (11, 20): 4,
            (21, 30): 6,
            (31, 40): 8,
        }
                                            
    def add_process(self, process):         #프로세스 할당
        self.process_queue.append(process)  #프로세스 큐에 프로세스 추가
                                            
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
            #레디큐에 있는 프로세스들 TQ 할당
            if self.ready_queue:                                                #ready큐에 존재하면
                for(lower, upper), quantum in self.time_quantum_table.items():  #TQ테이블 값들에 대해서
                    for process in self.ready_queue:                            
                        if lower <= process.remaining_time <= upper:            
                            process.time_quantum = quantum                      #타임퀀텀 값 정해주기
            #각 코어에 할당
            if not processor0.current_process and self.ready_queue:                 #0번째 프로세서에 존재x, 레디큐에 존재
                if processor0.core_type == "P":                                     #p코어면
                    if self.ready_queue[0].remaining_time > 1 and self.ready_queue[0].complexity > 4:   #복잡도 4초과, 남은시간 1초과
                        processor0.current_process = self.ready_queue.pop(0)                            #p코어(1)에 할당
                elif processor0.core_type == "E":                                                       #E코어
                    if self.ready_queue[0].remaining_time == 1 or self.ready_queue[0].complexity <= 4:  #복잡도 4이하, 남은시간1이면 e코어 할당
                        processor0.current_process = self.ready_queue.pop(0)
                    elif processor1.current_process and processor2.current_process and processor3.current_process:  #나머지 프로세서에 프로세스가 존재하면
                        processor0.current_process = self.ready_queue.pop(0)                                        #프로세서0에 프로세서 할당

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
            

            #프로세서 별로 전력 계산

            if processor0.current_process:              #0프로세서에 프로세스 있으면
                if processor0.power_on == False:        #꺼져있으면
                    processor0.power_on = True          #키고
                    if processor0.core_type == "P":     #p면
                        processor0.power_usage += 0.5   #시동전력 0.5
                    elif processor0.core_type == "E":   #e면
                        processor0.power_usage += 0.1   #시동전력 0.1
            elif not processor0.current_process:        #프로세서가 없으면
                if processor0.power_on == True:         #켜지있는거
                    processor0.power_on = False         #끄기

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


            #프로세스 처리 매 초마다
                                                        #프로세서0에 현재 프로세스가 있으면
            if processor0.current_process:
                processor0.current_process.count += 1   #현재 프로세스 카운트+1
                if processor0.core_type == "P":         #p코어이면
                    processor0.current_process.remaining_time -= 2  #남은시간 -2
                elif processor0.core_type == "E":       #e코어면
                    processor0.current_process.remaining_time -= 1  #남은시간 -2
                if processor0.core_type == "P":                     #전력계산
                    processor0.power_usage += 3
                elif processor0.core_type == "E":
                    processor0.power_usage += 1

                if processor0.current_process.remaining_time <= 0:  #남은시간이 0보다 작으면
                    #WT 계산 CT - AT - Count
                    processor0.current_process.waiting_time = (current_time - processor0.current_process.arrival_time - processor0.current_process.count + 1)
                    #TT 계산 = WT + Count
                    processor0.current_process.turnaround_time = (processor0.current_process.waiting_time + processor0.current_process.count)
                    #프로세스가 완료된 시간
                    processor0.current_process.completed_time = current_time + 1
                    #완성된 프로세스 리스트에 넣기
                    self.completed_processes.append(processor0.current_process)
                    #프로세서0의 현재 프로세스 비우기
                    processor0.current_process = None
                    #remaining_time 존재하면
                elif processor0.current_process.remaining_time > 0:
                    #진행된 시간 /3 햇는데 0이다? -> 타임퀀텀 다 썼다.
                    if (processor0.current_process.burst_time - processor0.current_process.remaining_time) % processor0.current_process.time_quantum == 0:
                        self.ready_queue.append(processor0.current_process)     #레디 큐로 올려버리기
                        processor0.current_process = None                       #프로세스 초기화


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
                if processor2.current_process.remaining_time <= 0:
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
                    processor3.current_process.completed_time = current_time + 1
                    self.completed_processes.append(processor3.current_process)
                    processor3.current_process = None
                elif processor3.current_process.remaining_time > 0:
                    if (processor3.current_process.burst_time - processor3.current_process.remaining_time) % processor3.current_process.time_quantum == 0:
                        self.ready_queue.append(processor3.current_process)
                        processor3.current_process = None

            #한 주기 긑
            current_time += 1

    #출력
    def print_results(self):
        
        print("Process ID | GPT Model | Complexity | Arrival Time | Burst Time | Waiting Time | Turnaround Time | Completed Time")
        for process in self.completed_processes:
            print(f"{process.pid} | {process.gpt_model} | {process.complexity} | {process.arrival_time} | {process.burst_time} | {process.waiting_time} | {process.turnaround_time} | {process.completed_time}")
        P_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "P"])
        E_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "E"])
        print("P코어 총 전력 사용량:",P_cores_power_usage,"W")
        print("E코어 총 전력 사용량:",E_cores_power_usage,"W")

class Main:
    def __init__(self,P, E, N):
        self.P = P  #P코어
        self.E = E  #E코어
        self.N = N  #프로세스 갯수
        self.processes = []
        self.fcfs_algorithm=FCFS(P,E)
        self.rr_algorithm = RoundRobinAlgorithm(P, E)   
#
    def create_process(self):
        for i in range(self.N):
            pid = i + 1 #ID
            arrival_time = random.randint(0,15) #0~15
            gpt_model = random.choice(["GPT 4","GPT 3.5"])  #둘중에 하나
            complexity = random.randint(1,12)               #1~12

            if gpt_model == "GPT 4":
                gpt_multiplier = 2                          
            elif gpt_model == "GPT 3.5":
                gpt_multiplier = 1

            burst_time = complexity * gpt_multiplier        #3*gpt4 = 6
            time_quantum = 0                                
            completed_time = 0

            process = Process(pid, arrival_time, burst_time, completed_time, gpt_model, complexity, time_quantum)
            self.processes.append(process)  #프로세스 리스트에 추가
    
    def run_scheduler_FCFS(self):                
        for process in self.processes:
            self.fcfs_algorithm.add_process(process)  #프로세스 하나씩 rr알고리즘에 추가
        self.fcfs_algorithm.schedule()

    def print_result_FCFS(self):                         #출력
        self.fcfs_algorithm.print_results()
    
    
    
    ##RR
    def run_scheduler_RR(self):                
        for process in self.processes:
            self.rr_algorithm.add_process(process)  #프로세스 하나씩 rr알고리즘에 추가
        self.rr_algorithm.schedule()                #rr알고리즘 실행

    def print_result_RR(self):                         #출력
        self.rr_algorithm.print_results()
            

def main():
    P = 3
    E = 1
    N = 3
    main_program = Main(P, E, N)
    main_program.create_process()                   #프로세스 생성
    main_program.run_scheduler_FCFS()                    #스케줄링
    main_program.print_result_FCFS()                     #출력
    #main_program.run_scheduler_RR()                    #스케줄링
    #main_program.print_result_RR()                     #출력


if __name__ == "__main__":
    main()
