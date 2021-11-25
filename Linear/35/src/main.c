#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <inttypes.h>

#include "queue.h"

void fill_test_data(S_Queue *queue, size_t count)
{
    srand(time(NULL));

    while (count--) S_Queue_push(queue, S_Node_init(rand() % 300));
}


S_Node *_pop_by_pos(S_Queue *queue, size_t pos)
{
    if (queue->size - 1 < pos) 
    {
        fprintf(stderr, "Out of bound! Queue size: %li, pop position: %li\n", queue->size, pos);
        exit(EXIT_FAILURE);
    }
    if(!pos) return S_Queue_pop(queue);

    size_t before = pos;
    size_t after = S_Queue_len(queue) - pos;

    S_Node *node;

    while (before--) S_Queue_rotate(queue);
    node = S_Queue_pop(queue);
    while (--after) S_Queue_rotate(queue);
    
    return node;
}

void _push_by_pos(S_Queue *queue, S_Node *node, size_t pos)
{
    if (pos >= queue->size) 
    {
        S_Queue_push(queue, node);
        return;
    }
   
    size_t before = pos;
    size_t after = S_Queue_len(queue) - pos;

    while(before--) S_Queue_rotate(queue);
    S_Queue_push(queue, node);
    while(after--) S_Queue_rotate(queue);
    
}

void _quick_sort(S_Queue *queue, int32_t left, int32_t right)
{
    int32_t i = left;
    int32_t j = right;

    const S_Node *pivot = S_Queue_peek(queue, (i + j) / 2);
    S_Node *temp;

    do
    {
        while(S_Queue_peek(queue, i)->v < pivot->v) i++;
        while(S_Queue_peek(queue, j)->v > pivot->v) j--;

        if (i <= j)
        {
            if (i < j)
            {
                 temp = _pop_by_pos(queue, i);
                _push_by_pos(queue, _pop_by_pos(queue, j - 1), i);
                _push_by_pos(queue, temp, j);
            }
            i++;
            j--;
        }

        // printf("i: %i, j: %i\n", i, j);
        // S_Queue_print(queue);
    
    } while (i < j);

    if (left < j)
        _quick_sort(queue, left, j);
    if (i < right)
        _quick_sort(queue, i, right);

}

void quick_sort(S_Queue *queue)
{
    _quick_sort(queue, 0, S_Queue_len(queue) - 1);
}

int main(int argc, char **argv)
{
    int nums;
    if (argc > 2) exit(EXIT_FAILURE);
    if (argc == 1) nums = 100;
    else nums = atoi(argv[1]);

    S_Queue *queue = S_Queue_init();
    fill_test_data(queue, nums);
    printf("Current queue: ");
    S_Queue_print(queue);
    time_t t_start = time(NULL);
    quick_sort(queue);
    time_t t_stop = time(NULL);
    printf("Sorted queue: ");
    S_Queue_print(queue);
    printf("N_OP: %li\nTime: %lf\n", queue->N_OP, difftime(t_stop, t_start));



    return 0;
}