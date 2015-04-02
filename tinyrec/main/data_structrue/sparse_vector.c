#include <stdlib.h>
#include <stdio.h>

#include "linkedlist.h"

struct s_sparse_vector{
	LinkedList * storelist; 	//store as a list

}

struct s_vec_cell{
	int index;
	double value;
}

typedef s_sparse_vector sparse_vector;
typedef s_cell vec_cell;

sparse_vector * new_sparse_vector(){
	sparse_vector * sv = (sparse_vector *)malloc(sizeof(sparse_vector));
	sv->storelist = new_Linked_list();

	return sv;

}

int sparse_vector_get_size(sparse_vector * sv){
	return list_get_len(sv->storelist);
}



void destroy_sparse_vec(sparse_vector * sv){

	vec_cell * cell;
	while((cell= list_iterator_next(l)) != NULL)
		free(cell);
	destory_linked_list(sv->storelist);
	free(sv)
}

double sparse_vector_get_mean(sparse_vector * sv){
	long double total = 0

	vec_cell * cell;
	while((cell= list_iterator_next(l)) != NULL)
		total += cell->value;
	return (double)(total / sparse_vector_get_size());
}

double sparse_vector_get_variance(sparse_vector * sv){
	double mean = sparse_vector_get_mean(sv);

	vec_cell * cell;
	double var = 0;
	while((cell= list_iterator_next(l)) != NULL){
		double tmp = cell->value - mean;
		var += tmp * tmp
	}
	return var;
}
