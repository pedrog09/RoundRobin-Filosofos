import random
import matplotlib.pyplot as plt

class Process:
    def __init__(self, process_id, burst_time):
        self.id = process_id
        self.burst_time = burst_time
        self.wait_time = 0
        self.turnaround_time = 0

def round_robin(processes, quantum):
    ready_queue = processes.copy()
    finished_queue = []
    current_time = 0

    while ready_queue:
        current_process = ready_queue.pop(0)
        current_process.burst_time -= quantum
        current_time += quantum

        if current_process.burst_time <= 0:
            current_process.wait_time = current_time - quantum
            current_process.turnaround_time = current_time
            finished_queue.append(current_process)
        else:
            ready_queue.append(current_process)

    return finished_queue

def calculate_metrics(processes):
    total_wait_time = 0
    total_turnaround_time = 0

    for process in processes:
        total_wait_time += process.wait_time
        total_turnaround_time += process.turnaround_time

    average_wait_time = total_wait_time / len(processes)
    average_turnaround_time = total_turnaround_time / len(processes)
    throughput = len(processes) / (processes[-1].turnaround_time)

    return average_wait_time, average_turnaround_time, throughput

def main():
    processes = [Process(i, random.randint(1, 10)) for i in range(10)]

    quantums = [1, 2, 3, 4, 5]
    wait_times = []
    turnaround_times = []
    throughputs = []

    for quantum in quantums:
        finished_queue = round_robin(processes, quantum)
        average_wait_time, average_turnaround_time, throughput = calculate_metrics(finished_queue)

        wait_times.append(average_wait_time)
        turnaround_times.append(average_turnaround_time)
        throughputs.append(throughput)

        print("Quantum = {}".format(quantum))
        for process in finished_queue:
            print("Processo {}: tempo de espera = {}, tempo de retorno = {}".format(process.id, process.wait_time, process.turnaround_time))

        print("Média de tempo de espera: {}".format(average_wait_time))
        print("Média de tempo de retorno: {}".format(average_turnaround_time))
        print("Vazão: {}".format(throughput))

    # Geração de gráficos
    plt.plot(quantums, wait_times, label='Tempo de Espera Médio')
    plt.plot(quantums, turnaround_times, label='Tempo de Retorno Médio')
    plt.plot(quantums, throughputs, label='Vazão')
    plt.xlabel('Quantum')
    plt.ylabel('Métricas')
    plt.title('Desempenho do Round Robin em diferentes valores de Quantum')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
