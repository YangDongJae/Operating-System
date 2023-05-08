from typing import List
import random


class Process:
    def __init__(self, process_id: int, arrival_time: int, burst_time: int, complexity: int, gpt_model: str):
        """
        Process 클래스 생성자입니다.
        process_id : 프로세스 ID를 나타냅니다.
        arrival_time : 프로세스 도착 시간을 나타냅니다.
        burst_time : 프로세스 버스트 시간을 나타냅니다.
        complexity : 프로세스 복잡도를 나타냅니다.
        gpt_model : 사용되는 GPT 모델을 나타냅니다. ("GPT4", "Default GPT 3.5" 또는 "Legacy GPT 3.5")
        """
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.complexity = complexity
        self.gpt_model = gpt_model
        self.waiting_time = 0
        self.turnaround_time = 0
        self.normalized_turnaround_time = 0
        self.initial_burst_time = burst_time
        self.last_active_time = 0
        self.start_time = None
    
    def get_process_info(self):
        print("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆")
        print(f'PID : {self.process_id}')
        print(f'AT : {self.arrival_time}')
        print(f'BT : {self.burst_time}')
        print(f'Complexity : {self.complexity}')
        print("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆")

class Processor:
    def __init__(self, processor_id: int, core_type: str):
        """
        Processor 클래스 생성자입니다.
        processor_id : 프로세서 ID를 나타냅니다.
        core_type : 프로세서의 코어 유형을 나타냅니다. ("P" 또는 "E")
        """
        self.processor_id = processor_id
        self.core_type = core_type
        self.total_power_usage = 0.0  # 전체 전력 사용량 속성 초기화
        self.power_on = False
        self.current_process = None
        self.current_time = 0

    def assign_process(self, process: Process):
        # 현재 프로세스를 할당합니다.
        self.current_process = process

    def execute(self):
        # 현재 프로세스가 있는 경우
        if self.current_process.burst_time is not None:
            # 코어 유형에 따른 버스트 시간 감소
            if self.core_type == "P":
                self.current_process.burst_time = max(0, self.current_process.burst_time - 2)
            elif self.core_type == "E":
                self.current_process.burst_time = max(0, self.current_process.burst_time - 1)
            else:
                raise ValueError("Invalid core type")
            # BT시간이 30초 이상이면서, 프로세서에서 30초이상 작업된 프로세스 강제종료
            if self.current_process.initial_burst_time - self.current_process.burst_time >= 30:
                print(f"Process {self.current_process.process_id} has been forcibly terminated.")
                self.current_process = None
    def calculate_initial_power_usage(self):
        if not self.power_on:
            if self.core_type == "P":
                self.total_power_usage += 0.5
                print(f'{self.core_type} TYPE {self.processor_id} Power is On')
                self.power_on = True
            elif self.core_type == "E":
                self.total_power_usage += 0.1
                print(f'{self.core_type} TYPE {self.processor_id} Power is On')
                self.power_on = True
            else:
                raise ValueError("Invalid core type")
        elif self.power_on:
            pass
        
        return self.total_power_usage

    def calculate_power_usage(self):
        """
        프로세서의 전력 사용량을 계산합니다.
        """ 
        # 코어 유형에 따른 전력 사용량 계산
        if self.power_on:
            if self.core_type == "P":
                self.total_power_usage += 3
            elif self.core_type == "E":
                self.total_power_usage += 1
            else:
                raise ValueError("Invalid core type")
                
        return self.total_power_usage
    
    def is_busy(self) -> bool:
        return self.current_process is not None


class SchedulingAlgorithm:
    def __init__(self, no_of_processors: int):
        self.no_of_processors = no_of_processors
        self.processors = [Processor(i, "P") if i < no_of_processors - 1 else Processor(i, "E") for i in range(no_of_processors)]
        self.processes = []

    def add_process(self, process: Process):
        self.processes.append(process)

    def schedule(self):
        raise NotImplementedError("schedule method must be implemented by a subclass")

    def update_quantum(self, remaining_bt: int):
        raise NotImplementedError("update_quantum method must be implemented by a subclass")

    def calculate_avg_response_time(self):
        raise NotImplementedError("calculate_avg_response_time method must be implemented by a subclass")

    def print_results(self):
        raise NotImplementedError("print_results method must be implemented by a subclass")



