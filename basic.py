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
                             #프로세스 초기화


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
                

            #한 주기 긑
            current_time += 1

    #출력
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
    def __init__(self, processor_select_signal):    #p코어 e코어 갯수 입력 받음
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
            
            
            if self.ready_queue:
                self.ready_queue=sorted(self.ready_queue, key=lambda process:process.burst_time)

             #각 코어에 할당, 비선점 할당
            if not processor0.current_process and not processor0.core_type == None and self.ready_queue:                 #0번째 프로세서에 존재x, 레디큐에 존재    
                processor0.current_process = self.ready_queue.pop(0)
                    

            if not processor1.current_process and not processor1.core_type == None and self.ready_queue:                                  
                processor1.current_process = self.ready_queue.pop(0)
                    

            if not processor2.current_process and not processor2.core_type == None and self.ready_queue:
                processor2.current_process = self.ready_queue.pop(0)
                    

            if not processor3.current_process and not processor3.core_type == None and self.ready_queue:
                processor3.current_process = self.ready_queue.pop(0)
                    
            
            #추가 된 부분
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
                

            #한 주기 긑
            current_time += 1

    #출력
    def print_results(self):
        
        print("Process ID | Arrival Time | Burst Time | Waiting Time | Turnaround Time | Completed Time")
        for process in self.completed_processes:
            print(f"{process.pid} | {process.arrival_time} | {process.burst_time} | {process.waiting_time} | {process.turnaround_time} | {process.completed_time}")
        P_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "P"])
        E_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "E"])
        print("P코어 총 전력 사용량:",round(P_cores_power_usage, 1),"W")
        print("E코어 총 전력 사용량:",round(E_cores_power_usage, 1),"W")
        print("총 전력 사용량:",round(P_cores_power_usage+E_cores_power_usage, 1),"W")
        print("프로세서 0에서 작업한 프로세스:", self.processor0_queue)
        print("프로세서 1에서 작업한 프로세스:", self.processor1_queue)
        print("프로세서 2에서 작업한 프로세스:", self.processor2_queue)
        print("프로세서 3에서 작업한 프로세스:", self.processor3_queue)

class SRTN(SchedulingAlgorithm):
    def __init__(self, processor_select_signal):    #p코어 e코어 갯수 입력 받음
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
                                            
    def schedule(self):                     #스케줄링 함수
        current_time = 0                    #현재 시간 0으로 지정
        processor0 = self.processors[0]     #0번째 프로세서
        processor1 = self.processors[1]     #1번째 프로세서
        processor2 = self.processors[2]     #2번째 프로세서
        processor3 = self.processors[3]     #3번째 프로세서

        #순서 : 없으면 할당 -> 코어on/off 및 전력계산 -> RT계산 ->SRTN 선점 결정 
        while self.process_queue or self.ready_queue or processor0.current_process or processor1.current_process or processor2.current_process or processor3.current_process:
            #프로세스큐, 레디큐, 각 프로세스 별로 원소들이 존재하면 반복
            incoming_processes = [proc for proc in self.process_queue if proc.arrival_time == current_time]
            #현재시간과 도착시간이 같은 프로세스 큐안에있는 프로세스들을 모아논 리스트
            for process in incoming_processes:      #AT=CT인 프로세스들을 큐에서 제거하고 레디큐로 내려보냄
                self.process_queue.remove(process)  
                self.ready_queue.append(process)
            
            #레디 큐 정렬, remaining_time이 작은 순으로
            if self.ready_queue:
                self.ready_queue=sorted(self.ready_queue, key=lambda process:process.remaining_time)

            #프로세서 비었을 떼 각 코어에 할당
            #0번째 프로세서에 존재x, 레디큐에 존재
            if not processor0.current_process and not processor0.core_type == None and self.ready_queue:               
                        processor0.current_process = self.ready_queue.pop(0)    #프로세서0에 프로세서 할당
                                                          

            if not processor1.current_process and not processor1.core_type == None and self.ready_queue:                                  
                        processor1.current_process = self.ready_queue.pop(0)
                   

            if not processor2.current_process and not processor2.core_type == None and self.ready_queue:
                        processor2.current_process = self.ready_queue.pop(0)
                    

            if not processor3.current_process and not processor3.core_type == None and self.ready_queue:
                        processor3.current_process = self.ready_queue.pop(0)
                    
            
            #추가 된 부분, 프로세스 처리 순서
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
                             #프로세스 초기화
                
                #STRN 선점 부분
                elif processor0.current_process.remaining_time > 0 and self.ready_queue: #시간 남아있으면 
                        if processor0.current_process.remaining_time > self.ready_queue[0].remaining_time:   #레디큐 0번째의 RT가 0프로세서의 프로세스의 RT보다 작으면
                            tmp = processor0.current_process                                #둘이 교환
                            processor0.current_process = self.ready_queue[0]
                            self.ready_queue[0]=tmp
                       


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
                elif processor1.current_process.remaining_time > 0 and self.ready_queue: #시간 남아있고 레디큐에 존재하면
                        if processor1.current_process.remaining_time > self.ready_queue[0].remaining_time:   #레디큐 0번째의 RT가 0프로세서의 프로세스의 RT보다 작으면
                            tmp = processor1.current_process                                #둘이 교환
                            processor1.current_process = self.ready_queue[0]
                            self.ready_queue[0]=tmp


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
                elif processor2.current_process.remaining_time > 0 and self.ready_queue: #시간 남아있고 레디큐에 존재하면
                        if processor2.current_process.remaining_time > self.ready_queue[0].remaining_time:   #레디큐 0번째의 RT가 0프로세서의 프로세스의 RT보다 작으면
                            tmp = processor2.current_process                                #둘이 교환
                            processor2.current_process = self.ready_queue[0]
                            self.ready_queue[0]=tmp
                

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
                elif processor3.current_process.remaining_time > 0 and self.ready_queue: #시간 남아있고 레디큐에 존재하면
                        if processor3.current_process.remaining_time > self.ready_queue[0].remaining_time:   #레디큐 0번째의 RT가 0프로세서의 프로세스의 RT보다 작으면
                            tmp = processor3.current_process                                #둘이 교환
                            processor3.current_process = self.ready_queue[0]
                            self.ready_queue[0]=tmp

            #한 주기 긑
            current_time += 1

    #출력
    def print_results(self):
        
        print("Process ID | Arrival Time | Burst Time | Waiting Time | Turnaround Time | Completed Time")
        for process in self.completed_processes:
            print(f"{process.pid} | {process.arrival_time} | {process.burst_time} | {process.waiting_time} | {process.turnaround_time} | {process.completed_time}")
        P_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "P"])
        E_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "E"])
        print("P코어 총 전력 사용량:",round(P_cores_power_usage, 1),"W")
        print("E코어 총 전력 사용량:",round(E_cores_power_usage, 1),"W")
        print("총 전력 사용량:",round(P_cores_power_usage+E_cores_power_usage, 1),"W")
        print("프로세서 0에서 작업한 프로세스:", self.processor0_queue)
        print("프로세서 1에서 작업한 프로세스:", self.processor1_queue)
        print("프로세서 2에서 작업한 프로세스:", self.processor2_queue)
        print("프로세서 3에서 작업한 프로세스:", self.processor3_queue)

