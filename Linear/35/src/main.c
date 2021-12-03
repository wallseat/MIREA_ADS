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


S_Node *_pop_by_pos(S_Queue *queue, size_t pos) // 3 + 10 + 1 + 2 + 10 + 2nk + 15k + 2n^2 + 13n - 2kn - 15k - 15 = 2n^2 + 13n + 11
{
    if (queue->size - 1 < pos)  // 3
    {
        fprintf(stderr, "Out of bound! Queue size: %li, pop position: %li\n", queue->size, pos);
        exit(EXIT_FAILURE);
    }
    if(!pos) return S_Queue_pop(queue); // 10

    size_t before = pos; // 1
    size_t after = S_Queue_len(queue) - pos; // 2

    S_Node *node;

    while (before--) S_Queue_rotate(queue); // k * (2n + 14 + 1) = 2nk + 15k
    node = S_Queue_pop(queue); // 10
    while (--after) S_Queue_rotate(queue); // (n - k - 1) * (2n + 14 + 1) = 2n^2 + 13n - 2kn - 15k - 15
    
    return node;
}

void _push_by_pos(S_Queue *queue, S_Node *node, size_t pos) // 1 + 3 + 2n + 3 + 2nk + 15k + 2n^2 + 15n - 2nk - 15k = 2n^2 + 17n + 7
{
    if (pos >= queue->size) // 2
    {
        S_Queue_push(queue, node); // 2n + 3
        return;
    }
   
    size_t before = pos; // 1
    size_t after = S_Queue_len(queue) - pos; // 3

    while(before--) S_Queue_rotate(queue); // k * (2n + 14 + 1) = 2nk + 15k
    S_Queue_push(queue, node); // 2n + 3
    while(after--) S_Queue_rotate(queue); // (n - k) * (2n + 15) = 2n^2 + 15n - 2nk - 15k
    
}

void _quick_sort(S_Queue *queue, int32_t left, int32_t right) // 2n^3 * log(n) + 5
{
    int32_t i = left; // 1
    int32_t j = right; // 1

    const S_Node *pivot = S_Queue_peek(queue, (i + j) / 2); // 2 * ((i + j) / 2) + 1 = i + j + 1
    S_Node *temp;

    do
    {
        while(S_Queue_peek(queue, i)->v < pivot->v) i++; // Σ(k=i -> (i + j) / 2) (3 + 2k + 2) ~= i + j + 5
        while(S_Queue_peek(queue, j)->v > pivot->v) j--; // Σ(k=j -> (i + j) / 2) (3 + 2k + 2) ~= i + j + 5

        if (i <= j) // 1
        {
            if (i < j) // 1
            {
                 temp = _pop_by_pos(queue, i); // 2i^2 + 13i + 12
                _push_by_pos(queue, _pop_by_pos(queue, j - 1), i); // 2i^2 + 17i + 7 + 2(j - 1)^2 + 13(j - 1) + 11 = 17i + 31 + 2j^2 + 9j
                _push_by_pos(queue, temp, j); // 2j^2 + 17j + 7
            }
            i++; // 1
            j--; // 1
        }
    
    } while (i < j); // 1
    // ((i + j) / 2) * (2i + 2j + 10 + 2i^2 + 13i + 12 + 17i + 31+ 2j^2 + 9j + 2j^2 + 17j + 12) = 
    // = 16i^2 + 30ij + 32i + i^3 + 2ij^2 + 14j^2 + 32j + i^2j + 2j^3 ~= n^3

    if (left < j) // 1
        _quick_sort(queue, left, j); // n3 * log(n)
    if (i < right) // 1
        _quick_sort(queue, i, right); // n3 * log(n)

}

void quick_sort(S_Queue *queue)
{
    _quick_sort(queue, 0, S_Queue_len(queue) - 1);
}

int64_t millis()
{
    struct timespec now;
    timespec_get(&now, TIME_UTC);
    return ((int64_t) now.tv_sec) * 1000 + ((int64_t) now.tv_nsec) / 1000000;
}


int main(int argc, char **argv)
{
    int step = 300;
    if (argc > 2) exit(EXIT_FAILURE);
    if (argc == 1) step = 300;
    else step = atoi(argv[1]);

    for (int i = step; i <= 10 * step; i += step)
    {
        S_Queue *queue = S_Queue_init();
        fill_test_data(queue, i);
        int64_t t_start = millis();
        quick_sort(queue);
        int64_t t_stop = millis(NULL);
        printf("Elems: %d\nN_OP: %li\nTime: %"PRId64"ms\n-------------------\n", i, queue->N_OP, t_stop - t_start);
    }
   
    return 0;
}