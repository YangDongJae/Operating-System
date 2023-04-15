import heapq

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time

    def __lt__(self, other):    #남은 시간을 기준으로 프로세스 정렬
        return self.remaining_time < other.remaining_time

class SRTN:
    def __init__(self, processes):
        self.processes = processes
        self.current_time = 0
        self.completed_processes = []

    def run(self):
        ready_queue = []
        heapq.heapify(ready_queue)

        while self.processes or ready_queue:    #남은 프로세스가 있거나 ready_queue 상태인 프로세스가 있으면 계속 실행
            if self.processes and self.processes[0].arrival_time == self.current_time:   #현재 시간에 도착한 프로세스가 있는지 확인
                process = self.processes.pop(0) #있으면 프로세스 목록에서 제거
                heapq.heappush(ready_queue, process)    #ready_queue힙에 추가

            if ready_queue: #ready_queue 상태인 프로세스가 있으면
                process = heapq.heappop(ready_queue)    #남은 시간이 가장 짧은 프로세스가 팝업
                process.remaining_time -= 1 #남은 시간 -1

                if process.remaining_time == 0: #남은 시간이 0이 되면
                    process.completion_time = self.current_time + 1 #해당 프로세스 완료시간에 현재시간을 저장
                    self.completed_processes.append(process)    #프로세스가 작업을 완료한것으로 표시
                else:
                    heapq.heappush(ready_queue, process)    #아니면 다시 ready_queue 힙에 추가

            self.current_time += 1  #현재 시간은 반복문이 1번 돌때마다 1씩 추가

    def get_average_waiting_time(self):
        total_waiting_time = 0

        for process in self.completed_processes:
            waiting_time = process.completion_time - process.arrival_time - process.burst_time
            total_waiting_time += waiting_time

        return round(total_waiting_time / len(self.completed_processes), 2)

    def get_average_Turnaround_time(self):
        total_turnaround_time = 0

        for process in self.completed_processes:
            turnaround_time = process.completion_time - process.arrival_time
            total_turnaround_time += turnaround_time

        return round(total_turnaround_time / len(self.completed_processes), 2)

    def get_average_Normalized_time(self):
        total_Normalized_time = 0

        for process in self.completed_processes:
            turnaround_time = process.completion_time - process.arrival_time
            Normalized_time = turnaround_time / process.burst_time
            total_Normalized_time += Normalized_time

        return round(total_Normalized_time / len(self.completed_processes), 2)

processes = [
    Process(1, 0, 3),
    Process(2, 1, 7),
    Process(3, 3, 2),
    Process(4, 5, 5),
    Process(5, 6, 3),
]

scheduler = SRTN(processes)
scheduler.run()
print("Average waiting time:", scheduler.get_average_waiting_time())
print("Average Turnaround Time:",scheduler.get_average_Turnaround_time())
print("Average Normalized Time:",scheduler.get_average_Normalized_time())