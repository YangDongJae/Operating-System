import random
from collections import deque

# 프로세스 실행 시간을 계산하는 수식
# 프로세스 실행 시간을 계산하는 수식
def calculate_bt(complexity, model):
    base_time = random.randint(1, 45)
    if model == "GPT4":
        return min(base_time + (complexity * 2), 45)
    else:
        return min(base_time + complexity, 45)


# Time Quantum Table을 생성
def create_time_quantum_table():
    table = {}
    for i in range(1, 46):
        if i <= 10:
            table[i] = 1
        elif i <= 20:
            table[i] = 2
        elif i <= 30:
            table[i] = 3
        else:
            table[i] = 4
    return table

# 프로세스 스케줄링 알고리즘 구현
def schedule_processes(processes, time_quantum_table):
    p_cores = [0, 0, 0]
    e_core = 0
    queue = deque(processes)
    finished_processes = []

    while queue:
        current_process = queue.popleft()
        at, bt, complexity, model = current_process

        # 프로세서 할당 정책 적용
        if bt == 1 or complexity <= 5 or sum(p_cores) == 3 and e_core == 0:
            time_quantum = 1
            remaining_bt = bt - time_quantum
            e_core += time_quantum
        else:
            time_quantum = min(time_quantum_table[bt], 2)
            remaining_bt = bt - time_quantum
            min_p_core_idx = p_cores.index(min(p_cores))
            p_cores[min_p_core_idx] += time_quantum

        # 프로세스 종료 여부 확인 및 처리
        if remaining_bt <= 0 or bt >= 30:
            finished_processes.append(current_process)
        else:
            queue.append((at, remaining_bt, complexity, model))

    return finished_processes

# 예제 프로세스 생성
processes = [
    (0, calculate_bt(5, "GPT4"), 5, "GPT4"),
    (1, calculate_bt(10, "Default GPT 3.5"), 10, "Default GPT 3.5"),
    (2, calculate_bt(15, "Legacy GPT 3.5"), 15, "Legacy GPT 3.5"),
    (3, calculate_bt(20, "GPT4"), 20, "GPT4"),
]

# Time Quantum Table 생성
time_quantum_table = create_time_quantum_table()

# 프로세스 스케줄링
finished_processes = schedule_processes(processes, time_quantum_table)
print(finished_processes)
