class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = 0

def SPN(processes):
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    burst_time = [process.burst_time for process in processes]
    time_elapsed = 0
    
    while True:
        remaining_processes = [process for process in processes if process.burst_time > 0]
        if not remaining_processes:
            break
        
        shortest_process = min(remaining_processes, key=lambda process: process.burst_time)
        index = processes.index(shortest_process)
        
        if processes[index].burst_time == burst_time[index]:
            processes[index].start_time = max(time_elapsed, processes[index].arrival_time)
        
        processes[index].burst_time -= 1
        time_elapsed += 1
        
        if processes[index].burst_time == 0:
            waiting_time[index] = time_elapsed - processes[index].arrival_time - burst_time[index]
            turnaround_time[index] = time_elapsed - processes[index].arrival_time
    
    return waiting_time, turnaround_time

if __name__ == '__main__':
    # Create some sample processes
    processes = [
        Process(1, 0, 6),
        Process(2, 1, 8),
        Process(3, 2, 7),
        Process(4, 3, 3),
        Process(5, 4, 4)
    ]
    
    # Run the SPN algorithm on the processes
    waiting_time, turnaround_time = SPN(processes)
    
    # Print the results
    print("Process\tWaiting Time\tTurnaround Time")
    for i in range(len(processes)):
        print(f"{processes[i].pid}\t{waiting_time[i]}\t\t{turnaround_time[i]}")
    
    # Calculate and print the average waiting time and average turnaround time
    avg_waiting_time = sum(waiting_time) / len(waiting_time)
    avg_turnaround_time = sum(turnaround_time) / len(turnaround_time)
    print(f"\nAverage Waiting Time: {avg_waiting_time}")
    print(f"Average Turnaround Time: {avg_turnaround_time}")