class HRRN(SchedulingAlgorithm):
    def __init__(self, processor_select_signal):    #p코어 e코어 갯수 입력 받음
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
            
            
            if self.ready_queue:
                self.ready_queue=sorted(self.ready_queue, key=lambda process:((process.waiting_time+process.burst_time)/process.burst_time))

             #각 코어에 할당, 비선점 할당
            if not processor0.current_process and not processor0.core_type == None and self.ready_queue:                 #0번째 프로세서에 존재x, 레디큐에 존재    
                processor0.current_process = self.ready_queue.pop(0)
                    

            if not processor1.current_process and not processor1.core_type == None and self.ready_queue:                                  
                processor1.current_process = self.ready_queue.pop(0)
                    

            if not processor2.current_process and not processor2.core_type == None and self.ready_queue:
                processor2.current_process = self.ready_queue.pop(0)
                    

            if not processor3.current_process and not processor3.core_type == None and self.ready_queue:
                processor3.current_process = self.ready_queue.pop(0)
                    
            
            #추가 된 부분
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
                

            #한 주기 긑
            current_time += 1

    #출력
    def print_results(self):
        
        print("Process ID | Arrival Time | Burst Time | Waiting Time | Turnaround Time | Completed Time")
        for process in self.completed_processes:
            print(f"{process.pid} | {process.arrival_time} | {process.burst_time} | {process.waiting_time} | {process.turnaround_time} | {process.completed_time}")
        P_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "P"])
        E_cores_power_usage = sum([processor.power_usage for processor in self.processors if processor.core_type == "E"])
        print("P코어 총 전력 사용량:",round(P_cores_power_usage, 1),"W")
        print("E코어 총 전력 사용량:",round(E_cores_power_usage, 1),"W")
        print("총 전력 사용량:",round(P_cores_power_usage+E_cores_power_usage, 1),"W")
        print("프로세서 0에서 작업한 프로세스:", self.processor0_queue)
        print("프로세서 1에서 작업한 프로세스:", self.processor1_queue)
        print("프로세서 2에서 작업한 프로세스:", self.processor2_queue)
        print("프로세서 3에서 작업한 프로세스:", self.processor3_queue)


