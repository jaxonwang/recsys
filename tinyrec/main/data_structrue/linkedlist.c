#include <stdlib.h>
#include <stdio.h>
#include "mem.h"
#include "linkedlist.h"


struct s_LinkedListNode{
	struct s_LinkedListNode * next;
	struct s_LinkedListNode * previous;
	void * data;
	
};

struct s_LinkedList{
	struct s_LinkedListNode * head;
	struct s_LinkedListNode * tail;
	struct s_LinkedListNode * curser;
	struct s_obj_list * mem_obj;		//for mem gc
	int list_length;

};

LinkedList * new_Linked_list(){
	//new list
	LinkedList * n_list = (LinkedList * )malloc(sizeof(LinkedList));
	//new mem_gc_obj
	n_list->mem_obj = init_objlist();

	//new head
	LinkedListNode * n_head = (LinkedListNode *)malloc(sizeof(LinkedListNode));
	append_to_list(n_list->mem_obj, n_head);
	n_head->next = NULL;
	n_head->previous = NULL;

	//init list
	n_list->head = n_head;
	n_list->tail = n_head;
	n_list->curser = n_head;
	n_list->list_length = 0;
	return n_list;
}

void list_append(LinkedList * list,void *data){
	LinkedListNode * node = (LinkedListNode *)malloc(sizeof(LinkedListNode));
	append_to_list(list->mem_obj,node);

	list->tail->next = node;
	node->previous = list->tail;
	node->data = data;
	list->tail = node;
	list->list_length++;
}

void * list_iterator_next(LinkedList * list){
	if((list->curser == list->tail)&&(list->list_length > 0) ){//get to the end
		return NULL;
	}else{
		list->curser = list->curser->next;
		return list->curser->data;	
	}
}

int list_get_len(LinkedList * l){
	return l->list_length;
}

inline LinkedListNode * list_get_next_node(LinkedListNode * node){
	return node->next;
}

inline LinkedListNode * list_get_previous(LinkedListNode * node){
	return node->previous;
}

void destory_linked_list(LinkedList * list){
	destroy_objlist(list->mem_obj);
	free(list);
}

/*
int main(){
	
	int i;
	int a[1];
	LinkedList * l = new_Linked_list();
	for(i = 0;i < sizeof(a)/sizeof(int);i++){
		a[i] = i;
		list_append(l,&a[i]);
	}

	int * it_data;
	while((it_data = list_iterator_next(l)) != NULL){
		printf("%d\n",*it_data);
	}

	destory_linked_list(l);

}
*/
