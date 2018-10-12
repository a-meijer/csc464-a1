//
// NAME:    readers-writers.c
// AUTHOR:  Andrew Meijer V00805554

//  I use MinGW on Windows10 and compile with the following command:
//      gcc -pthread readers-writers.c

#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

sem_t mutex;
sem_t roomEmpty;
int readers = 0;
//each writer has to tell main it is done.
short doneWriting = 0;
//in this program, the writing is an integer for simplicity.
int writing = 0;

void* writer(void* arg)
{
    int w = 0;
    printf("\nStarting new writer thread.\n");
    printf("Write a number: \n");
    scanf("%d",&w);

    sem_wait(&roomEmpty);
    //critical section
    writing = w;
    sem_post(&roomEmpty);

    printf("Writing is finished.\n");
    doneWriting = 1;
}

void* reader(void* arg)
{
    sem_wait(&mutex);
    readers = readers + 1;
    if(readers == 1){
        sem_wait(&roomEmpty);
    }
    sem_post(&mutex);
    //each reader reads for 2 seconds.
    printf("There are now %d readers reading \"%d\".\n", readers, writing);
    sleep(2);

    sem_wait(&mutex);
    readers = readers - 1;
    if(readers == 0){
        sem_post(&roomEmpty);
    }
    sem_post(&mutex);
}

int main()
{
    sem_init(&mutex, 0, 1);
    sem_init(&roomEmpty, 0, 1);

    pthread_t r1,r2,r3,w1,w2;
    pthread_create(&w1,NULL,writer,NULL);
    pthread_create(&r1,NULL,reader,NULL);

    while(!doneWriting){
        // don't worry. be happy. -_-
    }

    doneWriting = 0;
    pthread_create(&w2,NULL,writer,NULL);
    pthread_create(&r2,NULL,reader,NULL);
    pthread_create(&r3,NULL,reader,NULL);

    while(!doneWriting){}

    sem_destroy(&mutex);
    sem_destroy(&roomEmpty);
    printf("Exiting Main Thread.\n");
    return 0;
}
