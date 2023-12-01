import random
import matplotlib.pyplot as plt

class Processo:
    def __init__(self, identificador, tempo_execucao):
        self.id = identificador
        self.tempo_execucao = tempo_execucao
        self.tempo_espera = 0
        self.tempo_retorno = 0

def round_robin(processos, quantum):
    fila_prontos = processos.copy()
    fila_finalizados = []
    tempo_atual = 0

    while fila_prontos:
        processo_atual = fila_prontos.pop(0)
        processo_atual.tempo_execucao -= quantum
        tempo_atual += quantum

        if processo_atual.tempo_execucao <= 0:
            processo_atual.tempo_espera = tempo_atual - quantum
            processo_atual.tempo_retorno = tempo_atual
            fila_finalizados.append(processo_atual)
        else:
            fila_prontos.append(processo_atual)

    return fila_finalizados

def calcular_metricas(processos):
    total_tempo_espera = 0
    total_tempo_retorno = 0

    for processo in processos:
        total_tempo_espera += processo.tempo_espera
        total_tempo_retorno += processo.tempo_retorno

    tempo_espera_medio = total_tempo_espera / len(processos)
    tempo_retorno_medio = total_tempo_retorno / len(processos)
    vazao = len(processos) / (processos[-1].tempo_retorno)

    return tempo_espera_medio, tempo_retorno_medio, vazao

def main():
    processos = [Processo(i, random.randint(1, 10)) for i in range(10)]

    quantums = [1, 2, 3, 4, 5]
    tempos_espera = []
    tempos_retorno = []
    vazoes = []

    for quantum in quantums:
        fila_finalizados = round_robin(processos, quantum)
        tempo_espera_medio, tempo_retorno_medio, vazao = calcular_metricas(fila_finalizados)

        tempos_espera.append(tempo_espera_medio)
        tempos_retorno.append(tempo_retorno_medio)
        vazoes.append(vazao)

        print("Quantum = {}".format(quantum))
        for processo in fila_finalizados:
            print("Processo {}: tempo de espera = {}, tempo de retorno = {}".format(processo.id, processo.tempo_espera, processo.tempo_retorno))

        print("Média de tempo de espera: {}".format(tempo_espera_medio))
        print("Média de tempo de retorno: {}".format(tempo_retorno_medio))
        print("Vazão: {}".format(vazao))

    # Geração de gráficos
    plt.plot(quantums, tempos_espera, label='Tempo de Espera Médio')
    plt.plot(quantums, tempos_retorno, label='Tempo de Retorno Médio')
    plt.plot(quantums, vazoes, label='Vazão')
    plt.xlabel('Quantum')
    plt.ylabel('Métricas')
    plt.title('Desempenho do Round Robin em diferentes valores de Quantum')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
