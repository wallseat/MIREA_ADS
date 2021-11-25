#include "queue.h"

S_Node *S_Node_init(int32_t v)
{
    S_Node *node = (S_Node*) malloc(sizeof(S_Node)); 
    node->prev = NULL;
    node->v = v;

    return node;
}

void S_Node_print(const S_Node *node)
{
    printf("%i ", node->v);
}

S_Queue *S_Queue_init()
{
    S_Queue *queue = (S_Queue*) malloc(sizeof(S_Queue));
    queue->head = NULL;
    queue->size = 0;
    queue->N_OP = 0;

    return queue;
}

void S_Queue_push(S_Queue *queue, S_Node *node)
{
    if (!queue->size) // 1
    {
        queue->head = node; // 2
        queue->N_OP += 2;
    }
    else
    {
        S_Node *tail = queue->head; // 2
        while (tail->prev) { // 1
            tail = tail->prev; // 2
            queue->N_OP += 3;
        } // size - 1

        tail->prev = node; // 2
        node->prev = NULL; // 2
        queue->N_OP += 6;
    }
    queue->size++;

    queue->N_OP += 2;
}

S_Node *S_Queue_pop(S_Queue *queue)
{
    if (!queue->size) 
    {
        fprintf(stderr, "Invalaid opertion pop! Queue is empty!\n");
        exit(EXIT_FAILURE);
    }
    
    S_Node *node = queue->head; // 2
    queue->head = node->prev; // 3
    node->prev = NULL; // 2
    queue->size--; // 2
    
    queue->N_OP += 9;

    return node;    
}

void S_Queue_print(S_Queue *queue)
{
    if (!queue->size) return;
    else
    {
        S_Node *node = queue->head;
        while(node != NULL)
        {
            S_Node_print(node);
            node = node->prev;
        }
        printf("\n");
    }
}

size_t S_Queue_len(S_Queue *queue)
{
    return queue->size;
}

void S_Queue_rotate(S_Queue *queue)
{
    if(queue->size < 2) return;
    S_Queue_push(queue, S_Queue_pop(queue));
}

const S_Node *S_Queue_peek(S_Queue *queue, size_t pos)
{
    S_Node *node = queue->head; // 2
    queue->N_OP += 2;
    while (pos--) // 1
    {
        node = node->prev; // 2
        queue->N_OP += 3;
    }
    return node;
}