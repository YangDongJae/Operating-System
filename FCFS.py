class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.count = 0  #프로세스에서 돈 시간 카운트


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

        self.total_power_usage = []
                                            
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
                processor.current_process.NTT = round((processor.current_process.turnaround_time) / processor.current_process.count, 1)
                processor.current_process.completed_time = current_time + 1
                self.completed_processes.append((processor.current_process.pid, processor.current_process.arrival_time, processor.current_process.count ,processor.current_process.waiting_time,processor.current_process.turnaround_time,processor.current_process.NTT,processor.current_process.completed_time))
                processor.current_process = None
                     
                                                    
    def schedule(self):                     #스케줄링 함수
        current_time = 0                    #현재 시간 0으로 지정
        processor0 = self.processors[0]     #0번째 프로세서
        processor1 = self.processors[1]     #1번째 프로세서
        processor2 = self.processors[2]     #2번째 프로세서
        processor3 = self.processors[3]     #3번째 프로세서
        self.ready_queue_list = []
        self.list =[]

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
                

            processor0.update_power_status(processor0)
            processor1.update_power_status(processor1)
            processor2.update_power_status(processor2)
            processor3.update_power_status(processor3)    
            

  

            if processor0.current_process:
                self.processor0_queue.append((processor0.current_process.pid,processor0.power_usage))
            else:
                self.processor0_queue.append((0,processor0.power_usage))

            if processor1.current_process:
                self.processor1_queue.append((processor1.current_process.pid,processor1.power_usage))
            else:
                self.processor1_queue.append((0,processor1.power_usage))

            if processor2.current_process:
                self.processor2_queue.append((processor2.current_process.pid,processor2.power_usage))
            else:
                self.processor2_queue.append((0,processor2.power_usage))

            if processor3.current_process:
                self.processor3_queue.append((processor3.current_process.pid, processor3.power_usage))
            else:
                self.processor3_queue.append((0, processor3.power_usage))

            self.total_power_usage.append(round(processor0.power_usage + processor1.power_usage + processor2.power_usage + processor3.power_usage, 1))

            for i in self.ready_queue:
                self.list.append(i.pid)
            
            self.ready_queue_list.append(self.list)
            
            self.list =[]

            #프로세스 처리 매 초마다
            self.update_current_process(processor0, current_time)
            self.update_current_process(processor1, current_time)
            self.update_current_process(processor2, current_time)
            self.update_current_process(processor3, current_time)

           
            current_time += 1
            

    def print_results(self):

        list =[self.processor0_queue,self.processor1_queue,self.processor2_queue,self.processor3_queue, self.total_power_usage, self.completed_processes, self.ready_queue_list]

        return list

class Main:
    def __init__(self, process_select_signal, processor_select_signal):
        self.processes = []
        self.process_select_signal = process_select_signal
        self.fcfs_algorithm = FCFS(processor_select_signal)

    def create_process(self):
        for i in self.process_select_signal:
            pid = i[0]
            arrival_time = i[1]
            burst_time = i[2]
            completed_time = 0

            process = Process(pid, arrival_time, burst_time)
            self.processes.append(process)

    def run_scheduler(self):
        for process in self.processes:
            self.fcfs_algorithm.add_process(process)
        self.fcfs_algorithm.schedule()

    def print_result(self):
        return self.fcfs_algorithm.print_results()
            

def main(Info =[]):
    process_select_signal = Info[0]

    processor_select_signal = Info[1]

    main_program = Main(process_select_signal, processor_select_signal)
    main_program.create_process()
    main_program.run_scheduler()

    return main_program.print_result()



if __name__ == "__main__":
    main()