class RoundRobinAlgorithm(SchedulingAlgorithm):
    def __init__(self, no_of_processors: int):
        super().__init__(no_of_processors)
        self.time_quantum_table = {
            (1, 10): 2,
            (11, 20): 4,
            (21, 30): 6,
            (31, 45): 8,
        }
        self.quantum = 0
        self.completed_processes = []  # 안료된 프로세스 목록 초기화
    
    #정책 추가 가능성에 의한 allocation Policy 분할 개발 하지만 overhead
    def allocation_E_Core(self, process):
        # E 코어 할당 정책
        E_condition1 = process.burst_time == 1
        E_condition2 = process.complexity <= 4
        E_condition3 = all(proc.is_busy() for proc in self.processors if proc.core_type == "P") 
        E_condition4 = any(p for p in self.processors if not p.is_busy() and p.core_type == "E")  # 추가한 조건

        if (E_condition1 or E_condition2 or E_condition3) and E_condition4:
            return True
        else:
            return False

    def allocation_P_Core(self, process):
        # P 코어 할당 정책
        P_condition1 = process.burst_time >= 2
        P_condition2 = process.complexity > 4
        P_condition3 = all(proc.is_busy() for proc in self.processors if proc.core_type == "E")
        P_condition4 = any(p for p in self.processors if not p.is_busy() and p.core_type == "P")  # 추가한 조건
        

        if (P_condition1 or P_condition2 or P_condition3) and P_condition4:
            return True
        else:
            return False
        
    def update_waiting_time(self, current_time: int):
        for process in self.processes:
            if process.arrival_time <= current_time and process.process_id not in [completed_process.process_id for completed_process in self.completed_processes]:
                process.waiting_time += 1


    def schedule(self):  # 대기열을 인자로 받지 않음
        current_time = 0  # 현재 시간 초기화
        self.completed_processes = []  # 완료된 프로세스 목록 초기화
        
        # 프로세스 정렬: arrival_time이 작은 순서대로 정렬
        self.processes.sort(key=lambda x: x.arrival_time)
        # 프로세스들이 남아있거나 프로세서들 중 실행 중인 프로세스가 있는 경우 계속 실행
        while self.processes or any(processor.current_process for processor in self.processors):            
            # 프로세서별로 작업 수행
            for idx, processor in enumerate(self.processors):
                if processor.current_process is None and self.processes:
                    process = self.processes.pop(0)
                    process.get_process_info()
                    
                    # P코어 할당
                    if self.allocation_P_Core(process) == True:
                        assigned = False
                        for p in self.processors:
                            if not p.is_busy() and p.core_type == "P":
                                #추가사항 
                                self.update_quantum(process.burst_time)
                                p.assign_process(process)
                                assigned = True
                                p.calculate_initial_power_usage()  # 프로세서 시동 전력 계산                                
                                break
                        if not assigned:
                            self.processes.insert(0,process)
                            print(f"{process.process_id} is placed back in processes")
                            

                    # E코어 할당
                    elif self.allocation_E_Core(process):
                        assigned = False
                        for p in self.processors:
                            if not p.is_busy() and p.core_type == "E":
                                self.update_quantum(process.burst_time)                                    
                                p.assign_process(process)
                                assigned = True
                                p.calculate_initial_power_usage()  # 프로세서 시동 전력 계산
                                break
                        if not assigned:
                            self.processes.insert(0,process)
                            print(f"{process.process_id} is placed back in processes")
                    else:
                        print("------------ERROR------------")
                        print(process.get_process_info())
                        print(f'{[p.current_process for p in self.processors]}')
                        print("------------ERROR------------")
                        raise Exception("프로세서에 할당되지 않음")
                        
                # 프로세서에 프로세스가 할당된 경우 실행
                elif processor.current_process is not None:
                    remaining_quantum = self.quantum  # Time Quantum을 추적하는 변수를 추가합니다.
                    
                        #할당 시작
                    while remaining_quantum > 0:  # Time Quantum이 남아있는 동안 실행합니다.
                        processor.calculate_power_usage()  # 프로세서 동작 전력 계산
                        processor.execute()  # 프로세서 실행
                        self.update_waiting_time(processor.current_time)
                        print("!!!!!!!!!!!!!")                        
                        if processor.current_process is not None:
                            print(processor.current_process.waiting_time)                            
                        print("!!!!!!!!!!!!!")                     
                        #강제종료 조치 
                        if processor.current_process is None:
                            break
                        processor.current_time += 1
                        remaining_quantum -= 1  # Time Quantum을 감소시킵니다.
                        print("\n======================")
                        print(f'PID : {processor.current_process.process_id}')
                        print(f'PROCESSOR Type : {processor.core_type}')
                        print(f'PROCESSOR ID : {processor.processor_id}')                        
                        print(f'TOTAL USAGE POWER : {processor.total_power_usage}')                    
                        print(f'Initial BT : {processor.current_process.initial_burst_time}')
                        print(f'REMAIN BT : {processor.current_process.burst_time}')
                        print(f'Processing TIME : {processor.current_time}')

                        if remaining_quantum == 0 or processor.current_process.burst_time <= 0:
                            if processor.current_process.burst_time <= 0:
                                remaining_quantum = 0
                                                            
                            if processor.current_process is not None and processor.current_process.burst_time > 0:
                                if processor.current_process not in self.processes:
                                    self.processes.append(processor.current_process)
                                else:
                                    processor.current_process.burst_time = 0

                                print("▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
                                print(f'{[process.burst_time for process in self.processes]}')
                                print("▬▬▬▬▬▬▬▬▬▬▬▬▬▬")                                    
                                processor.current_process = None                                

                            elif processor.current_process is not None and processor.current_process.burst_time <= 0:
                                completed_process = processor.current_process
                                processor.current_process = None
                                                    
                                # 프로세스가 최초로 작업이 시작되는 시점을 저장
                                if not hasattr(completed_process, 'first_execution_start_time'):
                                    completed_process.first_execution_start_time = processor.current_time - self.quantum
                                                        
                                # TT 계산
                                completed_process.turnaround_time = (processor.current_time +  completed_process.arrival_time)- completed_process.arrival_time
                                

                                # WT 계산
                                completed_process.waiting_time = completed_process.waiting_time
                                
                                
                                if completed_process.initial_burst_time != 0:
                                    completed_process.normalized_turnaround_time = completed_process.turnaround_time / completed_process.initial_burst_time
                                else:
                                    completed_process.normalized_turnaround_time = completed_process.turnaround_time
                                self.completed_processes.append(completed_process)

                                print("▬▬▬▬▬COMPLETE▬▬▬▬▬")
                                print(f'{[process.process_id for process in self.completed_processes]}')
                                print("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")                                
                    
                    processor.power_on = False
                    print(f'\n\n Turn off {processor.core_type} type {processor.processor_id} core \n{[processor.power_on for processor in self.processors]}\n\n')
                    
##
##burst time 계산용 TT는 따로 추가해야함
##
    def update_quantum(self, remaining_bt: int):
        for bt_range, quantum in self.time_quantum_table.items():
            lower, upper = bt_range
            if lower <= remaining_bt <= upper:
                self.quantum = quantum
                break

    def calculate_avg_ntt(self) -> float:
        total_ntt = sum(process.normalized_turnaround_time for process in self.completed_processes)
        completed_processes_count = len(self.completed_processes)
        if completed_processes_count == 0:
            raise Exception("모든 프로세스가 강제종료 됨")
        return total_ntt / completed_processes_count



    def print_results(self):
        # 결과 헤더 출력
        print("Process ID | Arrival Time | Burst Time | Waiting Time | Turnaround Time | Normalized Turnaround Time | Completion Time ")
        
        sorted_completed_processes = sorted(self.completed_processes, key=lambda process: process.arrival_time)
        
        # 각 완료된 프로세스에 대한 정보 출력
        for process in sorted_completed_processes:
            completion_time = process.arrival_time + process.turnaround_time
            print(f"    {process.process_id}      |      {process.arrival_time}       |     {process.initial_burst_time}     |      {process.waiting_time}     |        {process.turnaround_time}        |            {round(process.normalized_turnaround_time,2)}             | {completion_time}")
        #AVG NTT 출력
        avg_ntt = self.calculate_avg_ntt()
        print(f"Average NTT : {avg_ntt} time")
        # P 코어와 E 코어의 전력 사용량을 계산하여 출력
        p_cores_power_usage = sum([processor.total_power_usage for processor in self.processors if processor.core_type == "P"])
        e_cores_power_usage = round(sum([processor.total_power_usage for processor in self.processors if processor.core_type == "E"]),2)
        #roud function은 파이썬 부동소수점 연산 결과에서 발생한 파이썬 프로그래밍 언어 자체적 문제
        print(f"P cores total power usage: {p_cores_power_usage} W")
        print(f"E cores total power usage: {e_cores_power_usage} W")
        
        



class MainProgram:
    def random_num_generator(self, M):
        nums = set() 
        while len(nums) != M: 
            nums.add(random.randint(1, M))
        return list(nums)
        
    def __init__(self, N: int, P: int):
        self.N = N  # 프로세스 개수
        self.P = P  # 프로세서 개수
        self.processes = []  # 프로세스 목록 초기화
        self.scheduler = RoundRobinAlgorithm(P)  # 라운드 로빈 스케줄러 생성

    def create_processes(self):
        # 각 프로세스를 생성하고 프로세스 목록에 추가
        # AT_TIMES = [1,2,3,4,100]
        # AT_TIMES = list(range(0,100))
        AT_TIMES = self.random_num_generator(100)
        
        # BT_ITEMS = [3,1,9]
        for i in range(self.N):
            process_id = i + 1
            arrival_time = AT_TIMES.pop(0)
            complexity = random.randint(1, 40)
            gpt_model = random.choice(["GPT4", "Default GPT 3.5", "Legacy GPT 3.5"])

            if gpt_model == "GPT4":
                gpt_multiplier = 1.5
            else:
                gpt_multiplier = 1

            burst_time = int(complexity * gpt_multiplier)
            burst_time = max(1, min(burst_time, 45))
            # burst_time = BT_ITEMS.pop(0)

            process = Process(process_id, arrival_time, burst_time, complexity, gpt_model)
            self.processes.append(process)

    def run_simulation(self):
        # 각 프로세스를 스케줄러에 추가하고 스케줄링 실행
        for process in self.processes:
            self.scheduler.add_process(process)
        self.scheduler.schedule()  # 대기열을 인자로 전달

    def print_final_results(self):
        # 스케줄러를 통해 최종 결과 출력
        self.scheduler.print_results()

def main():
    N = 50  # 프로세스 개수
    P = 4  # 프로세서 개수

    main_program = MainProgram(N, P)
    main_program.create_processes()
    main_program.run_simulation()
    main_program.print_final_results()

if __name__ == "__main__":
    main()