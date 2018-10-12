//
// NAME:    readers-writers.c
// AUTHOR:  Andrew Meijer V00805554

//  I use MinGW on Windows10 and compile with the following command:
//      gcc -pthread readers-writers.c

#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

sem_t ms;       //male lightswitch control
sem_t fs;       //female lightswitch control
sem_t e;        //emptiness of the restroom/washroom
sem_t gp;       //multiplex: 3 people maximum.
sem_t lp;       //multiplex: 4 people bathing together is too many. (3 is ok)
int mc = 0;     //counter of the number of male users in lav'
int fc = 0;     //counter of the number of female users in lav'

void* female(void* arg)
{
    sem_wait(&fs);
    fc = fc + 1;
    if(fc == 1){
        sem_wait(&e); // first in locks
    }
    sem_post(&fs);

    sem_wait(&lp);
    printf("A woman uses the bathroom.\n");
    sleep(2);
    sem_post(&lp);

    sem_wait(&fs);
    fc = fc - 1;
    if(fc == 0){
        sem_post(&e); // last out unlocks
    }
    sem_post(&fs);
}

void* male(void* arg)
{
    sem_wait(&ms);
    mc = mc + 1;
    if(mc == 1){
        sem_wait(&e); // first in locks
    }
    sem_post(&ms);

    sem_wait(&gp);
    printf("A man uses the bathroom.\n");
    sleep(1);
    sem_post(&gp);

    sem_wait(&ms);
    mc = mc - 1;
    if(mc == 0){
        sem_post(&e); // last out unlocks
    }
    sem_post(&ms);
}

int main()
{
    sem_init(&e, 0, 1);
    sem_init(&ms, 0, 1);
    sem_init(&fs, 0, 1);
    sem_init(&gp, 0, 3);
    sem_init(&lp, 0, 3);

    pthread_t m1,m2,m3,m4,f1,f2,f3,f4;
    pthread_create(&m1,NULL,male,NULL);
    pthread_create(&m2,NULL,male,NULL);
    pthread_create(&m3,NULL,male,NULL);
    pthread_create(&m4,NULL,male,NULL);
    pthread_create(&f1,NULL,female,NULL);
    pthread_create(&f2,NULL,female,NULL);
    pthread_create(&f3,NULL,female,NULL);
    pthread_create(&f4,NULL,female,NULL);

    pthread_join(m1, NULL);
    pthread_join(m2, NULL);
    pthread_join(m3, NULL);
    pthread_join(m4, NULL);
    pthread_join(f1, NULL);
    pthread_join(f2, NULL);
    pthread_join(f3, NULL);
    pthread_join(f4, NULL);

    sem_destroy(&e);
    sem_destroy(&ms);
    sem_destroy(&fs);
    sem_destroy(&gp);
    sem_destroy(&lp);
    printf("Exiting Main Thread.\n");
    return 0;
}
