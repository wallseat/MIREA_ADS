#ifndef _QUEUE_H_
#define _QUEUE_H_

#include <inttypes.h>
#include <stdlib.h>
#include <stdio.h>

typedef struct S_Node
{

    int32_t v;
    struct S_Node *prev;

} S_Node;

S_Node *S_Node_init(int32_t);
void S_Node_print(const S_Node*);


typedef struct S_Queue
{

    S_Node *head;
    size_t size;
    uint64_t N_OP;

} S_Queue;


S_Queue *S_Queue_init();
void S_Queue_push(S_Queue*, S_Node*);
S_Node *S_Queue_pop(S_Queue*);
const S_Node *S_Queue_peek(S_Queue*, size_t);
void S_Queue_print(S_Queue *);
size_t S_Queue_len(S_Queue*);
void S_Queue_rotate(S_Queue*);


#endif // _QUEUE_H_