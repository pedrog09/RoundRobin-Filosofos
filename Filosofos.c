#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define NUM_FILOSOFOS 5
#define PENSANDO 0
#define COMENDO 1
#define FOME 2
#define ESQUERDA (filosofo + 4) % NUM_FILOSOFOS
#define DIREITA (filosofo + 1) % NUM_FILOSOFOS

pthread_mutex_t mutex;
int estado[NUM_FILOSOFOS];
pthread_cond_t condicao[NUM_FILOSOFOS];

void test(int filosofo) {
    if (estado[filosofo] == FOME && estado[ESQUERDA] != COMENDO && estado[DIREITA] != COMENDO) {
        estado[filosofo] = COMENDO;
        printf("Filósofo %d está comendo\n", filosofo);
        pthread_cond_signal(&condicao[filosofo]);
    }
}

void pegar_hashi(int filosofo) {
    pthread_mutex_lock(&mutex);
    estado[filosofo] = FOME;
    printf("Filósofo %d está com fome\n", filosofo);
    test(filosofo);
    if (estado[filosofo] != COMENDO) {
        pthread_cond_wait(&condicao[filosofo], &mutex);
    }
    pthread_mutex_unlock(&mutex);
}

void largar_hashis(int filosofo) {
    pthread_mutex_lock(&mutex);
    estado[filosofo] = PENSANDO;
    printf("Filósofo %d está pensando\n", filosofo);
    test(ESQUERDA);
    test(DIREITA);
    pthread_mutex_unlock(&mutex);
}

void *filosofo(void *arg) {
    int filosofo = *(int *)arg;
    while (1) {
        sleep(rand() % 3);  // Filósofos pensam por um tempo
        pegar_hashi(filosofo);
        sleep(rand() % 3);  // Filósofos comem por um tempo
        largar_hashis(filosofo);
    }
}

int main() {
    pthread_t filosofos[NUM_FILOSOFOS];
    int id[NUM_FILOSOFOS];

    pthread_mutex_init(&mutex, NULL);

    for (int i = 0; i < NUM_FILOSOFOS; i++) {
        estado[i] = PENSANDO;
        pthread_cond_init(&condicao[i], NULL);
    }

    for (int i = 0; i < NUM_FILOSOFOS; i++) {
        id[i] = i;
        pthread_create(&filosofos[i], NULL, filosofo, &id[i]);
    }

    for (int i = 0; i < NUM_FILOSOFOS; i++) {
        pthread_join(filosofos[i], NULL);
    }

    pthread_mutex_destroy(&mutex);
    for (int i = 0; i < NUM_FILOSOFOS; i++) {
        pthread_cond_destroy(&condicao[i]);
    }

    return 0;
}
