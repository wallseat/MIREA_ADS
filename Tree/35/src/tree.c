#include "tree.h"

// public
S_Node* S_Node_init(int32_t v)
{
    S_Node* node = (S_Node*) malloc(Size_S_Node);
    node->size = 0;
    node->v = v;
    node->sub[0] = node->sub[1] = NULL;

    return node;
}

S_Tree* S_Tree_init()
{
    S_Tree* tree = (S_Tree*) malloc(Size_S_Tree);
    tree->N_OP = 0;
    tree->root = NULL;
    tree->size = 0;

    return tree;
}

void S_Node_free(S_Node *node)
{
    free(node);
}

void S_Tree_insert(S_Node *node, S_Tree *tree)
{
    tree->root = _S_Tree_insert(tree->root, node);
    tree->size++;
}

uint32_t S_Tree_size(S_Tree *tree)
{
    return tree->size;
}

void S_Tree_remove(int32_t v, S_Tree *tree)
{
    tree->root = _S_Tree_remove(tree->root, v);
}

void S_Tree_print(S_Tree *tree, uint fmt)
{
    if (!tree->root) return;

    switch (fmt) {
        case PRINTFMT_LINE:
            _S_Tree_print_line(tree->root);
            break;

        case PRINTFMT_SIMM:
            _S_Tree_print_simm(tree->root);
            break;

        case PRINTFMT_REVERSE:
            _S_Tree_print_reverse(tree->root);
    }
}

// private
static void _S_Tree_print_line(S_Node *node)
{
    fprintf(stdout, "%i\n", node->v);
    if(node->sub[0]) _S_Tree_print_line(node->sub[0]);
    if(node->sub[1]) _S_Tree_print_line(node->sub[1]);
}

static void _S_Tree_print_simm(S_Node *node)
{
    if(node->sub[0]) _S_Tree_print_simm(node->sub[0]);
    fprintf(stdout, "%i\n", node->v);
    if(node->sub[1]) _S_Tree_print_simm(node->sub[1]);
}

static void _S_Tree_print_reverse(S_Node *node)
{
    if(node->sub[0]) _S_Tree_print_reverse(node->sub[0]);
    if(node->sub[1]) _S_Tree_print_reverse(node->sub[1]);
    fprintf(stdout, "%i\n", node->v);
}

static S_Node *_S_Tree_remove(S_Node *p, uint32_t v)
{
    if(!p) return p; 

	if( p->v == v ) 
	{
		S_Node* q = _S_Tree_join(p->sub[0], p->sub[1]); 
		S_Node_free(p); 
		return q; 
	}
	else if( v < p->v ) 
		p->sub[0] = _S_Tree_remove(p->sub[0], v); 
	else 
		p->sub[1] = _S_Tree_remove(p->sub[1], v); 
	return p; 

}

static S_Node *_S_Tree_join(S_Node *p, S_Node *q)
{
    if(!p) return q;
	if(!q) return p;
    
	if(rand() % (p->size + q->size) < p->size) 
	{
		p->sub[1] = _S_Tree_join(p->sub[1], q); 
		_S_Tree_update_size(p); 
		return p; 
	}
	else 
	{
		q->sub[0] = _S_Tree_join(p, q->sub[0]); 
		_S_Tree_update_size(q); 
		return q; 
	}
}

static S_Node *_S_Tree_insert(S_Node *p, S_Node *q)
{
    if(!p) return q;

    if(rand() % (p->size + 1) == 0)
        p = _S_Tree_root_insert(p, q);
		
    else if(p->v > q->v)
        p->sub[0] = _S_Tree_insert(p->sub[0], q);

    else
        p->sub[1] = _S_Tree_insert(p->sub[1], q);

    _S_Tree_update_size(p);
    return p;
}

static S_Node *_S_Tree_root_insert(S_Node *p, S_Node *q)
{
    if(!p) return q;

 	if( p->v < q->v ) 
	{
		p->sub[0] = _S_Tree_root_insert(p->sub[0], q); 
		return _S_Tree_rrot(p); 
	}
	else 
	{
		p->sub[1] = _S_Tree_root_insert(p->sub[1], q);
		return _S_Tree_lrot(p);
	}
}

static S_Node * _S_Tree_rrot(S_Node *p)
{
    S_Node* q = p->sub[0]; 
	if(!q) return p; 

	p->sub[0] = q->sub[1]; 
	q->sub[1] = p; 
	q->size = p->size; 

	_S_Tree_update_size(p); 

	return q; 

}

static S_Node *_S_Tree_lrot(S_Node *q)
{
    S_Node* p = q->sub[1]; 
	if(!p) return q; 

	q->sub[1] = p->sub[0]; 
	p->sub[0] = q; 
	p->size = q->size; 

	_S_Tree_update_size(q); 

	return p; 

}

static uint32_t _S_Tree_size(S_Node *node)
{
    if(!node) return 0;
    else return node->size;
}

static void _S_Tree_update_size(S_Node *node)
{
    node->size = _S_Tree_size(node->sub[0]) + _S_Tree_size(node->sub[1]) + 1; 
}