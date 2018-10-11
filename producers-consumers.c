//
// NAME:    producers-consumers.c
// AUTHOR:  Andrew Meijer V00805554
//  This program is based off the code from this URL:
//  https://www.geeksforgeeks.org/use-posix-semaphores-c/

//  I also found an implementation using processes rather than threads:
//  https://www.thecrazyprogrammer.com/2016/09/producer-consumer-problem-c.html


//  I use MinGW on Windows10 and compile with the following command:
//      gcc -pthread producers-consumers.c

#include <windows.h>
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

sem_t mutex;
sem_t items;
//in this sample program, the buffer is only a single element.
int buffer = -1;
//~
short exitFlag = 0;
//startFlag keep program running until a production occurs
short startFlag = 0;

void* producer(void* arg)
{
    int n = 0;
    printf("\nStarting producer thread.\n");
    printf("Produce a number: ");
    scanf("%d",&n);

    startFlag = 1;

    sem_wait(&mutex);

    //critical section
    buffer = n;

    sem_post(&mutex);
    sem_post(&items);

    printf("Exiting producer thread.\n");
}

void* consumer(void* arg)
{
    int n = -1;
    while(!exitFlag){
        sem_wait(&items);
        sem_wait(&mutex);

        //critical section
        if(buffer != -1){
            n = buffer;
            buffer = -1;
            sem_post(&mutex);
            printf("Consumed %d\n", n);
        }else{
            sem_post(&mutex);
            //consumer waits for a production. 1fps-busywait
            sleep(1);
        }
    }
    printf("Exit flag is called. Consumption is over.\n");
}

int main()
{
    sem_init(&mutex, 0, 1);
    sem_init(&items, 0, 0);
    pthread_t prod,cons;
    pthread_create(&prod,NULL,producer,NULL);
    pthread_create(&cons,NULL,consumer,NULL);

    while(buffer != -1 || !startFlag){

    }

    exitFlag = 1;

    pthread_join(prod,NULL);
    pthread_join(cons,NULL);
    sem_destroy(&items);
    sem_destroy(&mutex);
    printf("Exiting Main Thread.\n");
}
