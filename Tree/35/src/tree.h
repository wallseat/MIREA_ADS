#ifndef _TREE_H_
#define _TREE_H_

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

#define Size_S_Tree sizeof(S_Tree)
#define Size_S_Node sizeof(S_Node)

#define PRINTFMT_LINE 1
#define PRINTFMT_SIMM 2
#define PRINTFMT_REVERSE 3

typedef struct _S_Node
{
    uint32_t size; 
    int32_t v;

    struct _S_Node *sub[2];

} S_Node;

typedef struct _S_Tree
{
    uint32_t size;
    uint64_t N_OP;

    S_Node *root;

} S_Tree;


// public
S_Tree* S_Tree_init();
S_Node* S_Node_init(int32_t v);
void S_Tree_insert(S_Node*, S_Tree*);
void S_Tree_remove(int32_t, S_Tree*);
uint32_t S_Tree_size(S_Tree*);
void S_Tree_print(S_Tree*, uint);

// private
static void _S_Tree_print_line(S_Node*);
static void _S_Tree_print_simm(S_Node*);
static void _S_Tree_print_reverse(S_Node*);
static S_Node *_S_Tree_join(S_Node*, S_Node*);
static S_Node *_S_Tree_remove(S_Node *, uint32_t);
static uint32_t _S_Tree_size(S_Node*);
static S_Node* _S_Tree_insert(S_Node*, S_Node*);
static S_Node* _S_Tree_root_insert(S_Node*, S_Node*);
static S_Node* _S_Tree_rrot(S_Node*);
static S_Node* _S_Tree_lrot(S_Node*);
static void _S_Tree_update_size(S_Node*);

#endif // _TREE_H_