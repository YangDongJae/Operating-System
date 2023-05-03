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

    def assign_process(self, process: Process):
        # 현재 프로세스를 할당합니다.
        self.current_process = process

    def execute(self):
        # 현재 프로세스가 있는 경우
        if self.current_process is not None:
            self.calculate_power_usage()  # 프로세스 실행 전 전력 사용량 계산 호출
            # 코어 유형에 따른 버스트 시간 감소
            if self.core_type == "P":
                self.current_process.burst_time -= 2
            elif self.core_type == "E":
                self.current_process.burst_time -= 1
            else:
                raise ValueError("Invalid core type")

            # 버스트 시간이 0 이하인 경우 프로세스 종료
            if self.current_process.burst_time <= 0:
                self.current_process = None

    def calculate_power_usage(self):
        """
        프로세서의 전력 사용량을 계산합니다.
        """
        if not self.power_on:
            # 코어 유형에 따른 전력 사용량 초기화
            if self.core_type == "P":
                self.total_power_usage += 0.5
            elif self.core_type == "E":
                self.total_power_usage += 0.1
            else:
                raise ValueError("Invalid core type")

            self.power_on = True

        if self.current_process is not None:
            # 코어 유형에 따른 전력 사용량 계산
            if self.core_type == "P":
                self.total_power_usage += 3
            elif self.core_type == "E":
                self.total_power_usage += 1
            else:
                raise ValueError("Invalid core type")

        return self.total_power_usage


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

    def schedule(self):
        current_time = 0  # 현재 시간 초기화
        self.completed_processes = []  # 완료된 프로세스 목록 초기화

        # 프로세스 정렬: arrival_time이 작은 순서대로 정렬
        self.processes.sort(key=lambda x: x.arrival_time)

        # 프로세스들이 남아있거나 프로세서들 중 실행 중인 프로세스가 있는 경우 계속 실행
        while self.processes or any(processor.current_process for processor in self.processors):
            # 프로세서별로 작업 수행
            for processor in self.processors:
                if processor.current_process is None and self.processes:
                    # 현재 시간이 프로세스의 arrival_time보다 크거나 같은 경우에만 프로세스 할당
                    if current_time >= self.processes[0].arrival_time:
                        process = self.processes.pop(0)
                        process.waiting_time += current_time - process.last_active_time
                        processor.assign_process(process)
                        self.update_quantum(process.burst_time)

                # 프로세서에 프로세스가 할당된 경우 실행
                if processor.current_process is not None:
                    remaining_bt = processor.current_process.burst_time
                    for _ in range(self.quantum):
                        processor.execute()  # 프로세서 실행
                        current_time += 1  # 시간 증가
                        if processor.current_process is None:
                            break

                    # 프로세서의 현재 프로세스가 남아있는 경우 다시 대기열에 추가
                    if processor.current_process is not None:
                        processor.current_process.last_active_time = current_time
                        self.processes.append(processor.current_process)
                        processor.current_process = None
                    # 프로세서의 현재 프로세스가 완료된 경우 completed_processes에 추가
                    else:
                        completed_process = process
                        completed_process.turnaround_time = current_time - completed_process.arrival_time + completed_process.waiting_time
                        if completed_process.initial_burst_time != 0:
                            completed_process.normalized_turnaround_time = completed_process.turnaround_time / completed_process.initial_burst_time
                        else:
                            completed_process.normalized_turnaround_time = completed_process.turnaround_time
                        self.completed_processes.append(completed_process)

            # 모든 프로세서가 비어있고 대기열에 프로세스가 남아있는 경우 현재 시간을 증가시킴
            if not any(processor.current_process for processor in self.processors) and self.processes:
                current_time += 1


    def update_quantum(self, remaining_bt: int):
        for bt_range, quantum in self.time_quantum_table.items():
            lower, upper = bt_range
            if lower <= remaining_bt <= upper:
                self.quantum = quantum
                break

    def calculate_avg_response_time(self):
        total_response_time = sum([process.waiting_time for process in self.processes])
        return total_response_time / len(self.processes)

    def print_results(self):
        # 결과 헤더 출력
        print("Process ID | Arrival Time | Burst Time | Waiting Time | Turnaround Time | Normalized Turnaround Time | Completion Time")
        # 각 완료된 프로세스에 대한 정보 출력
        for process in self.completed_processes:
            completion_time = process.arrival_time + process.turnaround_time
            print(f"{process.process_id} | {process.arrival_time} | {process.initial_burst_time} | {process.waiting_time} | {process.turnaround_time} | {process.normalized_turnaround_time} | {completion_time}")
        
        # P 코어와 E 코어의 전력 사용량을 계산하여 출력
        p_cores_power_usage = sum([processor.total_power_usage for processor in self.processors if processor.core_type == "P"])
        e_cores_power_usage = sum([processor.total_power_usage for processor in self.processors if processor.core_type == "E"])
        print(f"P cores total power usage: {p_cores_power_usage} units")
        print(f"E cores total power usage: {e_cores_power_usage} units")


class MainProgram:
    def __init__(self, N: int, P: int):
        self.N = N  # 프로세스 개수
        self.P = P  # 프로세서 개수
        self.processes = []  # 프로세스 목록 초기화
        self.scheduler = RoundRobinAlgorithm(P)  # 라운드 로빈 스케줄러 생성

    def create_processes(self):
        # 각 프로세스를 생성하고 프로세스 목록에 추가
        for i in range(self.N):
            process_id = i + 1
            arrival_time = random.randint(1, 100)
            complexity = random.randint(1, 30)
            gpt_model = random.choice(["GPT4", "Default GPT 3.5", "Legacy GPT 3.5"])

            if gpt_model == "GPT4":
                gpt_multiplier = 1.5
            else:
                gpt_multiplier = 1

            burst_time = int(complexity * gpt_multiplier)
            burst_time = max(1, min(burst_time, 45))

            process = Process(process_id, arrival_time, burst_time, complexity, gpt_model)
            self.processes.append(process)

    def run_simulation(self):
        # 각 프로세스를 스케줄러에 추가하고 스케줄링 실행
        for process in self.processes:
            self.scheduler.add_process(process)

        self.scheduler.schedule()

    def print_final_results(self):
        # 스케줄러를 통해 최종 결과 출력
        self.scheduler.print_results()

def main():
    N = 10  # 프로세스 개수
    P = 4  # 프로세서 개수

    main_program = MainProgram(N, P)
    main_program.create_processes()
    main_program.run_simulation()
    main_program.print_final_results()

if __name__ == "__main__":
    main()