class RRRTN(SchedulingAlgorithm):
    def __init__(self,processor_select_signal):    #p코어 e코어 갯수 입력 받음
        super().__init__(processor_select_signal)
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

        self.processor0_queue = []
        self.processor1_queue = []
        self.processor2_queue = []
        self.processor3_queue = []
                                            
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
            if not processor0.current_process and not processor0.core_type == None and self.ready_queue:                 #0번째 프로세서에 존재x, 레디큐에 존재
                if processor0.core_type == "P":                                     #p코어면
                    if self.ready_queue[0].remaining_time > 1 and self.ready_queue[0].complexity > 4:   #복잡도 4초과, 남은시간 1초과
                        processor0.current_process = self.ready_queue.pop(0)                            #p코어(1)에 할당
                elif processor0.core_type == "E":                                                       #E코어
                    if self.ready_queue[0].remaining_time == 1 or self.ready_queue[0].complexity <= 4:  #복잡도 4이하, 남은시간1이면 e코어 할당
                        processor0.current_process = self.ready_queue.pop(0)
                    elif processor1.current_process and processor2.current_process and processor3.current_process:  #나머지 프로세서에 프로세스가 존재하면
                        processor0.current_process = self.ready_queue.pop(0)                                        #프로세서0에 프로세서 할당

            if not processor1.current_process and not processor1.core_type == None and self.ready_queue:                                  
                if processor1.core_type == "P":
                    if self.ready_queue[0].remaining_time > 1 and self.ready_queue[0].complexity > 4:
                        processor1.current_process = self.ready_queue.pop(0)
                elif processor1.core_type == "E":
                    if self.ready_queue[0].remaining_time == 1 or self.ready_queue[0].complexity <= 4:
                        processor1.current_process = self.ready_queue.pop(0)
                    elif processor0.current_process and processor2.current_process and processor3.current_process:
                        processor1.current_process = self.ready_queue.pop(0)

            if not processor2.current_process and not processor2.core_type == None and self.ready_queue:
                if processor2.core_type == "P":
                    if self.ready_queue[0].remaining_time > 1 and self.ready_queue[0].complexity > 4:
                        processor2.current_process = self.ready_queue.pop(0)
                elif processor2.core_type == "E":
                    if self.ready_queue[0].remaining_time == 1 or self.ready_queue[0].complexity <= 4:
                        processor2.current_process = self.ready_queue.pop(0)
                    elif processor0.current_process and processor1.current_process and processor3.current_process:
                        processor2.current_process = self.ready_queue.pop(0)

            if not processor3.current_process and not processor3.core_type == None and self.ready_queue:
                if processor3.core_type == "P":
                    if self.ready_queue[0].remaining_time > 1 and self.ready_queue[0].complexity > 4:
                        processor3.current_process = self.ready_queue.pop(0)
                elif processor3.core_type == "E":
                    if self.ready_queue[0].remaining_time == 1 or self.ready_queue[0].complexity <= 4:
                        processor3.current_process = self.ready_queue.pop(0)
                    elif processor0.current_process and processor1.current_process and processor2.current_process:
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
        print("P코어 총 전력 사용량:",round(P_cores_power_usage, 1),"W")
        print("E코어 총 전력 사용량:",round(E_cores_power_usage, 1),"W")
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
        self.rrrtn_algorithm = RRRTN(processor_select_signal)


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

        if version=="RRRTN":
            for process in self.processes:
                self.rrrtn_algorithm.add_process(process)  #프로세스 하나씩 rr알고리즘에 추가
            self.rrrtn_algorithm.schedule()                #rr알고리즘 실행

        elif version =="FCFS":
            for process in self.processes:
                self.fcfs_algorithm.add_process(process)  #프로세스 하나씩 rr알고리즘에 추가
            self.fcfs_algorithm.schedule()                #rr알고리즘 실행

        elif version =="RR":
            for process in self.processes:
                self.rr_algorithm.add_process(process)  #프로세스 하나씩 rr알고리즘에 추가
            self.rr_algorithm.schedule()                #rr알고리즘 실행    

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

    def print_result(self, version):                         #출력
        
        if version== "FCFS":
            self.fcfs_algorithm.print_results()
        elif version== "SPN":
            self.spn_algorithm.print_results()
        elif version== "RR":
            self.rr_algorithm.print_results()
        elif version== "RRRTN":
            self.rrrtn_algorithm.print_results()

        elif version=="SRTN":
            self.srtn_algorithm.print_results()
        elif version=="HRRN":
            self.hrrn_algorithm.print_results()


            

def main(version, TQ=0):
        processor_select_signal = [1, 1, 1, 2]         #프로세서 p코어3개, e코어 1개 ,순서대로
        N = 10
        main_program = Main(processor_select_signal, N)

        if TQ==0:
            main_program.create_process(version)                   #프로세스 생성, 
            main_program.run_scheduler(version)                    #스케줄링
            main_program.print_result(version)                     #출력
        else:
            main_program.create_process(version,TQ)                   #프로세스 생성, 
            main_program.run_scheduler(version)                    #스케줄링
            main_program.print_result(version)                     #출력



    #processor_select_signal = [1, 1, 1, 2]         #프로세서 p코어3개, e코어 1개 ,순서대로
    #N = 10
    #main_program = Main(processor_select_signal, N)
    #version="RR"
    #main_program.create_process(version,3)                   #프로세스 생성, 
    #main_program.run_scheduler(version)                    #스케줄링
    #main_program.print_result(version)                     #출력


if __name__ == "__main__":
    main("HRRN")        #RR빼고 그냥 "FCFS", "SPN", "SRTN"
                        #RR은 Time Quantum값 지정 ex) main("RR",3)
