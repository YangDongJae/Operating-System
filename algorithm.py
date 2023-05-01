import queue

class Task:
    def __init__(self, arrival_time, burst_time, priority, model_info):
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.model_info = model_info
        self.remaining_time = burst_time
        self.executions = 0

class Core:
    def __init__(self, core_type):
        self.core_type = core_type
        self.is_busy = False

# 입력 조건
tasks = [
    Task(0, 10, 'paid', 'GPT-4'),
    Task(1, 5, 'free', 'Default GPT-3.5'),
    Task(2, 7, 'paid', 'Legacy GPT-3.5'),
    Task(3, 8, 'free', 'Default GPT-3.5')
]

# 코어 생성
cores = [
    Core('P'),
    Core('P'),
    Core('P'),
    Core('E')
]

def execute_task(task, core):
    core.is_busy = True
    task.executions += 1

# RR 알고리즘 구현
task_queue = queue.Queue()
current_time = 0
total_energy_consumption = 0

for task in tasks:
    task_queue.put(task)

while not task_queue.empty():
    task = task_queue.get()

    while task.arrival_time > current_time:
        current_time += 1

    available_core = None
    busy_cores = []
    for core in cores:
        if not core.is_busy:
            available_core = core
            break
        else:
            busy_cores.append(core)

    if available_core is None:
        available_core = busy_cores.pop(0)
        cores.append(available_core)

    if available_core.core_type == 'P':
        work_done = 2
        energy_consumption = 3
        startup_energy = 0.5
    else:
        work_done = 1
        energy_consumption = 1
        startup_energy = 0.1

    task.remaining_time -= work_done
    total_energy_consumption += energy_consumption + startup_energy

    if task.remaining_time <= 0:
        print(f"Task {tasks.index(task)} completed")
    elif task.executions >= 4:
        print(f"Task {tasks.index(task)} forcefully terminated")
    else:
        task_queue.put(task)

    execute_task(task, available_core)
    current_time += 1

print(f"Total energy consumption: {total_energy_consumption} W")
