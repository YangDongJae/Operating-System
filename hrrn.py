class Process:
    def __init__(self, pid, arrival_time, service_time):        #PID : 프로세스 번호, 도착시간, BT
        self.pid = pid
        self.arrival_time = arrival_time            #도착 시간
        self.service_time = service_time            #버스트 시간(BT)
        self.start_time = 0                         #할당 시작 시간
        self.completion_time = 0                    #완료 시간
        self.waiting_time = 0                       #대기한 시간
        self.turnaround_time = 0                    #프로세스 처리 부탁한 후 종료된 시간(기다린 시간(WT) + 실행시간(BT))=TT
        self.response_ratio = 0                     ##응답률(WT+BT)/BT
 
    def __repr__(self):
        return f"Process({self.pid}, {self.arrival_time}, {self.service_time})"
 
def hrrn_scheduling(processes):
    # 프로세스 실행 순서를 저장할 리스트
    process_order = []
    # 현재 시간
    current_time = 0
 
    while len(processes) > 0:
        # 대기 중인 모든 프로세스에 대해 Response Ratio를 계산한다.
        for process in processes:
            if current_time >= process.arrival_time:
                # 대기 시간 + 서비스 시간 / 서비스 시간
                process.response_ratio = (current_time - process.arrival_time + process.service_time) / process.service_time
            else:
                # 아직 도착하지 않은 프로세스는 Response Ratio를 계산할 수 없다.
                process.response_ratio = 0
 
        # Response Ratio가 가장 높은 프로세스를 실행한다.
        next_process = max(processes, key=lambda x: x.response_ratio)
 
        #다음 프로세스의 시작 시간, 완료 시간, 대기 시간, Turnaround Time을 계산한다.
        next_process.start_time = current_time                                                  #다음 프로세스 시작 시간   : 현재시간
        next_process.completion_time = current_time + next_process.service_time                 #다음 프로세스 완료 시간   : 현재시간 + 다음 프로세스 버스터 시간
        next_process.waiting_time = current_time - next_process.arrival_time                    #다음 프로세스 기다린 시간 : 현재시간 - 다음 프로세스 도착 시간
        next_process.turnaround_time = next_process.waiting_time + next_process.service_time    #다음 프로세스 총 시간     :             
 
        # 실행한 프로세스를 실행 순서 리스트에 추가한다.
        process_order.append(next_process.pid)
 
        # 현재 시간을 업데이트하고 실행한 프로세스를 리스트에서 제거한다.
        current_time = next_process.completion_time
        processes.remove(next_process)
 
    return process_order

processes = [
    Process(1, 0, 5),   
    Process(2, 1, 3),
    Process(3, 2, 8),
    Process(4, 3, 6)
]

process_order = hrrn_scheduling(processes)
print(process_order)  # [1, 2, 4, 3]