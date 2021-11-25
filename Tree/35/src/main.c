#include <time.h>

#include "tree.h"

int main(int argc, char **argv)
{
    srand(time(NULL));

    S_Tree *tree = S_Tree_init();
    S_Tree_insert(S_Node_init(5), tree);
    S_Tree_insert(S_Node_init(6), tree);
    S_Tree_insert(S_Node_init(2), tree);
    S_Tree_insert(S_Node_init(-1), tree);
    S_Tree_insert(S_Node_init(0), tree);
    S_Tree_insert(S_Node_init(4), tree);
    S_Tree_insert(S_Node_init(5), tree);
    S_Tree_insert(S_Node_init(6), tree);
    S_Tree_insert(S_Node_init(2), tree);
    S_Tree_insert(S_Node_init(-1), tree);
    S_Tree_insert(S_Node_init(0), tree);
    S_Tree_insert(S_Node_init(4), tree);
    S_Tree_insert(S_Node_init(5), tree);
    S_Tree_insert(S_Node_init(6), tree);
    S_Tree_insert(S_Node_init(2), tree);
    S_Tree_insert(S_Node_init(-1), tree);
    S_Tree_insert(S_Node_init(0), tree);
    S_Tree_insert(S_Node_init(4), tree);

    S_Tree_print(tree, PRINTFMT_SIMM);
    printf("%i", S_Tree_size(tree));
}