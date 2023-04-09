class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time

def spn(processes):
    # Initialize the waiting time and turnaround time for each process to 0
    waiting_time = [0] * len(processes)
    turnaround_time = [0] * len(processes)

    # Sort the processes by arrival time
    processes.sort(key=lambda x: x.arrival_time)

    # Set the current time to the arrival time of the first process
    current_time = processes[0].arrival_time

    # Keep track of the remaining burst time for each process
    remaining_time = [p.burst_time for p in processes]

    # Keep track of the processes that have completed execution
    completed = 0

    while completed != len(processes):
        # Find the index of the process with the shortest remaining burst time
        min_time = float('inf')
        min_index = -1
        for i in range(len(processes)):
            if processes[i].arrival_time <= current_time and remaining_time[i] < min_time and remaining_time[i] > 0:
                min_time = remaining_time[i]
                min_index = i

        # If no eligible process is found, move the current time to the arrival time of the next process
        if min_index == -1:
            current_time = processes[completed+1].arrival_time
        else:
            # Update the waiting time, remaining time, and current time for the selected process
            waiting_time[min_index] = current_time - processes[min_index].arrival_time
            remaining_time[min_index] -= 1
            current_time += 1

            # If the selected process has completed execution, update the turnaround time and mark it as completed
            if remaining_time[min_index] == 0:
                turnaround_time[min_index] = current_time - processes[min_index].arrival_time
                completed += 1

    # Calculate the average waiting time and turnaround time
    avg_waiting_time = sum(waiting_time) / len(processes)
    avg_turnaround_time = sum(turnaround_time) / len(processes)

    # Print the results
    print("SPN Scheduling:")
    print("Average Waiting Time:", avg_waiting_time)
    print("Average Turnaround Time:", avg_turnaround_time)

# Example usage
processes = [
    Process(1, 0, 6),
    Process(2, 2, 4),
    Process(3, 4, 3),
    Process(4, 5, 5)
]
spn(processes)
