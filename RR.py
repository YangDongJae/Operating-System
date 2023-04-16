from collections import deque

def round_robin(processes, quantum):
    ready_queue = deque(processes)
    total_time = 0
    while ready_queue:
        process = ready_queue.popleft()
        if process["burst_time"] > quantum:
            total_time += quantum
            process["burst_time"] -= quantum
            ready_queue.append(process)
        else:
            total_time += process["burst_time"]
            process["completion_time"] = total_time
    return processes
