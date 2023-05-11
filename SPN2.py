'''
SPN (Shortest-Process-Next)

Non-preemptive scheduling -> 한 프로세스는 끝까지 처리
스케줄링 기준(Criteria) -> BT이 작은 프로세스부터 처리
'''


# 각 프로세스는 Process ID, Arrival time, Burst time을 멤버 변수로 가짐
class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time

def spn(processes):
    # Initialize the waiting time and turnaround time for each process to 0
    # 0으로 main에서 입력받은 processes 리스트의 길이에 따라 WT, TT, NTT를 초기화함.
    waiting_time = [0] * len(processes)
    turnaround_time = [0] * len(processes)
    normalized_TT = [0] * len(processes)

    # Sort the processes by arrival time
    # 각 프로세스는 process[1]와 같은 방식으로 호출.
    # 우선 Arrival time 기준으로 정렬
    processes.sort(key=lambda x: x.arrival_time)

    # Set the current time to the arrival time of the first process
    # 가장 먼저 들어온 프로세서의 Arrival time으로 current time 설정
    current_time = processes[0].arrival_time

    # Keep track of the remaining burst time for each process
    # 남은 시간을 추적하기 위해 list comprehension을 이용해
    # 각 프로세서의 Burst time으로 초기화
    remaining_time = [p.burst_time for p in processes]

    # Keep track of the processes that have completed execution
    # 스케줄링 종료 시점을 위한 계산 완료된 프로세서 수
    completed = 0

    # preemption 방지를 위한 변수 선언
    exist_process = False
    
    print("SPN Scheduling:")
    # 모든 프로세스의 연산이 끝나면 종료
    while completed != len(processes):
        # print(remaining_time)
        # Find the index of the process with the shortest remaining burst time
        # 가장 짧은 BT를 가진 프로세스를 찾음.
        if exist_process is False:
            min_time = float('inf')
            min_index = -1

            for i in range(len(processes)):
                # 처음에는 들어온 프로세스가 없으므로 Arrival Time이 빠른 프로세스부터 처리
                # 이후에는 remaining_time 리스트에 담겨있는 Burst Time이 적은 프로세스부터 처리
                if processes[i].arrival_time <= current_time and remaining_time[i] < min_time and remaining_time[i] > 0:
                    min_time = remaining_time[i]
                    min_index = i
                    exist_process = True

        # If no eligible process is found, move the current time to the arrival time of the next process
        # Arrival time이 가장 빠른 프로세스가 처리가 불가능 상태일 경우
        # 다음 프로세스의 Arrival time으로 Current time을 바꿔줌
        if min_index == -1:
            current_time = processes[completed+1].arrival_time
        else:
            # Update the waiting time, remaining time, and current time for the selected process
            # 프로세스를 처리할 때의 연산들
            # 잔여시간(Remaing time) 1 감소, 현재 시간(Current time) 1 증가

            # 현재 시간 - Arrival Time = Waiting time => 알고리즘에서 적절치 않음
            # waiting_time[min_index] = current_time - \
            #     processes[min_index].arrival_time

            # print(f"P{processes[min_index].pid}'s waiting time = {waiting_time}")
            remaining_time[min_index] -= 1
            current_time += 1

            # If the selected process has completed execution, update the turnaround time and mark it as completed
            # 프로세스의 처리가 완료되었을 때의 연산들
            # TT = Current time - Arrival time, 완료된 프로세스 수(completed) 1 증가
            if remaining_time[min_index] == 0:
                turnaround_time[min_index] = current_time - \
                    processes[min_index].arrival_time
                # WT = TT - BT 이므로 WT를 아래처럼 계산, 계산 결과를 이용해서 NTT도 구해줌
                waiting_time[min_index] = turnaround_time[min_index] - processes[min_index].burst_time
                normalized_TT[min_index] = turnaround_time[min_index] / processes[min_index].burst_time

                completed += 1
                exist_process = False
                # 각 프로세스별 핵심 정보 출력
                print(f"P{processes[min_index].pid}'s info => WT : {str(waiting_time[min_index]).rjust(2)}    TT : {str(turnaround_time[min_index]).rjust(2)}   NTT : {normalized_TT[min_index]:.2f}")

    # Calculate the average waiting time and turnaround time
    # 평균 WT와 평균 TT 계산
    avg_waiting_time = sum(waiting_time) / len(processes)
    avg_turnaround_time = sum(turnaround_time) / len(processes)

    # Print the results
    # 결과 출력
    print("Average Waiting Time:", avg_waiting_time)
    print("Average Turnaround Time:", avg_turnaround_time)


# 예시 프로세스를 담는 리스트
processes = [
    Process(1, 0, 3),
    Process(2, 1, 7),
    Process(3, 3, 2),
    Process(4, 5, 5),
    Process(5, 6, 3)
]

# SPN 함수 호출
spn(processes)
